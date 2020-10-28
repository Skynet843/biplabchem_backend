from sqlalchemy import null, desc
from flask import jsonify, make_response, request, session, url_for, redirect
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
import os
#test
file_path = os.path.abspath(os.getcwd()) + "/biplabchem.db"
path = os.path.abspath(os.getcwd())
UPLOAD_FOLDER = path + "/static/upload"
# create Flask APP And Do Configuration
app = Flask(__name__)

# end of flask app configuration
# Get config parameter
file = open('config.json', 'r')
params = json.loads(file.read())['params']
file.close()
# end Get config parameter
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# configure database
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + file_path
app.secret_key = "3m*a*KpWRFfG"
db = SQLAlchemy()
db.init_app(app)


# end configure database

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    bio = db.Column(db.String(500), nullable=False)
    full_bio = db.Column(db.String(5000), nullable=False)
    facebook = db.Column(db.String(500), nullable=True)
    linkdin = db.Column(db.String(500), nullable=True)
    twitter = db.Column(db.String(500), nullable=True)
    instragram = db.Column(db.String(500), nullable=True)
    phone_no = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(500), nullable=True)


class Details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_part = db.Column(db.String(100), nullable=False)
    second_part = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), unique=False)


class Gallery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pic_link = db.Column(db.String(100), unique=False, nullable=False)
    file_name = db.Column(db.String(100), nullable=False, unique=False)


class Publication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(100), unique=False, nullable=False)
    image_filename = db.Column(db.String(100), unique=False, nullable=False)
    title = db.Column(db.String(500), nullable=False, unique=False)
    author = db.Column(db.String(500), nullable=False, unique=False)
    ref_no = db.Column(db.String(500), nullable=False, unique=False)
    pdf_link = db.Column(db.String(500), nullable=False, unique=False)
    pdf_name = db.Column(db.String(500), nullable=False, unique=False)


class Reasearch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(100), nullable=False, unique=False)
    image_filename = db.Column(db.String(100), nullable=False, unique=False)
    title = db.Column(db.String(500), nullable=False, unique=False)
    body = db.Column(db.String(1000), nullable=False, unique=False)


with app.app_context():
    db.create_all()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return 'Test'


@app.route('/get-profile', methods=["POST"])
def get_profile():
    if request.form.get("accesskey") == "9494":
        profile = Profile.query.filter_by(id=1).first()
        if profile == null:
            return make_response(jsonify({"error": True, "data": "No Data Found"}))
        data = {
            "id": profile.id,
            "name": profile.name,
            "bio": profile.bio,
            "full_bio": profile.full_bio,
            "facebook": profile.facebook,
            "linkdin": profile.linkdin,
            "twitter": profile.twitter,
            "instragram": profile.instragram,
            "phone_no": profile.phone_no,
            "email": profile.email,
            "address": profile.address
        }
        return make_response(jsonify({"error": False, "data": data}), 200)
    return make_response(jsonify({"error": True, "data": "Bitch Do You Want TO Hack"}))


@app.route('/update-profile', methods=["POST"])
def update_profile():
    if 'user' in session and session['user'] == params['user-name']:
        profile = Profile.query.filter_by(id=1).first()
        if profile == null:
            return make_response(jsonify({"error": True, "data": "No Data Found"}))
        if 'name' in request.form:
            profile.name = request.form.get("name")
        if 'bio' in request.form:
            profile.bio = request.form.get("bio")
        if 'full_bio' in request.form:
            profile.full_bio = request.form.get("full_bio")
        if 'facebook' in request.form:
            profile.facebook = request.form.get("facebook")
        if 'linkdin' in request.form:
            profile.linkdin = request.form.get("linkdin")
        if 'twitter' in request.form:
            profile.twitter = request.form.gte("twitter")
        if 'instragram' in request.form:
            profile.instragram = request.form.get("instragram")
        if 'phone_no' in request.form:
            profile.phone_no = request.form.get("phone_no")
        if 'email' in request.form:
            profile.email = request.form.get("email")
        if 'address' in request.form:
            profile.address = request.form.get("address")
        db.session.commit()
        return make_response(jsonify({"error": False, "data": "Update Successfully"}), 200)
    else:
        return make_response(jsonify({"error": True, "data": "Login First"}))


@app.route('/login', methods=["POST"])
def login():
    if 'user' in session and session['user'] == params['user-name']:
        return make_response(jsonify({"error": False, "data": "user already login"}))
    else:
        passw = str(request.form.get("password"))
        user = str(request.form.get("username"))
        if passw == params['user-password'] and user == params['user-name']:
            session['user'] = user
            return make_response(jsonify({"error": False, "data": "Login Success Full"}))
        else:
            return make_response({"error": True, "data": "Wrong User Name or Password"})


@app.route('/update-profile-pic', methods=["POST"])
def update_profile_pic():
    if 'user' in session and session['user'] == params['user-name']:
        if 'file' not in request.files:
            return jsonify({"error": True, "data": "Please Upload A Image"})
        pic = request.files['file']
        if pic.filename == '':
            return jsonify({"error": True, "data": "No File selected"})
        if pic and allowed_file(pic.filename):
            import os
            if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], "profile_pic.png")):
                os.remove(os.path.join(
                    app.config['UPLOAD_FOLDER'], "profile_pic.png"))
            pic.save(os.path.join(
                app.config['UPLOAD_FOLDER'], "profile_pic.png"))
            return jsonify({"error": False, "data": "Profile Photo Update Successfully"})
    return make_response(jsonify({"error": True, "data": "Login First"}))


@app.route('/logout', methods=["GET"])
def logout():
    if 'user' in session and session['user'] == params['user-name']:
        session.pop("user")
        return jsonify({"error": False, "data": "logout successfully"})
    else:
        return jsonify({"error": True, "data": "login first"})


@app.route('/display/<filename>')
def display_image(filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='upload/' + filename), code=301)


@app.route('/get-details-by-category', methods=["POST"])
def get_details():
    if request.form.get("accesskey") == params["accesskey"]:
        if 'category' not in request.form:
            return jsonify({"error": True, "data": "Please Enter A category."})
        category_key = request.form.get("category")
        details = Details.query.filter_by(
            category=category_key).order_by(desc(Details.id)).all()
        final_data = []
        for det in details:
            data = {
                "id": det.id,
                "first_part": det.first_part,
                "second_part": det.second_part,
                "category": det.category
            }
            final_data.append(data)
        return jsonify({"error": False, "data": final_data})
    return make_response(jsonify({"error": True, "data": "Bitch Do You Want TO Hack"}))


@app.route('/delete-details-by-id', methods=["POST"])
def delete_details():
    if 'user' in session and session['user'] == params['user-name']:
        id = request.form.get("id")
        detail = Details.query.filter_by(id=id).first()
        db.session.delete(detail)
        db.session.commit()
        return jsonify({"error": False, "data": "data deleted"})
    return jsonify({"error": True, "data": "Login First"})


@app.route('/update-details-by-id', methods=["POST"])
def update_details():
    if 'user' in session and session['user'] == params['user-name']:
        id = request.form.get("id")
        detail = Details.query.filter_by(id=id).first()
        detail.first_part = request.form.get("first_part")
        detail.second_part = request.form.get("second_part")
        detail.category = request.form.get("category")
        db.session.commit()
        return jsonify({"error": False, "data": "data updated"})
    return jsonify({"error": True, "data": "Login First"})


@app.route('/add-details', methods=["POST"])
def add_details():
    if 'user' in session and session['user'] == params['user-name']:
        detail = Details()
        detail.first_part = request.form.get("first_part")
        detail.second_part = request.form.get("second_part")
        detail.category = request.form.get("category")
        db.session.add(detail)
        db.session.commit()
        return jsonify({"error": False, "data": "data added"})
    return jsonify({"error": True, "data": "Login First"})


@app.route('/get-gallery', methods=["POST"])
def get_gallery():
    if request.form.get("accesskey") == params["accesskey"]:
        gallery_items = Gallery.query.filter_by().order_by(desc(Gallery.id)).all()
        data = []
        for item in gallery_items:
            dic = {
                "id": item.id,
                "pic_link": item.pic_link,
            }
            data.append(dic)
        return jsonify({"error": False, "data": data})
    return jsonify({"error": True, "data": "Bitch Do You Want TO Hack"})


@app.route('/add-image-gallery', methods=["POST"])
def add_image():
    if 'user' in session and session['user'] == params['user-name']:
        # if 'file' not in request:
        #     return jsonify({"error": True, "data": "Please Upload A Image"})
        pic = request.files['file']
        if pic.filename == '':
            return jsonify({"error": True, "data": "No File selected"})
        if pic and allowed_file(pic.filename):
            import datetime
            basename = "gallery_image"
            suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
            filename = "_".join([basename, suffix])
            filename = filename + "." + pic.filename.rsplit('.', 1)[1].lower()
            if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            gal = Gallery()
            gal.pic_link = url_for('static', filename='upload/' + filename)
            gal.file_name = filename
            db.session.add(gal)
            db.session.commit()
            return jsonify({"error": False, "data": "Photo Added"})
    return make_response(jsonify({"error": True, "data": "Login First"}))


@app.route('/delete-gallery-image', methods=["POST"])
def delete_gallery():
    if 'user' in session and session['user'] == params['user-name']:
        get_id = request.form.get("id")
        gallery = Gallery.query.filter_by(id=get_id).first()
        filename = gallery.file_name
        if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        db.session.delete(gallery)
        db.session.commit()
        return jsonify({"error": False, "data": "Photo deleted Successfully"})
    return make_response(jsonify({"error": True, "data": "Login First"}))


@app.route('/add-publication', methods=["POST"])
def add_publication():
    if 'user' in session and session['user'] == params['user-name']:
        if 'image' not in request.files:
            return jsonify({"error": True, "data": "Please Upload A Image"})
        image = request.files['image']
        if image.filename == '':
            return jsonify({"error": True, "data": "File Not Selected"})
        if not (image and allowed_file(image.filename)):
            return jsonify({"error": True, "data": "Please Upload A supported file"})
        if 'document' not in request.files:
            return jsonify({"error": True, "data": "Please Upload A Document"})
        document = request.files['document']
        if document.filename == '':
            return jsonify({"error": True, "data": "File Not Selected"})
        if not (document and allowed_file(document.filename)):
            return jsonify({"error": True, "data": "Please Upload Supported File"})
        import datetime
        basename = "publication"
        suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
        filename = "_".join([basename, suffix])
        filename_image = filename + "." + image.filename.rsplit('.', 1)[1].lower()
        basename = "publication_document"
        suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
        filename = "_".join([basename, suffix])
        filename_pdf = filename + "." + document.filename.rsplit('.', 1)[1].lower()
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_image))
        document.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_pdf))
        publication = Publication()
        publication.image = url_for('static', filename='upload/' + filename_image)
        publication.image_filename = filename_image
        publication.title = request.form.get("title")
        publication.author = request.form.get("author")
        publication.ref_no = request.form.get("ref_no")
        publication.pdf_link = url_for('static', filename='upload/' + filename_pdf)
        publication.pdf_name = filename_pdf
        db.session.add(publication)
        db.session.commit()
        return jsonify({"error": False, "data": "Publication added successfully"})
    return jsonify({"error": True, "data": "Login First"})


@app.route("/get-publication", methods=["POST"])
def get_publication():
    if request.form.get("accesskey") == params["accesskey"]:
        publications = Publication.query.filter_by().order_by(desc(Publication.id)).all()
        data = []
        for pub in publications:
            temp = {
                "id": pub.id,
                "image": pub.image,
                "image_filename": pub.image_filename,
                "title": pub.title,
                "author": pub.author,
                "ref_no": pub.ref_no,
                "pdf_link": pub.pdf_link,
                "pdf_name": pub.pdf_name
            }
            data.append(temp)
        return jsonify({"error": False, "data": data})
    return jsonify({"error": True, "data": "Please enter valid accesskey"})


@app.route("/delete-publication-by-id")
def delete_publication():
    if 'user' in session and session['user'] == params['user-name']:
        if 'id' not in request.form:
            return jsonify({"error": True, "data": "Please put id"})
        id = request.form.get("id")
        publication = Publication.query.filter_by(id=id).first()
        filename = publication.image_filename
        if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        filename = publication.pdf_name
        if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        db.session.delete(publication)
        db.session.commit()
        return jsonify({"error": False, "data": "Deleted Successfully"})
    return jsonify({"error": True, "data": "Please login first"})


@app.route("/update-publication", methods=["POST"])
def update_publication():
    if 'user' in session and session['user'] == params['user-name']:
        if 'image' not in request.files:
            return jsonify({"error": True, "data": "Please Upload A Image"})
        image = request.files['image']
        if image.filename == '':
            return jsonify({"error": True, "data": "File Not Selected"})
        if not (image and allowed_file(image.filename)):
            return jsonify({"error": True, "data": "Please Upload A supported file"})
        if 'document' not in request.files:
            return jsonify({"error": True, "data": "Please Upload A Document"})
        document = request.files['document']
        if document.filename == '':
            return jsonify({"error": True, "data": "File Not Selected"})
        if not (document and allowed_file(document.filename)):
            return jsonify({"error": True, "data": "Please Upload Supported File"})
        import datetime
        basename = "publication"
        suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
        filename = "_".join([basename, suffix])
        filename_image = filename + "." + image.filename.rsplit('.', 1)[1].lower()
        basename = "publication_document"
        suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
        filename = "_".join([basename, suffix])
        filename_pdf = filename + "." + document.filename.rsplit('.', 1)[1].lower()
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_image))
        document.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_pdf))
        id = request.form.get("id")
        publication = Publication.query.filter_by(id=id).first()
        if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], publication.image_filename)):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], publication.image_filename))
        if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], publication.pdf_name)):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], publication.pdf_name))
        publication.image = url_for('static', filename='upload/' + filename_image)
        publication.image_filename = filename_image
        publication.title = request.form.get("title")
        publication.author = request.form.get("author")
        publication.ref_no = request.form.get("ref_no")
        publication.pdf_link = url_for('static', filename='upload/' + filename_pdf)
        publication.pdf_name = filename_pdf
        db.session.commit()
        return jsonify({"error": False, "data": "Publication updated successfully"})
    return jsonify({"error": True, "data": "Login First"})


@app.route("/get-research", methods=["POST"])
def get_reasearch():
    if request.form.get("accesskey") == params["accesskey"]:
        researchs = Reasearch.query.filter_by().order_by(desc(Reasearch.id)).all()
        data = []
        for re in researchs:
            dic = {
                "id": re.id,
                "image": re.image,
                "image_filename": re.image_filename,
                "title": re.title,
                "body": re.body
            }
            data.append(dic)
            return jsonify({"error": False, "data": data})
    return jsonify({"error": True, "data": "Bitch Do You Want TO Hack"})


@app.route("/add-research", methods=["POST"])
def add_reasearch():
    if 'user' in session and session['user'] == params['user-name']:
        if 'image' not in request.files:
            return jsonify({"error": True, "data": "Please Upload A Image"})
        image = request.files['image']
        if image.filename == '':
            return jsonify({"error": True, "data": "File Not Selected"})
        if not (image and allowed_file(image.filename)):
            return jsonify({"error": True, "data": "Please Upload A supported file"})
        import datetime
        basename = "reasearch"
        suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
        filename = "_".join([basename, suffix])
        filename_image = filename + "." + image.filename.rsplit('.', 1)[1].lower()
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_image))
        reasearch = Reasearch()
        reasearch.image = url_for('static', filename='upload/' + filename_image)
        reasearch.image_filename = filename_image
        reasearch.title = request.form.get("title")
        reasearch.description = request.form.get("description")
        db.session.add(reasearch)
        db.session.commit()
        return jsonify({"error": False, "data": "Reasearch Successfully"})
    return jsonify({"error": True, "data": "Login First"})


@app.route("/update-research", methods=["POST"])
def update_reasearch():
    if 'user' in session and session['user'] == params['user-name']:
        id = request.form.get("id")
        res = Reasearch.query.filter_by(id=id).first()
        if 'image' in request.files:
            image = request.files['image']
            if image.filename == "":
                return jsonify({"error": True, "data": "File Not Selected"})
            if not (image and allowed_file(image.filename)):
                return jsonify({"error": True, "data": "Please Upload A supported file"})
            import datetime
            basename = "reasearch"
            suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
            filename = "_".join([basename, suffix])
            filename_image = filename + "." + image.filename.rsplit('.', 1)[1].lower()
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_image))
            if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], res.image_filename)):
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], res.image_filename))
            res.image_filename = filename_image
            res.image = url_for('static', filename='upload/' + filename_image)
        res.title = request.form.get("title")
        res.body = request.form.get("body")
        db.session.commit()
        return jsonify({"error": False, "data": "Reasearch updated successfully"})
    return jsonify({"error": True, "data": "Login First"})


@app.route("/delete-research")
def delete_reasearch():
    if 'user' in session and session['user'] == params['user-name']:
        id = request.form.get("id")
        res = Reasearch.query.filter_by(id=id).first()
        db.session.delete(res)
        db.session.commit()
        return jsonify({"error": False, "data": "Research deleted successfully"})
    return jsonify({"error": True, "data": "Login First"})


app.run(host='0.0.0.0')