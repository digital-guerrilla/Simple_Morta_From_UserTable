import requests
from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
load_dotenv(override=True)

API_KEY: str = str(os.getenv("API_KEY", default=""))
HEADERS: dict = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

def invite_user(email: str, project_id: str) -> None:
    with requests.request("POST", f"https://api.morta.io/v1/project/{project_id}/invite", json={"email": email, }, headers=HEADERS) as response:
        response.raise_for_status()
        return None

app = Flask(__name__)

@app.route("/invite", methods=["POST"])
def invite():
    print("Received invite request")
    data = request.get_json()
    project_id = data.get("project_Id") or data.get("contextProjectId")
    
    # Extract email from the new webhook payload structure
    email = ""
    cells = data.get("context", {}).get("cells", [])
    if cells:
        row_data = cells[0].get("row", {}).get("rowData", {})
        email = row_data.get("Email", "")
    if not email:
        return jsonify({"error": "Email is required"}), 400
    try:
        invite_user(email, project_id)
        print(f"Invitation sent to {email}")
        return jsonify({"message": f"Invitation sent to {email}"}), 200
    except requests.HTTPError as e:
        print(f"Error sending invitation: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000, threaded=True)