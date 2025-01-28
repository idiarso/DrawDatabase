import os
from dotenv import load_dotenv
from email_service import EmailService

def check_email_configuration():
    # Muat environment variables
    load_dotenv()

    print("🔍 Pemeriksaan Konfigurasi Email Schema Designer")
    print("=" * 50)

    # Periksa variabel lingkungan
    required_vars = [
        'SMTP_SERVER', 
        'SMTP_PORT', 
        'SMTP_USERNAME', 
        'SMTP_PASSWORD', 
        'FRONTEND_URL',
        'TEST_EMAIL'
    ]

    config_valid = True
    for var in required_vars:
        value = os.getenv(var)
        status = "✅ Terkonfigurasi" if value else "❌ Tidak Terkonfigurasi"
        print(f"{var}: {status}")
        if not value:
            config_valid = False

    print("\n📧 Tes Pengiriman Email")
    print("-" * 50)

    if not config_valid:
        print("❌ Konfigurasi tidak lengkap. Harap periksa file .env")
        return False

    test_email = os.getenv('TEST_EMAIL')
    
    try:
        result = EmailService.send_invitation_email(
            to_email=test_email,
            diagram_name="Tes Konfigurasi",
            inviter_name="Tim Pengembang",
            invitation_link=f"{os.getenv('FRONTEND_URL')}/test-invitation"
        )

        if result:
            print(f"✅ Email tes berhasil dikirim ke {test_email}")
            return True
        else:
            print("❌ Gagal mengirim email tes")
            return False

    except Exception as e:
        print(f"❌ Kesalahan saat mengirim email: {e}")
        return False

if __name__ == "__main__":
    check_email_configuration()
