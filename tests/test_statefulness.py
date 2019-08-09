from hypothesis_auto import *
from hypothesis.stateful import run_state_machine_as_test


def test_rule_based_state_machine():
    run_state_machine_as_test(TransmissionSystem)
