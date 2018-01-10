# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import mass_editing


def register():
    Pool.register(
        mass_editing.MassEdit,
        mass_editing.MassEditFields,
        mass_editing.MassEditWizardStart,
        module='mass_editing', type_='model')
    Pool.register(
        mass_editing.MassEditingWizard,
        module='mass_editing', type_='wizard')
