# This file is part of the mass_editing module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class MassEditingTestCase(ModuleTestCase):
    'Test Mass Editing module'
    module = 'mass_editing'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        MassEditingTestCase))
    return suite
