"""
Market data subscription example.

Demonstrates:
- Subscribing to security definition updates

This example shows how to receive real-time market data for multiple symbols.
"""

import asyncio

from trading_websocket import TradingClient
from trading_websocket.models import SecurityDefinition


# ==================== CẤU HÌNH ====================
import subprocess, os, sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
API_KEY_ENC = os.path.join(BASE_DIR, "api_key.enc")
API_SECRET_ENC = os.path.join(BASE_DIR, "api_secret.enc")
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
async def main():
    # Initialize client
    encoding = "msgpack"  # json or msgpack
    client = TradingClient(
        api_key=API_KEY,
        api_secret=API_SECRET,
        base_url="wss://ws-openapi.dnse.com.vn",
        encoding=encoding,
    )

    def handle_security_definition(sec_def: SecurityDefinition):
        print(f"SECURITY DEFINITION: {sec_def}")

    # Connect to gateway
    print("Connecting to WebSocket gateway...")
    await client.connect()
    print(f"Connected! Session ID: {client._session_id}\n")

    print("Subscribing to security definition for SSI and 41I1G2000...")
    await client.subscribe_sec_def(["SSI", "41I1G2000"], on_sec_def=handle_security_definition, encoding=encoding, board_id="G1")

    print("\nReceiving market data (will run for 1 hour)...\n")

    # Run for 1H to collect data
    # In a real application, you might run indefinitely or until a specific condition
    await asyncio.sleep(8 * 60 * 60)

    # Disconnect gracefully
    print("\n\nDisconnecting...")
    await client.disconnect()
    print("Disconnected!")


if __name__ == "__main__":
    asyncio.run(main())
