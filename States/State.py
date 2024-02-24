
class State:
    def __new__(cls, stateName, beginHandle, runningHandle, exitHandle):
        cls.mStateName = stateName
        beginHandle()
        runningHandle()
        exitHandle()

        return cls

