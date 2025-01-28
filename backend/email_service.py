import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class EmailService:
    @staticmethod
    def send_invitation_email(to_email: str, diagram_name: str, inviter_name: str, invitation_link: str):
        """
        Send email invitation for diagram collaboration
        """
        # Email configuration
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', 587))
        smtp_username = os.getenv('SMTP_USERNAME')
        smtp_password = os.getenv('SMTP_PASSWORD')
        
        if not all([smtp_username, smtp_password]):
            print("SMTP credentials not configured")
            return False

        # Create message
        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = to_email
        msg['Subject'] = f'Undangan Kolaborasi Diagram: {diagram_name}'

        # Email body
        body = f"""
        Halo,

        {inviter_name} mengundang Anda untuk berkolaborasi pada diagram '{diagram_name}' di Schema Designer.

        Untuk menerima undangan, klik tautan berikut:
        {invitation_link}

        Atau salin tautan ini ke browser Anda.

        Salam,
        Tim Schema Designer
        """

        msg.attach(MIMEText(body, 'plain'))

        try:
            # Establish SMTP connection
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"Email sending failed: {e}")
            return False

    @staticmethod
    def send_collaboration_notification(to_email: str, diagram_name: str, action: str, actor_name: str):
        """
        Send notification about collaboration changes
        """
        # Similar implementation to invitation email
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', 587))
        smtp_username = os.getenv('SMTP_USERNAME')
        smtp_password = os.getenv('SMTP_PASSWORD')
        
        if not all([smtp_username, smtp_password]):
            print("SMTP credentials not configured")
            return False

        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = to_email
        msg['Subject'] = f'Perubahan Kolaborasi Diagram: {diagram_name}'

        body = f"""
        Halo,

        {actor_name} telah {action} pada diagram '{diagram_name}'.

        Silakan periksa diagram untuk melihat detail perubahan.

        Salam,
        Tim Schema Designer
        """

        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"Notification email failed: {e}")
            return False
