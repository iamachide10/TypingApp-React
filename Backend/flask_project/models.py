from flask_sqlalchemy import SQLAlchemy 
from werkzeug.security import generate_password_hash,check_password_hash


db = SQLAlchemy() 
class User(db.Model): 
    id = db.Column(db.Integer,primary_key = True) 
    user_name = db.Column(db.String(100),nullable = False) 
    email = db.Column(db.String(120),unique = True,nullable = False)
    is_verified = db.Column(db.Boolean,default = False) 
    password = db.Column(db.String(150),nullable = False)
    profile_image = db.Column(db.String(300))
    general_settings = db.relationship("GeneralSettings",backref ="user",uselist = False,lazy=True)
    theme_settings = db.relationship("ThemeSettings",backref = "user",uselist = False,lazy=True)
    passage_settings = db.relationship("CustomPassageSettings",backref="user",uselist = False,lazy=True) 
    reset_tokens = db.relationship("ResetToken",backref="user", lazy = True)
    last_verification_sent=db.Column(db.DateTime, nullable=True)

    def set_password(self, password):
         self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)


    def to_dic(self):
        return {
            "user_id":self.id,
            "userName":self.user_name,
            "profile_image":self.profile_image,
            "email":self.email,
            "Verified":self.is_verified,
            "last_verification_sent":self.last_verification_sent    
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
            "user_id":self.user_id,
            "duration":self.duration,
            "difficulty":self.difficulty,
            "auto_stat_text":self.auto_stat_text,
            "enable_sound_effect":self.enable_sound_effect,
            "test_mode":self.test_mode
        }


class ThemeSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    theme_mode = db.Column(db.String(20), default="white")
    accent_color = db.Column(db.String(20), default="blue")
    text_size = db.Column(db.String(30), default="small")
    font_style = db.Column(db.String(30), default="monospace")

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "theme_mode": self.theme_mode,
            "accent_color": self.accent_color,
            "text_size": self.text_size,
            "font_style": self.font_style,
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
