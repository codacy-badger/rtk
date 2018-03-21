#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.modules.fmea.test_fmea.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing the FMEA class."""

from treelib import Tree

import pytest

from rtk.dao import RTKMode
from rtk.dao import RTKMechanism
from rtk.dao import RTKCause
from rtk.dao import RTKControl
from rtk.dao import RTKAction
from rtk.modules.fmea import (dtcFMEA, dtmFMEA, dtmAction, dtmControl, dtmMode,
                              dtmMechanism, dtmCause)

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_create_data_model(test_dao):
    """ __init__() should return instance of FMEA data model. """
    DUT = dtmFMEA(test_dao)

    assert isinstance(DUT, dtmFMEA)
    assert isinstance(DUT.dtm_mode, dtmMode)
    assert isinstance(DUT.dtm_mechanism, dtmMechanism)
    assert isinstance(DUT.dtm_cause, dtmCause)
    assert isinstance(DUT.dtm_control, dtmControl)
    assert isinstance(DUT.dtm_action, dtmAction)


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_select_all_functional(test_dao):
    """ select_all() should return a treelib Tree() on success when selecting a Functional FMEA. """
    DUT = dtmFMEA(test_dao)
    _tree = DUT.select_all(1, functional=True)

    assert isinstance(_tree, Tree)


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_select_all_hardware(test_dao):
    """ select_all() should return a treelib Tree() on success when selecting a Hardware FMEA. """
    DUT = dtmFMEA(test_dao)
    _tree = DUT.select_all(1, functional=False)

    assert isinstance(_tree, Tree)


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_select_all_non_existent_hardware_id(test_dao):
    """ select_all() should return an empty Tree() when passed a Hardware ID that doesn't exist. """
    DUT = dtmFMEA(test_dao)
    _tree = DUT.select_all(100, functional=False)

    assert isinstance(_tree, Tree)
    assert _tree.get_node(0).tag == 'FMEA'
    assert _tree.get_node(1) is None


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_select_all_non_existent_function_id(test_dao):
    """ select_all() should return an empty Tree() when passed a Function ID that doesn't exist. """
    DUT = dtmFMEA(test_dao)
    _tree = DUT.select_all(100, functional=True)

    assert isinstance(_tree, Tree)
    assert _tree.get_node(0).tag == 'FMEA'
    assert _tree.get_node(1) is None


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_select_mode(test_dao):
    """ select() should return an instance of RTKMode on success. """
    DUT = dtmFMEA(test_dao)
    DUT.select_all(1, functional=True)

    _entity = DUT.select('0.1')
    assert isinstance(_entity, RTKMode)
    assert _entity.description == ("Function Test Failure Mode")


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_select_mechanism(test_dao):
    """ select() should return an instance of RTKMechanism on success. """
    DUT = dtmFMEA(test_dao)
    DUT.select_all(1, functional=False)

    _entity = DUT.select('0.2.1')

    assert isinstance(_entity, RTKMechanism)
    assert _entity.description == 'Test Failure Mechanism #1'


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_select_cause(test_dao):
    """ select() should return an instance of RTKCause on success. """
    DUT = dtmFMEA(test_dao)
    DUT.select_all(1, functional=False)

    _entity = DUT.select('0.2.1.1')

    assert isinstance(_entity, RTKCause)
    assert _entity.description == 'Test Failure Cause #1'


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_select_control_functional(test_dao):
    """ select() should return an instance of RTKControl when selecting from a functional FMEA on success. """
    DUT = dtmFMEA(test_dao)
    DUT.select_all(1, functional=True)

    _entity = DUT.select('0.1.01')

    assert isinstance(_entity, RTKControl)
    assert _entity.description == ("Test Functional FMEA Control #1")


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_select_control_hardware(test_dao):
    """ select() should return an instance of RTKControl when selecting from a hardware FMEA on success. """
    DUT = dtmFMEA(test_dao)
    DUT.select_all(1, functional=False)
    _entity = DUT.select('0.2.1.1.02')

    assert isinstance(_entity, RTKControl)
    assert _entity.description == 'Functional FMEA control.'


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_select_action_functional(test_dao):
    """ select() should return an instance of RTKAction when selecting from a functional FMEA on success. """
    DUT = dtmFMEA(test_dao)
    DUT.select_all(1, functional=True)

    _entity = DUT.select('0.1.1')

    assert isinstance(_entity, RTKAction)
    assert _entity.action_recommended == ("Test Functional FMEA Recommended "
                                          "Action #1")


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_select_action_hardware(test_dao):
    """ select() should return an instance of RTKAction when selecting from a hardware FMEA on success. """
    DUT = dtmFMEA(test_dao)
    DUT.select_all(1, functional=False)

    _entity = DUT.select('0.2.1.1.2')
    print DUT.tree.nodes
    assert isinstance(_entity, RTKAction)
    assert _entity.action_recommended == 'Do this stuff and do it now!!'


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_insert_mode_functional(test_dao):
    """ insert() should return a zero error code on success when adding a new Mode to a Functional FMEA. """
    DUT = dtmFMEA(test_dao)
    DUT.select_all(1, functional=True)

    _error_code, _msg = DUT.insert(entity_id=1, parent_id=0, level='mode')

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Adding one or more items to the RTK Program "
                    "database.")
    _node_id = '0.' + str(DUT.dtm_mode.last_id)

    _mode = DUT.select(_node_id)

    assert isinstance(_mode, RTKMode)
    assert _mode.function_id == 1
    assert _mode.hardware_id == -1

    _tree_mode = DUT.tree.get_node(_node_id)
    assert isinstance(_tree_mode.data, RTKMode)
    assert _tree_mode.data == _mode


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_insert_mode_hardware(test_dao):
    """ insert() should return a zero error code on success when adding a new Mode to a Hardware FMEA. """
    DUT = dtmFMEA(test_dao)
    DUT.select_all(1, functional=False)

    _error_code, _msg = DUT.insert(entity_id=1, parent_id=0, level='mode')

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Adding one or more items to the RTK Program "
                    "database.")
    _node_id = '0.' + str(DUT.dtm_mode.last_id)

    _mode = DUT.select(_node_id)

    assert isinstance(_mode, RTKMode)
    assert _mode.function_id == -1
    assert _mode.hardware_id == 1

    _tree_mode = DUT.tree.get_node(_node_id)
    assert isinstance(_tree_mode.data, RTKMode)
    assert _mode == _tree_mode.data


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_insert_mode_hardware_non_existant_level(test_dao):
    """ insert() should return a non-zero error code when trying to add a non-existant level. """
    DUT = dtmFMEA(test_dao)
    DUT.select_all(1, functional=False)

    _error_code, _msg = DUT.insert(entity_id=1, parent_id=0, level='juice')

    assert _error_code == 2005
    assert _msg == ("RTK ERROR: Attempted to add an item to the FMEA with an "
                    "undefined indenture level.  Level juice was requested.  "
                    "Must be one of mode, mechanism, cause, control, or "
                    "action.")


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_insert_mechanism(test_dao):
    """ insert() should return a zero error code on success when adding a new Mechanism to a Hardware FMEA. """
    DUT = dtmFMEA(test_dao)
    DUT.select_all(1, functional=False)

    _error_code, _msg = DUT.insert(
        entity_id=1, parent_id='0.2', level='mechanism')

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Adding one or more items to the RTK Program "
                    "database.")
    _node_id = '0.2.' + str(DUT.dtm_mechanism.last_id)

    _mechanism = DUT.select(_node_id)

    assert isinstance(_mechanism, RTKMechanism)
    assert _mechanism.mode_id == 1
    assert _mechanism.mechanism_id == DUT.dtm_mechanism.last_id

    _tree_mechanism = DUT.tree.get_node(_node_id)
    assert isinstance(_tree_mechanism.data, RTKMechanism)
    assert _mechanism == _tree_mechanism.data


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_insert_cause(test_dao):
    """ insert() should return a zero error code on success when adding a new Cause to a Hardware FMEA. """
    DUT = dtmFMEA(test_dao)
    DUT.select_all(1, functional=False)

    _error_code, _msg = DUT.insert(
        entity_id=1, parent_id='0.2.1', level='cause')

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Adding one or more items to the RTK Program "
                    "database.")

    _node_id = '0.2.1.' + str(DUT.dtm_cause.last_id)

    _cause = DUT.select(_node_id)

    assert isinstance(_cause, RTKCause)
    assert _cause.mechanism_id == 1
    assert _cause.cause_id == DUT.dtm_cause.last_id

    _tree_cause = DUT.tree.get_node(_node_id)
    assert isinstance(_tree_cause.data, RTKCause)
    assert _tree_cause.data == _cause


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_insert_control_functional(test_dao):
    """ insert() should return a zero error code on success when adding a new Control to a Functional FMEA. """
    DUT = dtmFMEA(test_dao)
    DUT.select_all(1, functional=True)

    _error_code, _msg = DUT.insert(
        entity_id=1, parent_id='0.1', level='control')

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Adding one or more items to the RTK Program "
                    "database.")
    _node_id = '0.1.0' + str(DUT.dtm_control.last_id)

    _control = DUT.select(_node_id)

    assert isinstance(_control, RTKControl)
    assert _control.mode_id == 1
    assert _control.cause_id == -1

    _tree_control = DUT.tree.get_node(_node_id)
    assert isinstance(_tree_control.data, RTKControl)
    assert _control == _tree_control.data


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_insert_control_hardware(test_dao):
    """ insert() should return a zero error code on success when adding a new Control to a Hardware FMEA. """
    DUT = dtmFMEA(test_dao)
    DUT.select_all(1, functional=False)

    _error_code, _msg = DUT.insert(
        entity_id=2, parent_id='0.2.1.1', level='control')

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Adding one or more items to the RTK Program "
                    "database.")
    _node_id = '0.2.1.1.0' + str(DUT.dtm_control.last_id)

    _control = DUT.select(_node_id)

    assert isinstance(_control, RTKControl)
    assert _control.mode_id == -1
    assert _control.cause_id == 2

    _tree_control = DUT.tree.get_node(_node_id)
    assert isinstance(_tree_control.data, RTKControl)
    assert _control == _tree_control.data


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_insert_action_functional(test_dao):
    """ insert() should return a zero error code on success when adding a new Action to a Functional FMEA. """
    DUT = dtmFMEA(test_dao)
    DUT.select_all(1, functional=True)

    _error_code, _msg = DUT.insert(
        entity_id=1, parent_id='0.1', level='action')

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Adding one or more items to the RTK Program "
                    "database.")
    _node_id = '0.1.' + str(DUT.dtm_action.last_id)

    _action = DUT.select(_node_id)

    assert isinstance(_action, RTKAction)
    assert _action.mode_id == 1
    assert _action.cause_id == -1

    _tree_action = DUT.tree.get_node(_node_id)
    assert isinstance(_tree_action.data, RTKAction)
    assert _action == _tree_action.data


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_insert_action_hardware(test_dao):
    """ insert() should return a zero error code on success when adding a new Action to a Hardware FMEA. """
    DUT = dtmFMEA(test_dao)
    DUT.select_all(1, functional=False)

    _error_code, _msg = DUT.insert(
        entity_id=1, parent_id='0.2.1.1', level='action')

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Adding one or more items to the RTK Program "
                    "database.")
    _node_id = '0.2.1.1.' + str(DUT.dtm_action.last_id)

    _action = DUT.select(_node_id)

    assert isinstance(_action, RTKAction)
    assert _action.mode_id == -1
    assert _action.cause_id == 1

    _tree_action = DUT.tree.get_node(_node_id)
    assert isinstance(_tree_action.data, RTKAction)
    assert _action == _tree_action.data


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_insert_non_existent_type(test_dao):
    """ insert() should return a 2005 error code when attempting to add something other than a Mode, Mechanism, Cause, Control, or Action. """
    DUT = dtmFMEA(test_dao)
    DUT.select_all(1, functional=False)

    _error_code, _msg = DUT.insert(
        entity_id=100, parent_id=0, level='scadamoosh')

    assert _error_code == 2005
    assert _msg == ("RTK ERROR: Attempted to add an item to the FMEA with an "
                    "undefined indenture level.  Level scadamoosh was "
                    "requested.  Must be one of mode, mechanism, cause, "
                    "control, or action.")


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_insert_no_parent_in_tree(test_dao):
    """ insert() should return a 2005 error code when attempting to add something to a non-existant parent Node. """
    DUT = dtmFMEA(test_dao)
    DUT.select_all(1, functional=False)

    _error_code, _msg = DUT.insert(
        entity_id=1, parent_id='mode_1', level='action')

    assert _error_code == 2005
    assert _msg == ("RTK ERROR: Attempted to add an item under non-existent "
                    "Node ID: mode_1.")


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_delete_control_functional(test_dao):
    """ delete() should return a zero error code on success when removing a Control. """
    DUT = dtmFMEA(test_dao)
    DUT.select_all(1, functional=True)
    DUT.insert(entity_id=1, parent_id='0.1', level='control')

    _node_id = '0.1.0' + str(DUT.dtm_control.last_id)

    _error_code, _msg = DUT.delete(_node_id)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Deleting an item from the RTK Program "
                    "database.")


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_delete_non_existent_node_id(test_dao):
    """ delete() should return a 2105 error code when attempting to remove a non-existant item from the FMEA. """
    DUT = dtmFMEA(test_dao)
    DUT.select_all(1, functional=True)

    _error_code, _msg = DUT.delete('scadamoosh_1')

    assert _error_code == 2005
    assert _msg == ("  RTK ERROR: Attempted to delete non-existent entity "
                    "with Node ID scadamoosh_1 from the FMEA.")


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_update(test_dao):
    """ update() should return a zero error code on success. """
    DUT = dtmFMEA(test_dao)
    DUT.select_all(1, functional=True)

    _error_code, _msg = DUT.update('0.1')

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating the RTK Program database.")


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_update_non_existent_node_id(test_dao):
    """ update() should return a 2106 error code when attempting to update a non-existent Node ID from a functional FMEA. """
    DUT = dtmFMEA(test_dao)
    DUT.select_all(1, functional=True)

    _error_code, _msg = DUT.update('mode_1000')

    assert _error_code == 2006
    assert _msg == ("RTK ERROR: Attempted to save non-existent entity with "
                    "Node ID mode_1000.")


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_update_all(test_dao):
    """ update_all() should return a zero error code on success. """
    DUT = dtmFMEA(test_dao)
    DUT.select_all(1, functional=True)

    _error_code, _msg = DUT.update_all()

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating the RTK Program database.")


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_calculate_criticality(test_dao):
    """ calculate_criticality() returns a zero error code on success. """
    DUT = dtmFMEA(test_dao)
    DUT.select_all(1, functional=False)
    _mode = DUT.select('0.2')

    _mode.mode_ratio = 0.4
    _mode.mode_op_time = 100.0
    _mode.effect_probability = 1.0
    _error_code, _msg = DUT.calculate_criticality(0.00001)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Calculating failure mode 4 criticality.")
    assert _mode.mode_criticality == pytest.approx(0.0004)


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_calculate_mechanism_rpn(test_dao):
    """ calculate_mechanism_rpn() returns a zero error code on success. """
    DUT = dtmFMEA(test_dao)
    DUT.select_all(1, functional=False)

    for _node in DUT.tree.children('0.2'):
        _mechanism = _node.data
        _attributes = _mechanism.get_attributes()
        _attributes['rpn_detection'] = 4
        _attributes['rpn_occurrence'] = 7
        _attributes['rpn_detection_new'] = 3
        _attributes['rpn_occurrence_new'] = 5
        _mechanism.set_attributes(_attributes)

    _error_code, _msg = DUT.calculate_rpn('0.2', 7, 4)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Calculating failure mechanism {0:d} RPN.").\
                         format(DUT.dtm_mechanism.last_id)
    assert _mechanism.rpn == 196
    assert _mechanism.rpn_new == 60


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_calculate_cause_rpn(test_dao):
    """ calculate_cause_rpn() returns a zero error code on success. """
    DUT = dtmFMEA(test_dao)
    DUT.select_all(1, functional=False)

    for _node in DUT.tree.children('0.2.1'):
        _cause = _node.data
        _attributes = _cause.get_attributes()
        _attributes['rpn_detection'] = 4
        _attributes['rpn_occurrence'] = 7
        _attributes['rpn_detection_new'] = 3
        _attributes['rpn_occurrence_new'] = 5
        _cause.set_attributes(_attributes)

    _error_code, _msg = DUT.calculate_rpn('0.2.1', 7, 4)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Calculating failure cause {0:d} RPN.").\
                         format(DUT.dtm_cause.last_id)
    assert _cause.rpn == 196
    assert _cause.rpn_new == 60


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_create_data_controller(test_dao, test_configuration):
    """ __init__() should return instance of FMEA data controller. """
    DUT = dtcFMEA(test_dao, test_configuration, test=True)

    assert isinstance(DUT, dtcFMEA)
    assert isinstance(DUT._dtm_data_model, dtmFMEA)


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_request_select_all_hardware(test_dao, test_configuration):
    """ request_select_all() should return a treelib Tree() with the hardware FMEA. """
    DUT = dtcFMEA(test_dao, test_configuration, test=True)

    assert isinstance(DUT.request_select_all(1, functional=False), Tree)


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_request_select_all_functional(test_dao, test_configuration):
    """ request_select_all() should return a treelib Tree() with the functional FMEA. """
    DUT = dtcFMEA(test_dao, test_configuration, test=True)

    assert isinstance(DUT.request_select_all(1, functional=True), Tree)


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_request_insert_mode_functional(test_dao, test_configuration):
    """ request_insert() should return False on success when adding a mode to a functional FMEA. """
    DUT = dtcFMEA(test_dao, test_configuration, test=True)

    DUT.request_select_all(1, functional=True)
    assert not DUT.request_insert(1, 0, 'mode')


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_request_insert_mode_hardware(test_dao, test_configuration):
    """ request_insert() should return False on success when addin a mode to a hardware FMEA. """
    DUT = dtcFMEA(test_dao, test_configuration, test=True)
    DUT.request_select_all(1, functional=False)

    assert not DUT.request_insert(1, 0, 'mode')


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_request_insert_mechanism(test_dao, test_configuration):
    """ request_insert() should return a False on success when adding a new Mechanism to a Hardware FMEA. """
    DUT = dtcFMEA(test_dao, test_configuration, test=True)
    DUT.request_select_all(1, functional=False)

    assert not DUT.request_insert(1, '0.2', 'mechanism')


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_request_delete_control_functional(test_dao, test_configuration):
    """ request_delete() should return False on success when removing a Control from a functional FMEA. """
    DUT = dtcFMEA(test_dao, test_configuration, test=True)
    DUT.request_select_all(1, functional=True)
    _node_id = '0.1.0' + str(DUT._dtm_data_model.dtm_control.last_id)

    assert not DUT.request_delete(_node_id)


@pytest.mark.integration
@pytest.mark.hardware
@pytest.mark.fmea
def test_request_update_all(test_dao, test_configuration):
    """ request_update_all() should return False on success. """
    DUT = dtcFMEA(test_dao, test_configuration, test=True)
    DUT.request_select_all(1, functional=True)

    assert not DUT.request_update_all()