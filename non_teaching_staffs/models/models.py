import base64
from odoo import fields, models

class Staff(models.Model):
    _name = 'staff'
    _description = 'A module to add both teaching and non-teaching staffs'

    # Profile Photo field (binary field to store images in the database)
    profilePhoto = fields.Many2one('ir.attachment', string="Profile Photo")

    # Common Fields for both Teaching and Non-Teaching Staff
    nonTeachingStaffName = fields.Char("Staff Name")
    
    # Non-Teaching Specific Fields
    nonTeachingPosition = fields.Char("Non-Teaching Position", help="The position of the non-teaching staff")

    # Deleting a staff record (method)
    def delete_record(self):
        self.unlink()

    # Get Profile Photo in base64 encoding (method)
    def get_profile_photo_base64(self):
        if self.profilePhoto:
            return base64.b64encode(self.profilePhoto).decode('utf-8')
        return ''
