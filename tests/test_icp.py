# coding=utf-8

"""scikit-surgerytrackervisualisation tests"""

from numpy import hstack, ones, int64, arange, ascontiguousarray, warnings
from vtk import (vtkPoints, vtkCellArray, vtkPolyData, vtkPolyDataMapper,
                 VTK_ID_TYPE, vtkSurfaceReconstructionFilter,
                 vtkDelaunay3D)
from vtk.util import numpy_support

import sksurgerytrackervisualisation.algorithms.icp as icp

# Pytest style

def make_source_and_target():
    """
    Helper to make a source and target.
    """
    source_points=vtkPoints()
    source_points.InsertNextPoint(0.0,0.0,0.0)
    source_points.InsertNextPoint(4.0,3.0,0.0)
    source_points.InsertNextPoint(4.0,0.0,0.0)
    
    source_vtk_poly = vtkPolyData()
    source_vtk_poly.SetPoints(source_points)
    source2_vtk_poly = vtkPolyData()
    #urf = vtkSurfaceReconstructionFilter()
    surf = vtkDelaunay3D()
    surf.SetInputData(source_vtk_poly)
    surf.SetOutput(source2_vtk_poly)

    surf.Update()

    #source_vtk_poly.SetVerts(source_vtk_cells)

    target_points=vtkPoints()
    target_points.InsertNextPoint(0.0,0.0,1.0)
    target_points.InsertNextPoint(4.0,3.0,1.0)
    target_points.InsertNextPoint(4.0,0.0,1.0)

    target_vtk_poly = vtkPolyData()
    target_vtk_poly.SetPoints(target_points)
    return source2_vtk_poly, target_vtk_poly


def test_vtk_icp():
    """
    Tests vtk_icp.
    """
    source, target = make_source_and_target()
    locator = None
    max_iterations = 10
    max_landmarks = 3
    check_mean_distance = False
    maximum_mean_distance = 0.001
    icp.vtk_icp(source, target, locator, max_iterations, max_landmarks,
                check_mean_distance, maximum_mean_distance)
