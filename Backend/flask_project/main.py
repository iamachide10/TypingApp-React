from flask import Flask,request,jsonify,send_from_directory,url_for
from flask_cors import CORS 
from config import Config
from models import User,GeneralSettings,ThemeSettings,db,CustomPassageSettings,History,ResetToken
from werkzeug.utils import secure_filename
import os,logging,time
import uuid,secrets,random
from flask_jwt_extended import JWTManager,create_access_token,create_refresh_token,set_access_cookies,set_refresh_cookies,jwt_required,get_jwt_identity,unset_jwt_cookies,decode_token
from datetime import timedelta ,UTC,timezone
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail,Email,To,Content, TrackingSettings, ClickTracking,From
from PIL import Image
import secrets
from datetime import datetime
from logging.handlers import RotatingFileHandler







app = Flask(__name__)

CORS(app, resources={
    r"/*": {"origins": ["http://localhost:3000", "https://typingapp-mastery.onrender.com"]}
}, supports_credentials=True)

app.config.from_object(Config)
app.config["UPLOADS"] ="shark/uploads" 
db.init_app(app)
jwt = JWTManager(app)
os.makedirs("logs",exist_ok=True)
handler = RotatingFileHandler("logs/app.log",maxBytes=1_000_000,backupCount=3)
handler.setLevel(logging.WARNING)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
handler.setFormatter(formatter)
os.makedirs("logs",exist_ok=True)
app.logger.addHandler(handler)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
app.logger.addHandler(console_handler)


def save_profile_picture(file,upload_folder,preferred_format='JPEG'):
    try:
        img =Image.open(file)
        img.verify()
        file.seek(0)
        image=Image.open(file).convert('RGB')
        filename=f'{uuid.uuid4().hex}.{preferred_format.lower()}'
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        save_path = os.path.join(upload_folder,filename)
        image.save(save_path,format="JPEG")
        return filename
    except (UnidentifiedImageError,OSError) as e:
        app.logger.error(f"Error: {e}")
        print(f'error saving profile_pic:{e}')
        return None

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, From, To, Content, TrackingSettings, ClickTracking

def send_emails(recipient, subject, body):
    sg = SendGridAPIClient(api_key=app.config["SENDGRID_API_KEY"])

    # Make sure subject is always a string
    if not isinstance(subject, str):
        subject = str(subject)

    from_email = From(app.config["FROM_EMAIL"], app.config["FROM_NAME"])

    print(f"✅ DEBUG subject: {subject} ({type(subject)})")

    mail = Mail(
        from_email=from_email,
        to_emails=To(recipient),
        subject=subject
    )
    mail.add_content(Content("text/plain", str(body)))  # force body to string

    tracking_settings = TrackingSettings()
    tracking_settings.click_tracking = ClickTracking(enable=False, enable_text=False)
    mail.tracking_settings = tracking_settings

    try:
        response = sg.send(mail)
        print(f"📨 Email sent, status code: {response.status_code}")
        return response.status_code
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return None



@app.route("/refresh-token",methods = ["POST"])
def refresh_access_token():
    get_token = request.cookies.get("my_refresh_cookie")
    if not get_token:
        return jsonify({"message":"Couldn't get token"})
    try:
        decoded_token = decode_token(get_token)
        get_id = decoded_token.get("sub")
        expire_time = decoded_token.get("exp")
        get_type = decoded_token.get("type")
    except Exception as e:
        app.logger.error(f"Error: {e}")
        return jsonify({"message":"Invalid or corrupted token"})
    if get_type != "refresh":
        return jsonify({"message":"Only refresh tokens are allowed to this route"})
    current_user = User.query.filter_by(id=get_id).first()
    if not current_user:
        return jsonify({"message":"Can't find user"})
    current_time = int(time.time())
    if current_time > expire_time:
        return jsonify({"message":"Token has expired"})
    new_access_token = create_access_token(identity = current_user.id)
    new_refresh_token = create_refresh_token(identity = current_user.id)
    response = jsonify({"message":"Token refreshed successfully"})
    set_access_cookies(response,new_access_token)
    set_refresh_cookies(response,new_refresh_token)
    return response






@app.route("/general-settings",methods=["POST"])
@jwt_required() 
def general_settings(user_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"Message":"User not found"})
    data = request.get_json()
    general_data = data.get("generalSettings")
    if general_data == None:
        return jsonify({"message":"Couldn't get general settings"})
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


@app.route("/general-settings", methods=["GET"])
@jwt_required()
def get_general_settings():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"Message": "User not found"}), 404
    if not user.general_settings:
        return jsonify({"Message": "No general settings found"}), 404
    return jsonify(user.general_settings.to_dic()), 200




# @app.route("/general-settings/<int:user_id>", methods=["GET"])
# # @jwt_required()
# def get_general_settings(user_id):
#     # user_id = get_jwt_identity()
#     user = User.query.get(user_id)
#     if not user:
#         return jsonify({"Message": "User not found"}), 404
#     if not user.general_settings:
#         return jsonify({"Message": "No general settings found"}), 404
#     return jsonify(user.general_settings.to_dic()), 200


@app.route("/custom-passage-settings",methods=["POST"])
@jwt_required()
def passage_settings(user_id):
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

    return jsonify({"message":"Passage settings updated successfullu"}),200



@app.route("/theme-setting", methods=["POST"])
@jwt_required()
def theme_settings(user_id):
    verify = get_jwt_identity()
    person = User.query.get(user_id)
    if not person:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()
    theme_data = data.get("themeSettings", {})
    # check if user already has theme settings
    if person.theme_settings:
        theme = person.theme_settings
    else:
        theme = ThemeSettings(user_id=verify)
        db.session.add(theme)

    # update theme settings
    theme.theme = theme_data.get("theme", theme.theme )
    theme.accentColor = theme_data.get("accent_color", theme.accentColor )
    theme.textSize = theme_data.get("text_size", theme.textSize)
    theme.font = theme_data.get("font_style", theme.font)
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

   
    existing_user = User.query.filter_by(email=user_email).first()
   
    if existing_user and  existing_user.is_verified:
        return jsonify({"message": "User already exists"}), 202

    elif existing_user and not existing_user.is_verified:
        return jsonify({"message":"please click on resend verification below to resend verification email"}) 
    else:
        new_user = User(email=user_email, user_name=name_user)

        if photo:
            profile = save_profile_picture(photo, app.config["UPLOAD_FOLDER"])
            if profile == None:
                return jsonify({"message": "Something happened"}), 500
            new_user.profile_image = profile

        new_user.hash(password)
        try:
            db.session.add(new_user)
            db.session.flush()
            token = secrets.token_urlsafe(32)
            expired_time = datetime.now(UTC)+ timedelta(minutes=15)
            reset_token = ResetToken(user_id=new_user.id,expires_at = expired_time)
            reset_token.set_password(token)
            db.session.add(reset_token)
            db.session.commit()
            subject= "Please verify your email"
            link = f"https://typingapp-mastery.onrender.com/verify-email/{token}"
            body = f"Please click on this link to verify your email.\n\t{link}"
            print(body)
            check = send_emails(new_user.email,subject,body)
            if check == None:
                return jsonify({"message":"Something happened when trying to send email"}),500
            return jsonify({"message":"User created successfully,please verify your email", "credentials":new_user.to_dic() }),201
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error: {e}")
            return jsonify({"message":f"Something went wrong {e}"}),400





@app.route("/")
def display_users():
    get_users = User.query.all()
    if not get_users:
        return jsonify({"message":"Couldn't get users"})
    every_user = [user.to_dic() for user in get_users]
    return jsonify({"Users":every_user})


@app.route("/login", methods=["POST"])
def log_user():
    data = request.get_json()
    user_email = data.get("email")
    user_password = data.get("password")

    if not user_email or not user_password:
        return jsonify({
            "success": False,
            "message": "Email and password required"
        }), 400

    user_login = User.query.filter_by(email=user_email).first()
    if not user_login:
        return jsonify({
            "success": False,
            "message": "User not found"
        }), 401

    if not user_login.check_password(user_password):
        return jsonify({
            "success": False,
            "message": "Invalid email or password"
        }), 401

    # ✅ User exists & password is correct
    print("DEBUG:", user_login.email, "verified:", user_login.is_verified)
    print("Password check:", user_login.check_password(user_password))

    if user_login.is_verified:
        try:
            access_token = create_access_token(identity=str(user_login.id))
            refresh_token = create_refresh_token(identity=str(user_login.id))


            response = jsonify({
                "success": True,
                "message": "User login successful",
                "data": user_login.to_dic()
            })
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)
            return response, 200
        except Exception as e:
            app.logger.error(f"Login error: {e}")
            return jsonify({
                "success": False,
            "message": f"Something went wrong during login  {str(e)}"
            }), 500

    # ✅ User not verified → send verification email
    try:
        token = secrets.token_urlsafe(32)
        expiration_time = datetime.utcnow() + timedelta(minutes=15)

        reset_token = ResetToken(
            user_id=user_login.id,
            expires_at=expiration_time
        )
        reset_token.set_password(token)
        db.session.add(reset_token)
        db.session.commit()

        subject = "Verify your email"
        link = f"https://typingapp-mastery.onrender.com/verify-email/{token}"
        body = f"Please click this link to verify your email:\n{link}"

        status = send_emails(user_login.email, subject, body)

        if status == 202:
            return jsonify({
                "success": False,
                "message": "A verification link has been sent to your inbox"
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "Something went wrong, couldn't send the email"
            }), 500

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error sending verification email: {e}")
        return jsonify({
            "success": False,
            "message": "Something went wrong"
        }), 500



@app.route("/logout",methods = ["POST"])
@jwt_required()
def log_out():
    check = int(get_jwt_identity())
    verify = User.query.filter_by(id=check).first()
    if not verify:
        return jsonify({"Message":"Couldn't find user"}),404
    response = jsonify({"Message":"User logged out successfully"})
    unset_jwt_cookies(response)
    return response




@app.route("/verify-email",methods=["GET"])
def verify_new():
    token = request.args.get("token")
    print(token)
    if not token:
        return jsonify({"Message":"Verification token is missing"}),400
    existence = None
    bring_all = ResetToken.query.filter_by(used=False).all()
    for reset in bring_all:
        if reset.check_passwords(token):
            existence = reset
            print(f"This is the token {existence}")
            break
    if existence is None:
        return jsonify({"message":"Token is invalid"})
    if existence.expires_at < datetime.utcnow():
        return jsonify({"message":"Token has expired"})
    if existence.used:
        return jsonify({"message":"Token is used already"})
    user_check = User.query.filter_by(id=existence.user_id).first()
    if not user_check:
        return jsonify({"Message":"User not found"})
    if user_check.is_verified:
        return jsonify({"Message":"Email already verified"}),200
    try:
        user_check.is_verified = True
        db.session.commit()
        return jsonify({"Message":"Email verified successfully"})
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error: {e}")
        return jsonify({"Message":"Something happened"}),400  





@app.route("/resend-verification",methods=["GET"])
def new_verification():
    get_token = request.args.get("token")
    if not get_token:
        return jsonify({"message":"Couldn't get token"})
    check_exist = None
    bring_all = ResetToken.query.all()
    for reset in bring_all:
        if check_password(get_token,reset.token):
            check_exist = reset
            break
    if check_exist is None:
        return jsonify({"message":"Invalid token"})
    if check_exist.expires_at < datetime.now(UTC):
        return jsonify({"message":"Token has expired"})
    if check_exist.used:
        return jsonify({"message":"Invalid or used token"})
    verify = User.query.filter_by(id=check_exist.user_id).first()
    if not verify:
        return jsonify({"message":"User not found"})
    try:
        new_token = secrets.token_urlsafe(32)
        hashed_token = set_password(new_token)
        expires_time = datetime.now(UTC) + timedelta(minutes=15)
        reset_token = ResetToken(user_id=verify.id,token=hashed_token,expires_at=expires_time)
        db.session.add(reset_token)
        db.session.delete(check_exist)
        db.session.commit()
        subject = "Please verify your email"
        body = f"Click on this link to verify your email.\n\n{request.host_url}verify-email?token={new_token}"
        status = send_emails(verify.id,subject,body)
        if status == None:
            return jsonify({"message":"Something happened when trying to send email"})
        else:
            return jsonify({"message":"we've sent a verification email to your inbox"})
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Erro: {e}")
        return jsonify({"message":"Something went wrong"})



@app.route("/forgot-password",methods = ["POST"])
def forgot_password():
    email = request.json.get("email")
    if not email:
        return jsonify({"message":"Email required"}),400
    check_user = User.query.filter_by(email = email).first()
    if check_user:
        try:
            reset_token = secrets.token_urlsafe(32)
            expiry_time = datetime.utcnow() + timedelta(minutes=15)
            reset_entry = ResetToken(user_id=check_user.id,expires_at=expiry_time)
            reset_entry.set_password(reset_token)
          
            db.session.add(reset_entry)
            db.session.commit()
            subject = "Reset your password if you want to"
            link = f"https://typingapp-mastery.onrender.com/reset-password/{reset_token}"
            body = f"if you want to reset your password,click on this link.\n\t{link}"

            status = send_emails(check_user.email,subject,body)
            if status is None:
                return jsonify({"message":"Couldn't send email"})
            return jsonify({"message":"if an account with that email exist, we've sent a reset link"})
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error: {e}")
            return jsonify({"message":"Something went wrong"}) 
    else:
        return jsonify({"message":"if this email exists, a reset link has been sent"})




@app.route("/reset-password", methods=["POST"])
def new_password():
    token = request.args.get("token")
    if not token:
        return jsonify({"message": "Invalid request"}), 400

    verify = ResetToken.query.filter_by(used=False).all()
    existence = None
    for each in verify:
        if each.check_passwords(token):
            existence = each
            break

    if not existence:
        return jsonify({"message": "Invalid or non-existent token"}), 404

    if existence.used:
        return jsonify({"message": "This token has already been used"}), 400

    # --- FIX: handle naive vs aware datetime safely ---
    expires_at = existence.expires_at
    if expires_at.tzinfo is None:  # old value = naive
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at < datetime.now(timezone.utc):
        return jsonify({"message": "This token has expired"}), 400

    check = User.query.filter_by(id=existence.user_id).first()
    if not check:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()
    new_password = data.get("password", check.password)

    if not new_password:
        return jsonify({"Message": "Must type in new password"}), 400

    try:
        print(new_password)
        check.hash(new_password)
        db.session.delete(existence)  # remove token after use
        db.session.commit()
        return jsonify({"message": "Password reset successfully"}), 200
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error: {e}")
        return jsonify({"message": "Something went wrong"}), 500


@app.route("/history",methods=["POST"])
@jwt_required()
def history(retrieve_id):
    retrieve_id = get_jwt_identity()
    if not retrieve_id:
        return jsonify({"message":"Invalid or corrupted token"})
    check = User.query.filter_by(id=retrieve_id).first()
    if not check:
        return jsonify({"message":"User not found"})
    data = request.get_json()
    print(data)
    words_per_min = data.get("wpm")
    accuracy = data.get("accuracy")
    score = data.get("score")


    if words_per_min is None or accuracy is None  or score is None:       
         return jsonify({"message":"Must include all necessary details"})
    try:
        new_data = History(user_id=retrieve_id,wpm=words_per_min,accuracy=accuracy, score = score)
        db.session.add(new_data)
        db.session.commit()
        return jsonify({"message":"User scores saved successfully"})
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error saving history for {check.id}:  {e}")
        return jsonify({"message":f"An error occurred when trying to save user scores {e}"}),500

@app.route("/leaderboard",methods=["GET"])
def leaderboard():
    best_scores = History.query.order_by(History.score.desc()).all()
    if not best_scores:
        return jsonify({"message":"Couldn't get scores"})
    best_per_user = {}
    for entry in best_scores:
        if entry.user_id not in best_per_user:
            best_per_user[entry.user_id]=entry
    leaderboard = [entry.to_diction() for entry in best_per_user.values()][:50]
    return jsonify({"leaderboard":leaderboard})
    print(leaderboard)



@app.route("/progress-tracking",methods=["GET"])
@jwt_required()
def progress():
    get_id = get_jwt_identity()
    if not get_id:
        return jsonify({"message":"Invalid or expired token"})
    verify = User.query.filter_by(id=get_id).first()
    if not verify:
        return jsonify({"message":"User not found"})
    bring = History.query.filter_by(user_id=verify.id,completed=True).order_by(History.created_at.asc()).all()
    if not bring:
        return jsonify({"sessions":[]})
    try:
        conversion = [each.to_diction() for each in bring]
        scores = [sessions["score"] for sessions in conversion]
        wpms = [sessions["wpm"] for sessions in conversion]
        accuracies = [sessions["accuracy"] for sessions in conversion]

        best_score = max(scores) if scores else 0
        best_wpm = max(wpms) if wpms else 0
        best_accuracy = max(accuracies) if accuracies else 0

        average_score = sum(scores)/len(scores) if scores else 0
        average_wpm = sum(wpms)/len(wpms) if wpms else 0
        average_accuracy = sum(accuracies)/len(accuracies) if accuracies else 0
 
        return jsonify({"sessions":conversion,"bestScore":best_score,"bestWpm":best_wpm,"bestAccuracy":best_accuracy,"averageScore":average_score,"averageWpm":average_wpm,"averageAccuracy":average_accuracy})
    except Exception as e:
        app.logger.error(f"Error:{e}")
        return jsonify({"message":"Something went wrong while processing progress data"}),500

@app.route("/custom-texts",methods=["POST"])
@jwt_required()
def custom():
    get_id = get_jwt_identity()
    if not get_id:
        return jsonify({"message":"Invalid or expired token"})
    verify = User.query.filter_by(id=get_id).first()
    if not verify:
        return jsonify({"message":"User not found"})
    data = request.get_json()
    title = data.get("title")
    difficulty = data.get("difficulty","Medium")
    text = data.get("textContent")
    if not title or not text:
        return jsonify({"message":"Must include title and text content"}) 
    try:
        new_data = CustomTexts(creator=verify.id,title=title,difficulty=difficulty,text_content=text)
        db.session.add(new_data)
        db.session.commit()
        return jsonify({"message":f"{verify.user_name}, your custom texts is successfully"})
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error: {e}")
        return jsonify({"message":"Something went wrong while trying to save custom texts"})

@app.route("/custom-texts",methods=["GET"])
@jwt_required()
def fetch_custom():
    get_id = get_jwt_identity()
    if not get_id:
        return jsonify({"message":"Invalid or expired token"})
    verify = User.query.filter_by(id=get_id).first()
    if not verify:
        return jsonify({"message":"User not found"})
    get_content = CustomTexts.query.filter_by(creator=verify.id).order_by(CustomTexts.created_at.desc()).all()
    if not get_content:
        return jsonify({"message":[ ]})
    else:
        conversion = [content.to_shark() for content in get_content]
        return jsonify({"customTexts":conversion})

@app.route("/random-texts",methods=["GET"])
@jwt_required()
def random_texts():
    get_id = get_jwt_identity()
    if not get_id:
        return jsonify({"message":"Invalid or expired token"})
    check = User.query.filter_by(id=get_id).first()
    if not check:
        return jsonify({"message":"User not found"})
    data = request.args.get("difficulty")
    if not data:
        return jsonify({"message":"Must include the difficulty"})
    try:
        texts = TextSnippets.query.filter_by(difficulty=data).all()
        if not texts:
            return jsonify({"message":"Didn't find such difficulty"})
        random_text = random.choice(texts)
        return jsonify({"randomText":random_text.to_john()})
    except Exception as e:
        app.logger.error(f"Error: {e}")
        return jsonify({"message":"Error occurred when trying to get texts"})


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOADS'], filename)

@app.route("/tokens")
def tokens():
    all_tokens = ResetToken.query.all()
    if not all_tokens:
        return jsonify({"message":"No tokens found"})
    conversion = [token.to_dict() for token in all_tokens]
    return jsonify({"tokens":conversion})



@app.route("/updates",methods=["PATCH"])
@jwt_required()
def change_name(retrieve_id):
    retrieve_id = get_jwt_identity()
    verify = User.query.get(retrieve_id)
    if not verify:
        return jsonify({"message":"Invalid or expired token"})
    updated_fields = []
    messages = []
    user_name = request.form.get("name")
    profile = request.files.get("image")
    if user_name:
        verify.user_name = user_name
        response = "User name is updated successfully"
        updated_fields.append(verify.user_name)
        messages.append(response)
    if profile:
        old_filename = verify.profile_image
        file_path = os.path.join(app.config["UPLOAD_FOLDER"],old_filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        status = save_profile_picture(profile,app.config["UPLOAD_FOLDER"])
        if status is None:
            return jsonify({"message":"Please upload a real image"})
        else:
            verify.profile_image = status
            updated_fields.append(verify.profile_image)
            responses = "Profile image updated successfully"
            messages.append(responses)
    try:
        db.session.commit()
        return jsonify({"messages":messages,"name": verify.user_name if verify.user_name else None, "profilePic":url_for("uploaded_file",filename=verify.profile_image,_external=True) if verify.profile_image else None})
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error: {e}")
        return jsonify({"message":"Oops, an error occurred"})
    

@app.route("/history")
def get_history():
    histories = History.query.all()
    return jsonify({"history": [history.to_diction() for history in histories]})
 
if __name__=="__main__":
    with app.app_context():
        db.create_all()
        print("✅ Database tables created/verified")
        print("Tables in DB:", db.metadata.tables.keys())  #
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port= port   ,debug=False)
 


