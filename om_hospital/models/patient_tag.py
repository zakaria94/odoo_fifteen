# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class PatientTag(models.Model):
    _name = "patient.tag"
    _description = 'Patient Tag'

    name = fields.Char(string='name', required=True)
    active = fields.Boolean(string='Active', default=True, copy=False)
    color = fields.Integer(string='Color')
    color_two = fields.Char(string='Color Two')
    sequence = fields.Integer(string='Sequence')

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('name'):
            default['name'] = _("%s (copy)") % self.name
        default['sequence'] = 10
        return super(PatientTag, self).copy(default)

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', "The Name Must be unique"),
        ('check_sequence', 'CHECK(sequence > 0)', "The Sequence not allowed to be zero")
    ]
