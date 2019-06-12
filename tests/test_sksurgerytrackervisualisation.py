# coding=utf-8

"""scikit-surgerytrackervisualisation tests"""

from sksurgerytrackervisualisation.overlay_app.overlay import populate_models
from sksurgerycore.configuration.configuration_manager import \
        ConfigurationManager
from sksurgerytrackervisualisation.shapes import cone, cylinder

# Pytest style

def test_populate_models():

    configurer = ConfigurationManager("example_config.json")
    configuration = configurer.get_copy()
    populate_models(configuration.get("models"))

