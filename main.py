import requests
from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
load_dotenv(override=True)

API_KEY: str = str(os.getenv("API_KEY", default=""))
MORTA_API_BASE: str = "https://api.morta.io/v1"
HEADERS: dict = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

def invite_user(email: str, project_id: str) -> None:
    with requests.request("POST", f"https://api.morta.io/v1/project/{project_id}/invite", json={"email": email}) as response:
        response.raise_for_status()
        return None

app = Flask(__name__)

@app.route("/invite", methods=["POST"])
def invite():
    data = request.get_json()
    project_id = data.get("project_Id") or data.get("contextProjectId")
    email = data.get("rowData", {}).get("Email", "")
    if not email:
        return jsonify({"error": "Email is required"}), 400
    try:
        invite_user(email, project_id)
        return jsonify({"message": f"Invitation sent to {email}"}), 200
    except requests.HTTPError as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000, threaded=True)