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
    history = db.relationship("History", back_populates="user", lazy="select", cascade="all, delete-orphan")
    custom_text = db.relationship("CustomTexts", back_populates="user", lazy="select", cascade="all, delete-orphan")

    
    def hash(self, password):
         self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)


    def to_dic(self):
        return {
            "user_id":self.id,
            "userName":self.user_name,
            "profile_image":url_for("uploaded_file",filename=self.profile_image,_external=True) if self.profile_image else None,
            "email":self.email,
            "is_verified":self.is_verified
        }



class GeneralSettings(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    duration = db.Column(db.Integer,default=60)    
    difficulty = db.Column(db.String(20), default="medium")
    auto_stat_text = db.Column(db.Boolean,default = False)
    enable_sound_effect = db.Column(db.Boolean,default = False)
    test_mode = db.Column(db.String(20) ,default = "words")

    def to_dic(self):
        return {
            "duration": self.duration,
            "difficulty": self.difficulty,
            "auto_start_text": self.auto_stat_text,
            "enable_sound_effect": self.enable_sound_effect,
            "test_mode": self.test_mode,
        }



class ThemeSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    theme = db.Column(db.String(20), default="white")
    accentColor = db.Column(db.String(20), default="blue")
    textSize = db.Column(db.String(30), default="small")
    fontStyle = db.Column(db.String(30), default="monospace")

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "theme": self.theme_mode,
            "accentColor": self.accent_color,
            "textSize": self.text_size,
            "fontStyle": self.font_style,
        }


 


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

    def set_password(self, new_token):
        self.token = generate_password_hash(new_token)

    def to_dict(self):
        return {
            "user_id":self.user_id,
            "token":self.token,
            "expires_at":self.expires_at.isoformat(),
            "used":self.used
        }


    def check_passwords(self,password):
        return check_password_hash(self.token, password)
class History(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    wpm = db.Column(db.Float,nullable=False)
    accuracy = db.Column(db.Float,nullable=False)
    score = db.Column(db.Float,nullable=False)
    user = db.relationship("User", back_populates="history")

    def to_diction(self):
        return {
            "profileImage":url_for("uploaded_file",filename=self.user.profile_image,_external=True) if self.user.profile_image else None,
            "userId":self.user_id,
            "wpm":self.wpm,
            "accuracy":self.accuracy,
            "score":self.score,
            "userName":self.user.user_name
        } 



class TextSnippets(db.Model):
    id = db.Column(db.Integer,primary_key=True)
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
    user = db.relationship("User", back_populates="custom_text")

    def to_shark(self):
        return {
            "user":self.user.user_name,
            "content":self.text_content,
            "difficulty":self.difficulty,
            "createdAt":self.created_at.isoformat()
        } 

