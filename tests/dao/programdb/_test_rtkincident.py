#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKIncident.py is part of The RTK Project

#
# All rights reserved.
"""
This is the test class for testing the RTKIncident module algorithms and
models.
"""

import sys
from os.path import dirname

sys.path.insert(
    0,
    dirname(dirname(dirname(dirname(__file__)))) + "/rtk",
)

from datetime import date, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKIncident import RTKIncident

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKIncident(unittest.TestCase):
    """
    Class for testing the RTKIncident class.
    """

    _attributes = (1, 1, 0, 0, 0, 'Incident Analysis', 0, -1, -1,
                   -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0.0, 0,
                   date.today() + timedelta(days=30),
                   date.today() + timedelta(days=30), date.today(),
                   date.today() + timedelta(days=30), '', '', 0, 0, 0, 0, 0,
                   -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1, -1, '', 0, 0, 0, 0, 0, '', '', 0, '')

    def setUp(self):
        """
        Sets up the test fixture for the RTKIncident class.
        """

        engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKIncident).first()
        self.DUT.analysis = self._attributes[5]

        session.commit()

    @attr(all=True, unit=True)
    def test00_rtkincident_create(self):
        """
        (TestRTKIncident) __init__ should create an RTKIncident model.
        """

        self.assertTrue(isinstance(self.DUT, RTKIncident))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_incident')
        self.assertEqual(self.DUT.revision_id, 1)
        self.assertEqual(self.DUT.incident_id, 1)
        self.assertEqual(self.DUT.accepted, 0)
        self.assertEqual(self.DUT.approved, 0)
        self.assertEqual(self.DUT.approved_by, 0)
        self.assertEqual(self.DUT.analysis, 'Incident Analysis')
        self.assertEqual(self.DUT.category_id, 0)
        self.assertEqual(self.DUT.chargeable, -1)
        self.assertEqual(self.DUT.chargeable_1, -1)
        self.assertEqual(self.DUT.chargeable_2, -1)
        self.assertEqual(self.DUT.chargeable_3, -1)
        self.assertEqual(self.DUT.chargeable_4, -1)
        self.assertEqual(self.DUT.chargeable_5, -1)
        self.assertEqual(self.DUT.chargeable_6, -1)
        self.assertEqual(self.DUT.chargeable_7, -1)
        self.assertEqual(self.DUT.chargeable_8, -1)
        self.assertEqual(self.DUT.chargeable_9, -1)
        self.assertEqual(self.DUT.chargeable_10, -1)
        self.assertEqual(self.DUT.complete, 0)
        self.assertEqual(self.DUT.complete_by, 0)
        self.assertEqual(self.DUT.cost, 0)
        self.assertEqual(self.DUT.criticality_id, 0)
        self.assertEqual(
            self.DUT.date_approved, date.today() + timedelta(days=30))
        self.assertEqual(
            self.DUT.date_complete, date.today() + timedelta(days=30))
        self.assertEqual(self.DUT.date_requested, date.today())
        self.assertEqual(
            self.DUT.date_reviewed, date.today() + timedelta(days=30))
        self.assertEqual(self.DUT.description_long, '')
        self.assertEqual(self.DUT.description_short, '')
        self.assertEqual(self.DUT.detection_method_id, 0)
        self.assertEqual(self.DUT.execution_time, 0)
        self.assertEqual(self.DUT.hardware_id, 0)
        self.assertEqual(self.DUT.incident_age, 0)
        self.assertEqual(self.DUT.life_cycle_id, 0)
        self.assertEqual(self.DUT.relevant, -1)
        self.assertEqual(self.DUT.relevant_1, -1)
        self.assertEqual(self.DUT.relevant_2, -1)
        self.assertEqual(self.DUT.relevant_3, -1)
        self.assertEqual(self.DUT.relevant_4, -1)
        self.assertEqual(self.DUT.relevant_5, -1)
        self.assertEqual(self.DUT.relevant_6, -1)
        self.assertEqual(self.DUT.relevant_7, -1)
        self.assertEqual(self.DUT.relevant_8, -1)
        self.assertEqual(self.DUT.relevant_9, -1)
        self.assertEqual(self.DUT.relevant_10, -1)
        self.assertEqual(self.DUT.relevant_11, -1)
        self.assertEqual(self.DUT.relevant_12, -1)
        self.assertEqual(self.DUT.relevant_13, -1)
        self.assertEqual(self.DUT.relevant_14, -1)
        self.assertEqual(self.DUT.relevant_15, -1)
        self.assertEqual(self.DUT.relevant_16, -1)
        self.assertEqual(self.DUT.relevant_17, -1)
        self.assertEqual(self.DUT.relevant_18, -1)
        self.assertEqual(self.DUT.relevant_19, -1)
        self.assertEqual(self.DUT.relevant_20, -1)
        self.assertEqual(self.DUT.remarks, '')
        self.assertEqual(self.DUT.request_by, 0)
        self.assertEqual(self.DUT.reviewed, 0)
        self.assertEqual(self.DUT.reviewed_by, 0)
        self.assertEqual(self.DUT.software_id, 0)
        self.assertEqual(self.DUT.status_id, 0)
        self.assertEqual(self.DUT.test_case, '')
        self.assertEqual(self.DUT.test_found, '')
        self.assertEqual(self.DUT.type_id, 0)
        self.assertEqual(self.DUT.unit, '')

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """
        (TestRTKIncident) get_attributes should return a tuple of attribute values.
        """

        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """
        (TestRTKIncident) set_attributes should return a zero error code on success
        """

        _attributes = (0, 0, 0, 'Incident Analysis', 0, -1, -1, -1,
                       -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0.0, 0,
                       date.today() + timedelta(days=30),
                       date.today() + timedelta(days=30), date.today(),
                       date.today() + timedelta(days=30), '', '', 0, 0, 0, 0,
                       0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
                       -1, -1, -1, -1, -1, -1, -1, -1, '', 0, 0, 0, 0, 0, '',
                       '', 0, '')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKIncident {0:d} " \
                               "attributes.".format(self.DUT.incident_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_wrong_type(self):
        """
        (TestRTKIncident) set_attributes should return a 10 error code when passed the wrong type
        """

        _attributes = (0, 0, 0, 'Incident Analysis', 0, -1, -1, -1, -1,
                       -1, -1, -1, -1, -1, -1, -1, 0, 0, 0.0, 'zero',
                       date.today() + timedelta(days=30),
                       date.today() + timedelta(days=30), date.today(),
                       date.today() + timedelta(days=30), '', '', 0, 0, 0, 0,
                       0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
                       -1, -1, -1, -1, -1, -1, -1, -1, '', 0, 0, 0, 0, 0, '',
                       '', 0, '')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RTK ERROR: Incorrect data type when " \
                               "converting one or more RTKIncident " \
                               "attributes.")

    @attr(all=True, unit=True)
    def test02c_set_attributes_too_few_passed(self):
        """
        (TestRTKIncident) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = (0, 0, 0, 'Incident Analysis', 0, -1, -1, -1,
                       -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0.0, 0,
                       date.today() + timedelta(days=30),
                       date.today() + timedelta(days=30), date.today(),
                       date.today() + timedelta(days=30), '', '', 0, 0, 0, 0,
                       0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
                       -1, -1, -1, -1, -1, -1, -1, -1, '', 0, 0, 0, 0, 0, '')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKIncident.set_attributes().")
