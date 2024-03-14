# -*- coding: utf-8 -*-

from odoo import models, fields # Mandatory
from datetime import date, datetime, timedelta


class Attendance(models.Model):
    _name = 'hangry.attendance' # name_of_module.name_of_class 
    _description = 'Kehadiran / Absensi' # Some note of table
    _rec_name = 'user_id'

    # Header
    user_id = fields.Many2one(comodel_name='res.users', default=lambda self: self.default_loggedin())
    ordinat_id = fields.Many2one(comodel_name='res.users', default=lambda self: self.default_ordinat())
    jam_shift_id = fields.Many2one('hangry.jam_shift')
    checkin = fields.Datetime()
    checkout = fields.Datetime()
    geolocation_checkin = fields.Char()
    geolocation_checkout = fields.Char()
    longitude = fields.Char()
    latitude = fields.Char()
    is_validated = fields.Boolean()
    is_hadir = fields.Boolean()
    is_tidakhadir = fields.Boolean()

    def default_loggedin(self):
        loggedin_user = self.env['res.users'].search([('id', '=', self.env.user.id)])
        print(loggedin_user)
        return loggedin_user
    
    def default_ordinat(self):
        ordinat_loggedin = self.env['res.users'].search([('id', '=', self.env.user.id)]).ordinat
        print(ordinat_loggedin)
        return ordinat_loggedin
    
    def approve_spv(self):
        self.write({'is_validated': True})
        message = "Validasi Absensi Berhasil"
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'message': message,
                'type': 'success',
                'sticky': False,
            'next': {
                    'type': 'ir.actions.client',
                    'tag': 'reload'
                }
            }
        }