# coding=utf-8

"""scikit-surgerytrackervisualisation tests"""

from sksurgerycore.configuration.configuration_manager import \
        ConfigurationManager
from sksurgerytrackervisualisation.overlay_app.overlay import OverlayApp

# Pytest style

def test_overlay_example(setup_qt):
    """
    Test that the populate models function works
    """
    _ = setup_qt
    configurer = ConfigurationManager("example_config.json")
    configuration = configurer.get_copy()
    _ = OverlayApp(configuration)
