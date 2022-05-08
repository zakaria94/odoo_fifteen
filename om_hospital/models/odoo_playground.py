from odoo import models, fields, api
from odoo.tools.safe_eval import safe_eval


class OdooPlayGround(models.Model):
    _name = "odoo.play.ground"
    _description = 'Odoo Playground Addons'

    DEFAULT_ENV_VARIABLES = """# available variables:
    # - self: Current Object
    # - self.env: odoo environment on which the action is triggered
    # - self.env.user: return the current user (as an instance)
    # - self.env.is_system
    # - self.env.is_admin
    # - self.env.is_superuser
    # - self.env.company
    # - self.env.companies
    # - self.env.lang : return the current lang code \n\n\n\n """

    model_id = fields.Many2one('ir.model', string='Model')
    code = fields.Text(string='Code', default=DEFAULT_ENV_VARIABLES)
    result = fields.Text(string='Result')

    def action_execute(self):
        try:
            if self.model_id:
                model = self.env[self.model_id.model]
            else:
                model = self
            self.result = safe_eval(self.code.strip(), {'self': model})
        except Exception as e:
            self.result = str(e)
