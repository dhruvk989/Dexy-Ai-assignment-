from flask import Flask, request, render_template, flash, redirect, url_for
import requests

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = "YOUR_SECRET_KEY"

# GraphQL endpoint for Wellfound
WELLFOUND_GRAPHQL_URL = "https://wellfound.com/graphql"

# Update with your session cookies from DevTools
SESSION_COOKIES = {
    "_wellfound": "YOUR_WELLFOUND_COOKIE_VALUE",
    "cf_clearance": "YOUR_CF_CLEARANCE_VALUE",
}

# Headers for GraphQL requests
GRAPHQL_HEADERS = {
    "Content-Type": "application/json",
    "x-apollo-operation-name": "CandidateSendMessage"
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        message_text = request.form.get('message')

        if not message_text:
            flash("Please enter a message before sending.", "error")
            return redirect(url_for('index'))

        # GraphQL payload for sending a message
        payload = {
            "operationName": "CandidateSendMessage",
            "extensions": {
                "operationId": "tfe/1ee8d94da36a0811d05340d91a4427175dbb8abfafe2dab802483d375fdcfb7d"
            },
            "variables": {
                "input": {
                    "id": "966186090",  # Replace with the actual thread or job ID
                    "type": "JOBPAIRING",
                    "body": message_text
                }
            }
        }

        try:
            # Send the GraphQL request
            response = requests.post(
                WELLFOUND_GRAPHQL_URL,
                json=payload,
                cookies=SESSION_COOKIES,
                headers=GRAPHQL_HEADERS
            )

            # Debug logs for response
            print("Response Status Code:", response.status_code)
            print("Response Body:", response.text)

            # Handle server response
            if response.status_code == 200:
                response_json = response.json()
                if "errors" in response_json:
                    flash(f"Failed to send message. Errors: {response_json['errors']}", "error")
                else:
                    flash("Message sent successfully!", "success")
            else:
                flash(f"Failed to send message. Server responded with {response.status_code}.", "error")

        except Exception as e:
            flash(f"An error occurred: {e}", "error")
            print(f"Error: {e}")

        return redirect(url_for('index'))

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
