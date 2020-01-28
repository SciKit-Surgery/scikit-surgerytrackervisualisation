# coding=utf-8

"""Main loop for tracking visualisation"""
#from sksurgerytrackervisualisation.shapes import cone, cylinder
from math import isnan
from sksurgeryutils.common_overlay_apps import OverlayBaseApp
from sksurgeryvtk.text.text_overlay import VTKCornerAnnotation
from sksurgerytrackervisualisation.algorithms.algorithms import (
        np2vtk, configure_tracker, populate_models)
from sksurgerytrackervisualisation.algorithms.background_image import \
        OverlayBackground
from sksurgerytrackervisualisation.algorithms.icp import vtk_icp


class OverlayApp(OverlayBaseApp):
    """
    Inherits from OverlayBaseApp, adding code to move vtk models
    based on input from a scikitsurgery tracker.
    Adds a function to detect a key press event, ("g")
    and add points to a point cloud.
    """

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

        self._models = populate_models(config.get("models"))
        models_t = []
        for model in self._models:
            models_t.append(model.get("model"))

        self.vtk_overlay_window.add_vtk_models(models_t)

        for model in self._models:
            if model.get("point cloud") is not None:
                self.vtk_overlay_window.add_vtk_actor(
                    model.get("point cloud").actor)

        if "camera" in config:
            camera_config = config.get("camera")
            if "bounding box" in camera_config:
                self.vtk_overlay_window.foreground_renderer.ResetCamera(
                    camera_config.get("bounding box"))
            else:
                self.vtk_overlay_window.foreground_renderer.ResetCamera(
                    -300, 300, -300, 300, -200, 0)

        self.vtk_overlay_window.AddObserver("KeyPressEvent",
                                            self.key_press_event)

        self._text = VTKCornerAnnotation()
        self.vtk_overlay_window.add_vtk_actor(self._text.text_actor)
        self._status_strings = ["", "", "", ""]

    def update(self):
        """Update the background renderer with a new frame,
        move the model and render"""
        image = self.bg_image.next_image()

        #add a method to move the rendered models
        self._update_tracking()

        self.vtk_overlay_window.set_video_image(image)
        self.vtk_overlay_window.Render()


    def _update_tracking(self, record=False):
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
        self._status_strings[0] = ""
        for ph_index, port_handle in enumerate(port_handles):
            self._status_strings[0] = self._status_strings[0] + "\n" + \
                    str(port_handle)
            for model in self._models:
                if model.get("port handle") == port_handle \
                        and not isnan(quality[ph_index]):
                    self._status_strings[0] = self._status_strings[0] + " :" \
                            + model.get("name") + " OK"
                    model.get("transform manager").add(
                        "tracker2world", tracking[ph_index])
                    model2world = model.get(
                        "transform manager").get("model2world")
                    model.get("model").actor.SetUserMatrix(np2vtk(model2world))
                    if record:
                        if model.get("point cloud") is not None:
                            points = model.get("point cloud").add_point(
                                (model2world[0:3, 3]))
                            self._status_strings[1] = model.get("name") + \
                                    " : " + str(points)
                    break

        self._text.set_text(self._status_strings)

    def key_press_event(self, _obj_not_used, _ev_not_used):
        """
        Handles a key press event

        """

        if self.vtk_overlay_window.GetKeySym() == 'g':
            self._update_tracking(record=True)

        if self.vtk_overlay_window.GetKeySym() == 'i':
            self._run_icp()

    def _run_icp(self):
        for model in self._models:
            if model.get("target"):
                for target in self._models:
                    if target.get("name") == model.get("target"):
                        source = model.get("model")
                        target = target.get("point cloud")
                        model2world = vtk_icp(source.source,
                                              target.get_polydata())
                        model.get("model").actor.SetUserMatrix(model2world)
                        print(model2world)
