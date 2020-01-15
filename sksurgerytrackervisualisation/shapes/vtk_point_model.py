# -*- coding: utf-8 -*-

"""
Class to represent a point cloud via a vtkPolyData, with the
ability to dynamically add points
"""

from numpy import hstack, ones, int64, arange, ascontiguousarray
from vtk import (vtkPoints, vtkCellArray, vtkPolyData, vtkPolyDataMapper,
                 VTK_ID_TYPE)
from vtk.util import numpy_support
import sksurgeryvtk.models.vtk_base_model as vbm


class VTKPointCloud(vbm.VTKBaseModel):
    """
    Class to represent a point cloud via a vtkPolyData, with the
    ability to dynamically add points
    """
    def __init__(self, colour,
                 visibility=True, opacity=1.0):
        """
        Creates a new point model.

        :param colour: numpy 1 x 3 array containing RGB as [0-255] uchar
        :param visibility: boolean, True|False
        :param opacity: float [0,1]
        """
        super(VTKPointCloud, self).__init__((1.0, 1.0, 1.0),
                                            visibility,
                                            opacity)

        self._vtk_points = vtkPoints()
        self._vtk_points.SetDataTypeToFloat()


        self.actor.GetProperty().SetPointSize(5)
        self.actor.GetProperty().SetColor(colour)

    def _update_actor(self):

        number_of_points = self._vtk_points.GetNumberOfPoints()

        if number_of_points == 0:
            return

        cells = hstack((ones((number_of_points, 1), dtype=int64),
                        arange(number_of_points).reshape(-1, 1)))
        cells = ascontiguousarray(cells, dtype=int64)
        cell_array = numpy_support.numpy_to_vtk(
            num_array=cells, deep=True, array_type=VTK_ID_TYPE)

        vtk_cells = vtkCellArray()

        vtk_cells.SetCells(number_of_points, cell_array)

        vtk_poly = vtkPolyData()
        vtk_poly.SetPoints(self._vtk_points)
        vtk_poly.SetVerts(vtk_cells)

        vtk_mapper = vtkPolyDataMapper()
        vtk_mapper.SetInputData(vtk_poly)
        self.actor.SetMapper(vtk_mapper)

    def add_point(self, point):
        """
        Adds a point to the point cloud and updates the
        vtk actor to show the complete point cloud

        :param: A 3 tuple representing the point coordinate
        """

        self._vtk_points.InsertNextPoint(point)
        self._update_actor()
