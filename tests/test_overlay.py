# coding=utf-8

"""scikit-surgerytrackervisualisation tests"""
import pytest
from sksurgerytrackervisualisation.overlay_app.overlay import OverlayApp

# Pytest style

def test_default_image(setup_qt):
    """
    Test that the overlay function works when no image config
    """
    _ = setup_qt
    configuration = {
        "tracker config" :
        {
            "tracker type" : "aruco",
            "debug"	   : False,
            "video source" : "data/aruco_tag.avi"
        },
        "models" : [
            {
                "name"        : "tip",
                "port handle" : 0,
                "load"        : False,
                "filename"    : "n/a",
                "source"      : "cylinder",
                "colour"      : [1.0, 0.0, 0.0],
                "height"      : 50.0,
                "radius"      : 10.0,
                "angle"       : 90.0,
                "orientation" : [0.0, 0.0, 1.0]
            },
        ]
    }
    overlay = OverlayApp(configuration)
    overlay.update()


def test_with_camera(setup_qt):
    """
    Test that the overlay function works when camera is set
    """
    _ = setup_qt
    configuration = {
        "tracker config" :
        {
            "tracker type" : "aruco",
            "debug"	   : False,
            "video source" : "data/aruco_tag.avi"
        },
        "models" : [
            {
                "name"        : "tip",
                "port handle" : 0,
                "load"        : False,
                "filename"    : "n/a",
                "source"      : "cylinder",
                "colour"      : [1.0, 0.0, 0.0],
                "height"      : 50.0,
                "radius"      : 10.0,
                "angle"       : 90.0,
                "orientation" : [0.0, 0.0, 1.0]
            },
        ],
        "camera" :
        {
            "origin" 	  : [0.0, 0.0, 0.0],
            "normal" 	  : [0.0, 0.0, 1.0],
            "bounding box" : [0.0, 640.0, 0.0, 480.0, -100.0, 0.0]
        }
    }
    _ = OverlayApp(configuration)


def test_with_camera_no_bounding(setup_qt):
    """
    Test that the overlay function works when camera is set with no bounding
    box
    """
    _ = setup_qt
    configuration = {
        "tracker config" :
        {
            "tracker type" : "aruco",
            "debug"	   : False,
            "video source" : "data/aruco_tag.avi"
        },
        "models" : [
            {
                "name"        : "tip",
                "port handle" : 0,
                "load"        : False,
                "filename"    : "n/a",
                "source"      : "cylinder",
                "colour"      : [1.0, 0.0, 0.0],
                "height"      : 50.0,
                "radius"      : 10.0,
                "angle"       : 90.0,
                "orientation" : [0.0, 0.0, 1.0]
            },
        ],
        "camera" :
        {
            "origin" 	  : [0.0, 0.0, 0.0],
            "normal" 	  : [0.0, 0.0, 1.0],
        }
    }
    _ = OverlayApp(configuration)


def test_invalid_video(setup_qt):
    """
    This should get a runtime error when the
    video source is opened.
    """
    _ = setup_qt
    configuration = {
        "image" :
        {
            "source" 	: "data/notthere.notthere",
            "loop"   	: False,
            "logo" 	: False,
            "blank" 	: False
        },
        "tracker config" :
        {
            "tracker type" : "aruco",
            "debug"	   : False,
            "video source" : "data/aruco_tag.avi"
        },
        "models" : [
            {
                "name"        : "tip",
                "port handle" : 0,
                "load"        : False,
                "filename"    : "n/a",
                "source"      : "cylinder",
                "colour"      : [1.0, 0.0, 0.0],
                "height"      : 50.0,
                "radius"      : 10.0,
                "angle"       : 90.0,
                "orientation" : [0.0, 0.0, 1.0]
            },
        ]
    }
    with pytest.raises(RuntimeError):
        _ = OverlayApp(configuration)


def test_invalid_video_config(setup_qt):
    """
    Test that the overlay function works when using recorded backdrop
    """
    _ = setup_qt
    configuration = {
        "image" :
        {
        },
        "tracker config" :
        {
            "tracker type" : "aruco",
            "debug"	   : False,
            "video source" : "data/aruco_tag.avi"
        },
        "models" : [
            {
                "name"        : "tip",
                "port handle" : 0,
                "load"        : False,
                "filename"    : "n/a",
                "source"      : "cylinder",
                "colour"      : [1.0, 0.0, 0.0],
                "height"      : 50.0,
                "radius"      : 10.0,
                "angle"       : 90.0,
                "orientation" : [0.0, 0.0, 1.0]
            },
        ]
    }
    with pytest.raises(KeyError):
        _ = OverlayApp(configuration)

def test_key_press_event(setup_qt):
    """
    Test key press events
    """
    _ = setup_qt
    configuration = {
        "tracker config" :
        {
            "tracker type" : "aruco",
            "debug"	   : False,
            "video source" : "data/aruco_tag.avi"
        },
        "models" : [
            {
                "name"        : "tip",
                "port handle" : 0,
                "load"        : False,
                "source"      : "cylinder",
                "colour"      : [1.0, 0.0, 0.0],
                "height"      : 50.0,
                "radius"      : 10.0,
            },
        ]
    }
    overlay = OverlayApp(configuration)

    overlay.vtk_overlay_window.SetKeySym("p")
    overlay.vtk_overlay_window.KeyPressEvent()

    overlay.vtk_overlay_window.SetKeySym("x")
    overlay.vtk_overlay_window.KeyPressEvent()
