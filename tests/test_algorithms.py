# coding=utf-8

"""scikit-surgerytrackervisualisation tests"""

import numpy as np
import pytest
import sksurgerytrackervisualisation.algorithms.algorithms as tva

# Pytest style


def test_np2vtk_valid():
    """
    Tests np2vtk for a valid matrix.
    """
    np_mat = np.eye(4, 4)
    np_mat[0, 3] = -1.7
    np_mat[3, 1] = 2.3
    vtk_mat = tva.np2vtk(np_mat)

    for i in range(4):
        for j in range(4):
            assert (vtk_mat.GetElement(i, j) == np_mat[i, j])


def test_np2vtk_invalid():
    """
    Tests np2vtk throws value error for invalid matrix
    """
    np_mat = np.eye(3, 3)

    with pytest.raises(ValueError):
        _ = tva.np2vtk(np_mat)


def test_config_tracker_invalid():
    """
    Tests that configure_tracker throws a KeyError when invalid
    """
    config = {}
    with pytest.raises(KeyError):
        tva.configure_tracker(config)


def test_config_tracker_dummy():
    """
    Tests that configure_tracker for ndi, using dummy
    """
    config = {"tracker type" : "dummy"}
    try:
        tva.configure_tracker(config)
    except ValueError:
        pass


def test_config_tracker_aruco():
    """
    Tests that configure_tracker for ndi, using dummy
    """
    config = {
        "tracker type" : "aruco",
        "video source" : "data/aruco_tag.avi"
        }
    tva.configure_tracker(config)


def test_populate_models():
    """
    Test that the populate models function works
    """
    configuration = {
        "models" : [
            {
                "name"        : "tip",
                "port handle" : 0,
                "load"        : False,
                "filename"    : "n/a",
                "source"      : "sphere",
                "colour"      : [1.0, 0.0, 0.0],
                "radius"      : 10.0,
                "angle"       : 90.0,
                "orientation" : [0.0, 0.0, 1.0]
            },
            {
                "name"        : "section_1",
                "port handle" : 1,
                "load"        : False,
                "filename"    : "n/a",
                "source"      : "cylinder",
                "colour"      : [1.0, 0.0, 0.0],
                "height"      : 50.0,
                "radius"      : 6.0,
                "angle"       : 0.0,
                "resolution"  : 18,
                "orientation" : [0.0, 0.0, 1.0]
            },
            {
                "name"        : "section_2",
                "port handle" : 2,
                "load"        : False,
                "filename"    : "n/a",
                "source"      : "cone",
                "colour"      : [1.0, 0.0, 0.0],
                "height"      : 50.0,
                "radius"      : 6.0,
                "resolution"  : 10,
                "orientation" : [0.0, 0.0, 1.0]
            },
            {
                "name"        : "anatomy_0",
                "port handle" : -1,
                "load"        : "true",
                "filename"    : "data/example.vtp",
                "model to world" : "data/example_mtw.4x4"
            }
        ]
    }

    tva.populate_models(configuration.get("models"))