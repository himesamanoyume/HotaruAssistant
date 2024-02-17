from abc import ABC, abstractmethod

class BaseState(ABC):
    mCurrentState = None

    @abstractmethod
    def __new__(cls, state):
        cls.mCurrentState = state

    @abstractmethod
    @classmethod
    def StartState(cls):
        pass
    
    @abstractmethod
    @classmethod
    def RunningState(cls):
        pass
    
    @abstractmethod
    @classmethod
    def ExitState(cls):
        pass
