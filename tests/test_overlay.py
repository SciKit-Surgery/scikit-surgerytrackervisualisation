# coding=utf-8

"""scikit-surgerytrackervisualisation tests"""

from sksurgerytrackervisualisation.overlay_app.overlay import OverlayApp

# Pytest style

def test_overlay_example(setup_qt):
    """
    Test that the populate models function works
    """
    _ = setup_qt
    configuration = {
        "image" :
        {
            "source" 	: "data/noisy_logo.avi",
            "loop"   	: True,
            "logo" 	: False,
            "blank" 	: False
        },
        "tracker config" :
        {
            "tracker type" : "aruco",
            "debug"	   : True,
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
    _ = OverlayApp(configuration)
