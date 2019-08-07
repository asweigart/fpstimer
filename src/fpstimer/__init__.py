import time

__version__ = '0.0.1'

class FPSTimer:
    DEFAULT_FPS = 60 # If no ctor argument is provided, default to 60 FPS.

    def __init__(self, framesPerSecond=None):
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


    def fpsSleep(self):
        sleepTime = self._lastZeroCallEndTime + (self._frameDuration * self._lastZeroCount) - time.time()

        if sleepTime < 0:
            self._lastCallEndTime = time.time()
            self._lastZeroCallEndTime = self._lastCallEndTime
            self._lastZeroCount = 1
            return 0.0

        time.sleep(sleepTime)

        self._lastCallEndTime = time.time()
        self._lastZeroCount += 1

        return sleepTime
