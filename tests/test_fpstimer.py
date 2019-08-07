from __future__ import division, print_function
import pytest, random, time
import fpstimer

ACCEPTABLE_DEVIATION = 0.02 # 2%

def test_ctor():
    assert fpstimer.FPSTimer()._framesPerSecond == 60 # Test with no argument.
    assert fpstimer.FPSTimer(None)._framesPerSecond == 60 # Test with None argument.
    assert fpstimer.FPSTimer(1)._framesPerSecond == 1 # Test with 60 argument.
    assert fpstimer.FPSTimer(1.0)._framesPerSecond == 1 # Test with 60 argument.

    assert fpstimer.FPSTimer.DEFAULT_FPS == 60 # Test that this constant hasn't changed.

    # Test invalid ctor arguments:
    with pytest.raises(TypeError):
        fpstimer.FPSTimer('invalid')
    with pytest.raises(ValueError):
        fpstimer.FPSTimer(0)
    with pytest.raises(ValueError):
        fpstimer.FPSTimer(-1)


def test_basic():
    # NOTE: This test takes about 45 seconds.
    timer = fpstimer.FPSTimer()
    random.seed(42)

    for testFps in range(10, 110, 10): # Test fps rates 10, 20, ... up to 100.
        for trial in range(5): # Do five trials for each fps rate.

            timer = fpstimer.FPSTimer(testFps)

            start = time.time()
            for i in range(testFps): # Run enough timer.fpsSleep() calls for 1 second.
                pass
                if random.randint(0, 1) == 1:
                    time.sleep(1 / (testFps * 2))
                timer.fpsSleep()
            trialTime = time.time() - start

            assert trialTime < (1 + ACCEPTABLE_DEVIATION), 'Failed for testFps == %s, trialTime was %s' % (testFps, trialTime)

def test_zero():
    timer = fpstimer.FPSTimer(60)
    time.sleep(0.1) # 0.1 seconds is much longer than the 1/60 that fpsSleep() should at most pause for.
    assert timer.fpsSleep() == 0 # fpsSleep() should therefore not have any pause.



if __name__ == '__main__':
    pytest.main()
