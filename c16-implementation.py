from flask import Flask, request, jsonify
import math

app = Flask(__name__)

# In-memory storage for noisy data (in production, you'd use a database or queue)
click_data = []

# Differential privacy parameters
EPSILON = 1.0  # You can lower this for more privacy (e.g., 0.5)
prob = math.exp(EPSILON) / (math.exp(EPSILON) + 1)

@app.route('/submit', methods=['POST'])
def submit():
    """Receives noisy click data from the client"""
    data = request.get_json()
    if 'click' in data:
        click_data.append(int(data['click']))
        return jsonify({"status": "received"}), 200
    return jsonify({"error": "missing 'click' key"}), 400

@app.route('/report', methods=['GET'])
def report():
    """Estimates the true click count using inverse randomized response"""
    n = len(click_data)
    if n == 0:
        return jsonify({"users": 0, "estimated_clicks": 0})

    noisy_sum = sum(click_data)
    est_true_count = (noisy_sum - n * (1 - prob)) / (2 * prob - 1)

    return jsonify({
        "users": n,
        "estimated_clicks": round(est_true_count),
        "epsilon": EPSILON
    })

if __name__ == '__main__':
    app.run(debug=True)
