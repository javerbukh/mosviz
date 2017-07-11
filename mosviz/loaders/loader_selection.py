from __future__ import absolute_import, division, print_function

import os
from itertools import repeat

from qtpy import QtWidgets
from glue.external.echo import HasCallbackProperties, CallbackProperty
from glue.external.echo.qt import autoconnect_callbacks_to_qt
from glue.utils.qt import load_ui, update_combobox

# TODO: uncomment first line and remove second once we support glueviz >= 0.11
# from glue.core.qt.data_combo_helper import ComponentIDComboHelper
from ..compat import ComponentIDComboHelper

from ..loaders.mos_loaders import (SPECTRUM1D_LOADERS, SPECTRUM2D_LOADERS,
                                   CUTOUT_LOADERS)
from .. import UI_DIR


class LoaderSelectionDialog(QtWidgets.QDialog, HasCallbackProperties):

    # The dialog has a number of combo boxes that are linked to columns/fields
    # in the data. We now define these all here and the set things up and
    # check things programmatically to avoid duplicating too much code.

    columns = [{'property': 'spectrum1d', 'default': 'spectrum1d',
                'categorical': True, 'numeric': False},
               {'property': 'spectrum2d', 'default': 'spectrum2d',
                'categorical': True, 'numeric': False},
               {'property': 'cutout', 'default': 'cutout',
                'categorical': True, 'numeric': False},
               {'property': 'slit_ra', 'default': 'ra',
                'categorical': False, 'numeric': True},
               {'property': 'slit_dec', 'default': 'dec',
                'categorical': False, 'numeric': True},
               {'property': 'slit_width', 'default': 'slit_width',
                'categorical': False, 'numeric': True},
               {'property': 'slit_length', 'default': 'slit_length',
                'categorical': False, 'numeric': True}]

    loader_spectrum1d = CallbackProperty()
    loader_spectrum2d = CallbackProperty()
    loader_cutout = CallbackProperty()

    spectrum1d = CallbackProperty()
    spectrum2d = CallbackProperty()
    cutout = CallbackProperty()

    slit_ra = CallbackProperty()
    slit_dec = CallbackProperty()
    slit_width = CallbackProperty()
    slit_length = CallbackProperty()

    slit_north_aligned = CallbackProperty()

    def __init__(self, parent=None, data=None):

        QtWidgets.QDialog.__init__(self, parent=parent)

        self.ui = load_ui('loader_selection.ui', self, directory=UI_DIR)

        update_combobox(self.ui.combotext_loader_spectrum1d, zip(SPECTRUM1D_LOADERS, repeat(None)))
        update_combobox(self.ui.combotext_loader_spectrum2d, zip(SPECTRUM2D_LOADERS, repeat(None)))
        update_combobox(self.ui.combotext_loader_cutout, zip(CUTOUT_LOADERS, repeat(None)))

        if 'loaders' in data.meta:

            loaders = data.meta['loaders']

            if "spectrum1d" in loaders and loaders['spectrum1d'] in SPECTRUM1D_LOADERS:
                self.loader_spectrum1d = loaders['spectrum1d']
            if "spectrum2d" in loaders and loaders['spectrum2d'] in SPECTRUM2D_LOADERS:
                self.loader_spectrum2d = loaders['spectrum2d']
            if "cutout" in loaders and loaders['cutout'] in CUTOUT_LOADERS:
                self.loader_cutout = loaders['cutout']

        if self.loader_spectrum1d is None:
            self.loader_spectrum1d = 'NIRSpec 1D Spectrum'
        if self.loader_spectrum2d is None:
            self.loader_spectrum2d = 'NIRSpec 2D Spectrum'
        if self.loader_cutout is None:
            self.loader_cutout = 'NIRCam Image'

        # We set up ComponentIDComboHelper which takes care of populating the
        # combo box with the components.

        self._helpers = {}

        for column in self.columns:

            combo = getattr(self, 'combotext_' + column['property'])

            helper = ComponentIDComboHelper(combo,
                                            data=data,
                                            numeric=column['numeric'],
                                            categorical=column['categorical'])

            self._helpers[column['property']] = helper

            # Store components that appear in the combo inside the column object
            column['components'] = [combo.itemText(i) for i in range(combo.count())]

        # We check whether any of the properties are already defined in the
        # Data.meta dictionary. This could happen for example if the user has
        # encoded some of these defaults in their data file (which we
        # document how to do).

        if 'special_columns' in data.meta:
            special_columns = data.meta['special_columns']
            for column in self.columns:
                if column['property'] in special_columns:
                    column_name = special_columns[column['property']]
                    if column_name in column['components']:
                        setattr(self, column['property'], column_name)

        # We now check whether each property is None, and if so we set it either
        # to the default, if present, or to the first component otherwise. In
        # future we could replace the default by a function that could do more
        # sophisticated auto-testing.

        for column in self.columns:
            if getattr(self, column['property']) is None:
                if column['default'] in column['components']:
                    setattr(self, column['property'], column['default'])
                else:
                    setattr(self, column['property'], column['components'][0])

        # The following is a call to a function that deals with setting up the
        # linking between the callback properties here and the Qt widgets.

        autoconnect_callbacks_to_qt(self, self.ui)

        self.data = data

    def accept(self):

        if 'loaders' not in self.data.meta:
            self.data.meta['loaders'] = {}

        self.data.meta['loaders']['spectrum1d'] = self.loader_spectrum1d
        self.data.meta['loaders']['spectrum2d'] = self.loader_spectrum2d
        self.data.meta['loaders']['cutout'] = self.loader_cutout

        if 'special_columns' not in self.data.meta:
            self.data.meta['special_columns'] = {}

        for column in self.columns:
            self.data.meta['special_columns'][column['property']] = getattr(self, column['property'])

        self.data.meta['loaders_confirmed'] = True

        super(LoaderSelectionDialog, self).accept()


def confirm_loaders_and_column_names(data, force=False):
    if force or not data.meta.get('loaders_confirmed', False):
        loader_selection = LoaderSelectionDialog(data=data)
        loader_selection.exec_()
    return data


if __name__ == "__main__":

    from glue.core import Data
    from glue.utils.qt import get_qapp

    app = get_qapp()

    d = Data()
    d['spectrum1d'] = ['a', 'b', 'c']
    d['spectrum2d'] = ['d', 'e', 'f']
    d['cutout'] = ['a', 'a', 'a']
    d['ra'] = [1, 2, 2]
    d['dec'] = [1, 2, 2]
    d['slit_width'] = [1, 2, 2]
    d['slit_length'] = [1, 2, 2]

    print(confirm_loaders_and_column_names(d))
    print(confirm_loaders_and_column_names(d))