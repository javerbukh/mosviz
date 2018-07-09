from __future__ import print_function, division

from glue.config import startup_action

from mosviz.viewers.mos_viewer import MOSVizViewer


@startup_action('mosviz')
def mosviz_setup(session, data_collection):

    # Make sure the application is visible first to avoid issues with
    # splitters not being in sync in MOSViz viewer
    session.application.show()
    session.application.app.processEvents()

    for data in data_collection[:]:
        session.application.new_data_viewer(MOSVizViewer, data=data)