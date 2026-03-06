from flask import Flask, jsonify, request
from datetime import datetime, timezone
import os

app = Flask(__name__)

@app.get("/info")
def info():
    payload = {
        "service": "simple-python-api",
        "status": "ok",
        "version": os.getenv("APP_VERSION", "dev"),
        "utc_time": datetime.now(timezone.utc).isoformat(),
        "endpoints": {
            "GET": ["/info"],
            "POST": ["/sum"]
        }
    }
    return jsonify(payload), 200

@app.post("/sum")
def sum_numbers():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Invalid JSON body"}), 400

    if "a" not in data or "b" not in data:
        return jsonify({"error": "Body must include numeric fields 'a' and 'b'"}), 400

    try:
        a = float(data["a"])
        b = float(data["b"])
    except (TypeError, ValueError):
        return jsonify({"error": "'a' and 'b' must be numbers"}), 400

    return jsonify({"a": a, "b": b, "total": a + b}), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
