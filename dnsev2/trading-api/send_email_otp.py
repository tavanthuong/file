#!/usr/bin/env python3
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from dnse import DNSEClient


# ==================== CẤU HÌNH ====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
import subprocess
API_KEY_ENC = os.path.join(BASE_DIR, "api_key.enc")
API_SECRET_ENC = os.path.join(BASE_DIR, "api_secret.enc")
BASE_URL = "https://openapi.dnse.com.vn"
# lấy password từ biến môi trường
BOT_PASS = os.getenv("BOT_PASS")
# ================= Giải mã API =================
def decrypt_file(encrypted_file: str) -> str:
    if not BOT_PASS:
        print("❌ Chưa có biến môi trường BOT_PASS")
        sys.exit(1)
    try:
        result = subprocess.run(
            [
                "openssl",
                "enc",
                "-aes-256-cbc",
                "-d",
                "-pbkdf2",
                "-in",
                encrypted_file,
                "-pass",
                f"pass:{BOT_PASS}"
            ],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        print(f"❌ Lỗi giải mã {encrypted_file}")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ Lỗi: OpenSSL chưa được cài đặt")
        sys.exit(1)
print("🔄 Đang giải mã thông tin...")
API_KEY = decrypt_file(API_KEY_ENC)
API_SECRET = decrypt_file(API_SECRET_ENC)
print("✅ Giải mã thành công!")



def main():
    client = DNSEClient(
        api_key=API_KEY,
        api_secret=API_SECRET,
        base_url=BASE_URL,
    )

    status, body = client.send_email_otp(dry_run=False)
    print(status, body)


if __name__ == "__main__":
    main()
