#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.dao.programdb.test_rtkmissionphase.py is part of The RTK Project
#
# All rights reserved.
"""Test class for testing the RTKPhase module algorithms and models."""

import pytest

from rtk.dao.programdb.RTKMissionPhase import RTKMissionPhase

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'

ATTRIBUTES = {
    'description': 'Test Mission Phase 1',
    'phase_end': 0.0,
    'phase_start': 0.0,
    'mission_id': 1,
    'phase_id': 1,
    'name': ''
}


@pytest.mark.integration
def test_rtkmissionphase_create(test_dao):
    """ __init__() should create an RTKPhase model. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKMissionPhase).first()

    assert isinstance(DUT, RTKMissionPhase)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'rtk_mission_phase'
    assert DUT.mission_id == 1
    assert DUT.phase_id == 1
    assert DUT.description == 'Test Mission Phase 1'
    assert DUT.name == ''
    assert DUT.phase_start == 0.0
    assert DUT.phase_end == 0.0


@pytest.mark.integration
def test_get_attributes(test_dao):
    """ get_attributes() should return a tuple of attributes values on success. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKMissionPhase).first()

    assert DUT.get_attributes() == ATTRIBUTES


@pytest.mark.integration
def test_set_attributes(test_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKMissionPhase).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating RTKMissionPhase {0:d} "
                    "attributes.".format(DUT.phase_id))


@pytest.mark.integration
def test_set_attributes_wrong_type(test_dao):
    """ set_attributes() should return a 10 error code when passed the wrong data type. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKMissionPhase).first()

    ATTRIBUTES.pop('phase_end')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RTK ERROR: Missing attribute 'phase_end' in attribute "
                    "dictionary passed to RTKMissionPhase.set_attributes().")
