# -*- coding: utf-8 -*-

"""
VTK pipeline to represent a surface model via a vtkPolyData.
"""
import vtk
import sksurgeryvtk.models.vtk_surface_model as vbs

# pylint: disable=no-member

class VTKSphereModel(vbs.VTKSurfaceModel):
    """
    Class to create a VTK surface model of a sphere.
    """
    def __init__(self, radius, colour, name, visibility=True,
                 opacity=1.0):
        """
        Creates a new surface model.

        :param diameter: the radius of the sphere
        :param name: a name for the model
        :param colour: (R,G,B) where each are floats [0-1]
        :param visibility: boolean, True|False
        :param opacity: float [0,1]
        """

        super(VTKSphereModel, self).__init__(None, colour, visibility,
                                             opacity)
        self.name = name

        sphere = vtk.vtkSphereSource()
        sphere.SetThetaResolution(36)
        sphere.SetPhiResolution(36)
        sphere.SetRadius(radius)
        sphere.Update()
        self.source = sphere.GetOutput()

        #this is from super init, have to redo as we now have data
        self.transform = vtk.vtkTransform()
        self.transform.Identity()
        self.transform_filter = vtk.vtkTransformPolyDataFilter()
        self.transform_filter.SetInputData(self.source)
        self.transform_filter.SetTransform(self.transform)
        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInputConnection(self.transform_filter.GetOutputPort())
        self.mapper.Update()
        self.actor.SetMapper(self.mapper)
