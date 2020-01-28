"""
Algorithms used by the trackervisualisation module
"""
import vtk
from numpy import eye, float64, reshape
from sksurgerynditracker.nditracker import NDITracker
from sksurgeryarucotracker.arucotracker import ArUcoTracker
from sksurgerycore.transforms.transform_manager import TransformManager
from sksurgeryvtk.models.vtk_cylinder_model import VTKCylinderModel
from sksurgeryvtk.models.vtk_surface_model import VTKSurfaceModel
from sksurgerytrackervisualisation.shapes.cone import VTKConeModel
from sksurgerytrackervisualisation.shapes.sphere import VTKSphereModel
from sksurgerytrackervisualisation.shapes.dynamic_point_cloud import \
        VTKDynamicPointCloud


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

      :return: a list of dictionaries, one for each model
      :return: port_handles
      :return: actors
      :return: transform_managers

      :raises: KeyError if asked to load model without filename
      """
    model_dictionaries = []
    for model in model_config:
        model_temp = None
        transform_manager = TransformManager()

        colour = model.get("colour", (1.0, 1.0, 1.0))
        port_handle = model.get("port handle", -1)
        name = model.get("name", "unnamed")
        height = model.get("height", 10.0)
        radius = model.get("radius", 3.0)
        angle = model.get("angle", 90.0)
        orientation = model.get("orientation", (1.0, 0.0, 0.0))
        resolution = model.get("resolution", 88)
        opacity = model.get("opacity", 1.0)
        visibility = model.get("visibility", True)

        transform_manager.add("model2tracker", make_offset_matrix(model))

        if not model.get("load", False):
            model_type = model.get("source")

            if model_type == "cylinder":
                model_temp = VTKCylinderModel(height, radius, colour, name,
                                              angle, orientation, resolution,
                                              visibility, opacity)
            if model_type == "sphere":
                model_temp = VTKSphereModel(radius, colour, name, visibility,
                                            opacity)
            if model_type == "cone":
                model_temp = VTKConeModel(height, radius, colour, 'name',
                                          visibility, opacity)

        else:
            if not model.get("filename", False):
                raise KeyError("Config set load, but no filename given")

            filename = model.get("filename")
            model_temp = VTKSurfaceModel(filename, colour, visibility, opacity)

        dictionary = {
            "model" : model_temp,
            "port handle" : port_handle,
            "transform manager" : transform_manager,
            "name" : name
            }
        if model.get("grab points"):
            dictionary["point cloud"] = VTKDynamicPointCloud(colour)
        else:
            dictionary["point cloud"] = None
        if model.get("register to"):
            dictionary["target"] = model.get("register to")

        model_dictionaries.append(dictionary)

    return model_dictionaries


def make_offset_matrix(model_config):
    """
    generates an offset (or handeye) matrix

    :param:  Model configuration
    :return: If valid offset specified, returns a 4x4 offset matrix, if no
             offset, returns identity.
    :raises: ValueError
    """

    offset_matrix = eye(4, 4, dtype=float64)
    if "offset" in model_config:
        offset_t = model_config.get("offset")

        if len(offset_t) == 3:
            for i in range(3):
                offset_matrix[i, 3] = offset_t[i]
            return offset_matrix

        if len(offset_t) == 16:
            offset_matrix = reshape(offset_t, (4, 4))
            return offset_matrix

        raise ValueError("Offset matrix must be a transform of length 3 or ",
                         "a 4x4 tranform matrix (length 16)")

    return offset_matrix
