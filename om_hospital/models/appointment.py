# -*- coding: utf-8 -*-
import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Appointment Details"
    _rec_name = 'ref'

    name = fields.Char(string='Appointment')
    # patient_id = fields.Many2one('hospital.patient', string='Patient', ondelete='restrict')
    patient_id = fields.Many2one('hospital.patient', string='Patient', ondelete='cascade')
    date_time = fields.Datetime(string='Appointment Date & Time', default=fields.Datetime.now)
    date = fields.Date(string='Appointment Date', default=datetime.date.today())  # default=fields.Date.context_today
    gender = fields.Selection(string='Gender', related='patient_id.gender')
    ref = fields.Char(string='reference')
    prescription = fields.Html(string='Prescription')
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')], string="Priority")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_consultation', 'In Consultation'),
        ('done', 'Done'),
        ('cancel', 'Cancel')], default='draft', string="Status", required=True)
    hide_sale_price = fields.Boolean(string='Hide')
    doctor_id = fields.Many2one('res.users', string='Doctor', tracking=True)
    pharmacy_line_ids = fields.One2many('appointment.pharmacy.line', 'appointment_id', string='Pharmacy Lines')

    def unlink(self):
        # print("=============== Test Unlink ==============")
        if self.state == 'done':
            raise ValidationError(_("You can't delete appointment in done state"))
        super(HospitalAppointment, self).unlink()

    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        if self.patient_id:
            self.ref = self.patient_id.ref

    def action_test(self):
        print("Button clicked")
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'button clickable done ',
                'type': 'rainbow_man',
            }
        }

    def action_consultation(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state = 'in_consultation'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'
        action = self.env.ref('om_hospital.cancel_appointment_action').read()[0]
        return action

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'


class AppointmentPharmacyLine(models.Model):
    _name = "appointment.pharmacy.line"
    _description = 'Appointment Pharmacy lines'

    product_id = fields.Many2one('product.product', string='Product', required=True)
    price_unit = fields.Float(string='Price', related='product_id.list_price')
    qty = fields.Integer(string='Quantity')
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')
