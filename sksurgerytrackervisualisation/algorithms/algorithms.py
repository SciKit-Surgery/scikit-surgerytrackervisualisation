"""
Algorithms used by the trackervisualisation module
"""
import vtk
from sksurgerynditracker.nditracker import NDITracker
from sksurgeryarucotracker.arucotracker import ArUcoTracker
from sksurgeryvtk.models.vtk_cylinder_model import VTKCylinderModel
from sksurgerytrackervisualisation.shapes.cone import VTKConeModel
from sksurgerytrackervisualisation.shapes.sphere import VTKSphereModel


def np2vtk(mat):
    """
    Converts a Numpy array to a vtk matrix
    :param: the number array, should be 4x4
    :return: a vtk 4x4 matrix
    :raises: ValueError when matrix is not 4x4
    """
    if mat.shape == (4, 4):
        obj = vtk.vtkMatrix4x4()
        for i in range(4):
            for j in range(4):
                obj.SetElement(i, j, mat[i, j])
        return obj
    raise ValueError('Array must be 4x4')


def configure_tracker(config):
    """
    Configures the tracking system.
    :param: A dictionary containing configuration data
    :return: The tracker object
    :raises: KeyError if no tracker entry in config
    """
    if "tracker type" not in config:
        raise KeyError('Tracker configuration requires tracker type')

    tracker_type = config.get("tracker type")
    tracker = None
    if tracker_type in ("vega", "polaris", "aurora", "dummy"):
        tracker = NDITracker(config)
    if tracker_type in "aruco":
        tracker = ArUcoTracker(config)

    tracker.start_tracking()
    return tracker


def populate_models(model_config):
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
            angle = 90.0
            orientation = (1.0, 0.0, 0.0)
            resolution = 88
            port_handle = -1
            port_handle = model.get("port handle")
            if model_type == "cylinder":
                height = model.get("height")
                radius = model.get("radius")
                colour = model.get("colour")
                name = model.get("name")
                if "angle" in model:
                    angle = model.get("angle")
                if "orientation" in model:
                    orientation = model.get("orientation")
                if "resolution" in model:
                    resolution = model.get("resolution")

                model_temp = VTKCylinderModel(height, radius, colour, name,
                                              angle, orientation, resolution,
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
                model_temp = VTKConeModel(height, radius, colour, 'name',
                                          True, 1.0)
            models.append(model_temp)
            port_handles.append(port_handle)
        else:
            print("load it in")

    return port_handles, models
