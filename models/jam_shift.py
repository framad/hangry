# -*- coding: utf-8 -*-

from odoo import models, fields # Mandatory
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo import models, api


class JamShift(models.Model):
    _name = 'hangry.jam_shift'
    _description = 'Master Data Jam Shift'
    _rec_name = 'name'

    # Header
    name = fields.Char()
    month = fields.Char()
    date = fields.Date()
    shift_type = fields.Selection([
        ('Pagi', 'Pagi'),
        ('Siang', 'Siang'),
        ('Malam', 'Malam')
    ], tracking=True)
    is_taken = fields.Boolean()
    is_available = fields.Boolean()
    taken_by = fields.Many2one('res.users')

    def generate_records(self):
        today = datetime.today() + timedelta(hours=7)
        first_day_of_month = today.replace(day=1)
        last_day_of_month = first_day_of_month + relativedelta(months=1, days=-1)
        
        num_days_in_month = (last_day_of_month - first_day_of_month).days + 1

        for day in range(1, num_days_in_month + 1):
            for shift_type in ['Pagi', 'Siang', 'Malam']:
                record_date = first_day_of_month + timedelta(days=day-1)
                record_name = f"{record_date.strftime('%d-%m-%Y')} {shift_type}"
                self.env['hangry.jam_shift'].create({
                    'name': record_name,
                    'month': today.strftime('%B %Y'),
                    'date': record_date,
                    'is_available': True,
                    'shift_type': shift_type
                })

        next_month = today.replace(day=1) + relativedelta(months=1)
        next_run_time = next_month.replace(hour=0, minute=1, second=0)

        cron = self.env.ref('hangry.generate_records')
        cron.write({'nextcall': next_run_time.strftime('%Y-%m-%d %H:%M:%S')})

        return True
