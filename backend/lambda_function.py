"""
B2B Chat - Lambda Function with Security & Architecture Improvements
=====================================================================
Changes made:
1. Input sanitization (Security - HIGH)
2. Restricted CORS origins (Security - HIGH)
3. Service layer abstraction (Architecture)
4. Logging middleware (Architecture)
5. JSON validation (Security - LOW)
"""

import json
import re
import logging
from datetime import datetime
from IntentService import IntentService
from ResponseService import ResponseService
from knowledgebase import INTENT_MAP, RESPONSE_MAP, FALLBACK_RESPONSE

# ============================================
# CONFIGURATION
# ============================================

# Logging setup (Architecture: Middleware Layer)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Security: Allowed origins (replace wildcard CORS)
ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
    'http://localhost:3000',
    # More production origins can be added here or loaded from environment variables
    # 'https://yourdomain.com'
]

# Security: Input constraints
MAX_MESSAGE_LENGTH = 500
MIN_MESSAGE_LENGTH = 1

# NLU: Confidence threshold for intent matching
CONFIDENCE_THRESHOLD = 75

# ============================================
# SECURITY LAYER
# ============================================

def sanitize_input(text):
    """
    Security: Sanitize user input to prevent injection attacks.
    - Validates input type
    - Removes control characters
    - Limits length
    - Strips whitespace
    """
    if not isinstance(text, str):
        logger.warning(f"Invalid input type: {type(text)}")
        return ''
    
    # Remove control characters (ASCII 0-31 and 127-159)
    cleaned = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
    
    # Remove potential script tags (basic XSS prevention)
    cleaned = re.sub(r'<[^>]*>', '', cleaned)
    
    # Limit length and strip whitespace
    cleaned = cleaned[:MAX_MESSAGE_LENGTH].strip()
    
    return cleaned


def validate_request_body(body):
    """
    Security: Validate JSON request structure.
    Returns (is_valid, error_message)
    """
    if not isinstance(body, dict):
        return False, "Invalid request format"
    
    if 'message' not in body:
        return False, "Missing 'message' field"
    
    message = body.get('message', '')
    if not isinstance(message, str):
        return False, "Message must be a string"
    
    if len(message) < MIN_MESSAGE_LENGTH:
        return False, "Message cannot be empty"
    
    if len(message) > MAX_MESSAGE_LENGTH:
        return False, f"Message exceeds {MAX_MESSAGE_LENGTH} characters"
    
    return True, None


def get_cors_origin(event):
    """
    Security: Return allowed CORS origin instead of wildcard.
    """
    headers = event.get('headers', {}) or {}
    origin = headers.get('origin', '') or headers.get('Origin', '')
    
    if origin in ALLOWED_ORIGINS:
        return origin
    
    # Default to first allowed origin for local development
    return ALLOWED_ORIGINS[0]


# Initialize services
intent_service = IntentService(INTENT_MAP)
response_service = ResponseService(RESPONSE_MAP, FALLBACK_RESPONSE)


# ============================================
# MAIN HANDLER
# ============================================

def lambda_handler(event, context):
    """
    Main entry point for chat requests.
    """
    request_id = datetime.now().strftime("%Y%m%d%H%M%S%f")
    logger.info(f"[{request_id}] New request received")
    
    # Parse request body
    body = event.get('body', {})
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except json.JSONDecodeError as e:
            logger.error(f"[{request_id}] JSON parse error: {e}")
            return build_response(
                {"error": "Invalid JSON format"},
                400,
                event
            )
    
    # Validate request
    is_valid, error_msg = validate_request_body(body)
    if not is_valid:
        logger.warning(f"[{request_id}] Validation failed: {error_msg}")
        return build_response(
            {"error": error_msg},
            400,
            event
        )
    
    # Sanitize input
    raw_text = body.get('message', '')
    user_text = sanitize_input(raw_text)
    
    if not user_text:
        logger.warning(f"[{request_id}] Empty message after sanitization")
        return build_response(
            {"message": "Please enter a valid message.", "action": None},
            200,
            event
        )
    
    logger.info(f"[{request_id}] Processing: '{user_text[:50]}...'")
    
    # Detect intent
    intent, confidence = intent_service.detect_intent(user_text)
    logger.info(f"[{request_id}] Intent: {intent}, Confidence: {confidence}")
    
    # Generate response
    response_data = response_service.get_response(intent)
    
    result = {
        "message": response_data["msg"],
        "action": response_data["act"],
        "debug": {
            "intent": intent,
            "confidence": confidence,
            "request_id": request_id
        }
    }
    
    logger.info(f"[{request_id}] Response sent: intent={intent}")
    
    return build_response(result, 200, event)


def build_response(body, status_code, event):
    """
    Build HTTP response with security headers.
    """
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': get_cors_origin(event),
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST',
            'Access-Control-Allow-Credentials': 'true',
            # Security headers
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block'
        },
        'body': json.dumps(body)
    }
