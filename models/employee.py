# -*- coding: utf-8 -*-

from odoo import models, fields, api # Mandatory
from datetime import date, datetime, timedelta


class Employee(models.Model):
    _name = 'hangry.employee' # name_of_module.name_of_class 
    _description = 'Master Data Employee' # Some note of table
    _rec_name = 'name'

    # Header
    name = fields.Char()
    date = fields.Date()
    type = fields.Selection([
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time')
    ], tracking=True)
    jabatan = fields.Selection([
        ('SPV', 'SPV'),
        ('Staff', 'Staff')
    ], tracking=True)
    ordinat = fields.Many2one('res.users')
    password = fields.Char()
    login = fields.Char()
    user_id = fields.Many2one(comodel_name='res.users')

    @api.model
    def create(self, vals):
        res = super(Employee, self).create(vals)
        if vals['jabatan'] == 'SPV':
            try:
                data_user = {
                    'name' : vals['name'],
                    'login' : vals['login'],
                    'jabatan' : vals['jabatan'],
                    'password' : vals['password'],
                    'type' : vals['type'],
                    'ordinat' : vals['ordinat'],
                    # 'marketing' : int(res.marketing.nama_user_id.id),
                    }
                # print(data_user, "ini data userrrr")
                user = self.env['res.users'].create(data_user)
                res.write({'user_id' : user.id})
                user.sudo().write({'groups_id': [(4,self.env.ref('hangry.group_spv').id)]})
            except Exception as e:
                print(f"Error creating user: {e}")
        elif vals['jabatan'] == 'Staff':
            try:
                data_user = {
                    'name' : vals['name'],
                    'login' : vals['login'],
                    'jabatan' : vals['jabatan'],
                    'password' : vals['password'],
                    'type' : vals['type'],
                    'ordinat' : vals['ordinat'],
                    # 'marketing' : int(res.marketing.nama_user_id.id),
                    }
                # print(data_user, "ini data userrrr")
                user = self.env['res.users'].create(data_user)
                res.write({'user_id' : user.id})
                user.sudo().write({'groups_id': [(4,self.env.ref('hangry.group_staff').id)]})
            except Exception as e:
                print(f"Error creating user: {e}")
        return res
    
    def write(self, vals):
        res = super(Employee, self).write(vals)
        if self.jabatan == 'SPV':
            query = {}
            if 'name' in vals:
                query['name'] = vals['name']
            if 'login' in vals:
                query['login'] = vals['login']
            if 'password' in vals:
                query['password'] = vals['password']
            if 'jabatan' in vals:
                query['jabatan'] = vals['jabatan']
            if 'type' in vals:
                query['type'] = vals['type']
            if 'ordinat' in vals:
                query['ordinat'] = vals['ordinat']
            if query:
                partner = self.env['res.users'].search([('id','=',self.user_id.id)])
                partner.write(query)
        elif self.jabatan == 'Staff':
            query = {}
            if 'name' in vals:
                query['name'] = vals['name']
            if 'login' in vals:
                query['login'] = vals['login']
            if 'password' in vals:
                query['password'] = vals['password']
            if 'jabatan' in vals:
                query['jabatan'] = vals['jabatan']
            if 'type' in vals:
                query['type'] = vals['type']
            if 'ordinat' in vals:
                query['ordinat'] = vals['ordinat']
            if query:
                partner = self.env['res.users'].search([('id','=',self.user_id.id)])
                partner.write(query)
        return res
    
    class ResUsers(models.Model):
        _inherit = 'res.users'

        ordinat = fields.Many2one('res.users')
        jabatan = fields.Selection([
            ('SPV', 'SPV'),
            ('Staff', 'Staff')
        ], tracking=True)
        type = fields.Selection([
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time')
        ], tracking=True)
        ordinat = fields.Many2one('res.users')
