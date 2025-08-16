from flask import Flask,request,jsonify
from flask_cors import CORS 
from config import Config
from models import User,GeneralSettings,ThemeSettings,db,CustomPassageSettings
from werkzeug.utils import secure_filename
import os
import uuid
from flask_jwt_extended import JWTManager,create_access_token,create_refresh_token,set_access_cookies,set_refresh_cookies,jwt_required,get_jwt_identity,unset_jwt_cookies,decode_token
from datetime import timedelta
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail,Email,To,Content
from PIL import Image
import secrets
from datetime import datetime

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db.init_app(app)
jwt = JWTManager(app)

def send_emails(recipient,subject,body):
    sg = SendGridAPIClient(api_key=app.config["SENDGRID_API_KEY"])
    from_email = Email(app.config["FROM_EMAIL"],app.config["FROM_NAME"])
    to_email = To(recipient)
    content = Content("text/plain",body)
    mail = Mail(from_email,to_email,subject,content)
    try:
       response = sg.send(mail)
       return response.status_code
    except Exception as e:
       print(f"Error sending email:{e}")
       return None 

@app.route("/refresh-token",methods = ["POST"])
@jwt_required()
def refresh_access_token():
    current_user = get_jwt_identity()
    if not current_user:
        return jsonify({"message":"something went wrong"})
    new_access_token = create_access_token(identity = current_user.id)
    new_refresh_token = create_refresh_token(identity = current_user.id)
    response = jsonify({"message":"Token refreshed successfully"})
    set_access_cookies(response,new_access_token)
    set_refresh_cookies(response,new_refresh_token)
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
    return jsonify({"message":"General settings updated successfully"}),200

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

def save_profile_picture(file,upload_folder,preferred_format="JPEG"):
    try:
       img = Image.open(file)
       img.verify()

       file.seek(0)
       img = Image.open(file).convert("RGB")

       filename = f"{uuid.uuid4().hex}.{preferred_format.lower()}"
       os.makedirs(app.config["UPLOAD_FOLDER"],exist_ok=True)
       save_path = os.path.join(upload_folder,filename)
       
       img.save(save_path,preferred_format)
       return filename
    except Exception as e:
        print(f"error saving profile_pic:{e}")
        return None

@app.route("/sign-in",methods=["POST"]) 
def register():
    name_user = request.form.get("name")  
    user_email = request.form.get("email") 
    password = request.form.get("password") 
    photo = request.files.get("profile_image")

    if not name_user or not user_email or not password:
        return jsonify({"Message":"Must include name,password and email"}),400
    existing_user = User.query.filter_by(email=user_email).first()
    if existing_user and not existing_user.is_verified:
        token = create_access_token(identity=existing_user.id)
        subject = "Please verify your email"
        body = f"Please click on this link to verify your email.\n\t{host_url}verify-email?token={token}"
        status = send_emails(existing_user.email,subject,body)
        if status == None:
            return jsonify({"Message":"Something happened"}),500
        else:
            return jsonify({"Message":"A link has been sent to your inbox, click it to verify your email"}),202
    elif existing_user and existing_user.is_verified:
        return jsonify({"Message":"User already verified"}),202
    else:
        new_user = User(email = user_email,name=name_user) 
        if photo:
            profile = save_profile_picture(photo,app.config["UPLOAD_FOLDER"])
            if profile == None:
                return jsonify({"Message":"Something happened"}),500
            else:
                new_user.profile_image = profile
        new_user.set_password(password)
        try:
            db.session.add(new_user)
            db.session.commit()
            token = create_access_token(identity=new_user.id)
            subject= "Please verify your email"
            body = f"Please click on this link to verify your email.\n\t{host_url}verify-email?token={token}"
            check = send_emails(new_user.email,subject,body)
            if check == None:
                return jsonify({"Message":"Something happened when trying to send email"}),500
            else:
                return jsonify({"Message":"User created successfully,please verify your email"}),201
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
        return jsonify({"message":"Email and password required"}),400
    user_login = User.query.filter_by(email=user_email).first()
    
    if user_login and user_login.check_password(user_password):
        if user_login.is_verified:
            access_token = create_access_token(identity=user_login.id)
            refresh_token = create_refresh_token(identity=user_login.id)
            response = jsonify({"message":"User login successfully"})
            set_access_cookies(response,access_token)
            set_refresh_cookies(response,refresh_token)
            return response
        else:
            token = create_access_token(identity=user_login.id)
            subject = "Verify your email"
            body = f"Please click on this link to verify your email.\n\n{request.host_url}verify-email?token={token}"
            status = send_emails(user_login.email,subject,body)
            if status == 202:
                return jsonify({"message":"A link has been sent into your inbox, kindly click on it and verify your email"})
            else:
                return jsonify({"message":"Something happened, couldn't send the email"})
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
    else:
        token = create_access_token(identity=person.id)
        subject = "Please verify your email"
        body = f"Please click on this link to verify your email.\n{request.host_url}verify-email?token={token}"
        status = send_emails(person.email,subject,body)
        if status == 202:
            return jsonify({"Message":"verification resend again"}),200
        else:
            return jsonofy({"Message":"Something happened")

@app.route("/forgot-password",methods = ["POST"])
def forgot_password():
    email = request.json.get("email")
    if not email:
        return jsonify({"message":"Email required"}),400
    check_user = User.query.filter_by(email = email).first()
    if check_user:
        reset_token = secrets.token_urlsafe(32)
        expiry_time = datetime.utcnow() + timedelta(minutes=15)
        reset_entry = ResetToken(user_id=check_user.id,expires_at=expiry_time)
        hashed_token = set_password(reset_token)
        reset_entry.token = hashed_token
        db.session.add(reset_entry)
        db.session.commit()
        subject = "Reset your password if you want to"
        body = f"if you want to reset your password,click on this link.\n\t{request.host_url}reset-password?token={reset_token}"
        status = send_emails(check_user.email,subject,body)
        if status != 202:
            return jsonify({"message":"Couldn't send email"})
    	return jsonify({"message":"if an account with that email exist, we've sent a reset link"})

@app.route("/reset-password",methods = ["POST"])
def new_password():
    token = request.args.get("token")
    if not token:
        return jsonify({"message":"Invalid request"}),400
    verify = ResetToken.query.filter_by(token = token).first()
    if not verify:
        return jsonify({"message":"Invalid or non-existent token"}),404
    if verify.used:
        return jsonify({"message":"This token has already been used"}),400
    if verify.expires_at < datetime.utcnow():
        return jsonify({"message":"This token has expired"}),400
        
    data = request.get_json()
    new_password = data.get("password",None)
    if not new_password:
        return jsonify({"Message":"Must type in new passw2ord"}),400
    if len(new_password) < 8:
        return jsonify({"Message":"Password must have at least 8 characters"}),400
    if not any(c.isupper() for c in new_password):
        return jsonify({"Message":"Must include at least one capital letter"}),400
    if not any(c.islower() for c in new_password):
        return jsonify({"Message":"Must have at least a small letter"}),400
    if not any(c.isdigit() for c in new_password):
        return jsonify({"Message":"Must have at least a digit"}),400
    verify.user.set_password(new_password)
    db.session.commit()
    return jsonify({"Message":"Password reset successfully"}),200

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

