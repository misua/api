from flask import Flask, jsonify, request
from datetime import datetime, timedelta

app = Flask(__name__)

# Dictionary to store the last request timestamp for each IP address
request_timestamps = {}

default_limit = 2
default_window = 60


# Function to check if the rate limit for an IP address has been exceeded
def is_rate_limited(ip_address, limit=None, window=None):
    current_time = datetime.now()

    if ip_address not in request_timestamps:
        request_timestamps[ip_address] = {'timestamps': []}
        return False

    if limit is None:
        limit = default_limit
    if window is None:
        window = default_window

    # Remove timestamps that are outside the time window
    request_timestamps[ip_address]['timestamps'] = [t for t in request_timestamps[ip_address]['timestamps'] if current_time - t <= timedelta(seconds=window)]

    if len(request_timestamps[ip_address]['timestamps']) < limit:
        request_timestamps[ip_address]['timestamps'].append(current_time)
        return False
    else:
        return True


@app.route('/api/resource', methods=['GET'])
def get_resource():
    client_ip = request.remote_addr
    limit = request_timestamps.get(client_ip, {}).get('limit', default_limit)
    window = request_timestamps.get(client_ip, {}).get('window', default_window)

    if not is_rate_limited(client_ip, limit=limit, window=window):
        return jsonify(data="This is a rate-limited resource.")
    else:
        return jsonify(error="Rate limit exceeded."), 429


# create api endpoint to change limit value to a new one by just calling this endpoint with new limit value
@app.route('/api/limit', methods=['POST'])
def change_limit():
    client_ip = request.remote_addr
    new_limit = request.json.get('limit')
    new_window = request.json.get('window')

    if client_ip not in request_timestamps:
        request_timestamps[client_ip] = {'timestamps': []}

    if new_limit is not None and new_window is not None:
        request_timestamps[client_ip]['limit'] = new_limit
        request_timestamps[client_ip]['window'] = new_window
        request_timestamps[client_ip]['timestamps'] = []
        return jsonify(data="Rate limit has been changed.")
    else:
        return jsonify(error="Invalid request body."), 400


# curl -X POST -H "Content-Type: application/json" -d '{"limit": 5, "window": 120}' http://localhost:5000/api/limit

if __name__ == '__main__':
    app.run(debug=True)
