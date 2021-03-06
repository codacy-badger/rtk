# -*- coding: utf-8 -*-
#
#       tests.modules.hardware.test_designmechanic.py is part of The RTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing DesignMechanic module algorithms and models. """

from treelib import Tree

import pytest

from rtk.modules.hardware import dtmDesignMechanic
from rtk.dao import DAO
from rtk.dao import RTKDesignMechanic

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "weibullguy" Rowland'


@pytest.mark.integration
def test_data_model_create(test_dao):
    """ __init__() should return a DesignMechanic model. """
    DUT = dtmDesignMechanic(test_dao)

    assert isinstance(DUT, dtmDesignMechanic)
    assert isinstance(DUT.tree, Tree)
    assert isinstance(DUT.dao, DAO)
    assert DUT._tag == 'DesignMechanic'


@pytest.mark.integration
def test_select_all(test_dao):
    """ select_all() should return a Tree() object populated with RTKDesignMechanic instances on success. """
    DUT = dtmDesignMechanic(test_dao)

    _tree = DUT.select_all(2)

    assert isinstance(_tree, Tree)
    assert isinstance(_tree.get_node(2).data, RTKDesignMechanic)


@pytest.mark.integration
def test_select(test_dao):
    """ select() should return an instance of the RTKDesignMechanic data model on success. """
    DUT = dtmDesignMechanic(test_dao)
    DUT.select_all(2)

    _design_mechanic = DUT.select(2)

    assert isinstance(_design_mechanic, RTKDesignMechanic)
    assert _design_mechanic.hardware_id == 2
    assert _design_mechanic.lubrication_id == 0


@pytest.mark.integration
def test_select_non_existent_id(test_dao):
    """ select() should return None when a non-existent DesignMechanic ID is requested. """
    DUT = dtmDesignMechanic(test_dao)

    _design_electric = DUT.select(100)

    assert _design_electric is None


@pytest.mark.integration
def test_insert(test_dao):
    """ insert() should return False on success when inserting a DesignMechanic record. """
    DUT = dtmDesignMechanic(test_dao)
    DUT.select_all(3)

    _error_code, _msg = DUT.insert(hardware_id=9)

    assert _error_code == 0
    assert _msg == ('RTK SUCCESS: Adding one or more items to the RTK Program '
                    'database.')


@pytest.mark.integration
def test_delete(test_dao):
    """ delete() should return a zero error code on success. """
    DUT = dtmDesignMechanic(test_dao)
    DUT.select_all(4)

    _error_code, _msg = DUT.delete(DUT.last_id)

    assert _error_code == 0
    assert _msg == ('RTK SUCCESS: Deleting an item from the RTK Program '
                    'database.')


@pytest.mark.integration
def test_delete_non_existent_id(test_dao):
    """ delete() should return a non-zero error code when passed a DesignMechanic ID that doesn't exist. """
    DUT = dtmDesignMechanic(test_dao)
    DUT.select_all(3)

    _error_code, _msg = DUT.delete(300)

    assert _error_code == 2005
    assert _msg == ('  RTK ERROR: Attempted to delete non-existent '
                    'DesignMechanic record ID 300.')


@pytest.mark.integration
def test_update(test_dao):
    """ update() should return a zero error code on success. """
    DUT = dtmDesignMechanic(test_dao)
    DUT.select_all(3)

    _design_electric = DUT.select(3)
    _design_electric.resistance = 0.9832

    _error_code, _msg = DUT.update(3)

    assert _error_code == 0
    assert _msg == ('RTK SUCCESS: Updating the RTK Program database.')


@pytest.mark.integration
def test_update_non_existent_id(test_dao):
    """ update() should return a non-zero error code when passed a DesignMechanic ID that doesn't exist. """
    DUT = dtmDesignMechanic(test_dao)
    DUT.select_all(3)

    _error_code, _msg = DUT.update(100)

    assert _error_code == 2006
    assert _msg == ('RTK ERROR: Attempted to save non-existent DesignMechanic '
                    'record ID 100.')


@pytest.mark.integration
def test_update_all(test_dao):
    """ update_all() should return a zero error code on success. """
    DUT = dtmDesignMechanic(test_dao)
    DUT.select_all(3)

    _error_code, _msg = DUT.update_all()

    assert _error_code == 0
    assert _msg == ('RTK SUCCESS: Updating the RTK Program database.')
