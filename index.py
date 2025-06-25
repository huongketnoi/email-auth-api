from flask import Flask, jsonify, request

app = Flask(__name__)

# Route mặc định để test trên Vercel
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Email Auth API đang chạy!"})

# Route ví dụ để xác thực email
@app.route("/verify", methods=["POST"])
def verify_email():
    data = request.get_json()
    email = data.get("email")
    if email and "@" in email:
        return jsonify({"status": "success", "email": email})
    return jsonify({"status": "error", "message": "Invalid email"}), 400

if __name__ == "__main__":
    app.run()
