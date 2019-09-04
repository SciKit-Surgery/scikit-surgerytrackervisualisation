# coding=utf-8

"""scikit-surgerytrackervisualisation tests"""
import pytest
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
        "logo" 	: False,
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
        "logo" 	: False,
        "blank" 	: False
    }
    bg_maker = OverlayBackground(configuration)
    bg_maker.next_image()

