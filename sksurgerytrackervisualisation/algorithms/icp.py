"""
Algorithms for doing Iterative Closest Point
"""
#from numpy import zeros, uint8
from vtk import vtkIterativeClosestPointTransform, vtkCellLocator, vtkMatrix4x4

def vtk_icp(source, target, locator=None, max_iterations=100,
            max_landmarks=50, check_mean_distance=False,
            maximum_mean_distance=0.001):

    """
    An iterative closest point algorithm, delegating to vtk.
    Target is a point set, source is a point cloud
    """

    #why not let vtk handle this, because vtk seg faults in a rather
    #unhelpful way
    if source.GetNumberOfCells() == 0:
        raise ValueError("vtk_icp needs a polydata surface",
                         source.GetNumberOfCells())

    vtk_icp_transform = vtkIterativeClosestPointTransform()
    vtk_icp_transform.GetLandmarkTransform().SetModeToRigidBody()

    vtk_icp_transform.SetSource(target)
    vtk_icp_transform.SetTarget(source)
    print("making locator")
    if locator is None:
        locator = vtkCellLocator()
        locator.SetDataSet(source)
        locator.SetNumberOfCellsPerBucket(1)
        locator.BuildLocator()

    print("made locator")
    vtk_icp_transform.SetLocator(locator)
    vtk_icp_transform.SetMaximumNumberOfIterations(max_iterations)
    vtk_icp_transform.SetMaximumNumberOfLandmarks(max_landmarks)
    vtk_icp_transform.SetCheckMeanDistance(check_mean_distance)
    vtk_icp_transform.SetMaximumMeanDistance(maximum_mean_distance)

    vtk_icp_transform.Modified()
    vtk_icp_transform.Update()

    print(vtk_icp_transform.GetMatrix())
    result = vtkMatrix4x4()
    result = vtk_icp_transform.GetMatrix()

    inverted = vtkMatrix4x4()

    vtkMatrix4x4.Invert(result, inverted)

    return inverted
