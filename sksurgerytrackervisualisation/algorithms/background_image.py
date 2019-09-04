"""
A class to provide the background image
"""
from itertools import cycle
from cv2 import VideoCapture
from numpy import zeros, uint8
from sksurgeryimage.utilities.weisslogo import WeissLogo

class OverlayBackground():
    """
    Provides the background image for the overlay
    window.
    """

    def __init__(self, config):
        """
        Initialises and configures class to provide a background image.
        Image can be a WEISS logo, a blank image, or an image from an
        OpenCV video source.
        :param: A configuration dictionary
        :raises: RunTimeError, KeyError
        """
        self._video_loop_buffer = []
        self._logo_maker = None
        self._blank_image = None
        if "source" in config:
            self.source = VideoCapture(config.get("source"))
            if not self.source.isOpened():
                raise RuntimeError("Failed to open Video camera:"
                                   + str(config.get("source")))

            self.source_name = config.get("source")

            if "loop" in config:
                if config.get("loop"):
                    video_buffer = []
                    ret, image = self.source.read()
                    while ret:
                        video_buffer.append(image)
                        ret, image = self.source.read()

                    self._video_loop_buffer = cycle(video_buffer)
        else:
            if config.get("blank") or config.get("logo"):
                if config.get("logo"):
                    self._logo_maker = WeissLogo()
                else:
                    self._blank_image = zeros(shape=[512, 512, 3], dtype=uint8)
            else:
                raise KeyError("Configuration must contain a" +
                               "video source, blank, or logo")

    def next_image(self):
        """
        Returns a background image.
        The behaviour is determined by the configuration
        dictionary used at init.
        """
        if self._video_loop_buffer:
            image = next(self._video_loop_buffer)
        else:
            if self._logo_maker is not None:
                image = self._logo_maker.get_noisy_logo()
            else:
                if self._blank_image is not None:
                    image = self._blank_image
                else:
                    _, image = self.source.read()
        return image
