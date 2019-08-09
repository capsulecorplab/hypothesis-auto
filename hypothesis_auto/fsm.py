# Template classes for implementing a Finite State Machine
from abc import ABC, abstractmethod


class State(ABC):
    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def next(self, condition):
        pass


class StateMachine(ABC):
    def __init__(self, initialState: State, initialCondition) -> None:
        self.state = initialState
        self.condition = initialCondition

    @abstractmethod
    def run(self) -> None:
        self.state.run()
        while True:
            self.state.next(self.condition)
            self.state.run()
