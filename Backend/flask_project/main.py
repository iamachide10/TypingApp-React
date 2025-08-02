from flask import Flask,request,jsonify
from flask_cors import CORS 
from config import Config
from models import User,GeneralSettings,ThemeSettings,db,CustomPassageSettings
from werkzeug.utils import secure_filename
import os
import uuid
from flask_jwt_extended import JWTManager,create_access_token,create_refresh_token,set_access_cookies,set_refresh_cookies,jwt_required,get_jwt_identity,unset_jwt_cookies,decode_token
from datetime import timedelta
from flask_mail import Mail,Message

app = Flask(__name__)
CORS(app)
mail = Mail()
app.config.from_object(Config)
db.init_app(app)
mail.init_app(app)
jwt = JWTManager(app)

@app.route("/refresh-token",methods = ["POST"])
@jwt_required(refresh = True)
def refresh_access_token():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity = current_user)
    response = jsonify({"message":"Token refreshed successfully"})
    set_access_cookies(response,new_access_token)
    return response

@app.route("/general-settings",methods=["POST"])
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

def send_verification_email(user):
    token = create_access_token(identity=user.id,expires_delta = timedelta(minutes=15))
    verify_url = f"http://localhost:5000/verify_email?token={token}"
    msg = Message(
        subject = "Verify your email",sender = app.config["MAIL_DEFAULT_SENDER"],recipients=[user.email],body=f"Click this link to verify your email:{verify_url}"
    )
    mail.send(msg)

@app.route("/custom-passage-settings",methods=["POST"])
@jwt_required()
def passage_settings():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"Message":"User not found"}),404
    data = request.get_json()
    verify = data.get("passageSettings",{})
    if user.passage_settings:
        settings  = user.passage_settings
    else:
        settings = CustomPassageSettings(user_id = user.id)
        db.session.add(settings)

    settings.passage = verify.get("passage",settings.passage)
    settings.title = verify.get("title",settings.title)
    db.session.commit()

    return jsonify({"Message":"Passage settings updated successfullu"}),200

@app.route("/theme-settings",methods = ["POST"])
@jwt_required()
def theme_settings():
    verify = get_jwt_identity()
    person = User.query.get(verify)
    if not person:
        return jsonify({"Message":"User not found"})
    data = request.get_json()
    theme_data = data.get("themeSettings",{})
    if person.theme_settings:
        theme = person.theme_settings
    else:
        theme = ThemeSettings(user_id=verify)
        db.session.add(theme)

    theme.theme_mode = theme_data.get("themeMode",theme.theme_mode)
    theme.accent_color = theme_data.get("accentColor",theme.accent_color)
    theme.text_size = theme_data.get("textSize",theme.text_size)
    theme.font_style = theme_data.get("fontStyle",theme.font_style)

    db.session.commit()
    return jsonify({"Message":"Theme settings updated successfully"}),200

@app.route("/sign-in",methods=["POST"]) 
def register():
    name_user = request.form.get("name")  
    user_email = request.form.get("email") 
    password = request.form.get("password") 
    photo = request.files.get("profile_image")

    if not name_user or not user_email or not password:
        return jsonify({"Message":"Must include name,password and email"}),400
    new_user=User(user_name = name_user,email = user_email) 
    if new_user.is_verified:
        return jsonify({"Message":"User already verified"})
    if photo:
        nice_name = secure_filename(photo.filename)
        com = os.path.splitext(nice_name)[1]
        unique_name = f"{uuid.uuid4().hex}{com}"
        os.makedirs(app.config["UPLOAD_FOLDER"],exist_ok = True)
        save_path = os.path.join(app.config["UPLOAD_FOLDER"],unique_name) 
        photo.save(save_path) 

        new_user.profile_image=unique_name
    new_user.set_password(password)
    try:
        db.session.add(new_user)
        db.session.commit()
        send_verification_email(new_user)
        return jsonify({"message":"User created successfully.Please verify your email."}),201
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
    if not user_login or not user_login.check_password(user_password):
        return jsonify({"Message":"Invalid email or password"})

    if user_login:
        if not user_login.is_verified:
            return jsonify({"Message":"Email not verified.Please check your inbox or request a new verification link.","Resend":True}),403
        access_tokens = create_access_token(identity=user_login.id)
        refresh_tokens = create_refresh_token(identity = user_login.id)
        response = jsonify({"message":"User login successful","credentials":{"name":user_login.user_name,"email":user_login.email ,"user_id":user_login.id}})
        set_access_cookies(response,access_tokens)
        set_refresh_cookies(response,refresh_tokens)
        return response,200
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

@app.route("/verify-email",methods=["GET"])
def verify_new():
    token = request.args.get("token")
    if not token:
        return jsonify({"Message":"Verification token is missing"}),404
    try:
        decoded = decode_token(token)
        user_id = decoded["sub"]
        
        new_user = User.query.get(user_id)
        if not new_user:
            return jsonify({"Message":"User not found"})
        if new_user.is_verified:
            return jsonify({"Message":"Email already verified"}) ,200
        
        new_user.is_verified = True
        db.session.commit()
        
        return jsonify({"Message":"Email verified successfully"})
    except Exception as e:
        return jsonify({"Message":str(e)}),400  

@app.route("/resend-verification",methods=["POST"])
@jwt_required()
def new_verification():
    user_id = get_jwt_identity()
    person = User.query.get(user_id)
    if not person:
        return jsonify({"Message":"User not found"}),404
    if person.is_verified:
        return jsonify({"Message":"User already verified"}),400
    send_verification_email(person)
    return jsonify({"Message":"Verification email resent successfully"}),200

@app.route("/forgot-password",methods = ["POST"])
def forgot_password():
    email = request.json.get("email")
    if not email:
        return jsonify({"Message":"Email not found"}),404
    check_user = User.query.filter_by(email = email).first()
    if not check_user:
        return jsonify({"Message":"Invalid email"})
    new_token = create_access_token(identity = check_user.id)
    reset_link = f"http://localhost:3000/reset_password?token={new_token}"
    msg = Message(
        subject = "Reset your password",
        sender = app.config["MAIL_DEFAULT_SENDER"],
        recipients = [check_user.email],
        body = f"Click on this link to reset your password:\n{reset_link}"
    )
    mail.send(msg)
    return jsonify({"Message":"Reset link sent to email"}),200

@app.route("/reset-password",methods = ["POST"])
def new_password():
    token = request.args.get("token")
    try:
        decoded = decode_token(token)
        user_id = decoded["sub"]
    except Exception as e:
        return jsonify({"Message":str(e)}),500
    check = User.query.get(user_id)
    if not check:
        return jsonify({"Message":"User not found"}),404
    data = request.get_json()
    new_password = data.get("password")
    if not new_password:
        return jsonify({"Message":"Must type in new password"}),404
    if len(new_password) < 8:
        return jsonify({"Message":"Password must have at least 8 characters"})
    if not any(c.isupper() for c in new_password):
        return jsonify({"Message":"Must include at least one capital letter"})
    if not any(c.islower() for c in new_password):
        return jsonify({"Message":"Must have at least a small letter"})
    if not any(c.isdigit() for c in new_password):
        return jsonify({"Message":"Must have at least a digit"})
    check.set_password(new_password)
    db.session.commit()
    return jsonify({"Message":"Password reset successfully"}),200

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

