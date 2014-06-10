from lxml import etree

from trytond.transaction import Transaction
from trytond.pool import Pool
from trytond.wizard import Wizard, StateView, StateTransition, Button
from trytond.model import ModelView, ModelSQL, fields
from trytond.pyson import Eval

__all__ = ['MassEdit', 'MassEditFields', 'MassEditWizardStart',
    'MassEditingWizard']


class MassEdit(ModelSQL, ModelView):
    'Mass Edit'
    __name__ = 'mass.editing'
    _rec_name = 'model'
    model = fields.Many2One('ir.model', 'Model', required=True)
    model_fields = fields.Many2Many('mass.editing-ir.model.field',
        'mass_edit', 'field', 'Fields',
        domain=[
            ('model', '=', Eval('model', 0)),
            ],
        depends=['model'])
    keyword = fields.Many2One('ir.action.keyword', 'Keyword', readonly=True)

    @classmethod
    def __setup__(cls):
        super(MassEdit, cls).__setup__()
        cls._sql_constraints += [
            ('model_uniq', 'unique (model)', 'unique_model')
            ]
        cls._error_messages.update({
                'unique_model': 'Mass Edit must be unique per model.',
                'not_modelsql': 'Model "%s" does not store information '
                    'to an SQL table.',
                })
        cls._buttons.update({
                'create_keyword': {
                    'invisible': Eval('keyword'),
                    },
                'remove_keyword': {
                    'invisible': ~Eval('keyword'),
                    },
                })

    @classmethod
    def validate(cls, massedits):
        super(MassEdit, cls).validate(massedits)
        for massedit in massedits:
            Model = Pool().get(massedit.model.model)
            if not issubclass(Model, ModelSQL):
                cls.raise_user_error('not_modelsql',
                    (massedit.model.rec_name,))

    @classmethod
    @ModelView.button
    def create_keyword(cls, massedits):
        pool = Pool()
        Action = pool.get('ir.action.wizard')
        ModelData = pool.get('ir.model.data')
        Keyword = pool.get('ir.action.keyword')

        for massedit in massedits:
            if massedit.keyword:
                continue
            action = Action(ModelData.get_id('mass_editing',
                    'wizard_mass_editing'))
            keyword = Keyword()
            keyword.keyword = 'form_action'
            keyword.model = '%s,-1' % massedit.model.model
            keyword.action = action.action
            keyword.save()
            massedit.keyword = keyword
            massedit.save()

    @classmethod
    @ModelView.button
    def remove_keyword(cls, massedits):
        pool = Pool()
        Keyword = pool.get('ir.action.keyword')
        Keyword.delete([x.keyword for x in massedits if x.keyword])

    @classmethod
    def delete(cls, massedits):
        cls.remove_keyword(massedits)
        super(MassEdit, cls).delete(massedits)


class MassEditFields(ModelSQL):
    'Mass Edit Fields'
    __name__ = 'mass.editing-ir.model.field'

    mass_edit = fields.Many2One('mass.editing', 'Mass', required=True)
    field = fields.Many2One('ir.model.field', 'Field', required=True)


class MassEditWizardStart(ModelView):
    'Mass Edit Wizard Start'
    __name__ = 'mass.editing.wizard.start'

    @classmethod
    def __setup__(cls):
        super(MassEditWizardStart, cls).__setup__()
        cls._error_messages.update({
                'add': 'Add',
                'remove_all': 'Remove All',
                'remove': 'Remove',
                'set': 'Set',
                })

    @classmethod
    def fields_view_get(cls, view_id=None, view_type='form'):
        pool = Pool()
        MassEdit = pool.get('mass.editing')

        res = super(MassEditWizardStart, cls).fields_view_get(view_id,
            view_type)

        context = Transaction().context
        model = context.get('active_model', None)
        if not model:
            return res
        EditingModel = pool.get(model)
        edits = MassEdit.search([('model.model', '=', model)], limit=1)
        if not edits:
            return res
        edit, = edits
        fields = res['fields']
        root = etree.fromstring(res['arch'])
        form = root.find('separator').getparent()

        fields.update(EditingModel.fields_get([f.name for f in
                    edit.model_fields]))
        for field in edit.model_fields:
            if fields[field.name].get('states'):
                fields[field.name]['states'] = {
                    'readonly': {},
                    'invisible': {},
                    }
            if fields[field.name].get('required'):
                fields[field.name]['required'] = False

            if fields[field.name].get('on_change'):
                fields[field.name]['on_change'] = []
            if fields[field.name].get('on_change_with'):
                fields[field.name]['on_change_with'] = []
            #TODO: Check domain with pyson. In case of domain, if the domain
            #clause contains and Eval it must be removed. If it's a static
            #domain it must be the same.

            if field.ttype in ['many2many', 'one2many']:
                selection_vals = [
                    ('', ''),
                    ('set', 'Set'),
                    ('remove_all', 'Remove All'),
                    ]
                _field = getattr(EditingModel, field.name, None)
                if field.ttype == 'many2many'or _field.add_remove:
                    selection_vals.append(('add', 'Add'),)
                    selection_vals.append(('remove', 'Remove'),)
            else:
                selection_vals = [
                    ('', ''),
                    ('set', 'Set'),
                    ('remove', 'Remove')
                ]
            translated_vals = []
            for val in selection_vals:
                translated_vals.append((val[0], cls.raise_user_error(val[0],
                            raise_exception=False),))

            colspan = '1'
            if field.ttype in ['many2many', 'one2many']:
                colspan = '2'

            fields['selection_%s' % field.name] = {
                'type': 'selection',
                'string': fields[field.name]['string'],
                'selection': translated_vals,
                }
            xml_group = etree.SubElement(form, 'group', {
                    'col': '2',
                    'colspan': '4',
                    })
            etree.SubElement(xml_group, 'label', {
                    'id': "label_%s" % field.name,
                    'string': fields[field.name]['string'],
                    'xalign': '0.0',
                    'colspan': '4',
                    })
            etree.SubElement(xml_group, 'field', {
                    'name': "selection_%s" % field.name,
                    'colspan': colspan,
                    })
            etree.SubElement(xml_group, 'field', {
                    'name': field.name,
                    'colspan': colspan,
                    })

        res['arch'] = etree.tostring(root)
        res['fields'] = fields
        return res

    @classmethod
    def default_get(cls, fields, with_rec_name=True, with_on_change=True):
        pool = Pool()
        context = Transaction().context
        model = context.get('active_model', None)
        EditingModel = pool.get(model)
        res = dict.fromkeys([f for f in fields
                    if f[:10] == 'selection_'], '')
        res.update(EditingModel.default_get([f for f in fields
                    if f[:10] != 'selection_'], with_rec_name, with_on_change))
        return res


class CustomDict(dict):

    def __getattr__(self, name):
        return {}

    def __setattr__(self, name, value):
        self[name] = value


class MassEditingWizard(Wizard):
    'Mass Edit Wizard'
    __name__ = 'mass.editing.wizard'
    start = StateView('mass.editing.wizard.start',
                      'mass_editing.view_mass_editing_wizard_start', [
                    Button('Cancel', 'end', 'tryton-cancel'),
                    Button('Apply', 'update', 'tryton-ok', True),
                    ])

    update = StateTransition()

    def __getattribute__(self, name):
        if name == 'start':
            if not hasattr(self, 'start_data'):
                self.start_data = CustomDict()
            name = 'start_data'
        return super(MassEditingWizard, self).__getattribute__(name)

    def transition_update(self):
        pool = Pool()
        context = Transaction().context
        model = context['active_model']
        EditingModel = pool.get(model)
        res = {}
        vals = self.start_data
        for field, value in vals.items():
            if field.startswith('selection_'):
                split_key = field.split('_', 1)[1]
                _field = getattr(EditingModel, split_key, None)
                xxx2many = False
                if (isinstance(_field, fields.One2Many) or
                     isinstance(_field, fields.Many2Many)):
                    xxx2many = True
                if value == 'set':
                    if xxx2many:
                        manyvals = vals.get(split_key, None)
                        to_set = []
                        to_create = []
                        for val in manyvals:
                            if isinstance(val, dict):
                                #check_xxx2many
                                for field_name, field_value in val.iteritems():
                                    if isinstance(field_value, list):
                                        val[field_name] = [tuple(['add',
                                                field_value])]
                                to_create.append(val)
                            else:
                                to_set.append(val)
                        to_write = []
                        if to_set:
                            to_write.append(('set', to_set),)
                        if to_create:
                            to_write.append(('create', to_create),)
                        if to_write:
                            res.update({split_key: to_write})
                    else:
                        res.update({split_key: vals.get(split_key, None)})
                elif value == 'remove':
                    if xxx2many:
                        res.update({split_key: [
                                    ("unlink", vals.get(split_key, []))
                                    ]})
                    else:
                        res.update({split_key: None})
                elif value == 'remove_all':
                    res.update({split_key: [
                                ('unlink_all',)
                                ]})
                elif value == 'add':
                    res.update({split_key: [('add', vals.get(split_key, []))]})
        if res:
            instances = EditingModel.browse(Transaction().context.get(
                    'active_ids'))
            EditingModel.write(instances, res)
        return 'end'
