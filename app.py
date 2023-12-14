from flask import Flask, jsonify, request
from main import __main  # Make sure to import your function

app = Flask(__name__)

@app.route('/call_main', methods=['GET'])
def call_main():
    user_input = request.args.get('input', '')  # Get user input from query parameters
    response = __main(user_input)  # Pass user input to the function
    return jsonify({'message': response})

if __name__ == '__main__':
    app.run(debug=True)