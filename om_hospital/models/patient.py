# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Patient Details"

    name = fields.Char(string='Name', tracking=True)
    ref = fields.Char(string='reference')
    birthday = fields.Date(string='Birth Day')
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], string='Gender')
    active = fields.Boolean(string='Active', default=True)
    image = fields.Image(string='Image')
    parent = fields.Char(string='Parent')
    marital = fields.Selection([
        ('s', 'Single'),
        ('m', 'Married'),
    ], string='Marital Status', tracking=True)
    partner_name = fields.Char(string='Partner Name')
    tag_ids = fields.Many2many('patient.tag', string='Tags')
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')
    appointment_count = fields.Integer(string='Appointment Count', compute='_compute_appointment_count', store=True)
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string='Appointments')

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])

    @api.model
    def create(self, vals):
        # print("Zakariya Mahmoud ========================================")
        # print(" Vals_list  ======================================== ", vals_list)
        vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _('New')
        return super(HospitalPatient, self).create(vals)

    def write(self, vals):
        # print("================================= Write Method Triggered ==============================")
        if not self.ref and not vals.get('ref'):
            vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _('New')
        return super(HospitalPatient, self).write(vals)

    @api.constrains('birthday')
    def _check_birthday(self):
        for rec in self:
            if rec.birthday and rec.birthday > fields.Date.today():
                raise ValidationError(_("You entered wrong Date"))

    @api.depends('birthday')
    def _compute_age(self):
        print("self ", self)
        for rec in self:
            today = date.today()
            if rec.birthday:
                rec.age = today.year - rec.birthday.year
            else:
                rec.age = 0

    # def name_get(self):
    #     patient_list = []
    #     for rec in self:
    #         name = rec.ref + ' ' + rec.name
    #         patient_list.append((rec.id, name))
    #     return patient_list

    def name_get(self):
        return [(rec.id, "[%s:%s]" % (rec.ref, rec.name)) for rec in self]
