from odoo import http
from odoo.http import request
import base64
from io import BytesIO
from PIL import Image
import os

class TeachingStaffController(http.Controller):

    @http.route('/teaching_staffs/form', type='http', auth='user', website=True)
    def teaching_staff_form(self, **kw):
        staff_id = int(kw.get('staff_id', 0))
        staff = None
        if staff_id:
            staff = request.env['teaching.staffs'].sudo().browse(staff_id)
        
        # Fetch all teaching staff records for display in the table
        staffs = request.env['teaching.staffs'].sudo().search([])

        # Render the form view template with the staff data
        return request.render('teaching_staffs.teaching_staff_form', {
            'staff': staff,  # Either the specific staff record or None for new staff
            'staffs': staffs,  # List of all staff records for display in the table
        })

    @http.route('/teaching_staffs/save', type='http', auth='user', methods=['POST'], website=True)
    def save_teaching_staff(self, **kw):
        staff_id = int(kw.get('staff_id', 0))
        profile_photo = request.httprequest.files.get('profile_photo')  # Get the image file from the form

        attachment_id = None  # Initialize attachment ID as None
        
        # Check if the file is uploaded and validate the file type (only jpg, jpeg, png allowed)
        if profile_photo:
            # Get file extension and check if it is one of the allowed formats
            filename = profile_photo.filename
            ext = os.path.splitext(filename)[1].lower()  # Get file extension
            allowed_extensions = ['.jpg', '.jpeg', '.png']
            
            if ext not in allowed_extensions:
                # You can handle invalid file format here
                return request.render('teaching_staffs.teaching_staff_form', {
                    'error': 'Invalid file format! Only JPG, JPEG, and PNG are allowed.'
                })

            # Read the image using Pillow
            img = Image.open(profile_photo)

            # Save the image to a buffer
            image_buffer = BytesIO()
            img.save(image_buffer, format='JPEG')  # Save as JPEG format
            image_data = image_buffer.getvalue()  # Get the binary data from the buffer

            # Create an attachment in ir.attachment
            attachment = request.env['ir.attachment'].sudo().create({
                'name': 'Profile Photo',  # The name of the attachment
                'datas': base64.b64encode(image_data),  # Attach the image binary data (base64 encoded)
                'res_model': 'teaching.staffs',  # Link to the teaching staff model
                'res_id': staff_id if staff_id else None,  # Link to the teaching staff record
                'type': 'binary',  # This specifies that it's a binary file
            })

            # Get the attachment ID and save it on the teaching staff record
            attachment_id = attachment.id
        
        # Update or create the staff record with the uploaded image reference
        if staff_id:
            # Update existing staff record
            staff = request.env['teaching.staffs'].sudo().browse(staff_id)
            staff.write({
                'teachingStaffName': kw.get('teaching_staff_name'),
                'teachingSubject': kw.get('teaching_subject'),
                'profilePhoto': attachment_id,  # Store the attachment ID as a reference
            })
        else:
            # Create a new staff record with the image attachment
            request.env['teaching.staffs'].sudo().create({
                'teachingStaffName': kw.get('teaching_staff_name'),
                'teachingSubject': kw.get('teaching_subject'),
                'profilePhoto': attachment_id,  # Store the attachment ID as a reference
            })

        return request.redirect('/teaching_staffs/form')

    @http.route('/teaching_staffs/delete/<int:staff_id>', type='http', auth='user', website=True)
    def delete_teaching_staff(self, staff_id):
        staff = request.env['teaching.staffs'].sudo().browse(staff_id)
        if staff:
            # Check if there's a profile photo (attachment ID)
            if staff.profilePhoto:
                # Get the attachment object linked to the staff's profile photo
                attachment = request.env['ir.attachment'].sudo().browse(staff.profilePhoto.id)
                if attachment:
                    attachment.unlink()  # Delete the attachment (profile photo)

            # Now delete the staff record
            staff.unlink()
        
        # Redirect back to the form page after deletion
        return request.redirect('/teaching_staffs/form')

    @http.route('/teaching_staffs/views', type='http', auth="user", website=True)
    def teaching_staff_view(self, **kw):
        # Fetch all teaching staff records
        staffs = request.env['teaching.staffs'].sudo().search([])

        # Render the teaching staff view template
        return request.render('teaching_staffs.teaching_staff_views', {
            'staffs': staffs,
        })
