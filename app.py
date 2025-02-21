from flask import Flask, request, jsonify

app = Flask(_name_)


def handle_exception(e):
    return jsonify({"is_success": False, "error": str(e)}), 400

app.register_error_handler(Exception, handle_exception)

@app.route('/bfhl', methods=['POST'])
def bfhl_post():
    try:
        
        data = request.get_json()

        if "data" not in data:
            raise ValueError("Missing 'data' field in the request")

        input_data = data["data"]

        
        numbers = [item for item in input_data if item.isdigit()]
        alphabets = [item for item in input_data if item.isalpha()]

        
        highest_alphabet = max(alphabets, key=lambda x: x.lower(), default=None)

        
        response = {
            "is_success": True,
            "user_id": "john_doe_17091999",
            "email": "john@xyz.com",
            "roll_number": "ABCD123",
            "numbers": numbers,
            "alphabets": alphabets,
            "highest_alphabet": [highest_alphabet] if highest_alphabet else []
        }

        return jsonify(response), 200
    except Exception as e:
        return handle_exception(e)

@app.route('/bfhl', methods=['GET'])
def bfhl_get():
    # Expected GET response body
    return jsonify({"operation_code": 1}), 200

if _name_ == '_main_':
    app.run(debug=True)
