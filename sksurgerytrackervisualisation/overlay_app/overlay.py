# coding=utf-8

"""Main loop for tracking visualisation"""
#from sksurgerytrackervisualisation.shapes import cone, cylinder
from math import isnan
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
    """Parses a model configuration dictionary, returning 
       a list of vtk actors and associated port handles

       :param: model config
               a list of dictionaries, one for each model 
               dictionary entries are:
               name : a descriptive name
               port handle : the port handle of the associated tracker
               load : True if model is to be loaded from file
               filename : if load is true the filename to load from
               source : supported values are cylinder, sphere, cone
               colour : the rgb colour to use for the actor
               height : the height of the cylinder or cone
               radius : the diameter of the cylinder, cone, or sphere

      :return: port_handles
      :return: actors
      """
    models = []
    port_handles = []
   
    for model in model_config:
        model_temp = None
        if not model.get("load"):
            model_type = model.get("source")
            height = 10.0
            radius = 3.0
            colour = (1.0, 1.0, 1.0)
            port_handle = -1
            port_handle = model.get("port handle")
            if model_type == "cylinder":
                height = model.get("height")
                radius = model.get("radius")
                colour = model.get("colour")
                name = model.get("name")
                model_temp = VTKCylinderModel(height, radius, colour, name, 
                        True, 1.0)
            if model_type == "sphere":
                radius = model.get("radius")
                colour = model.get("colour")
                name = model.get("name")
                model_temp = VTKSphereModel(radius, colour, name, True, 1.0)
            if model_type == "cone":
                height = model.get("height")
                radius = model.get("radius")
                colour = model.get("colour")
                name = model.get("name")
                model_temp = VTKCConeModel(height, radius, colour, 'name',
                        True, 1.0)
            models.append(model_temp)
            port_handles.append(port_handle)
        else:
            print ("load it in")

    return port_handles, models

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

        self._model_handles , models = populate_models (config.get("models")) 
        self.vtk_overlay_window.add_vtk_models(models)

        if "camera" in config:
            camera_config = config.get("camera")
            if "bounding box" in camera_config:
                self.vtk_overlay_window.foreground_renderer.ResetCamera(camera_config.get("bounding box"))
            else:
                self.vtk_overlay_window.foreground_renderer.ResetCamera(-300,300,-300,300,-200,0)


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
        port_handles, _, _, tracking, quality = self._tracker.get_frame()
        
        for ph_index, port_handle in enumerate(port_handles):
            #these will need working on, need a way to match model names with port handles
            #need to check that port handle matches a tracked object, then that tracking
            #is occuring, as for ndi, we'll get NaN's
            matched = False
            for actor_index, actor in enumerate(self.vtk_overlay_window.get_foreground_renderer().GetActors()):
                if self._model_handles[actor_index] == port_handle:
                    if not isnan(quality[ph_index]):
                        actor.SetUserMatrix(np2vtk(tracking[ph_index]))
                        break

from sksurgerycore.configuration.configuration_manager import (
        ConfigurationManager
        )


#here's a dummy app just to test the class. Quickly
if __name__ == '__main__':
    app = QApplication([])
    configurer = ConfigurationManager("../../example_config.json")
    configuration = configurer.get_copy()

    viewer = OverlayApp(configuration)

    viewer.start()

    exit(app.exec_())


