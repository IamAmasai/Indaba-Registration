from flask import Flask, render_template, request 
import qrcode
from PIL import Image
import io
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    # Get attendee details from the form
    name = request.form['name']
    email = request.form['email']
    University = request.form['University']
    

    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(f"Name: {name}\nEmail: {email}")
    qr.make(fit=True)
    qr_image = qr.make_image(fill="black", back_color="white")

    # Save QR code as image
    qr_image_io = io.BytesIO()
    qr_image.save(qr_image_io, 'PNG')
    qr_image_io.seek(0)

    # Create email message
    msg = MIMEMultipart()
    msg['From'] = 'your_email@example.com'
    msg['To'] = email
    msg['Subject'] = 'Event Registration Confirmation'

    # Attach QR code image to the email
    qr_image_attachment = MIMEImage(qr_image_io.read())
    qr_image_attachment.add_header('Content-Disposition', 'attachment', filename='qr_code.png')
    msg.attach(qr_image_attachment)

    # Send email
    smtp_server = 'smtp.example.com'
    smtp_port = 587
    smtp_username = 'your_email@example.com'
    smtp_password = 'your_password'

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)

    return 'Registration successful! Please check your email for the QR code.'

if __name__ == '__main__':
    app.run()