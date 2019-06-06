# coding=utf-8

"""Main loop for tracking visualisation"""
#from sksurgerytrackervisualisation.shapes import cone, cylinder
from itertools import cycle
from sys import version_info, exit
from vtk.util import numpy_support
import vtk
from PySide2.QtWidgets import QApplication
from sksurgeryutils.common_overlay_apps import OverlayBaseApp
from sksurgerynditracker.nditracker import NDITracker
from sksurgeryarucotracker.arucotracker import ArUcoTracker
from sksurgerytrackervisualisation.shapes.cylinder import VTKCylinderModel

def np2vtk(mat):
    if mat.shape == (4, 4):
        obj = vtk.vtkMatrix4x4()
        for i in range(4):
            for j in range(4):
                obj.SetElement(i, j, mat[i, j])
        return obj


def configure_tracker (config):
    if "tracker type" not in config:
        raise KeyError ('Tracker configuration requires tracker type')

    tracker_type = config.get("tracker type")
    tracker = None
    if tracker_type in ("vega", "polaris", "aurora", "dummy"):
        tracker = NDITracker(config)
    if tracker_type in ("aruco"):
        tracker = ArUcoTracker(config)

    tracker.start_tracking()
    return tracker

def populate_models (model_config):

    models = []
    return models

class OverlayApp(OverlayBaseApp):
    """Inherits from OverlayBaseApp, adding code to move vtk models
    based on input from a scikitsurgery tracker"""

    def __init__(self, config):
        """Overides overlay base app's init, to initialise the
        external tracking system. Together with a video source"""

        if "image source" in config:
            #and call the constructor for the base class
            if version_info > (3, 0):
                super().__init__(config.get("image source"))
            else:
                #super doesn't work the same in py2.7
                OverlayBaseApp.__init__(self, config.get("image source"))
        else:
            raise KeyError ("Configuration must contain a video source")

        self._video_loop_buffer = []
        video_buffer = []
        if "loop video" in config:
            if config.get("loop video"):
                ret, image = self.video_source.read()
                while ret:
                    video_buffer.append(image)
                    ret, image = self.video_source.read()

                self._video_loop_buffer = cycle(video_buffer)

        self._tracker = None
        if "tracker config" in config:
            tracker_config = config.get("tracker config")
            self._tracker = configure_tracker(config.get("tracker config"))



        cylinder = VTKCylinderModel(10.0, 5.0, (1.0, 0.0, 0.0), 'cyl01',True,1.0)
        #models will be a list containing vtk actors and 
        models = populate_models (config.get("models")) 
        models.append(cylinder)
        self.vtk_overlay_window.add_vtk_models(models)

    def update(self):
        """Update the background renderer with a new frame,
        move the model and render"""
        if  self._video_loop_buffer:
            image = next (self._video_loop_buffer)
        else:
            _, image = self.video_source.read()

        #add a method to move the rendered models
        self._update_tracking()

        self.vtk_overlay_window.set_video_image(image)
        self.vtk_overlay_window.Render()
        self.vtk_overlay_window.foreground_renderer.ResetCamera(-300,300,-300,300,-200,0)
        #self.vtk_overlay_window._RenderWindow.Render()

    def _update_tracking(self):
        """Internal method to move the rendered models in
        some interesting way
        #Iterate through the rendered models
        for actor in \
                self.vtk_overlay_window.get_foreground_renderer().GetActors():
            #get the current orientation
            orientation = actor.GetOrientation()
            #increase the rotation around the z-axis by 1.0 degrees
            orientation = [orientation[0], orientation[1], orientation[2] + 1.0]
            #add update the model's orientation
            actor.SetOrientation(orientation)
        """
        port_handles, _, _, tracking, _ = self._tracker.get_frame()

         for index, port_handle in enumerate(port_handles):
            #these will need working on, need a way to match model names with port handles
            print (port_handle)
            #need to check that port handle matches a tracked object, then that tracking
            #is occuring, as for ndi, we'll get NaN's
            if port_handle == 0:
                for actor in self.vtk_overlay_window.get_foreground_renderer().GetActors():
                    print (tracking[index])
                    actor.SetUserMatrix(np2vtk(tracking[index]))


#here's a dummy app just to test the class. Quickly
if __name__ == '__main__':
    app = QApplication([])

    configuration = { "image source" : "../../data/noisy_logo.avi",
                      "loop video"   : True,
                        "tracker config" :
                        {
                            "tracker type" : "aruco",
                            "debug" : True
                        },
                        #a list of models, either loaded or 
                        #generated, together with their port
                        #handles
                        "models" : 
                        {
                            "tip" : { 
                                "port_handle" : "0",
                                "load"        : False,
                                "filename"    : "n/a",
                                "source"      : VTKCylinderModel(10.0, 5.0, (1.0, 0.0, 0.0), 'tip',True,1.0),
                                },
                            "section_1" : {
                                "port_handle" : "1",
                                "load"        : False,
                                "filename"    : "n/a",
                                "source"      : VTKCylinderModel(10.0, 3.0, (1.0, 0.0, 0.0), 'section_1',True,1.0),
                                },
                            "section_2" : {
                                "port_handle" : "2",
                                "load"        : False,
                                "filename"    : "n/a",
                                "source"      : VTKCylinderModel(10.0, 3.0, (1.0, 0.0, 0.0), 'section_2',True,1.0),
                                },
                        }
                    }

    configuration_live = { "image source" : 0,
                      "loop video"   : False }
    viewer = OverlayApp(configuration)

    #model_dir = '../models'
    #viewer.add_vtk_models_from_dir(model_dir)

    viewer.start()

   #start the application
    exit(app.exec_())


