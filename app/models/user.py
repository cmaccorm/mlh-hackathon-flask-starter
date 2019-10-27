from app.extensions import db
from app.services.github import GitHub
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'
        
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    avatar_url = db.Column(db.String(80), nullable=True)
    github_id = db.Column(db.Integer(), nullable=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    
    def __init__(self, username, avatar_url, github_id):
        self.username = username
        self.avatar_url = avatar_url
        self.github_id = github_id
    
    @staticmethod
    def find_or_create_from_token(access_token):
        data = GitHub.get_user_from_token(access_token)
    
        """Find existing user or create new User instance"""
        instance = User.query.filter_by(username=data['login']).first()
    
        if not instance:
            instance = User(data['login'], data['avatar_url'], data['id'])
            db.session.add(instance)
            db.session.commit()

        return instance
    
    def __repr__(self):
        return "<User: {}>".format(self.username)

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    Event = db.Column(db.Text)
    Location = db.Column(db.Text)
    Date = db.Column(db.Text)
    Cap = db.Column(db.Text)
    Description = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
