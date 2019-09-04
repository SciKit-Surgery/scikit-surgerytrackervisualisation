# coding=utf-8

"""scikit-surgerytrackervisualisation tests"""

from sksurgerycore.configuration.configuration_manager import \
        ConfigurationManager
import sksurgerytrackervisualisation.algorithms.algorithms as tva

# Pytest style

def test_populate_models():
    """
    Test that the populate models function works
    """
    configurer = ConfigurationManager("example_config.json")
    configuration = configurer.get_copy()
    tva.populate_models(configuration.get("models"))
