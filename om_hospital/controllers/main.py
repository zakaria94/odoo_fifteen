from odoo import http
from odoo.http import request


class Hospital(http.Controller):

    # Sample Controller Created
    # auth='public' or user or none
    @http.route('/hospital/patient/', type="http", auth="public", website=True, sitemap=True)
    def hospital_patient(self, **kw):
        patients = request.env['hospital.patient'].sudo().search([])
        return request.render("om_hospital.patients_page", {
            'patients': patients
        })
        # return "Hello World"

    @http.route('/patient_webform', type="http", auth="public", website=True)
    def patient_webform(self, **kw):
        return request.render('om_hospital.create_patient', {})

    @http.route('/create/webpatient', type="http", auth="public", website=True)
    def create_webpatient(self, **kw):
        request.env['hospital.patient'].sudo().create(kw)
        return request.render('om_hospital.patient_thanks', {})


