from flask_sqlalchemy import SQLAlchemy 
from werkzeug.security import generate_password_hash,check_password_hash


db = SQLAlchemy() 
class User(db.Model): 
    id = db.Column(db.Integer,primary_key = True) 
    user_name = db.Column(db.String(100),nullable = False) 
    email = db.Column(db.String(120),unique = True,nullable = False) 
    password = db.Column(db.String(150),nullable = False)
    profile_image = db.Column(db.String(300))
    
    general_settings = db.relationship("GeneralSettings",backref ="user",uselist = False)
    theme_settings = db.relationship("ThemeSettings",backref = "user",uselist = False)

    def set_password(self, password):
         self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)


    def to_dic(self):
        return {
            "id":self.id,
            "userName":self.user_name,
            "profile_image":self.profile_image,
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


