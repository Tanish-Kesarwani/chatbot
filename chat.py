from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Path to the .txt file where the chatbot will learn from
FILE_PATH = "knowledge_base.txt"

# Sample product database (this can be replaced with a real database)
PRODUCTS = {
    "laptop": ["laptop case", "mouse", "keyboard"],
    "phone": ["phone case", "screen protector", "charger"],
    "headphones": ["headphone stand", "audio splitter", "carrying case"]
}

# Function to read the .txt file and return responses based on user input
def get_response(user_input):
    user_input = user_input.lower().strip()
    response = None
    related_products_response = ""

    # Check if the user's query is already in the knowledge base
    with open(FILE_PATH, 'r') as file:
        for line in file:
            if line.lower().startswith(user_input + " :"):
                response = line[len(user_input) + 2:].strip()
                break

    # Check if the query involves any product in the PRODUCTS database
    for product in PRODUCTS:
        if product in user_input:
            related_products = PRODUCTS[product]
            related_products_response = f"If you're interested in {product}, you might also like: " + ", ".join(related_products)
            break

    # If no predefined response is found, ask the user for the correct response
    if response is None:
        response = "I don't know the answer to that. Can you teach me?"

    # Combine the response with related product suggestions if applicable
    final_response = response
    if related_products_response:
        final_response += "\n" + related_products_response

    return final_response

# Function to learn a new response from the user
def learn_response(user_input, new_response):
    user_input = user_input.lower().strip()

    # Append the new question-answer pair to the knowledge base
    with open(FILE_PATH, 'a') as file:
        file.write(f"{user_input} : {new_response}\n")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def respond():
    user_input = request.json.get("query")
    response = get_response(user_input)

    # If the chatbot doesn't know the answer, expect the user to provide it
    if "I don't know the answer to that" in response:
        return jsonify({"response": response, "learning": True})
    else:
        return jsonify({"response": response, "learning": False})

@app.route('/learn_response', methods=['POST'])
def learn():
    user_input = request.json.get("query")
    new_response = request.json.get("response")
    learn_response(user_input, new_response)
    return jsonify({"status": "learned"})

if __name__ == "__main__":
    if not os.path.exists(FILE_PATH):
        open(FILE_PATH, 'w').close()  # Create the file if it doesn't exist
    app.run(debug=True)
