# coding=utf-8

"""scikit-surgerytrackervisualisation tests"""

from vtk import vtkPolyData
from sksurgeryvtk.models.vtk_surface_model import VTKSurfaceModel

import sksurgerytrackervisualisation.algorithms.icp as icp

# Pytest style

def make_source_and_target():
    """
    Helper to make a source and target.
    """
    filename = "data/liverphantom-iso=-130_cleaned2_mc_smooth2.stl"
    colour = [1.0, 1.0, 1.0]
    source_poly = VTKSurfaceModel(filename, colour)

    target_points = source_poly.source.GetPoints()

    target_vtk_poly = vtkPolyData()
    target_vtk_poly.SetPoints(target_points)
    return source_poly.source, target_vtk_poly


def test_vtk_icp():
    """
    Tests vtk_icp.
    """
    source, target = make_source_and_target()
    locator = None
    max_iterations = 100
    max_landmarks = 3
    check_mean_distance = False
    maximum_mean_distance = 0.001
    print(icp.vtk_icp(source, target, locator, max_iterations, max_landmarks,
                      check_mean_distance, maximum_mean_distance))
