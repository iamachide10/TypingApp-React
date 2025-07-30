from flask import Flask,request,jsonify
from flask_cors import CORS 
from config import Config
from models import User,db
from werkzeug.utils import secure_filename
import os
import uuid
from flask_jwt_extended import JWTManager,create_access_token,create_refresh_token,set_access_cookies,set_refresh_cookies,jwt_required,get_jwt_identity,unset_jwt_cookies

app = Flask(__name__)

CORS(app)
app.config.from_object(Config)
db.init_app(app)   
jwt = JWTManager(app)

@app.route("/refresh/token",methods = ["POST"])
@jwt_required(refresh = True)
def refresh_access_token():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity = current_user)
    response = jsonify({"message":"Token refreshed successfully"})
    set_access_cookies(response,new_access_token)
    return response

@app.route("/general_settings",methods=["POST"])
@jwt_required() 
def general_settings():
    user_id = get_jwt_identity()
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
   
    db.session.commit()
    return jsonify({"Message":"General settings updated successfully"}),200

@app.route("/theme_settings",methods = ["POST"])
@jwt_required()
def theme_settings():
    verify = get_jwt_identity()
    person = User.query.get(verify)
    if not verify:
        return jsonify({"Message":"User not found"})
    data = request.get_json()
    theme_data = data.get("themeSettings",{})
    if person.theme_settings:
        theme = person.theme_settings
    else:
        theme = ThemeSettings(user_id=verify)
        db.session.add(theme)

    theme.theme_mode = data.get("themeMode",theme.theme_mode)
    theme.accent_color = data.get("accentColor",theme.accent_color)
    theme.text_size = data.get("textSize",theme.text_size)
    theme.font_style = data.get("fontStyle",theme.font_style)

    db.session.commit()
    return jsonify({"Message":"Theme settings updated successfully"}),200
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
        com = os.path.splitext(nice_name)[1]
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
        access_tokens = create_access_token(identity=user_login.id)
        refresh_tokens = create_refresh_token(identity = user_login.id)
        
        response = jsonify({"message":"User login successful","credentials":{"name":user_login.user_name,"email":user_login.email ,"user_id":user_login.id}}),200
        set_access_cookies(response,access_tokens)
        set_refresh_cookies(response,refresh_tokens)
        return response
    else:
        return jsonify({"Message":"invalid email and password"}),401  

@app.route("/logout",methods = ["POST"])
@jwt_required()
def log_out():
    check = get_jwt_identity()
    verify = User.query.get(check)
    if not verify:
        return jsonify({"Message":"Something happened"}),404
    response = jsonify({"Message":"User logged out successfully"}),200
    unset_jwt_cookies(response)
    return response

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
