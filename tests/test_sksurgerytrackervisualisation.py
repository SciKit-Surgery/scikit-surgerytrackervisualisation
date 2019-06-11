# coding=utf-8

"""scikit-surgerytrackervisualisation tests"""

from sksurgerytrackervisualisation.ui.sksurgerytrackervisualisation_demo import run
from sksurgerytrackervisualisation.shapes import cone, cylinder

# Pytest style

def test_using_pytest_sksurgerytrackervisualisation():
    run("example_config.json") 

