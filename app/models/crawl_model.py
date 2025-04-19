from datetime import datetime
import json
from app import db

class Crawls(db.Model):
    __tablename__ = 'crawls'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(2048), nullable=False)
    markdown = db.Column(db.Text)
    extracted_content = db.Column(db.Text)
    html = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)
   
    def __repr__(self):
        return f'<Crawl {self.id}: {self.url}>'

    def to_dict(self):
        # Parse JSON strings back to dictionaries if they exist
        extracted_content_data = json.loads(self.extracted_content) if self.extracted_content else None
        
        return {
            'id': self.id,
            'user_id': self.user_id,
            'url': self.url,
            'markdown': self.markdown,
            'extracted_content': extracted_content_data,
            'html': self.html,
            'date': self.date.isoformat() if self.date else None
        } 
    @classmethod
    def from_dict(cls, data):
        """
        Create a new Crawls instance from a dictionary.
        
        Args:
            data (dict): Dictionary containing crawl data
            
        Returns:
            Crawls: New Crawls instance
        """
        # Convert date string to datetime if provided
        if 'date' in data and data['date']:
            try:
                data['date'] = datetime.fromisoformat(data['date'])
            except (ValueError, TypeError):
                data['date'] = None

        # Filter out any keys that aren't model attributes
        valid_fields = {column.key for column in cls.__table__.columns}
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}
        
        return cls(**filtered_data) 