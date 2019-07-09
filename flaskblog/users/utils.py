import secrets
import os
from PIL import Image
from flask import url_for
from flaskblog import app, mail
from flask_mail import Message


def save_picture(form_picture):
    random_hex_for_pic_name = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_f_name = random_hex_for_pic_name + f_ext

    # app.root_path gives us the path to our app
    picture_path = os.path.join(app.root_path, 'static/profile_pics/', picture_f_name)
    
    # resize image to smaller size and then save it, saves size and prevents slow down of site
    output_size = (125, 125)
    resized_picture = Image.open(form_picture)
    resized_picture.thumbnail(output_size)
    resized_picture.save(picture_path)

    return picture_f_name


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', 
                   recipients=[user.email])
    # _external gives a non relative url
    msg.body = f'''To reset your password, click the link below:
    {url_for('reset_token', token=token, _external=True)}

    If you didn't make this request, ignore and delete the email and no changes will be made.
    '''
    
    mail.send(msg)
