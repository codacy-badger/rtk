#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       rtk.tests.modules.usage.test_mission.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing Mission module algorithms and models."""

from treelib import Tree

import pytest

from rtk.modules.usage import dtmMission
from rtk.dao import DAO
from rtk.dao import RTKMission

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


@pytest.mark.integration
def test_create_data_model(test_dao):
    """ __init__() should return a Mission data model. """
    DUT = dtmMission(test_dao)

    assert isinstance(DUT, dtmMission)
    assert isinstance(DUT.tree, Tree)
    assert isinstance(DUT.dao, DAO)


@pytest.mark.integration
def test_select_all(test_dao):
    """ select_all() should return a Tree() object populated with RTKMission instances on success. """
    DUT = dtmMission(test_dao)

    _tree = DUT.select_all(1)

    assert isinstance(_tree, Tree)
    assert isinstance(_tree.get_node(1).data, RTKMission)


@pytest.mark.integration
def test_select(test_dao):
    """ select() should return an instance of the RTKMission data model on success. """
    DUT = dtmMission(test_dao)
    DUT.select_all(1)

    _mission = DUT.select(1)

    assert isinstance(_mission, RTKMission)
    assert _mission.mission_id == 1
    assert _mission.description == 'Test Mission'


@pytest.mark.integration
def test_select_non_existent_id(test_dao):
    """ select() should return None when passed a Mission ID that doesn't exist. """
    DUT = dtmMission(test_dao)
    DUT.select_all(1)

    assert DUT.select(100) is None


@pytest.mark.integration
def test_insert(test_dao):
    """ insert() should return a zero error code on success. """
    DUT = dtmMission(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.insert(revision_id=1)

    assert _error_code == 0
    assert _msg == ('RTK SUCCESS: Adding one or more items to the RTK Program '
                    'database.')
    assert DUT.last_id == 2


@pytest.mark.integration
def test_delete(test_dao):
    """ delete() should return False on success. """
    DUT = dtmMission(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.delete(DUT.last_id)

    assert _error_code == 0
    assert _msg == ('RTK SUCCESS: Deleting an item from the RTK Program '
                    'database.')


@pytest.mark.integration
def test_delete_non_existent_id(test_dao):
    """ delete() should return True when passed a Mission ID that doesn't exist. """
    DUT = dtmMission(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.delete(300)

    assert _error_code == 2005
    assert _msg == ('  RTK ERROR: Attempted to delete non-existent Mission ID '
                    '300.')


@pytest.mark.integration
def test_update(test_dao):
    """ update() should return a zero error code on success. """
    DUT = dtmMission(test_dao)
    DUT.select_all(1)

    _mission = DUT.select(1)
    _mission.description = 'Test Mission'

    _error_code, _msg = DUT.update(1)

    assert _error_code == 0
    assert _msg == ('RTK SUCCESS: Updating the RTK Program database.')


@pytest.mark.integration
def test_update_non_existent_id(test_dao):
    """ update() should return a non-zero error code when passed a Mission ID that doesn't exist. """
    DUT = dtmMission(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.update(100)

    assert _error_code == 2006
    assert _msg == ('RTK ERROR: Attempted to save non-existent Mission ID '
                    '100.')


@pytest.mark.integration
def test_update_all(test_dao):
    """ update_all() should return a zero error code on success. """
    DUT = dtmMission(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.update_all()

    assert _error_code == 0
    assert _msg == ('RTK SUCCESS: Updating the RTK Program database.')
