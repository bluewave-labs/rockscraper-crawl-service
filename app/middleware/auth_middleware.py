from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from flask_jwt_extended.exceptions import JWTExtendedException
from jwt.exceptions import DecodeError, InvalidSignatureError, InvalidTokenError
import logging
from datetime import datetime, UTC

logger = logging.getLogger(__name__)

def verify_jwt(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # Verify JWT token
            verify_jwt_in_request()
            
            # Get user identity and claims
            user_id = get_jwt_identity()
            claims = get_jwt()
            
            # Log the claims for debugging
            logger.debug(f"JWT Claims: {claims}")
            
            # Get roles for Uptime
            roles = [
                role['role_name'] 
                for role in claims.get('roles', []) 
                if role.get('team_name') == 'UPTIME'
            ]
            
            # Add user data to request context
            request.user = {
                **claims,
                'roles': roles
            }
            
            # Add user_id to kwargs
            kwargs['user_id'] = user_id

            # Log successful authentication
            logger.info(f"User {user_id} authenticated successfully at {datetime.now(UTC)}")
            
            return f(*args, **kwargs)
            
        except (JWTExtendedException, DecodeError, InvalidSignatureError, InvalidTokenError) as e:
            logger.error(f"JWT validation error: {str(e)}")
            return jsonify({
                'error': 'Authentication error',
                'message': 'Invalid or expired token'
            }), 401
            
        except Exception as e:
            logger.error(f"Unexpected error during authentication: {str(e)}")
            return jsonify({
                'error': 'Authentication error',
                'message': 'An unexpected error occurred during authentication'
            }), 500
            
    return decorated_function 