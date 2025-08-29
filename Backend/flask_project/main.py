from flask import Flask,request,jsonify,send_from_directory
from flask_cors import CORS 
from config import Config
from models import User,GeneralSettings,ThemeSettings,db,CustomPassageSettings
from werkzeug.utils import secure_filename
import os
import uuid
from flask_jwt_extended import JWTManager,create_access_token,create_refresh_token,set_access_cookies,set_refresh_cookies,jwt_required,get_jwt_identity,unset_jwt_cookies,decode_token
from datetime import timedelta
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail,Email,To,Content, TrackingSettings, ClickTracking
from PIL import Image
import secrets
from datetime import datetime, timedelta, timezone


app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
app.config["UPLOADS"] ="shark/uploads" 
db.init_app(app)
jwt = JWTManager(app)

def save_profile_picture(file,upload_folder,preferred_format='JPEG'):
    try:
        img =Image.open(file)
        img.verify()
        file.seek(0)
        image=Image.open(file).convert('RGB')
        filename=f'{uuid.uuid4().hex}.{preferred_format.lower()}'
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        save_path = os.path.join(upload_folder,filename)
        image.save(save_path)
        return filename
    except Exception as e:
        print(f'error saving profile_pic:{e}')
        return None

def send_emails(recipient, subject, body):
    sg = SendGridAPIClient(api_key=app.config["SENDGRID_API_KEY"])
    from_email = Email(app.config["FROM_EMAIL"], app.config["FROM_NAME"])
    print(f"DEBUG subject: {subject} ({type(subject)})")

    
    mail = Mail(
        from_email=from_email,
        to_emails=recipient,
        subject=subject
    )
    mail.add_content(Content("text/plain", body))  # ✅ Properly add plain text

    # Disable click tracking properly
    tracking_settings = TrackingSettings()
    tracking_settings.click_tracking = ClickTracking(enable=False, enable_text=False)
    mail.tracking_settings = tracking_settings
    try:
        response = sg.send(mail)
        return response.status_code
    except Exception as e:
        print(f"Error sending email: {e}")
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






@app.route("/general-settings/<int:user_id>",methods=["POST"])
#@jwt_required() 
def general_settings(user_id):
    #user_id = get_jwt_identity()
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
    general.test_mode = general_data.get("test_mode",general.test_mode)
    print(general.to_dic())  
    db.session.commit()
    return jsonify({"message":"General settings updated successfully", "settings":general.to_dic()}),200


@app.route("/general-settings/<int:user_id>", methods=["GET"])
# @jwt_required()
def get_general_settings(user_id):
    # user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"Message": "User not found"}), 404
    if not user.general_settings:
        return jsonify({"Message": "No general settings found"}), 404
    return jsonify(user.general_settings.to_dic()), 200


@app.route("/custom-passage-settings/<int:user_id>",methods=["POST"])
#@jwt_required()
def passage_settings(user_id):
    #user_id = get_jwt_identity()
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

    return jsonify({"message":"Passage settings updated successfullu"}),200



@app.route("/theme-settings/<int:user_id>", methods=["POST"])
##@jwt_required()
def theme_settings(user_id):
    #verify = get_jwt_identity()
    person = User.query.get(user_id)

    if not person:
        return jsonify({"Message": "User not found"}), 404

    data = request.get_json()
    theme_data = data.get("themeSettings", {})

    # check if user already has theme settings
    if person.theme_settings:
        theme = person.theme_settings
    else:
        theme = ThemeSettings(user_id=verify)
        db.session.add(theme)

    # update theme settings
    theme.theme_mode = theme_data.get("theme_mode", theme.theme_mode)
    theme.accent_color = theme_data.get("accent_color", theme.accent_color)
    theme.text_size = theme_data.get("text_size", theme.text_size)
    theme.font_style = theme_data.get("font_style", theme.font_style)

    print(theme.to_dict())  # for debugging

    db.session.commit()

    return jsonify({
        "message": "Theme settings updated successfully",
        "settings": theme.to_dict()
    }), 200










@app.route("/sign_in", methods=["POST"]) 
def register():
    name_user = request.form.get("name")  
    user_email = request.form.get("email") 
    password = request.form.get("password") 
    photo = request.files.get("profile_image")

    if not name_user or not user_email or not password:
        return jsonify({"message":"Must include name, password and email"}), 400

    # <-- This was unreachable before
    existing_user = User.query.filter_by(email=user_email).first()
   
    if existing_user and  existing_user.is_verified:
            return jsonify({"message": "User already exists"}), 202

    elif existing_user and not existing_user.is_verified:
            token = create_access_token(identity=str(existing_user.id))
            subject = "Please verify your email"
            body = f"Please click this link to verify your email:\n\nhttp://localhost:5000/verify-email?token={token}"
            status = send_emails(recipient=existing_user.email,subject=subject,body=body)
            if status == None:
                return jsonify({"message":"Something happened"}),500
            else:
                return jsonify({"message":"A link has been sent to your inbox, click it to verify your email"}),202
    else:
        new_user = User(email=user_email, user_name=name_user)

        if photo:
            profile = save_profile_picture(photo, app.config["UPLOAD_FOLDER"])
            if profile is None:
                return jsonify({"message": "Something happened"}), 500
            new_user.profile_image = profile

        new_user.set_password(password)

        try:
            db.session.add(new_user)
            db.session.commit()
            token = create_access_token(identity=new_user.id)
            subject= "Please verify your email"
            body = f"Please click this link to verify yoursssss email:\n\nhttp://localhost:5000/verify-email?token={token}"
            check = send_emails(new_user.email,subject,body)
            if check == None:
                return jsonify({"message":"Something happened when trying to send email"}),500
            else:
                return jsonify({"message":"User created successfully,please verify your email", "credentials":new_user.to_dic()}),201
        except Exception as e:
            return jsonify({"message":str(e)}),400    

        except Exception as e:
            return jsonify({"message": str(e)}), 400







@app.route("/")
def display_users():
    pupils = User.query.all()
    if not pupils:
        return jsonify({"Message":"Couldn't get users"}),400
    pupils_json = [pupil.to_dic() for pupil in pupils] 
    return jsonify({"users":pupils_json})






@app.route("/login", methods=["POST"])
def log_user():
    user_email = request.json.get("email")
    user_password = request.json.get("password")

    if not user_email or not user_password:
        return jsonify({"message": "Email and password required"}), 400

    user_email = user_email.lower()
    user_login = User.query.filter_by(email=user_email).first()

    if not user_login:
        return jsonify({"message": "User not found"}), 401

    # ✅ Check password
    if not user_login.check_password(user_password):
        return jsonify({"message": "Invalid email or password"}), 401

    # ✅ If verified → issue tokens
    if user_login.is_verified:
        access_token = create_access_token(identity=user_login.id)
        refresh_token = create_refresh_token(identity=user_login.id)
        return jsonify({
            "message": "User login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "credentials": user_login.to_dic(),
        }), 200

    # 🚫 If not verified → re-send verification link (avoid spamming)
    now = datetime.now(timezone.utc)

    if (not user_login.last_verification_sent) or  ((now - user_login.last_verification_sent).total_seconds() > 300):  
        token = create_access_token(
            identity=user_login.id,
            expires_delta=timedelta(hours=1)   # ⏳ 1 hour expiry for verification link
        )
        subject = "Verify your email"
        body = f"Please click this link to verify your email:\n\n{request.host_url}verify-email?token={token}"
        status = send_emails(user_login.email, subject, body)

        if status == 202:
            # store the time when the last verification email was sent
            user_login.last_verification_sent = now
            db.session.commit()

            return jsonify({"message": "Verification email sent. Please check your inbox."}), 403
        else:
            return jsonify({"message": "Something went wrong, couldn't send the verification email"}), 500
    else:
        return jsonify({"message": "Verification email already sent recently. Please check your inbox."}), 403



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
        user_id = int(decoded["sub"])

        
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
            return jsonofy({"Message":"Something happened"})

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


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOADS'], filename)


if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

