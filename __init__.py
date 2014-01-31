#The COPYRIGHT file at the top level of this repository contains the full
#copyright notices and license terms.
from trytond.pool import Pool
from .mass_editing import *


def register():
    Pool.register(
        MassEdit,
        MassEditFields,
        MassEditWizardStart,
        module='mass_editing', type_='model')
    Pool.register(
        MassEditingWizard,
        module='mass_editing', type_='wizard')
