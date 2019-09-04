# coding=utf-8

"""Main loop for tracking visualisation"""
#from sksurgerytrackervisualisation.shapes import cone, cylinder
from math import isnan
from sksurgeryutils.common_overlay_apps import OverlayBaseApp
from sksurgerytrackervisualisation.algorithms.algorithms import (
        np2vtk, configure_tracker, populate_models)
from sksurgerytrackervisualisation.algorithms.background_image import \
        OverlayBackground


class OverlayApp(OverlayBaseApp):
    """Inherits from OverlayBaseApp, adding code to move vtk models
    based on input from a scikitsurgery tracker"""

    def __init__(self, config):
        """Overides overlay base app's init, to initialise the
        external tracking system. Together with a video source"""
        try:
            super().__init__(None)
        except RuntimeError:
            self.update_rate = 30
            self.img = None
            self.timer = None
            self.save_frame = None

        if "image" in config:
            self.bg_image = OverlayBackground(config.get("image"))
        else:
            default_config = {"logo" : True}
            self.bg_image = OverlayBackground(default_config)

        self._tracker = None
        if "tracker config" in config:
            self._tracker = configure_tracker(config.get("tracker config"))

        self._model_handles, models = populate_models(config.get("models"))
        self.vtk_overlay_window.add_vtk_models(models)

        if "camera" in config:
            camera_config = config.get("camera")
            if "bounding box" in camera_config:
                self.vtk_overlay_window.foreground_renderer.ResetCamera(
                    camera_config.get("bounding box"))
            else:
                self.vtk_overlay_window.foreground_renderer.ResetCamera(
                    -300, 300, -300, 300, -200, 0)


    def update(self):
        """Update the background renderer with a new frame,
        move the model and render"""
        image = self.bg_image.next_image()

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
            for actor_index, actor in enumerate(
                    self.vtk_overlay_window.get_foreground_renderer().
                    GetActors()):
                if self._model_handles[actor_index] == port_handle:
                    if not isnan(quality[ph_index]):
                        actor.SetUserMatrix(np2vtk(tracking[ph_index]))
                        break
