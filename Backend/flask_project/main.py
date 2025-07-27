from flask import Flask,request,jsonify,Blueprint 
from flask_cors import CORS 
from config import Config
from models import User,db
from werkzeug.utils import secure_filename
import os
import uuid

app = Flask(__name__)

CORS(app)
app.config.from_object(Config)
db.init_app(app) 
settings_bp = Blueprint("settings",__name__)  



@settings_bp.route("/settings/<int:user_id>",methods=["POST"]) 
def settings(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"Message":"User not found"})
    data = request.get_json()
    general_data = data.get("generalSettings",{})
    if user.general_settings:
        general = user.general_settings
    else:
        general = GeneralSettings(user_id=user_id)
        db.session.add(general)
    #for general settings
    general.duration = general_data.get("duration",general.duration)
    general.difficulty = general_data.get("difficulty",general.difficulty)
    general.auto_stat_text = general_data.get("auto_stat_text",general.auto_stat_text)
    general.enable_sound_effect = general_data.get("enable_sound_effect",general.enable_sound_effect)
    ##for theme
    data = request.get_json()
    theme_data = data.get("themeSettings",{})
    if user.theme_settings:
        theme = user.theme_settings
    else:
        theme = themeSettings(user_id=user_id)
        db.session.add(theme)
    
    general.theme_mode = general_data.get("theme_mode",general.theme_mode)
    general.accent_color = general_data.get("accent_color",general.accent_color)
    general.text_size  = general_data.get("text_size",general.text_size )
    general.font_style = general_data.get("font_style",general.font_style)
    db.session.commit()
    return jsonify({"Message":"Settings updated successfully"}),200

@app.route("/sign_in",methods=["POST"]) 
def register():
    name_user = request.form.get("name")  
    user_email = request.form.get("email") 
    password = request.form.get("password") 
    photo = request.files.get("profile_image")

    if not name_user or not user_email or not password:
        return jsonify({"Message":"Must include name,password and email"}),400
    new_user=User(user_name = name_user,email = user_email,password = password) 
    if photo:
        nice_name = secure_filename(photo.filename)
        com = os.path.splitext(nice_name)
        unique_name = f"{uuid.uuid4().hex} {com}"
        os.makedirs(app.config["UPLOAD_FOLDER"],exist_ok = True)
        save_path = os.path.join(app.config["UPLOAD_FOLDER"],unique_name) 
        photo.save(save_path) 

        new_user.profile_image=unique_name
    new_user.set_password(password)
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message":"User created successfully"}),200
    except Exception as e:
        return jsonify({"Message":str(e)}),400    



@app.route("/")
def display_users():
    pupils = User.query.all()
    if not pupils:
        return jsonify({"Message":"Couldn't get users"}),400
    pupils_json = [pupil.to_dic() for pupil in pupils] 
    return jsonify({"users":pupils_json})



@app.route("/login",methods=["POST"])
def log_user():
    user_email = request.json.get("email")
    user_password = request.json.get("password")
    if not user_email or not user_password:
        return jsonify({"Message":"Email and password required"}),400
    user_login = User.query.filter_by(email=user_email).first()
    if user_login and user_login.check_password(user_password):
        return jsonify({"message":"User login successful","credentials":{"name":user_login.user_name,"email":user_login.email ,"user_id":user_login.id}}),200
    else:
        return jsonify({"Message":"invalid email and password"}),400  

app.register_blueprint(settings_bp)
if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
