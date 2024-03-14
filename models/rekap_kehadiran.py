from odoo import models, fields, api

class RekapKehadiran(models.Model):
    _name = 'hangry.rekap_kehadiran'
    _rec_name = 'user_id'

    user_id = fields.Many2one('res.users', string='User')
    MONTH_SELECTION = [
        ('01', 'January'),
        ('02', 'February'),
        ('03', 'March'),
        ('04', 'April'),
        ('05', 'May'),
        ('06', 'June'),
        ('07', 'July'),
        ('08', 'August'),
        ('09', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December'),
    ]
    ordinat_id = fields.Many2one(related='user_id.ordinat', store=True)
    month_selection = fields.Selection(MONTH_SELECTION, string='Month')
    tanggal_1 = fields.Char()
    tanggal_2 = fields.Char()
    tanggal_3 = fields.Char()
    tanggal_4 = fields.Char()
    tanggal_5 = fields.Char()
    tanggal_6 = fields.Char()
    tanggal_7 = fields.Char()
    tanggal_8 = fields.Char()
    tanggal_9 = fields.Char()
    tanggal_10 = fields.Char()
    tanggal_11 = fields.Char()
    tanggal_12 = fields.Char()
    tanggal_13 = fields.Char()
    tanggal_14 = fields.Char()
    tanggal_15 = fields.Char()
    tanggal_16 = fields.Char()
    tanggal_17 = fields.Char()
    tanggal_18 = fields.Char()
    tanggal_19 = fields.Char()
    tanggal_20 = fields.Char()
    tanggal_21 = fields.Char()
    tanggal_22 = fields.Char()
    tanggal_23 = fields.Char()
    tanggal_24 = fields.Char()
    tanggal_25 = fields.Char()
    tanggal_26 = fields.Char()
    tanggal_27 = fields.Char()
    tanggal_28 = fields.Char()
    tanggal_29 = fields.Char()
    tanggal_30 = fields.Char()
    tanggal_31 = fields.Char()

    def fill_tanggal_fields(self):
        absensi_records = self.env['hangry.attendance'].search([
            ('user_id', '=', self.user_id.id),
            ('create_date', 'like', f'{self.month_selection}-%'),
            ('is_validated','=',True)
        ])

        for absensi in absensi_records:
            day = absensi.jam_shift_id.date.day
            field_name = f'tanggal_{day}'
            if absensi.is_hadir == True:
                self[field_name] = 'H'
            elif absensi.is_tidakhadir == True:
                self[field_name] = 'OFF'
            else:
                pass

        return True
