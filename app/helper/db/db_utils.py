from app import db
from flask import current_app
import traceback

def save_to_db(model_instance):
    """
    Save a model instance to the database with error handling.
    
    Args:
        model_instance: SQLAlchemy model instance to save
        
    Returns:
        tuple: (success, result, error_message)
            - success (bool): Whether the operation was successful
            - result: The saved model instance if successful, None otherwise
            - error_message (str): Error message if unsuccessful, None otherwise
    """
    try:
        db.session.add(model_instance)
        db.session.commit()
        return True, model_instance, None
    except Exception as e:
        db.session.rollback()
        error_message = f"Database error: {str(e)}"
        current_app.logger.error(f"{error_message}\n{traceback.format_exc()}")
        return False, None, error_message

def get_by_id(model_class, id):
    """
    Get a model instance by ID with error handling.
    
    Args:
        model_class: SQLAlchemy model class
        id: ID of the instance to retrieve
        
    Returns:
        tuple: (success, result, error_message)
            - success (bool): Whether the operation was successful
            - result: The model instance if successful, None otherwise
            - error_message (str): Error message if unsuccessful, None otherwise
    """
    try:
        result = model_class.query.get(id)
        if result:
            return True, result, None
        else:
            return False, None, f"{model_class.__name__} with ID {id} not found"
    except Exception as e:
        error_message = f"Database error: {str(e)}"
        current_app.logger.error(f"{error_message}\n{traceback.format_exc()}")
        return False, None, error_message

def delete_from_db(model_instance):
    """
    Delete a model instance from the database with error handling.
    
    Args:
        model_instance: SQLAlchemy model instance to delete
        
    Returns:
        tuple: (success, error_message)
            - success (bool): Whether the operation was successful
            - error_message (str): Error message if unsuccessful, None otherwise
    """
    try:
        db.session.delete(model_instance)
        db.session.commit()
        return True, None
    except Exception as e:
        db.session.rollback()
        error_message = f"Database error: {str(e)}"
        current_app.logger.error(f"{error_message}\n{traceback.format_exc()}")
        return False, error_message 