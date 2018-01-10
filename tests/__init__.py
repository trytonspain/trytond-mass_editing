# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
try:
    from trytond.modules.mass_editing.tests.test_mass_editing import suite
except ImportError:
    from .test_mass_editing import suite

__all__ = ['suite']
