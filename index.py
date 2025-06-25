
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Dữ liệu người dùng và license
valid_users = {
    "huong@gmail.com": {
        "tools": {
            "voice_cloner": {
                "token": "ghp_voice_123abc",
                "license_type": "lifetime",
                "expired": "none"
            },
            "srt_converter": {
                "token": "ghp_srt_456def",
                "license_type": "1-year",
                "expired": "2026-12-31"
            }
        }
    }
}

@app.route('/get-token', methods=['POST'])
def get_token():
    data = request.json
    email = data.get("email", "").strip().lower()
    tool = data.get("tool", "").strip()

    if not email or not tool:
        return jsonify({"success": False, "error": "Thiếu email hoặc tên tool"}), 400

    user = valid_users.get(email)
    if not user or tool not in user["tools"]:
        return jsonify({"success": False, "error": "Email hoặc tool không hợp lệ"}), 403

    license_info = user["tools"][tool]

    if license_info["license_type"] != "lifetime":
        today = datetime.today().date()
        expired = datetime.strptime(license_info["expired"], "%Y-%m-%d").date()
        if today > expired:
            return jsonify({"success": False, "error": "Bản quyền đã hết hạn"}), 403

    return jsonify({"success": True, "token": license_info["token"]})

if __name__ == "__main__":
    app.run()
