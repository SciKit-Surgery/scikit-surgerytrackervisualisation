# coding=utf-8

"""scikit-surgerytrackervisualisation tests"""

import numpy as np
import pytest
from sksurgerycore.configuration.configuration_manager import \
        ConfigurationManager
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
    config = {"tracker type" : "aruco"}
    tva.configure_tracker(config)


def test_populate_models():
    """
    Test that the populate models function works
    """
    configurer = ConfigurationManager("example_config.json")
    configuration = configurer.get_copy()
    tva.populate_models(configuration.get("models"))
