# coding=utf-8

"""scikit-surgerytrackervisualisation tests"""

import sksurgerytrackervisualisation.algorithms.icp as icp

# Pytest style


def test_vtk_icp():
    """
    Tests vtk_icp.
    """
    source = None
    target = None
    locator = None
    max_iterations = 10
    max_landmarks = 3
    check_mean_distance = False
    maximum_mean_distance = 0.001
    icp.vtk_icp(source, target, locator, max_iterations, max_landmarks,
                check_mean_distance, maximum_mean_distance)
