# coding=utf-8

"""scikit-surgerytrackervisualisation tests"""
from sksurgerytrackervisualisation.algorithms.background_image import \
        OverlayBackground

# Pytest style

def test_video():
    """
    Test that the overlay function works when using recorded backdrop
    """
    configuration = {
        "source" 	: "data/noisy_logo.avi",
        "loop"   	: True,
        "logo" 	        : False,
        "blank" 	: False
    }
    bg_maker = OverlayBackground(configuration)
    bg_maker.next_image()


def test_video_no_loop():
    """
    Test that the overlay function works when using recorded backdrop
    without looping
    """
    configuration = {
        "source" 	: "data/noisy_logo.avi",
        "loop"   	: False,
        "logo" 	        : False,
        "blank" 	: False
    }
    bg_maker = OverlayBackground(configuration)
    bg_maker.next_image()


def test_video_logo():
    """
    Test that the overlay function works when using the logo
    """
    configuration = {
        "logo" 	        : True,
        "blank" 	: False
    }
    bg_maker = OverlayBackground(configuration)
    bg_maker.next_image()


def test_video_blank():
    """
    Test that the overlay function works when using the logo
    """
    configuration = {
        "blank" 	: True
    }
    bg_maker = OverlayBackground(configuration)
    bg_maker.next_image()
