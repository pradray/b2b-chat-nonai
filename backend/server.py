"""
B2B Chat - Flask Server with Security Improvements
===================================================
Changes made:
1. Rate limiting (Security - MEDIUM)
2. Restricted CORS origins (Security - HIGH)
3. Security headers middleware (Security - LOW)
4. Request logging middleware (Architecture)
5. Error handling middleware (Architecture)
"""

from flask import Flask, request, jsonify
from lambda_function import lambda_handler
from flask_cors import CORS
from functools import wraps
import logging
import time

# ============================================
# APP CONFIGURATION
# ============================================

app = Flask(__name__)

# Security: Restricted CORS (not wildcard)
CORS(app, origins=[
    'http://localhost:5173',
    'http://127.0.0.1:5173',
    'http://localhost:3000'
])

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================
# RATE LIMITING (Simple In-Memory Implementation)
# ============================================

class RateLimiter:
    """
    Simple rate limiter using in-memory storage.
    For production, use Redis-based solution.
    """
    def __init__(self, requests_per_minute=30):
        self.requests_per_minute = requests_per_minute
        self.clients = {}  # {ip: [timestamps]}
    
    def is_allowed(self, client_ip):
        current_time = time.time()
        minute_ago = current_time - 60
        
        # Initialize or get client's request history
        if client_ip not in self.clients:
            self.clients[client_ip] = []
        
        # Remove old timestamps (older than 1 minute)
        self.clients[client_ip] = [
            ts for ts in self.clients[client_ip] 
            if ts > minute_ago
        ]
        
        # Check if under limit
        if len(self.clients[client_ip]) >= self.requests_per_minute:
            return False
        
        # Add current request timestamp
        self.clients[client_ip].append(current_time)
        return True
    
    def get_remaining(self, client_ip):
        if client_ip not in self.clients:
            return self.requests_per_minute
        return max(0, self.requests_per_minute - len(self.clients[client_ip]))


# Initialize rate limiter (30 requests per minute per IP)
rate_limiter = RateLimiter(requests_per_minute=30)


# ============================================
# MIDDLEWARE DECORATORS
# ============================================

def rate_limit(f):
    """
    Middleware: Rate limiting decorator.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        client_ip = request.remote_addr or 'unknown'
        
        if not rate_limiter.is_allowed(client_ip):
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            return jsonify({
                "error": "Rate limit exceeded. Please wait before sending more messages.",
                "retry_after": 60
            }), 429
        
        return f(*args, **kwargs)
    return decorated_function


def log_request(f):
    """
    Middleware: Request logging decorator.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        client_ip = request.remote_addr or 'unknown'
        
        logger.info(f"REQUEST: {request.method} {request.path} from {client_ip}")
        
        response = f(*args, **kwargs)
        
        duration = (time.time() - start_time) * 1000  # ms
        logger.info(f"RESPONSE: {request.path} completed in {duration:.2f}ms")
        
        return response
    return decorated_function


def handle_errors(f):
    """
    Middleware: Error handling decorator.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"ERROR: {str(e)}", exc_info=True)
            return jsonify({
                "error": "An internal error occurred. Please try again.",
                "message": "Contact admin for advanced queries."
            }), 500
    return decorated_function


# ============================================
# SECURITY HEADERS (Applied to all responses)
# ============================================

@app.after_request
def add_security_headers(response):
    """
    Add security headers to all responses.
    """
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate'
    return response


# ============================================
# ROUTES
# ============================================

@app.route('/chat', methods=['POST'])
@log_request
@rate_limit
@handle_errors
def chat():
    """
    Main chat endpoint.
    """
    # Validate content type
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400
    
    # Build event for lambda handler
    event = {
        'body': request.json,
        'headers': dict(request.headers)
    }
    
    # Process through lambda handler
    lambda_response = lambda_handler(event, None)
    
    # Return response
    return lambda_response['body'], lambda_response['statusCode']


@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for monitoring.
    """
    return jsonify({
        "status": "healthy",
        "service": "b2b-chat-backend",
        "version": "2.0.0"
    }), 200


@app.route('/chat/status', methods=['GET'])
def rate_limit_status():
    """
    Check rate limit status for current client.
    """
    client_ip = request.remote_addr or 'unknown'
    remaining = rate_limiter.get_remaining(client_ip)
    
    return jsonify({
        "requests_remaining": remaining,
        "limit_per_minute": rate_limiter.requests_per_minute
    }), 200


# ============================================
# MAIN
# ============================================

if __name__ == '__main__':
    print("=" * 50)
    print("B2B Chat Backend Server v2.0")
    print("=" * 50)
    print("Security features enabled:")
    print("  ✓ Rate limiting (30 req/min)")
    print("  ✓ CORS restricted to localhost")
    print("  ✓ Security headers")
    print("  ✓ Request logging")
    print("  ✓ Error handling")
    print("=" * 50)
    print("Running on http://127.0.0.1:5000")
    print("=" * 50)
    
    app.run(port=5000, debug=False)
