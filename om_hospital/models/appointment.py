# -*- coding: utf-8 -*-
import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Appointment Details"
    _rec_name = 'ref'
    _order = 'id desc'

    name = fields.Char(string='Appointment')
    # patient_id = fields.Many2one('hospital.patient', string='Patient', ondelete='restrict')
    patient_id = fields.Many2one('hospital.patient', string='Patient', ondelete='cascade')
    date_time = fields.Datetime(string='Appointment Date & Time', default=fields.Datetime.now)
    date = fields.Date(string='Appointment Date', default=datetime.date.today())  # default=fields.Date.context_today
    gender = fields.Selection(string='Gender', related='patient_id.gender')
    ref = fields.Char(string='reference')
    # email = fields.Char(string="Email", related='patient_id.email', readonly=False)
    # phone = fields.Char(string="Phone", related='patient_id.phone', readonly=False)
    # website = fields.Char(string="Website", related='patient_id.website', readonly=False)
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
    # tracking=Integer for arrange fields Tracking
    hide_sale_price = fields.Boolean(string='Hide')
    doctor_id = fields.Many2one('res.users', string='Doctor', tracking=True)
    operation_id = fields.Many2one('hospital.operation', string='Operation')
    progress = fields.Integer(string='Progress', compute='compute_progress')
    pharmacy_line_ids = fields.One2many('appointment.pharmacy.line', 'appointment_id', string='Pharmacy Lines')
    duration = fields.Float(string='Duration')
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company)

    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')

    # mapped, sorted
    def test_recordset(self):
        for rec in self:
            print("Odoo ORM : Record Set Operations")
            partners = self.env['res.partner'].search([])
            patients = self.env['hospital.patient'].search([])
            print("Partners ==================", partners)
            print("Mapped Partners name ==================", partners.mapped('name'))
            print("Sorted Partners ==================", partners.sorted(lambda p: p.create_date, reverse=True))
            print("Filtered Partners ==================", patients.filtered(lambda p: p.age >= 28))

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
        return {
            'type': 'ir.actions.act_url',
            'url': 'https://www.yallakora.com/',
            'target': 'new',
        }

    def action_consultation(self):
        for rec in self:
            # odoo search method
            patients = self.env['hospital.patient'].search([])
            # print("Patients .................. ", patients)
            # odoo search and
            male_patients = self.env['hospital.patient'].search([
                ('gender', '=', 'male'), ('age', '>=', 28)
            ])
            # print("Male Patients .................. ", male_patients)
            # odoo search or
            male_patients = self.env['hospital.patient'].search(['|',
                                                                 ('gender', '=', 'male'), ('age', '>=', 28)
                                                                 ])
            # print("Male Patients OR .................. ", male_patients)

            # odoo search count
            patients_count = self.env['hospital.patient'].search_count([])
            # print("Patients Count .................. ", patients_count)

            male_patients = self.env['hospital.patient'].search_count(['|',
                                                                       ('gender', '=', 'male'), ('age', '>=', 28)
                                                                       ])
            # print("Male Patients OR Count .................. ", male_patients)

            # odoo Ref method
            om_hospital = self.env.ref('om_hospital.patient_tag_vip')
            # print('om_hospital ...........', om_hospital.id)

            # odoo browse method     Take a List
            browse_res = self.env['hospital.patient'].browse([21, 2])
            # print('om_hospital browse ...........', browse_res)

            # odoo browse method and exists
            browse_res = self.env['hospital.patient'].browse(200)
            print('om_hospital browse ...........', browse_res)
            if browse_res.exists():
                print("Existing")
            else:
                print("No")

            # if rec.state == 'draft':
            #     rec.state = 'in_consultation'

    def action_done(self):
        for rec in self:
            rec.state = 'done'
        return {'effect': {
            'fadeout': 'slow',
            'message': 'done ',
            'type': 'rainbow_man',
        }}

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'
        action = self.env.ref('om_hospital.cancel_appointment_action').read()[0]
        return action

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    @api.depends('state')
    def compute_progress(self):
        for rec in self:
            if rec.state == 'draft':
                progress = 25
            elif rec.state == 'in_consultation':
                progress = 50
            elif rec.state == 'done':
                progress = 100
            else:
                progress = 0
            rec.progress = progress

    def action_share_whatsapp(self):
        if not self.patient_id.phone:
            raise ValidationError(_("Missing Phone Number"))
        msg = 'Hi %s' % self.patient_id.name
        whatsapp_api_url = 'https://wa.me/%s/?text=%s' % (self.patient_id.phone, msg)
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': whatsapp_api_url,
        }


class AppointmentPharmacyLine(models.Model):
    _name = "appointment.pharmacy.line"
    _description = 'Appointment Pharmacy lines'

    product_id = fields.Many2one('product.product', string='Product', required=True)
    price_unit = fields.Float(string='Price', related='product_id.list_price')
    qty = fields.Integer(string='Quantity')
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')

    company_currency_id = fields.Many2one('res.currency', related='appointment_id.currency_id')

    prise_subtotal = fields.Monetary(string='Sub Total', compute='compute_prise_subtotal',
                                     currency_field='company_currency_id')

    @api.depends('price_unit', 'qty')
    def compute_prise_subtotal(self):
        for rec in self:
            rec.prise_subtotal = rec.price_unit * rec.qty

# Search, search_count, ref, browse, exists, create, write, copy, unlink, default_get, name_get, name_search
# filtered, sudo, with_context
