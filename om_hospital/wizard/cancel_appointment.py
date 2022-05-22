import datetime

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date
from dateutil import relativedelta


class CancelAppointmentWizard(models.TransientModel):
    _name = 'cancel.appointment.wizard'
    _description = 'Cancel Appointment'

    @api.model
    def default_get(self, fields):
        print("============================ Default get Executed =======================", fields)
        res = super(CancelAppointmentWizard, self).default_get(fields)
        print("============== Res =================", res)
        res['cancel_date'] = datetime.date.today()
        # res['appointment_id'] = self.env.context.get('active_id')
        return res

    appointment_id = fields.Many2one('hospital.appointment', string='Appointment', domain=[('state', '=', 'draft')])
    reason = fields.Text(string='Reason')
    cancel_date = fields.Date(string='Cancellation Date')

    def action_cancel(self):
        cancel = self.env['ir.config_parameter'].sudo().get_param('om_hospital.cancel_days')
        print("Cancel Day", cancel)
        allowed_days = self.appointment_id.date - relativedelta.relativedelta(days=int(cancel))
        print("Allowed Days", allowed_days)
        # if allowed_days < date.today() or self.appointment_id.date == fields.Date.today():
        #     raise ValidationError("error")
        self.appointment_id.state = 'cancel'
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
