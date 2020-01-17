# coding=utf-8

"""scikit-surgerytrackervisualisation tests"""

from sksurgerytrackervisualisation.shapes.cone import VTKConeModel
from sksurgerytrackervisualisation.shapes.sphere import VTKSphereModel
from sksurgerytrackervisualisation.shapes.dynamic_point_cloud import \
        VTKPointCloud

# Pytest style

def test_cone():
    """
    Tests cone model
    """

    _ = VTKConeModel(height=1.0, radius=1.0, colour=(1.0, 1.0, 1.0),
                     name="cone")


def test_sphere():
    """
    Tests sphere model
    """
    _ = VTKSphereModel(radius=1.0, colour=(1.0, 1.0, 1.0),
                       name="spere")


def test_point_cloud():
    """
    Tests for the point cloud.
    """

    cloud = VTKPointCloud(colour=(0.0, 0.2, 0.3))

    cloud.add_point((1.0, 1.0, 1.0))
