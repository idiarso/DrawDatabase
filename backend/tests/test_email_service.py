import pytest
from email_service import EmailService
import os
from dotenv import load_dotenv

# Muat environment variable untuk tes
load_dotenv()

def test_send_invitation_email():
    """
    Tes pengiriman email undangan
    """
    test_email = os.getenv('TEST_EMAIL')
    
    if not test_email:
        pytest.skip("Email tes tidak dikonfigurasi")
    
    result = EmailService.send_invitation_email(
        to_email=test_email,
        diagram_name="Diagram Tes",
        inviter_name="Penguji",
        invitation_link="http://localhost:3000/invitations/123"
    )
    
    assert result is True, "Pengiriman email gagal"

def test_send_collaboration_notification():
    """
    Tes pengiriman notifikasi kolaborasi
    """
    test_email = os.getenv('TEST_EMAIL')
    
    if not test_email:
        pytest.skip("Email tes tidak dikonfigurasi")
    
    result = EmailService.send_collaboration_notification(
        to_email=test_email,
        diagram_name="Diagram Tes",
        action="menambahkan",
        actor_name="Admin"
    )
    
    assert result is True, "Pengiriman notifikasi gagal"

def test_email_configuration():
    """
    Periksa konfigurasi email dasar
    """
    assert os.getenv('SMTP_SERVER') is not None, "SMTP Server tidak dikonfigurasi"
    assert os.getenv('SMTP_PORT') is not None, "Port SMTP tidak dikonfigurasi"
    assert os.getenv('SMTP_USERNAME') is not None, "Username SMTP tidak dikonfigurasi"
    assert os.getenv('SMTP_PASSWORD') is not None, "Password SMTP tidak dikonfigurasi"
