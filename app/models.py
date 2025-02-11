from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # Coordinated Universal Time (always save it to this time when storing, and convert it later on front end)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    # this creates relationship between the many table that has the foreign key
    # db.relationship('Method', backref='name'--references user_id, always lazy)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Save the password as the hashed version of the password
        self.set_password(kwargs['password'])
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<User {self.id} | {self.username}>"

    
    def check_password(self, password):
        return check_password_hash(self.password, password)

    
    def set_password(self, password):
        self.password = generate_password_hash(password)



@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)




class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    body = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # lowercase 'user' because that is the name of the table, user.id because id is the column
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # SQL Equivalent = FOREIGN KEY(user_id) REFERENCES user(id)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()


    def __repr__(self):
        return f"<Post {self.id} | {self.title}>"

    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key in {'title', 'body'}:
                setattr(self, key, value)
        db.session.commit()


    def delete(self):
        db.session.delete(self)
        db.session.commit()