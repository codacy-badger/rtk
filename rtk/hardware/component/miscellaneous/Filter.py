#!/usr/bin/env python
"""
######################################################
Hardware.Component.Miscellaneous Package Filter Module
######################################################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.miscellaneous.Filter.py is part of the RTK
#       Project
#
# All rights reserved.

import gettext
import locale

try:
    import calculations as _calc
    import configuration as _conf
    from hardware.component.Component import Model as Component
except ImportError:                         # pragma: no cover
    import rtk.calculations as _calc
    import rtk.configuration as _conf
    from rtk.hardware.component.Component import Model as Component

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


def _error_handler(message):
    """
    Converts string errors to integer error codes.

    :param str message: the message to convert to an error code.
    :return: _err_code
    :rtype: int
    """

    if 'argument must be a string or a number' in message[0]:   # Type error
        _error_code = 10
    elif 'invalid literal for int() with base 10' in message[0]:   # Type error
        _error_code = 10
    elif 'index out of range' in message[0]:   # Index error
        _error_code = 40
    else:                                   # Unhandled error
        print message
        _error_code = 1000                  # pragma: no cover

    return _error_code


class Filter(Component):
    """
    The Filter data model contains the attributes and methods of a Filter
    component.  The attributes of an Filter are:

    :cvar category: default value: 10
    :cvar subcategory: default value: 81

    :ivar quality: default value: 0
    :ivar specification: default value: 0
    :ivar style: default value: 0
    :ivar q_override: default value: 0.0
    :ivar base_hr: default value: 0.0
    :ivar piQ: default value: 0.0
    :ivar piE: default value: 0.0
    :ivar reason: default value: ""

    Hazard Rate Models:
        # MIL-HDBK-217F, section 21.1.
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_piE = [1.0, 2.0, 6.0, 4.0, 9.0, 7.0, 9.0, 11.0, 13.0, 11.0, 0.8, 7.0,
                15.0, 120.0]
    _lst_piQ = [1.0, 2.9]
    _lst_lambdab = [[0.022, 0.12], [0.12, 0.27]]
    _lst_lambdab_count = [[0.022, 0.044, 0.13, 0.088, 0.20, 0.15, 0.20, 0.24,
                           0.29, 0.24, 0.018, 0.15, 0.33, 2.6],
                          [0.12, 0.24, 0.72, 0.48, 1.1, 0.84, 1.1, 1.3, 1.6,
                           1.3, 0.096, 0.84, 1.8, 1.4],
                          [0.27, 0.54, 1.6, 1.1, 2.4, 1.9, 2.4, 3.0, 3.5, 3.0,
                           0.22, 1.9, 4.1, 32.0]]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    category = 10
    subcategory = 81

    def __init__(self):
        """
        Initialize an Filter data model instance.
        """

        super(Filter, self).__init__()

        # Initialize public scalar attributes.
        self.quality = 0                    # Quality index.
        self.specification = 0              # Governing specification.
        self.style = 0                      # Filter style.
        self.q_override = 0.0               # User-defined quality factor.
        self.base_hr = 0.0                  # Base hazard rate.
        self.piQ = 0.0                      # Quality pi factor.
        self.piE = 0.0                      # Environment pi factor.
        self.reason = ""                    # Overstress reason.

    def set_attributes(self, values):
        """
        Sets the Filter data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Component.set_attributes(self, values[:96])

        try:
            self.q_override = float(values[96])
            self.base_hr = float(values[97])
            self.piQ = float(values[98])
            self.piE = float(values[99])
            self.quality = int(values[116])
            self.specification = int(values[117])
            self.style = int(values[118])
            # TODO: Add field to rtk_stress to hold overstress reason.
            self.reason = ''
        except IndexError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Retrieves the current values of the Filter data model
        attributes.

        :return: (quality, specification, style, q_override, base_hr, piQ, piE,
                  reason)
        :rtype: tuple
        """

        _values = Component.get_attributes(self)

        _values = _values + (self.quality, self.specification, self.style,
                             self.q_override, self.base_hr, self.piQ, self.piE,
                             self.reason)

        return _values

    def calculate(self):
        """
        Calculates the hazard rate for the Filter data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.hazard_rate_model = {}

        # Set the model's quality correction factor.
        self.piQ = self._lst_piQ[self.quality - 1]
        self.hazard_rate_model['piQ'] = self.piQ

        if self.hazard_rate_type == 1:
            self.hazard_rate_model['equation'] = 'lambdab'

            # Base hazard rate.
            self.base_hr = self._lst_lambdab_count[self.style - 1][self.environment_active - 1]
            self.hazard_rate_model['lambdab'] = self.base_hr

        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piQ * piE'

            # Set the model's base hazard rate.
            self.base_hr = self._lst_lambdab[self.specification - 1][self.style - 1]
            self.hazard_rate_model['lambdab'] = self.base_hr

            # Set the model's environmental correction factor.
            self.piE = self._lst_piE[self.environment_active - 1]
            self.hazard_rate_model['piE'] = self.piE

        # Calculate component active hazard rate.
        self.hazard_rate_active = _calc.calculate_part(self.hazard_rate_model)
        self.hazard_rate_active = (self.hazard_rate_active + \
                                   self.add_adj_factor) * \
                                  (self.duty_cycle / 100.0) * \
                                  self.mult_adj_factor * self.quantity
        self.hazard_rate_active = self.hazard_rate_active / _conf.FRMULT

        # Calculate operating point ratios.
        self.current_ratio = self.operating_current / self.rated_current
        self.voltage_ratio = self.operating_voltage / self.rated_voltage
        self.power_ratio = self.operating_power / self.rated_power

        return False
