import time

__version__ = '0.0.1'

class FPSTimer:
    """
    A class for timer objects that can wait a variable amount of time to
    maintain a certain framerate.
    """
    DEFAULT_FPS = 60 # If no ctor argument is provided, default to 60 FPS.

    def __init__(self, framesPerSecond=None):
        """
        Create an FPSTimer object that is locked at a specific framerate,
        as dictated by the integer passed for the framesPerSecond parameter.
        """
        if framesPerSecond is None:
            self._framesPerSecond = self.__class__.DEFAULT_FPS
        else:
            self._framesPerSecond = framesPerSecond

        if not isinstance(self._framesPerSecond, (int, float)):
            raise TypeError('framesPerSecond must be a positive, nonzero int or float')
        if isinstance(self._framesPerSecond, (int, float)) and self._framesPerSecond <= 0:
            raise ValueError('framesPerSecond must be a positive, nonzero int or float')

        self._frameDuration = 1.0 / self._framesPerSecond

        self._lastCallEndTime = time.time()
        self._lastZeroCallEndTime = self._lastCallEndTime
        self._lastZeroCount = 1


    def sleep(self):
        """
        Pause for a certain length of time to maintain the a regular
        framerate. The framerate is set by the constructor argument and
        cannot be changed. This method should be called after the work
        for the current frame has been completed. If it has been longer
        than 1 / self._framesPerSecond seconds, the pause duration will be
        0.0. Returns the pause length in seconds as a float.
        """

        # Calculate the amount of time the pause should last, in seconds:
        sleepTime = self._lastZeroCallEndTime + (self._frameDuration * self._lastZeroCount) - time.time()

        # If it has been too long since the last time sleep() was called,
        # don't pause at all.
        if sleepTime < 0:
            self._lastCallEndTime = time.time()
            self._lastZeroCallEndTime = self._lastCallEndTime
            self._lastZeroCount = 1
            return 0.0

        time.sleep(sleepTime)

        self._lastCallEndTime = time.time()
        self._lastZeroCount += 1

        return sleepTime
