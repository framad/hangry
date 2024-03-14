# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions # Mandatory
from datetime import date, datetime, timedelta
from odoo.exceptions import ValidationError
import requests


class WorkSchedule(models.Model):
    _name = 'hangry.work_schedule' 
    _description = 'Jadwal Kerja'
    _rec_name = 'user_id'

    # Header
    user_id = fields.Many2one(comodel_name='res.users', default=lambda self: self.default_loggedin())
    jam_shift_id = fields.Many2one('hangry.jam_shift')
    type = fields.Selection([
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time')
    ], tracking=True)
    type_id = fields.Selection(related='user_id.type', store=True)
    change_shift = fields.Boolean(default=False)
    is_posting = fields.Boolean()
    is_attend = fields.Boolean()
    is_off = fields.Boolean()
    is_finish = fields.Boolean()
    attendance_id = fields.Many2one('hangry.attendance')

    def absen_off(self):
        if self.is_attend != True and self.jam_shift_id.date.day == datetime.today().date().day:
            tanggal = self.jam_shift_id.date.day
            data_kehadiran = {
                'ordinat_id': self.user_id.ordinat.id,
                'jam_shift_id': self.jam_shift_id.id,
                'checkin': fields.Datetime.now(),
                'is_tidakhadir': True,
            }
            # field_name = f'tanggal_{tanggal}'
            # data_kehadiran[field_name] = 'OFF'
            # print(field_name, "ini nama field")
            user = self.env['hangry.attendance'].create(data_kehadiran)
            self.is_off = True
            self.attendance_id = user.id
        else:
            raise exceptions.ValidationError('Tidak Bisa OFF untuk absen sudah checkin / Tidak bisa OFF pada hari yang berbeda dengan jadwal')
        
    def attend_kehadiran(self):
        print(self.jam_shift_id.date.day, "ini")
        print(datetime.today().date().day, "itu")
        latitude, longitude = self.get_coordinates()
        if self.is_attend != True and self.jam_shift_id.date.day == datetime.today().date().day:
            tanggal = self.jam_shift_id.date.day
            latitude, longitude = self.get_coordinates()
            data_kehadiran = {
                'ordinat_id': self.user_id.ordinat.id,
                'jam_shift_id': self.jam_shift_id.id,
                'checkin': fields.Datetime.now(),
                'is_hadir': True,
                'geolocation_checkin': f"{latitude},{longitude}"
            }
            # field_name = f'tanggal_{tanggal}'
            # data_kehadiran[field_name] = 'H'
            # print(field_name, "ini nama field")
            user = self.env['hangry.attendance'].create(data_kehadiran)
            self.is_attend = True
            self.attendance_id = user.id
        elif self.is_finish != True:
            self.attendance_id.checkout = fields.Datetime.now()
            self.attendance_id.geolocation_checkout = f"{latitude},{longitude}"
            self.is_finish = True
        elif self.jam_shift_id.date.day != datetime.today().date().day:
            raise exceptions.ValidationError('Tidak Bisa Checkin untuk Jadwal yang Bukan Hari Ini!!')
        

    def pilih_shift(self):
        if self.user_id.type == "Part Time":
            self.change_shift = True
        else:
            raise exceptions.ValidationError('Hanya Employee Part Time yang Bisa Memilih Shift Sendiri!!')

    def default_loggedin(self):
        loggedin_user = self.env['res.users'].search([('id', '=', self.env.user.id)])
        print(loggedin_user)
        return loggedin_user
    
    def post_schedule(self):
        for record in self:
            if record.is_posting == False:
                record.is_posting = True

    def get_coordinates(self):
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": "Bandung, Indonesia",
            "format": "json"
        }
        response = requests.get(url, params=params)
        data = response.json()

        if data:
            latitude = float(data[0]['lat'])
            longitude = float(data[0]['lon'])
            return latitude, longitude
        else:
            return None, None