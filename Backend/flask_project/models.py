from flask_sqlalchemy import SQLAlchemy 
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
from flask import url_for

db = SQLAlchemy() 
class User(db.Model): 
    id = db.Column(db.Integer,primary_key = True) 
    user_name = db.Column(db.String(100),nullable = False) 
    email = db.Column(db.String(120),unique = True,nullable = False)
    is_verified = db.Column(db.Boolean,default = False) 
    password = db.Column(db.String(150),nullable = False)
    profile_image = db.Column(db.String(300))
    general_settings = db.relationship("GeneralSettings",backref ="user",uselist = False,lazy="select")
    theme_settings = db.relationship("ThemeSettings",backref = "user",uselist = False,lazy="select")
    passage_settings = db.relationship("CustomPassageSettings",backref="user",uselist = False,lazy="select") 
    reset_tokens = db.relationship("ResetToken",backref="user", lazy = "select")
    history = db.relationship("History",backref=db.backref("user",cascade="all,delete-orphan"),lazy="select")
    text_snippet = db.relationship("TextSnippets",backref=db.backref("user",cascade="all, delete-orphan"),lazy="select")
    custom_text = db.relationship("CustomTexts",backref=db.backref("user",cascade="all,delete-orphan"),lazy="select")

    def set_password(self, password):
         self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)


    def to_dic(self):
        return {
            "id":self.id,
            "userName":self.user_name,
            "profile_image":url_for("uploaded_file",filename=self.profile_image,_external=True) if self.profile_image else None,
            "email":self.email
        }



class GeneralSettings(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    duration = db.Column(db.Integer,default=60)    
    difficulty = db.Column(db.String(20), default="medium")
    auto_stat_text = db.Column(db.Boolean,default = False)
    enable_sound_effect = db.Column(db.Boolean,default = False)


class ThemeSettings(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    theme_mode = db.Column(db.String(20),default = "white")
    accent_color = db.Column(db.String(20),default = "blue")
    text_size = db.Column(db.String(30),default = "small")
    font_style = db.Column(db.String(30),default = "monospace")


class CustomPassageSettings(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable = False)
    passage = db.Column(db.String(300),nullable = False,default="Start typing here ...")
    title = db.Column(db.String(90),nullable = False,default="Untitled")

class ResetToken(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable = False)
    token = db.Column(db.String(300),nullable = False,unique=True)
    expires_at = db.Column(db.DateTime,nullable = False)
    used = db.Column(db.Boolean,default = False)

class History(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    wpm = db.Column(db.Float,nullable=False)
    accuracy = db.Column(db.Float,nullable=False)
    score = db.Column(db.Float,nullable=False)
    fixed_time = db.Column(db.Float,default=120.0)
    stopped_time = db.Column(db.Float,nullable=False)
    created_at = db.Column(db.DateTime,default = datetime.utcnow)
    completed = db.Column(db.Boolean,default=False)

    def to_diction(self):
        return {
            "profileImage":url_for("uploaded_file",filename=self.user.profile_image,_external=True) if self.user.profile_image else None,
            "userId":self.user_id,
            "wpm":self.wpm,
            "accuracy":self.accuracy,
            "score":self.score,
            "createdAt":self.created_at.isoformat(),
            "userName":self.user.user_name
        } 

class TextSnippets(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    difficulty = db.Column(db.String(15), default = "Medium")
   
    def to_john(self):
        return {
            "content":self.content, 
            "difficulty":self.difficulty
        }

class Duel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    player1_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    player2_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    text_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    start_time = db.Column(db.DateTime,nullable=False)
    end_time = db.Column(db.DateTime,nullable=False)
    winner_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    status = db.Column(db.String(20),default="Pending")

class CustomTexts(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    creator = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    title = db.Column(db.String(40),nullable = False)
    text_content = db.Column(db.String(500),nullable=False)
    difficulty = db.Column(db.String(10),default="Medium",nullable=False)
    created_at = db.Column(db.DateTime,default=datetime.utcnow)

    def to_shark(self):
        return {
            "user":self.user.user_name,
            "content":self.text_content,
            "difficulty":self.difficulty,
            "createdAt":self.created_at.isoformat()
        } 

