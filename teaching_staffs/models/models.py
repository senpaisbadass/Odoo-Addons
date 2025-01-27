import base64
from odoo import fields, models

class TeachingStaffs(models.Model):
    _name = 'teaching.staffs'
    _description = 'A module to add the teaching staffs'

    profilePhoto = fields.Many2one('ir.attachment', string='Profile Photo')
    teachingStaffName = fields.Char("Teaching Staff Name")
    teachingSubject = fields.Char("Teaching Subject")
    
    def delete_record(self):
        self.unlink()

    def get_profile_photo_base64(self):
        if self.profilePhoto:
            return base64.b64encode(self.profilePhoto).decode('utf-8')
        return ''
