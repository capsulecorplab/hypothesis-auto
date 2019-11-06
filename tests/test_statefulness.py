import hypothesis.strategies as st
import pytest
from hypothesis import given
from hypothesis.stateful import (Bundle, RuleBasedStateMachine, consumes,
                                 invariant, multiple, precondition, rule)

from hypothesis_auto import (FirstGear, GearState, Neutral, SecondGear,
                             ThirdGear, TransmissionSystem)


class AutoFSMTest(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.auto = TransmissionSystem()

    rpms = Bundle('rpms')
    rpm_sets = Bundle('rpm_sets')

    @rule(target=rpms, rpm=st.integers(min_value=0))
    def add_rpm(self, rpm):
        return rpm

    @rule(target=rpm_sets, rpms=st.lists(st.integers(min_value=0)))
    def add_rpms(self, rpms):
        return rpms

    ## These methods exercise the step and run methods of
    ## TransmissionSystem, as possible intervening actions between
    ## test assertions
    @rule(rpm=consumes(rpms))
    def step(self, rpm):
        self.auto.step(rpm)

    @rule(rpms=consumes(rpm_sets))
    def run(self, rpms):
        self.auto.run(rpms)


    # These are the test methods that assert facts about the state machine
    @invariant()
    def state_is_always_a_gear_state(self):
        assert isinstance(self.auto.state, GearState)

    @precondition(lambda self: isinstance(self.auto.state, Neutral))
    @rule(rpm=consumes(rpms))
    def step_from_neutral_must_be_neutral_or_first(self, rpm):
        """Given Neutral state, then next state must be Neutral or FirstGear"""
        self.auto.step(rpm)
        state = self.auto.state
        assert isinstance(state, Neutral) or isinstance(state, FirstGear)

TestAutoFSM = AutoFSMTest.TestCase
