from flask import Flask, jsonify, render_template

app = Flask(__name__)

variable_value = "Initial Value"

@app.route('/')
def ajax_testing():
    return render_template('ajax_testing.html', variable_value=variable_value)

@app.route('/update_variable', methods=['GET'])
def update_variable():
    global variable_value
    new_value = "Updated Value" if variable_value == "Initial Value" else "Initial Value"
    variable_value = new_value
    return jsonify({"new_value": new_value})

if __name__ == '__main__':
    app.run(debug=True)
