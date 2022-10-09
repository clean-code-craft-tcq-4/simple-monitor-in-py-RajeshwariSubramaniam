import io
import sys
from unittest import TestCase

from bms.bms import BatteryManagementSystem


class TestBMS(TestCase):

    def setUp(self):
        self.capturedOutput = io.StringIO()
        sys.stdout = self.capturedOutput

    def test_battery_is_ok(self):
        bms = BatteryManagementSystem('li-ion', 43, 25, 0.7)
        bms.is_battery_ok()
        console_output = self.capturedOutput.getvalue()
        self.assertIn('Battery is OK!', console_output)

    def test_battery_is_not_ok(self):
        bms = BatteryManagementSystem('li-ion', -10, 25, 0.9)
        bms.is_battery_ok()
        console_output = self.capturedOutput.getvalue()
        self.assertIn('Battery is NOT OK!', console_output)
        self.assertIn('temperature is out of range!', console_output)
        self.assertIn('charge_rate is out of range!', console_output)
        self.assertNotIn('state_of_charge is out of range!', console_output)
