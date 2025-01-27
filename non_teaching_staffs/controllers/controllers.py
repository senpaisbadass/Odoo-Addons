from odoo import http
from odoo.http import request
import base64
from io import BytesIO
from PIL import Image  # Import the Image module from PIL (Pillow)
import os

class StaffController(http.Controller):

    @http.route('/non_teaching_staffs/form', type='http', auth='user', website=True)
    def staff_form(self, **kw):
        staff_id = int(kw.get('staff_id', 0))
        staff = None
        if staff_id:
            staff = request.env['staff'].sudo().browse(staff_id)
        
        # Fetch all staff records for display in the table
        staffs = request.env['staff'].sudo().search([])

        # Render the form view template with the staff data
        return request.render('non_teaching_staffs.non_teaching_staff_form', {
            'staff': staff,  # Either the specific staff record or None for new staff
            'staffs': staffs,  # List of all staff records for display in the table
        })

    @http.route('/non_teaching_staffs/save', type='http', auth='user', methods=['POST'], website=True)
    def save_staff(self, **kw):
        staff_id = int(kw.get('staff_id', 0))
        profile_photo = request.httprequest.files.get('profile_photo')  # Get the image file from the form

        attachment_id = None  # Initialize attachment ID as None
        
        # Check if the file is uploaded and validate the file type (only jpg, jpeg, png allowed)
        if profile_photo:
            filename = profile_photo.filename
            ext = os.path.splitext(filename)[1].lower()  # Get file extension
            allowed_extensions = ['.jpg', '.jpeg', '.png']
            
            if ext not in allowed_extensions:
                return request.render('staff.staff_form', {
                    'error': 'Invalid file format! Only JPG, JPEG, and PNG are allowed.'
                })

            img = Image.open(profile_photo)

            image_buffer = BytesIO()
            img.save(image_buffer, format='JPEG')  # Save as JPEG format
            image_data = image_buffer.getvalue()  # Get the binary data from the buffer

            attachment = request.env['ir.attachment'].sudo().create({
                'name': 'Profile Photo',  # The name of the attachment
                'datas': base64.b64encode(image_data),  # Attach the image binary data (base64 encoded)
                'res_model': 'staff',  # Link to the staff model
                'res_id': staff_id if staff_id else None,  # Link to the staff record
                'type': 'binary',  # This specifies that it's a binary file
            })

            attachment_id = attachment.id
        
        if staff_id:
            staff = request.env['staff'].sudo().browse(staff_id)
            staff.write({
                'nonTeachingStaffName': kw.get('non_teaching_staff_name'),
                'nonTeachingPosition': kw.get('non_teaching_position'),
                'profilePhoto': attachment_id,  # Store the attachment ID as a reference
            })
        else:
            request.env['staff'].sudo().create({
                'nonTeachingStaffName': kw.get('non_teaching_staff_name'),
                'nonTeachingPosition': kw.get('non_teaching_position'),
                'profilePhoto': attachment_id,  # Store the attachment ID as a reference
            })

        return request.redirect('/non_teaching_staffs/form')

    @http.route('/non_teaching_staffs/delete/<int:staff_id>', type='http', auth='user', website=True)
    def delete_staff(self, staff_id):
        staff = request.env['staff'].sudo().browse(staff_id)
        
        if not staff.exists():
            return request.redirect('/non_teaching_staffs/form')  # Redirect if the staff doesn't exist
        
        if staff.profilePhoto:
            attachment = request.env['ir.attachment'].sudo().browse(staff.profilePhoto.id)
            if attachment.exists():
                attachment.unlink()  # Delete the attachment (profile photo)
        
        staff.unlink()

        # Redirect back to the form page after deletion
        return request.redirect('/non_teaching_staffs/form')

    @http.route('/non_teaching_staffs/views', type='http', auth='user', website=True)
    def staff_view(self, **kw):
        # Fetch all staff records
        staffs = request.env['staff'].sudo().search([])

        # Render the staff view template (show only staff list)
        return request.render('non_teaching_staffs.non_teaching_staff_views', {
            'staffs': staffs,  # List of all staff records for display in the table
        })
