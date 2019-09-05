# -*- coding: utf-8 -*-

"""
VTK pipeline to represent a surface model via a vtkPolyData.
"""
import vtk
import sksurgeryvtk.models.vtk_surface_model as vbs

# pylint: disable=no-member

class VTKConeModel(vbs.VTKSurfaceModel):
    """
    Class to create a VTK surface model of a cone.
    """
    def __init__(self, height, radius, colour, name, visibility=True,
                 opacity=1.0):
        """
        Creates a new surface model.

        :param height: the height of the cone
        :param diameter: the radius of the cone
        :param name: a name for the model
        :param colour: (R,G,B) where each are floats [0-1]
        :param visibility: boolean, True|False
        :param opacity: float [0,1]
        """

        super(VTKConeModel, self).__init__(None, colour, visibility,
                                           opacity)
        self.name = name

        cone = vtk.vtkConeSource()
        cone.SetResolution(88)
        cone.SetRadius(radius)
        cone.SetHeight(height)
        cone.Update()
        self.source = cone.GetOutput()

        #this is from super init, have to redo as we now have data
        self.normals = None
        self.normals = vtk.vtkPolyDataNormals()
        self.normals.SetInputData(self.source)
        self.normals.SetAutoOrientNormals(True)
        self.normals.SetFlipNormals(False)
        self.transform = vtk.vtkTransform()
        self.transform.Identity()
        self.transform_filter = vtk.vtkTransformPolyDataFilter()
        self.transform_filter.SetInputConnection(self.normals.GetOutputPort())
        self.transform_filter.SetTransform(self.transform)
        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInputConnection(self.transform_filter.GetOutputPort())
        self.mapper.Update()
        self.actor.SetMapper(self.mapper)
