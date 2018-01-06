#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit.TestInductor.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for the inductor module."""

import sys
from os.path import dirname

import gettext

import unittest
from nose.plugins.attrib import attr

sys.path.insert(
    0,
    dirname(dirname(dirname(dirname(__file__)))) + "/rtk",
)

from analyses.prediction import Inductor

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


class TestInductorModule(unittest.TestCase):
    """Class for testing the Inductor module functions."""

    _attributes = {
        'hazard_rate_percent': 0.0,
        'voltage_ac_operating': 0.0,
        'pressure_upstream': 0.0,
        'frequency_operating': 0.0,
        'type_id': 0,
        'resistance': 0.0,
        'friction': 0.0,
        'length_compressed': 0.0,
        'balance_id': 0,
        'scale_parameter': 0.0,
        'lubrication_id': 0,
        'temperature_dormant': 25.0,
        'Cmu': 0.0,
        'ref_des': 'C1',
        'hazard_rate_method_id': 1,
        'lambdaBP': 0.0,
        'Cm': 0.0,
        'flow_operating': 0.0,
        'temperature_case': 0.0,
        'Cac': 0.0,
        'surface_finish': 0.0,
        'contact_form_id': 0,
        'repairable': 0,
        'parent_id': 4,
        'alt_part_num': '',
        'hazard_rate_logistics': 0.0,
        'lambdaBD': 0.0,
        'manufacturer_id': 0,
        'hazard_rate_software': 0.0,
        'shape_parameter': 0.0,
        'total_power_dissipation': 0.0,
        'current_rated': 0.0,
        'cost_type_id': 0,
        'power_operating': 0.0,
        'pressure_downstream': 0.0,
        'diameter_coil': 0.0,
        'configuration_id': 0,
        'meyer_hardness': 0.0,
        'temperature_junction': 0.0,
        'reliability_goal_measure_id': 0,
        'Cgp': 0.0,
        'lcn': '',
        'Ce': 0.0,
        'piR': 0.0,
        'reliability_miss_variance': 0.0,
        'piCYC': 0.0,
        'piS': 0.0,
        'name': '',
        'construction_id': 0,
        'level': 0,
        'insert_id': 0,
        'n_ten': 0,
        'manufacturing_id': 0,
        'Cgt': 0.0,
        'cost_failure': 0.0,
        'family_id': 0,
        'load_id': 0,
        'B1': 0.0,
        'B2': 0.0,
        'piNR': 0.0,
        'revision_id': 1,
        'hazard_rate_dormant': 0.0,
        'comp_ref_des': 'S1:SS1:A1:C1',
        'piTAPS': 0.0,
        'operating_life': 0.0,
        'hazard_rate_specified': 0.0,
        'attachments': '',
        'weight': 0.0,
        'subcategory_id': 1,
        'Csf': 0.0,
        'Csc': 0.0,
        'deflection': 0.0,
        'filter_size': 0.0,
        'reliability_goal': 0.0,
        'cost': 0.0,
        'material_id': 0,
        'voltage_ratio': 0.0,
        'availability_logistics': 1.0,
        'Cst': 0.0,
        'Csw': 0.0,
        'Csv': 0.0,
        'diameter_inner': 0.0,
        'environment_active_id': 0,
        'pressure_rated': 0.0,
        'quality_id': 0,
        'piCV': 0.0,
        'hardware_id': 6,
        'altitude_operating': 0.0,
        'piCR': 0.0,
        'thickness': 0.0,
        'specification_id': 0,
        'diameter_outer': 0.0,
        'matching_id': 0,
        'figure_number': '',
        'hr_mission_variance': 0.0,
        'piCD': 0.0,
        'piCF': 0.0,
        'particle_size': 0.0,
        'reliability_mission': 1.0,
        'environment_dormant_id': 0,
        'n_elements': 0,
        'hazard_rate_active': 5.0,
        'casing_id': 0,
        'mtbf_log_variance': 0.0,
        'temperature_active': 35.0,
        'Ccw': 0.0,
        'Ccv': 0.0,
        'Cpd': 0.0,
        'Ccp': 0.0,
        'Cpf': 0.0,
        'Cs': 0.0,
        'reason': u'',
        'Ccs': 0.0,
        'offset': 0.0,
        'load_operating': 0.0,
        'Ccf': 0.0,
        'impact_id': 0,
        'Cpv': 0.0,
        'Cbl': 0.0,
        'year_of_manufacture': 2017,
        'n_wave_soldered': 0,
        'category_id': 4,
        'pressure_delta': 0.0,
        'length': 0.0,
        'cage_code': '',
        'Cf': 0.0,
        'load_design': 0.0,
        'mtbf_logistics': 0.0,
        'tagged_part': 0,
        'nsn': '',
        'temperature_hot_spot': 0.0,
        'feature_size': 0.0,
        'Clc': 0.0,
        'hr_logistics_variance': 0.0,
        'package_id': 0,
        'technology_id': 0,
        'n_cycles': 0,
        'mtbf_spec_variance': 0.0,
        'n_circuit_planes': 1,
        'contact_gauge': 0,
        'current_operating': 0.0,
        'location_parameter': 0.0,
        'water_per_cent': 0.0,
        'cost_hour': 0.0,
        'contact_rating_id': 0,
        'misalignment_angle': 0.0,
        'area': 0.0,
        'add_adj_factor': 5.0,
        'lambdaCYC': 0.0,
        'rpm_design': 0.0,
        'n_active_pins': 0,
        'capacitance': 0.0,
        'mission_time': 100.0,
        'reliability_logistics': 1.0,
        'lambda_b': 0.0,
        'C2': 0.0,
        'C1': 0.0,
        'failure_distribution_id': 0,
        'hazard_rate_model': u'',
        'quantity': 1,
        'pressure_contact': 0.0,
        'part': 1,
        'duty_cycle': 100.0,
        'Crd': 0.0,
        'voltage_rated': 0.0,
        'n_hand_soldered': 0,
        'hazard_rate_type_id': 1,
        'current_ratio': 0.0,
        'rpm_operating': 0.0,
        'avail_mis_variance': 0.0,
        'Ck': 0.0,
        'mult_adj_factor': 1.0,
        'Ci': 0.0,
        'Ch': 0.0,
        'Cn': 0.0,
        'length_relaxed': 0.0,
        'Cl': 0.0,
        'Cc': 0.0,
        'Cb': 0.0,
        'theta_jc': 0.0,
        'hr_dormant_variance': 0.0,
        'Cg': 0.0,
        'availability_mission': 1.0,
        'voltage_dc_operating': 0.0,
        'Cd': 0.0,
        'power_ratio': 0.0,
        'Cy': 0.0,
        'Cbv': 0.0,
        'Cbt': 0.0,
        'reliability_log_variance': 0.0,
        'overstress': 0,
        'Cr': 0.0,
        'Cq': 0.0,
        'Cp': 0.0,
        'Cw': 0.0,
        'Cv': 0.0,
        'Ct': 0.0,
        'Cnw': 0.0,
        'hr_specified_variance': 0.0,
        'Cnp': 0.0,
        'total_part_count': 0,
        'Csz': 0.0,
        'Calt': 0.0,
        'contact_pressure': 0.0,
        'insulation_id': 0,
        'temperature_rated_max': 0.0,
        'lambdaEOS': 0.0,
        'flow_design': 0.0,
        'years_in_production': 1,
        'hazard_rate_mission': 0.0,
        'avail_log_variance': 0.0,
        'piK': 0.0,
        'piL': 0.0,
        'piM': 0.0,
        'piN': 0.0,
        'Cga': 0.0,
        'piA': 0.0,
        'piC': 0.0,
        'piE': 0.0,
        'piF': 0.0,
        'temperature_rated_min': 0.0,
        'A1': 0.0,
        'A2': 0.0,
        'page_number': '',
        'piP': 0.0,
        'piQ': 10.0,
        'Cgs': 0.0,
        'power_rated': 0.0,
        'piT': 0.0,
        'piU': 0.0,
        'piV': 0.0,
        'Cgv': 0.0,
        'description': '',
        'piPT': 0.0,
        'viscosity_dynamic': 0.0,
        'viscosity_design': 0.0,
        'torque_id': 0,
        'voltage_esd': 0.0,
        'leakage_allowable': 0.0,
        'hr_active_variance': 0.0,
        'remarks': '',
        'width_minimum': 0.0,
        'mtbf_mission': 0.0,
        'application_id': 0,
        'piMFG': 0.0,
        'Cgl': 0.0,
        'piI': 0.0,
        'spring_index': 0.0,
        'mtbf_miss_variance': 0.0,
        'mtbf_specified': 0.0,
        'Cdc': 0.0,
        'Cdl': 0.0,
        'survival_analysis_id': 0,
        'Cdt': 0.0,
        'part_number': '',
        'Cdw': 0.0,
        'Cdp': 0.0,
        'temperature_rise': 0.0,
        'Cds': 0.0,
        'clearance': 0.0,
        'specification_number': '',
        'Cdy': 0.0,
        'diameter_wire': 0.0,
        'service_id': 0
    }

    def setUp(self):
        """Set up the test fixture for the Inductor module."""
        self._dic_lambda_b = {
        1: {
            1: [
                0.0035, 0.023, 0.049, 0.019, 0.065, 0.027, 0.037, 0.041, 0.052,
                0.11, 0.0018, 0.053, 0.16, 2.3
            ],
            2: [
                0.0071, 0.046, 0.097, 0.038, 0.13, 0.055, 0.073, 0.081, 0.10,
                0.22, 0.035, 0.11, 0.31, 4.7
            ],
            3: [
                0.023, 0.16, 0.35, 0.13, 0.45, 0.21, 0.27, 0.35, 0.45, 0.82,
                0.011, 0.37, 1.2, 16.0
            ],
            4: [
                0.028, 0.18, 0.39, 0.15, 0.52, 0.22, 0.29, 0.33, 0.42, 0.88,
                0.015, 0.42, 1.2, 19.0
            ]
        },
        2: {
            1: [
                0.0017, 0.0073, 0.023, 0.0091, 0.031, 0.011, 0.015, 0.016,
                0.022, 0.052, 0.00083, 0.25, 0.073, 1.1
            ],
            2: [
                0.0033, 0.015, 0.046, 0.018, 0.061, 0.022, 0.03, 0.033, 0.044,
                0.10, 0.0017, 0.05, 0.15, 2.2
            ]
        }
    }
        self._lst_piQ = [0.25, 1.0, 1.0]

    @attr(all=True, unit=True)
    def test00a_calculate_mil_hdbk_217f_part_count(self):
        """(TestInductorModule) calculate_mil_hdbk_217f_part_count() should return a dictionary of updated values on success."""
        self._attributes['subcategory_id'] = 2
        self._attributes['type_id'] = 1
        self._attributes['environment_active_id'] = 1
        self._attributes['quality_id'] = 2
        self._attributes['add_adj_factor'] = 0.0
        self._attributes['mult_adj_factor'] = 1.0
        self._attributes['duty_cycle'] = 100.0
        self._attributes['quantity'] = 1

        _attributes, _msg = Inductor.calculate_217f_part_count(
            **self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(_msg, '')
        self.assertEqual(_attributes['lambda_b'], 0.0017)
        self.assertEqual(_attributes['piQ'], 1.0)
        self.assertAlmostEqual(_attributes['hazard_rate_active'], 0.0017)

    @attr(all=True, unit=True)
    def test00b_calculate_mil_hdbk_217f_part_count_all(self):
        """(TestInductorModule) calculate_mil_hdbk_217f_part_count() should return a dictionary of updated values on success for each subcategory, active environment, and quality level combination."""
        self._attributes['type_id'] = 1
        self._attributes['add_adj_factor'] = 0.0
        self._attributes['mult_adj_factor'] = 1.0
        self._attributes['duty_cycle'] = 100.0
        self._attributes['quantity'] = 1

        for subcategory_id in xrange(1, 3):
            self._attributes['subcategory_id'] = subcategory_id
            for environment_active_id in xrange(1, 15):
                self._attributes[
                    'environment_active_id'] = environment_active_id
                for quality_id in xrange(1, 4):
                    self._attributes['quality_id'] = quality_id
                    _test_msg = 'test00b_calculate_mil_hdbk_217f_part_count_{}_{}_{} ' \
                                'failed'.format(subcategory_id,
                                                environment_active_id,
                                                quality_id)

                    _attributes, _msg = Inductor.calculate_217f_part_count(
                        **self._attributes)

                    self.assertTrue(isinstance(_attributes, dict), _test_msg)
                    self.assertEqual(_msg, '', _test_msg)

                    _lambda_b = self._dic_lambda_b[subcategory_id][1][
                        environment_active_id - 1]
                    _piQ = self._lst_piQ[quality_id - 1]
                    self.assertEqual(_attributes['lambda_b'], _lambda_b,
                                     _test_msg)
                    self.assertEqual(_attributes['piQ'], _piQ, _test_msg)
                    self.assertEqual(_attributes['hazard_rate_active'],
                                     _lambda_b * _piQ, _test_msg)

    @attr(all=True, unit=True)
    def test00c_calculate_mil_hdbk_217f_part_count_missing_subcategory(self):
        """(TestInductorModule) calculate_mil_hdbk_217f_part_count() should return an error message when the subcategory ID is missing."""
        self._attributes['subcategory_id'] = 0
        self._attributes['specification_id'] = 1
        self._attributes['environment_active_id'] = 1
        self._attributes['quality_id'] = 1
        self._attributes['add_adj_factor'] = 0.0
        self._attributes['mult_adj_factor'] = 1.0
        self._attributes['duty_cycle'] = 100.0
        self._attributes['quantity'] = 1

        _attributes, _msg = Inductor.calculate_217f_part_count(
            **self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(
            _msg,
            'RTK WARNING: Base hazard rate is 0.0 when calculating ' \
            'inductor, hardware ID: 6, subcategory ID: 0, type ID: 1, and ' \
            'active environment ID: 1.'
        )
        self.assertEqual(_attributes['lambda_b'], 0.0)
        self.assertEqual(_attributes['piQ'], 0.25)
        self.assertEqual(_attributes['hazard_rate_active'], 0.0)

    @attr(all=True, unit=True)
    def test00d_calculate_mil_hdbk_217f_part_count_missing_type(self):
        """(TestInductorModule) calculate_mil_hdbk_217f_part_count() should return an error message when the type ID is missing and needed."""
        self._attributes['subcategory_id'] = 2
        self._attributes['type_id'] = 0
        self._attributes['environment_active_id'] = 1
        self._attributes['quality_id'] = 1
        self._attributes['add_adj_factor'] = 0.0
        self._attributes['mult_adj_factor'] = 1.0
        self._attributes['duty_cycle'] = 100.0
        self._attributes['quantity'] = 1

        _attributes, _msg = Inductor.calculate_217f_part_count(
            **self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(
            _msg,
            'RTK WARNING: Base hazard rate is 0.0 when calculating ' \
            'inductor, hardware ID: 6, subcategory ID: 2, type ID: 0, and ' \
            'active environment ID: 1.'
        )
        self.assertEqual(_attributes['lambda_b'], 0.0)
        self.assertEqual(_attributes['piQ'], 0.25)
        self.assertEqual(_attributes['hazard_rate_active'], 0.0)

    @attr(all=True, unit=True)
    def test00e_calculate_mil_hdbk_217f_part_count_missing_environment(self):
        """(TestInductorModule) calculate_mil_hdbk_217f_part_count() should return an error message when the active environment ID is missing."""
        self._attributes['subcategory_id'] = 1
        self._attributes['type_id'] = 1
        self._attributes['environment_active_id'] = 100
        self._attributes['quality_id'] = 1
        self._attributes['add_adj_factor'] = 0.0
        self._attributes['mult_adj_factor'] = 1.0
        self._attributes['duty_cycle'] = 100.0
        self._attributes['quantity'] = 1

        _attributes, _msg = Inductor.calculate_217f_part_count(
            **self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(
            _msg,
            'RTK WARNING: Base hazard rate is 0.0 when calculating ' \
            'inductor, hardware ID: 6, subcategory ID: 1, type ID: 1, and ' \
            'active environment ID: 100.'
        )
        self.assertEqual(_attributes['lambda_b'], 0.0)
        self.assertEqual(_attributes['piQ'], 0.25)
        self.assertEqual(_attributes['hazard_rate_active'], 0.0)

    @attr(all=True, unit=True)
    def test01a_calculate_mil_hdbk_217f_part_stress(self):
        """(TestInductorModule) calculate_mil_hdbk_217f_part_stress() should return a dictionary of updated values on success."""
        self._attributes['subcategory_id'] = 2
        self._attributes['insulation_id'] = 3
        self._attributes['construction_id'] = 2
        self._attributes['quality_id'] = 2
        self._attributes['environment_active_id'] = 4
        self._attributes['temperature_active'] = 32.0
        self._attributes['power_operating'] = 4.2
        self._attributes['weight'] = 0.75
        self._attributes['add_adj_factor'] = 0.0
        self._attributes['mult_adj_factor'] = 1.0
        self._attributes['duty_cycle'] = 100.0
        self._attributes['quantity'] = 1

        _attributes, _msg = Inductor.calculate_217f_part_stress(
            **self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(_msg, '')
        self.assertAlmostEqual(_attributes['lambda_b'], 0.0003462094)
        self.assertEqual(_attributes['piQ'], 0.1)
        self.assertEqual(_attributes['piE'], 5.0)
        self.assertEqual(_attributes['piC'], 2.0)
        self.assertAlmostEqual(_attributes['hazard_rate_active'], 0.0003462094)

    @attr(all=True, unit=True)
    def test02a_calculate_dormant_hazard_rate(self):
        """(TestInductorModule) calculate_dormant_hazard_rate() should return a dictionary of updated values on success."""
        self._attributes['environment_active_id'] = 4
        self._attributes['environment_dormant_id'] = 3
        self._attributes['hazard_rate_active'] = 1.005887691

        _attributes, _msg = Inductor.calculate_dormant_hazard_rate(
            **self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(_msg, '')
        self.assertAlmostEqual(_attributes['hazard_rate_dormant'], 0.3017663)

    @attr(all=True, unit=True)
    def test02b_calculate_dormant_hazard_rate_unknown_env_id(self):
        """(TestInductorModule) calculate_dormant_hazard_rate() should return an error message when an unknown environment ID is passed."""
        self._attributes['environment_active_id'] = 24
        self._attributes['environment_dormant_id'] = 3
        self._attributes['hazard_rate_active'] = 1.005887691

        _attributes, _msg = Inductor.calculate_dormant_hazard_rate(
            **self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(
            _msg, 'RTK ERROR: Unknown active and/or dormant environment ID. '
            'Active ID: 24, Dormant ID: 3')
        self.assertEqual(_attributes['hazard_rate_dormant'], 0.0)

    @attr(all=True, unit=True)
    def test03a_overstressed_mild_env(self):
        """(TestInductorModule) overstressed() should return overstress=False and reason='' on success without an overstressed condition in non-harsh environment."""
        self._attributes['environment_active_id'] = 1
        self._attributes['current_operating'] = 0.18
        self._attributes['current_rated'] = 0.5
        self._attributes['voltage_ac_operating'] = 0.02
        self._attributes['voltage_dc_operating'] = 5.0
        self._attributes['voltage_rated'] = 10.0

        _attributes = Inductor.overstressed(**self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertFalse(_attributes['overstress'])
        self.assertEqual(_attributes['reason'], '')

    @attr(all=True, unit=True)
    def test03b_overstressed_mild_env_current_margin(self):
        """(TestInductorModule) overstressed() should return overstress=True on success with operating current too close to rated in a non-harsh environment."""
        self._attributes['environment_active_id'] = 1
        self._attributes['current_operating'] = 0.48
        self._attributes['current_rated'] = 0.5
        self._attributes['voltage_ac_operating'] = 0.02
        self._attributes['voltage_dc_operating'] = 5.0
        self._attributes['voltage_rated'] = 10.0

        _attributes = Inductor.overstressed(**self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertTrue(_attributes['overstress'])
        self.assertEqual(_attributes['reason'],
                         '1. Operating current > 90% rated current.\n')

    @attr(all=True, unit=True)
    def test03d_overstressed_harsh_env(self):
        """(TestInductorModule) overstressed() should return overstress=False and reason='' on success without an overstressed condition in a harsh environment."""
        self._attributes['environment_active_id'] = 3
        self._attributes['current_operating'] = 0.18
        self._attributes['current_rated'] = 0.5
        self._attributes['voltage_ac_operating'] = 0.02
        self._attributes['voltage_dc_operating'] = 4.0
        self._attributes['voltage_rated'] = 10.0
        self._attributes['temperature_rated_max'] = 85.0
        self._attributes['temperature_hot_spot'] = 65.0

        _attributes = Inductor.overstressed(**self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertFalse(_attributes['overstress'])
        self.assertEqual(_attributes['reason'], '')

    @attr(all=True, unit=True)
    def test03f_overstressed_harsh_env_current_margin(self):
        """(TestInductorModule) overstressed() should return overstress=True on success with operating current too close to rated in a harsh environment."""
        self._attributes['environment_active_id'] = 3
        self._attributes['current_operating'] = 0.38
        self._attributes['current_rated'] = 0.5
        self._attributes['voltage_ac_operating'] = 0.02
        self._attributes['voltage_dc_operating'] = 4.0
        self._attributes['voltage_rated'] = 10.0
        self._attributes['temperature_rated_max'] = 85.0
        self._attributes['temperature_hot_spot'] = 65.0

        _attributes = Inductor.overstressed(**self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertTrue(_attributes['overstress'])
        self.assertEqual(_attributes['reason'],
                         '1. Operating current > 60% rated current.\n')

    @attr(all=True, unit=True)
    def test03f_overstressed_harsh_env_voltage_margin(self):
        """(TestInductorModule) overstressed() should return overstress=True on success with operating voltage too close to rated in a harsh environment."""
        self._attributes['environment_active_id'] = 3
        self._attributes['current_operating'] = 0.18
        self._attributes['current_rated'] = 0.5
        self._attributes['voltage_ac_operating'] = 0.02
        self._attributes['voltage_dc_operating'] = 5.0
        self._attributes['voltage_rated'] = 10.0
        self._attributes['temperature_rated_max'] = 85.0
        self._attributes['temperature_hot_spot'] = 65.0

        _attributes = Inductor.overstressed(**self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertTrue(_attributes['overstress'])
        self.assertEqual(_attributes['reason'],
                         '1. Operating voltage > 50% rated voltage.\n')

    @attr(all=True, unit=True)
    def test03g_overstressed_harsh_env_temperature_margin(self):
        """(TestInductorModule) overstressed() should return overstress=True on success with hot spot temperature too close to rated in a harsh environment."""
        self._attributes['environment_active_id'] = 3
        self._attributes['current_operating'] = 0.18
        self._attributes['current_rated'] = 0.5
        self._attributes['voltage_ac_operating'] = 0.02
        self._attributes['voltage_dc_operating'] = 4.0
        self._attributes['voltage_rated'] = 10.0
        self._attributes['temperature_rated_max'] = 85.0
        self._attributes['temperature_hot_spot'] = 73.8

        _attributes = Inductor.overstressed(**self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertTrue(_attributes['overstress'])
        self.assertEqual(_attributes['reason'],
                         '1. Operating temperature within 15.0C of maximum ' \
                         'rated temperature.\n')

    @attr(all=True, unit=True)
    def test04a_calculate(self):
        """(TestInductorModule) calculate() should return should return a dictionary of updated values on success."""
        self._attributes['subcategory_id'] = 2
        self._attributes['type_id'] = 1
        self._attributes['environment_active_id'] = 1
        self._attributes['quality_id'] = 2
        self._attributes['add_adj_factor'] = 0.0
        self._attributes['mult_adj_factor'] = 1.0
        self._attributes['duty_cycle'] = 100.0
        self._attributes['quantity'] = 1

        self._attributes['hazard_rate_method_id'] = 1
        _attributes, _msg = Inductor.calculate(**self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(_msg, '')
        self.assertEqual(_attributes['lambda_b'], 0.0017)
        self.assertEqual(_attributes['piQ'], 1.0)
        self.assertAlmostEqual(_attributes['hazard_rate_active'], 0.0017)

        self._attributes['hazard_rate_method_id'] = 2
        self._attributes['subcategory_id'] = 2
        self._attributes['insulation_id'] = 3
        self._attributes['construction_id'] = 2
        self._attributes['quality_id'] = 2
        self._attributes['environment_active_id'] = 4
        self._attributes['temperature_active'] = 32.0
        self._attributes['power_operating'] = 4.2
        self._attributes['weight'] = 0.75
        self._attributes['add_adj_factor'] = 0.0
        self._attributes['mult_adj_factor'] = 1.0
        self._attributes['duty_cycle'] = 100.0
        self._attributes['quantity'] = 1
        _attributes, _msg = Inductor.calculate(**self._attributes)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(_msg, '')
        self.assertAlmostEqual(_attributes['lambda_b'], 0.0009980554)
        self.assertEqual(_attributes['piQ'], 0.1)
        self.assertEqual(_attributes['piE'], 5.0)
        self.assertEqual(_attributes['piC'], 2.0)
        self.assertAlmostEqual(_attributes['hazard_rate_active'], 0.0009980554)
