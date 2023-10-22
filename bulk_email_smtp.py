import smtplib
import csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders

# csv_file: Column1 (Email Recipient), Column2 (Email Body/Message)
csv_file = 'email_list.csv'

# Attachments (pdf files + mp4 file)
pdf_file1 = 'file1.pdf'
pdf_file2 = 'file2.pdf'
mp4_file = 'video.mp4'

DEFAULT_FROM_EMAIL = 'example@gmail.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'example@gmail.com'
EMAIL_HOST_PASSWORD = 'Generated App Password'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

email_list = []
with open(csv_file, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        print(f"Email: {row[0]}, Body: {row[1]}")
        email_list.append({'email': row[0], 'body': row[1]})

print(email_list)

emails_sent = 0
for email in email_list:
    subject = "Email Subject"
    to = email['email']
    content = email['body']

    print("sending email to: ", to)
    
    # Create the email message
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = DEFAULT_FROM_EMAIL
    msg['To'] = email['email']
    msg.attach(MIMEText(content))
    
# Attach the PDF file
    with open(pdf_file1, 'rb') as pdf:
        pdf_attachment = MIMEBase('application', 'pdf')
        pdf_attachment.set_payload(pdf.read())
        encoders.encode_base64(pdf_attachment)
        pdf_attachment.add_header('Content-Disposition', f'attachment; filename={pdf_file1}')
        msg.attach(pdf_attachment)
        print(f"PDF1 attached: {pdf_file1}")

    with open(pdf_file2, 'rb') as pdf:
        pdf_attachment = MIMEBase('application', 'pdf')
        pdf_attachment.set_payload(pdf.read())
        encoders.encode_base64(pdf_attachment)
        pdf_attachment.add_header('Content-Disposition', f'attachment; filename={pdf_file2}')
        msg.attach(pdf_attachment)
        print(f"PDF2 attached: {pdf_file2}")
    
# Attach the MP4 file
    try:
        # Attach the MP4 file
        with open(mp4_file, 'rb') as mp4:
            mp4_attachment = MIMEBase('video', 'mp4')
            mp4_attachment.set_payload(mp4.read())
            encoders.encode_base64(mp4_attachment)
            mp4_attachment.add_header('Content-Disposition', f'attachment; filename={mp4_file}')
            msg.attach(mp4_attachment)
            print(f"Video attached: {mp4_file}")
    except Exception as e:
        print(f"Error attaching video: {e}")
    
    
# Send the email message
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        try:
            response = smtp.send_message(msg)
            print('Email sent successfully')
            emails_sent += 1
            print("Total email sent: ", emails_sent)
        except smtplib.SMTPException as e:
            print(f"An error occurred: {e}")
        smtp.close()