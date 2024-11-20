import openai
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API Key and Endpoint
openai.api_key = os.getenv("AZURE_OPENAI_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_type = "azure"
openai.api_version = "2024-08-01-preview"

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Route to test if the app is running
@app.route("/")
def index():
    return "App is running!"  # This is just to check if the app is running

# Route to analyze arguments
@app.route("/analyze", methods=["POST"])
def analyze_argument():
    try:
        # Get text input from the request
        data = request.get_json()
        if "argument" not in data:
            return jsonify({"error": "No argument provided"}), 400

        argument = data["argument"]

        # Analyze the argument using Azure OpenAI
        response = openai.Completion.create(
            engine="gpt-35-turbo",  # Replace with your deployment name
            prompt=f"Analyze this argument: {argument}",
            max_tokens=500,
            temperature=0.7
        )

        feedback = response.choices[0].text.strip()
        return jsonify({"feedback": feedback})

    except Exception as e:
        print(f"Error: {e}")  # Print the detailed error message to the terminal
        return jsonify({"error": str(e)}), 500

# Run the app on the specified host and port
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
