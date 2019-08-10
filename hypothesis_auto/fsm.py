# Template classes for implementing a Finite State Machine
from abc import ABC, abstractmethod


class State(ABC):
    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def next(self, condition) -> "State":
        pass


class StateMachine(ABC):
    def __init__(self, initial_state: State, initial_condition) -> None:
        self._state = initial_state
        self.condition = initial_condition

    def run(self, conditions) -> None:
        for cond in conditions:
            self.step(cond)
            if self.stop_predicate():
                return

    def step(self, condition):
        self.condition = condition
        self.state = self._state.next(self.condition)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value: State):
        self._state = value
        self._state.run()

    def stop_predicate(self):
        """State machine will run until this function returns True"""
        return False
