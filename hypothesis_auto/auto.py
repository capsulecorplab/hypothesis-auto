from hypothesis.stateful import RuleBasedStateMachine, rule, precondition

from hypothesis_auto.fsm import State, StateMachine


class GearState(State):
    def run(self):
        print("entered", self.__class__.__name__)

    def next(self, rpm: int):
        pass


class Neutral(GearState):
    def next(self, rpm: int) -> "GearState":
        if rpm > 0:
            return FirstGear()
        else:
            return Neutral()


class FirstGear(GearState):
    def next(self, rpm: int) -> "GearState":
        if rpm >= 1000:
            return SecondGear()
        elif rpm == 0:
            return Neutral()
        else:
            return FirstGear()


class SecondGear(GearState):
    def next(self, rpm: int) -> "GearState":
        if rpm >= 2000:
            return ThirdGear()
        elif rpm < 1000:
            return FirstGear()
        else:
            return Neutral()


class ThirdGear(GearState):
    def next(self, rpm: int) -> "GearState":
        if rpm < 2000:
            return SecondGear()
        else:
            return ThirdGear()


class TransmissionSystem(RuleBasedStateMachine):
    def __init__(self, initialState=FirstGear(), initialCondition=100) -> None:
        super(TransmissionSystem, self).__init__()
        self.set_state(initialState)
        self.rpm = initialCondition

    def runAll(self) -> None:
        self.state().run()
        self.set_state(self.state().next(self.rpm))
        while not isinstance(self.state(), Neutral):
            self.state.run()
            self.state = self.state().next(self.rpm)

    @rule()  # type: ignore
    @precondition(lambda self: self.rpm is int)  # type: ignore
    def state(self):
        return self._state

    def set_state(self, state) -> None:
        self._state = state
