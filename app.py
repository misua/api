# create a flask rest api that accepts connections but implements ratelimits

from flask import Flask, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# Initialize Flask-Limiter with default rate limit settings
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["5 per minute", "1 per second"]
)

# Sample API endpoint with rate limit applied

@app.route('/api/resource', methods=['GET'])
@limiter.limit("2 per minute") # Custom rate limit for this endpoint
def get_resource():
    return jsonify(data="This is a rate-limited resource.")

# add an endpoint that can change the default_limits
@app.route('/api/change_limit', methods=['GET'])
def change_limit():

    new_limits = request.json.get('limits')

    if new_limits:
        limiter._limiters.clear()
        limiter._load_limits(new_limits)
        return jsonify(data="The default rate limits have been changed.")
    else:
        return jsonify(error="invalid request body."), 400


if __name__ == '__main__':
    app.run(debug=True)


#curl -X POST -H "Content-Type: application/json" -d '{"limits": {"3 per minute": "0.5 per second"}}' http://localhost:5000/api/update-limits
#pipenv shell
