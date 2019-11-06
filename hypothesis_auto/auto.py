from hypothesis_auto.fsm import State, StateMachine


class GearState(State):
    def run(self):
        print("entered", self.__class__.__name__)


class Neutral(GearState):
    def next(self, rpm: int) -> GearState:
        if rpm > 0:
            return FirstGear()
        else:
            return Neutral()


class FirstGear(GearState):
    def next(self, rpm: int) -> GearState:
        if rpm >= 1000:
            return SecondGear()
        elif rpm == 0:
            return Neutral()
        else:
            return FirstGear()


class SecondGear(GearState):
    def next(self, rpm: int) -> GearState:
        if rpm >= 2000:
            return ThirdGear()
        elif rpm < 1000:
            return FirstGear()
        else:
            return Neutral()


class ThirdGear(GearState):
    def next(self, rpm: int) -> GearState:
        if rpm < 2000:
            return SecondGear()
        else:
            return ThirdGear()


class TransmissionSystem(StateMachine):
    def __init__(self,
                 initial_state: GearState = FirstGear(),
                 initial_condition: int = 100) -> None:
        super().__init__(initial_state, initial_condition)
        self.rpm = self.condition

    def stop_predicate(self):
        return isinstance(self.state, Neutral)
