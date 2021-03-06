#!/usr/bin/env python -O
"""
This is the test class for testing Incident module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       tests.unit.TestIncident.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER
#    OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import sys
from os.path import dirname

sys.path.insert(
    0,
    dirname(dirname(dirname(__file__))) + "/rtk",
)

import unittest
from nose.plugins.attrib import attr

from incident.Incident import Model, Incident

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestIncidentModel(unittest.TestCase):
    """
    Class for testing the Incident data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Incident class.
        """

        self.DUT = Model()

    @attr(all=True, unit=True)
    def test00_create(self):
        """
        (TestIncident) __init__ should return an Incident model
        """

        self.assertTrue(isinstance(self.DUT, Model))
        self.assertEqual(self.DUT.lstRelevant, [
            -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
            -1, -1, -1
        ])
        self.assertEqual(self.DUT.lstChargeable,
                         [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1])
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.incident_id, None)
        self.assertEqual(self.DUT.incident_category, 0)
        self.assertEqual(self.DUT.incident_type, 0)
        self.assertEqual(self.DUT.short_description, '')
        self.assertEqual(self.DUT.detail_description, '')
        self.assertEqual(self.DUT.criticality, 0)
        self.assertEqual(self.DUT.detection_method, 0)
        self.assertEqual(self.DUT.remarks, '')
        self.assertEqual(self.DUT.status, 0)
        self.assertEqual(self.DUT.test, '')
        self.assertEqual(self.DUT.test_case, '')
        self.assertEqual(self.DUT.execution_time, 0.0)
        self.assertEqual(self.DUT.unit_id, '')
        self.assertEqual(self.DUT.cost, 0.0)
        self.assertEqual(self.DUT.incident_age, 0.0)
        self.assertEqual(self.DUT.hardware_id, 0)
        self.assertEqual(self.DUT.software_id, 0)
        self.assertEqual(self.DUT.request_by, 0)
        self.assertEqual(self.DUT.request_date, 0)
        self.assertEqual(self.DUT.reviewed, False)
        self.assertEqual(self.DUT.review_by, 0)
        self.assertEqual(self.DUT.review_date, 0)
        self.assertEqual(self.DUT.approved, False)
        self.assertEqual(self.DUT.approve_by, 0)
        self.assertEqual(self.DUT.approve_date, 0)
        self.assertEqual(self.DUT.closed, False)
        self.assertEqual(self.DUT.close_by, 0)
        self.assertEqual(self.DUT.close_date, 0)
        self.assertEqual(self.DUT.life_cycle, 0)
        self.assertEqual(self.DUT.analysis, '')
        self.assertEqual(self.DUT.accepted, False)
        self.assertEqual(self.DUT.relevant, -1)
        self.assertEqual(self.DUT.chargeable, -1)

    @attr(all=True, unit=True)
    def test01_set_attributes(self):
        """
        (TestIncident) set_attributes should return a 0 error code on success
        """

        _values = (0, 1, 2, 3, 'Short Description', 'Detailed Description', 4,
                   5, 'Remarks', 6, 'Test', 'Test Case', 7.0, 8, 9.0, 10.0, 11,
                   12, 0, 719163, True, 0, 719163, False, 0, 719164, False, 0,
                   719163, 3, 'Analysis', True, -1, -1, -1, -1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1, -1, -1, -1, -1)

        (_error_code, _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test02_set_attributes_wrong_type(self):
        """
        (TestIncident) set_attributes should return a 10 error code when passed a wrong data type
        """

        _values = (0, 1, 2, 3, 'Short Description', 'Detailed Description', 4,
                   'Remarks', 6, 'Test', 'Test Case', 7.0, 8, 9.0, 10.0, 11,
                   12, 0, 719163, True, 0, 719163, False, 0, 719164, False, 0,
                   719163, 'Design', 'Analysis', True, -1, -1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1)

        (_error_code, _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test03_set_attributes_missing_index(self):
        """
        (TestIncident) set_attributes should return a 40 error code when too few items are passed
        """

        _values = (0, 1, 2, 3, 'Short Description', 'Detailed Description', 4,
                   5, 'Remarks', 6, 'Test', 'Test Case', 7.0, 8, 9.0, 10.0, 11,
                   12, 0, 719163, True, 0, 719163, False, 0, 719164, False, 0,
                   719163, 3, 'Analysis', -1, -1, -1, -1, -1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1, -1, -1, -1)

        (_error_code, _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test04_get_attributes(self):
        """
        (TestIncident) get_attributes should return a tuple of attribute values
        """

        self.assertEqual(self.DUT.get_attributes(),
                         (None, None, 0, 0, '', '', 0, 0, '', 0, '', '', 0.0,
                          '', 0.0, 0.0, 0, 0, 0, 0, False, 0, 0, False, 0, 0,
                          False, 0, 0, 0, '', False, -1, -1, [
                              -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
                              -1, -1, -1, -1, -1, -1, -1, -1
                          ], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]))

    @attr(all=True, unit=True)
    def test05_sanity(self):
        """
        (TestIncident) get_attributes(set_attributes(values)) == values
        """

        _values = (0, 1, 2, 3, 'Short Description', 'Detailed Description', 4,
                   5, 'Remarks', 6, 'Test', 'Test Case', 7.0, 8, 9.0, 10.0, 11,
                   12, 0, 719163, True, 0, 719163, False, 0, 719164, False, 0,
                   719163, 3, 'Analysis', True, -1, -1, -1, -1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1, -1, -1, -1, -1)
        _output = (0, 1, 2, 3, 'Short Description', 'Detailed Description', 4,
                   5, 'Remarks', 6, 'Test', 'Test Case', 7.0, '8', 9.0, 10.0,
                   11, 12, 0, 719163, True, 0, 719163, False, 0, 719164, False,
                   0, 719163, 3, 'Analysis', True, -1, -1, [
                       -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
                       -1, -1, -1, -1, -1, -1
                   ], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1])

        self.DUT.set_attributes(_values)
        _result = self.DUT.get_attributes()
        self.assertEqual(_result, _output)


class TestIncidentController(unittest.TestCase):
    """
    Class for testing the Incident data controller class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the Incident class.
        """

        self.DUT = Incident()

    @attr(all=True, unit=True)
    def test00_controller_create(self):
        """
        (TestIncident) __init__ should create a Incident data controller
        """

        self.assertTrue(isinstance(self.DUT, Incident))
        self.assertEqual(self.DUT._dao, None)
        self.assertEqual(self.DUT._last_id, None)
        self.assertEqual(self.DUT.dicIncidents, {})
