import datetime

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


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
        if self.appointment_id.date == fields.Date.today():
            raise ValidationError("error")

