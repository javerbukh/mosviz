import os

from qtpy import QtCore

from ..jwst_loaders import (pre_nirspec_spectrum1d_reader,
                            pre_nirspec_spectrum2d_reader,
                            pre_nircam_image_reader)
from ..deimos_loaders import (deimos_spectrum1D_reader,
                              deimos_spectrum2D_reader)
from ..hst_loaders import acs_cutout_image_reader

from glue.core import DataCollection
from glue.app.qt.application import GlueApplication

from ...viewers.mos_viewer import MOSVizViewer
import pytest
import time

from ...loaders.loader_selection import confirm_loaders_and_column_names



DATA = os.path.join(os.path.dirname(__file__), 'data')

JWST1D = os.path.join(DATA, 'jwst', 'Final_spectrum_MOS_1_105_039_CLEAR-PRISM_MOS_PRISM-observation-2-c0e0_000.fits.gz')
JWST2D = os.path.join(DATA, 'jwst', '2Dspectrum_MOS_1_105_039_CLEAR-PRISM_MOS_PRISM-observation-2-c0e0_000.fits.gz')
JWSTCUTOUT = os.path.join(DATA, 'jwst', 'nrc_oct16_969.fits.gz')

DEIMOS1D = os.path.join(DATA, 'deimos', 'spec1d.1153.151.12004808.fits.gz')
DEIMOS2D = os.path.join(DATA, 'deimos', 'slit.1153.151R.fits.gz')
DEIMOSCUTOUT = os.path.join(DATA, 'deimos', '12004808.acs.v_6ac_.fits.gz')

DEIMOSTABLE = os.path.join("/Users/javerbukh/Documents/", "data_for_mosviz", "workshop_examples", "deimos", "spec1D", "spec1d.1153.151.12004808.fits")

PLAYTABLE = os.path.join("/Users/javerbukh/Documents/", "data_for_mosviz", "playdata", "jw95065-MOStable.txt")

#@pytest.fixture(scope='module')
def test_mosviz_basic(qtbot, mosviz_gui):
    # TODO:
    #   Not able to have mosviz gui show up before the add_data dialogbox pops up.
    #   I can however set all of the values for the different comboboxes and check that, which is what
    #   I will do on Thursday
    # mosviz_gui.show()

    from glue.core import data_factories
    d = data_factories.load_data(PLAYTABLE)
    widget_1 = mosviz_gui.add_data(d)

    widget_1.show()
    qtbot.addWidget(widget_1)

    widget = widget_1.ui

    assert widget.combosel_spectrum1d.currentIndex() == 0

    move_down(qtbot, widget.combosel_spectrum1d, 1)

    assert widget.combosel_spectrum1d.currentIndex() == 1

    move_down(qtbot, widget.combosel_spectrum2d, 2)

    move_down(qtbot, widget.combosel_cutout, 3)

    move_down(qtbot, widget.combosel_loader_spectrum1d, 2)

    move_down(qtbot, widget.combosel_loader_spectrum2d, 2)

    move_down(qtbot, widget.combosel_slit_dec, 1)

    move_down(qtbot, widget.combosel_slit_width, 2)

    move_down(qtbot, widget.combosel_slit_length, 3)

    print(widget.combosel_spectrum1d.currentText(), widget.combosel_spectrum2d.currentText(), widget.combosel_cutout.currentText())

    print(widget.combosel_loader_spectrum1d.currentText(), widget.combosel_loader_spectrum2d.currentText(), widget.combosel_loader_cutout.currentText())

    print(widget.combosel_slit_ra.currentText(), widget.combosel_slit_dec.currentText(), widget.combosel_slit_width.currentText(), widget.combosel_slit_length.currentText())

    assert widget_1._validation_checks() == True

    left_click(qtbot, widget.button_ok)

    mosviz_gui.add_data_con(d)






#     combosel_slit_ra
#
#     combosel_slit_dec
#
#
# combosel_spectrum1d
#
#
# combosel_loader_cutout
#
# combosel_loader_spectrum1d

    # loader_spectrum1d = SelectionCallbackProperty()
    # loader_spectrum2d = SelectionCallbackProperty()
    # loader_cutout = SelectionCallbackProperty()
    #
    # spectrum1d = SelectionCallbackProperty()
    # spectrum2d = SelectionCallbackProperty()
    # cutout = SelectionCallbackProperty()
    #
    # slit_ra = SelectionCallbackProperty()
    # slit_dec = SelectionCallbackProperty()
    # slit_width = SelectionCallbackProperty()
    # slit_length = SelectionCallbackProperty()


def move_down(qtbot, widget, num):
    for i in range(0, num):
        qtbot.mouseClick(widget, QtCore.Qt.LeftButton)
        qtbot.keyPress(widget, QtCore.Qt.Key_Down)
        qtbot.keyPress(widget, QtCore.Qt.Key_Enter)
        print(i)

def left_click(qtbot, widget):
    qtbot.mouseClick(widget, QtCore.Qt.LeftButton)



def ttest_mosviz_gui(qtbot):
    from glue.core import DataCollection
    from glue.app.qt.application import GlueApplication

    from ...viewers.mos_viewer import MOSVizViewer

    import sys
    import os

    PLAYTABLE = os.path.join("/Users/javerbukh/Documents/", "data_for_mosviz", "playdata", "jw95065-MOStable.txt")

    from glue.core import data_factories

    d = data_factories.load_data(PLAYTABLE)

    dc = DataCollection([])

    dc.append(d)

    ga = GlueApplication(dc)

    qtbot.addWidget(ga)

    m = ga.new_data_viewer(MOSVizViewer)

    qtbot.addWidget(m)

    m.add_data(d)

    m.result_loader.ui.combosel_spectrum1d.setCurrentIndex(1)

    print(m.result_loader.ui.combosel_spectrum1d.currentText())

    qtbot.mouseClick(m.result_loader.ui.combosel_spectrum1d, QtCore.Qt.LeftButton)
    qtbot.keyPress(m.result_loader.ui.combosel_spectrum1d, QtCore.Qt.Key_Down)
    qtbot.keyPress(m.result_loader.ui.combosel_spectrum1d, QtCore.Qt.Key_Enter)


    # mosviz = ga.new_data_viewer(MOSVizViewer)
    #qtbot.addWidget(m.result_loader)
    #qtbot.mouseClick(m.result_loader.button_cancel, QtCore.Qt.LeftButton)

    # mosviz = MOSVizViewer(ga.session)
    # app = create_glue_app()
    # layout = app.tab(0)

    # Cheap workaround for Windows test environment
    # if sys.platform.startswith('win'):
    #     layout._cubeviz_toolbar._toggle_sidebar()

    #return mosviz

def ttest_pre_nirspec_spectrum1d_reader(qtbot, mosviz_gui):
    mosviz = run_mosviz_basic(mosviz_gui)
    #mosviz.show()
    #mosviz.initialize_toolbar()
    #data = pre_nirspec_spectrum1d_reader(JWST1D)
    #data = PLAYTABLE
    #data = DEIMOSTABLE
    data = deimos_spectrum1D_reader(DEIMOSTABLE)
    #confirm_loaders_and_column_names(data)
    print("mosviz_gui", mosviz_gui)
    print("data for mosviz_gui", data)
    mosviz.add_data(data)
    print("wont see this")
    mosviz.show()
    qtbot.addWidget(mosviz)
    assert data.ndim == 1

def ttest_mosviz_viewer(qtbot):
    from glue.core import DataCollection
    from glue.app.qt.application import GlueApplication

    from ...viewers.mos_viewer import MOSVizViewer

    dc = DataCollection([])
    ga = GlueApplication(dc)
    ga.show()
    qtbot.addWidget(ga)
    # mosviz = ga.new_data_viewer(MOSVizViewer)
    # mosviz = MOSVizViewer(ga.session)
    # mosviz.show()
    # qtbot.addWidget(mosviz)


def test_pre_nirspec_spectrum2d_reader():
    data = pre_nirspec_spectrum2d_reader(JWST2D)
    assert data.ndim == 2


def test_pre_nircam_image_reader():
    data = pre_nircam_image_reader(JWSTCUTOUT)
    assert data.ndim == 2


def test_deimos_spectrum1D_reader():
    data = deimos_spectrum1D_reader(DEIMOS1D)
    assert data.ndim == 1


def test_deimos_spectrum2D_reader():
    data = deimos_spectrum2D_reader(DEIMOS2D)
    assert data.ndim == 2


def test_acs_cutout_image_reader():
    data = acs_cutout_image_reader(DEIMOSCUTOUT)
    assert data.ndim == 2
