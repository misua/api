from flask import Flask, jsonify, request
from datetime import datetime, timedelta

app = Flask(__name__)

# Dictionary to store the last request timestamp for each IP address
request_timestamps = {}


# Function to check if the rate limit for an IP address has been exceeded
def is_rate_limited(ip_address, limit=2, window=60):
    current_time = datetime.now()
    
    if ip_address not in request_timestamps:
        request_timestamps[ip_address] = [current_time]
        return False

    # Remove timestamps that are outside the time window
    request_timestamps[ip_address] = [t for t in request_timestamps[ip_address] if current_time - t <= timedelta(seconds=window)]

    if len(request_timestamps[ip_address]) < limit:
        request_timestamps[ip_address].append(current_time)
        return False
    else:
        return True


# Sample API endpoint with rate limit applied
@app.route('/api/resource', methods=['GET'])
def get_resource():
    client_ip = request.remote_addr
    
    if not is_rate_limited(client_ip):
        return jsonify(data="This is a rate-limited resource.")
    else:
        return jsonify(error="Rate limit exceeded."), 429


if __name__ == '__main__':
    app.run(debug=True)
