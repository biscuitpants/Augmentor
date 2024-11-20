import openai
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set OpenAI API Key and Endpoint
openai.api_key = os.getenv("AZURE_OPENAI_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_type = "azure"
openai.api_version = "2024-08-01-preview"

# Initialize Flask app
app = Flask(__name__)
CORS(app)

def rate_argument(feedback):
    """Rate the argument on a scale of 1-10 with 0.5 increments."""
    score = 5  # Default score, assuming average quality
    
    # Check for various feedback keywords to rate the argument
    if "logically sound" in feedback or "well-reasoned" in feedback:
        score = 9.5  # Excellent argument
    elif "valid" in feedback and "supported" in feedback:
        score = 8  # Strong argument with evidence
    elif "weak" in feedback or "flawed" in feedback:
        score = 4  # Argument has flaws
    elif "invalid" in feedback or "illogical" in feedback:
        score = 2  # Argument is weak or invalid
    
    # Round to nearest 0.5
    rounded_score = round(score * 2) / 2

    # Print the rating for visibility in the console
    print(f"Rating for argument: {rounded_score}")
    
    return rounded_score

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
        rating = rate_argument(feedback)  # Get the rating based on the feedback

        return jsonify({"feedback": feedback, "rating": rating})

    except Exception as e:
        print(f"Error: {e}")  # Print the detailed error message to the terminal
        return jsonify({"error": str(e)}), 500

from waitress import serve

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)
