from sqlalchemy import null, desc
from flask import jsonify, make_response, request, session, url_for, redirect,render_template
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
import os
from flask_cors import CORS
#test
file_path = os.path.abspath(os.getcwd()) + "/biplabchem.db"
path = os.path.abspath(os.getcwd())
UPLOAD_FOLDER = path + "/static/upload"
# create Flask APP And Do Configuration
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
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
    image = db.Column(db.String(100), unique=False, nullable=True)
    image_filename = db.Column(db.String(100), unique=False, nullable=True)
    title = db.Column(db.String(500), nullable=False, unique=False)
    author = db.Column(db.String(500), nullable=False, unique=False)
    ref_no = db.Column(db.String(500), nullable=False, unique=False)
    pdf_link = db.Column(db.String(500), nullable=False, unique=True)
    pdf_name = db.Column(db.String(500), nullable=False, unique=True)


class Reasearch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(100), nullable=True, unique=False)
    image_filename = db.Column(db.String(100), nullable=True, unique=False)
    title = db.Column(db.String(500), nullable=True, unique=False)
    body = db.Column(db.String(1000), nullable=True, unique=False)


with app.app_context():
    db.create_all()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS





@app.route('/get-profile', methods=["POST"])
def get_profile():
    if request.json["accesskey"] == "9494":
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
            profile.twitter = request.form.get("twitter")
        if 'instragram' in request.form:
            profile.instragram = request.form.get("instragram")
        if 'phone_no' in request.form:
            profile.phone_no = request.form.get("phone_no")
        if 'email' in request.form:
            profile.email = request.form.get("email")
        if 'address' in request.form:
            profile.address = request.form.get("address")
        db.session.commit()
        return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))


@app.route('/', methods=["POST","GET"])
def login():
    if 'user' in session and session['user'] == params['user-name']:
        profileData=Profile.query.filter_by().first()
        return render_template("adminProfile.html",profile=profileData)
    else:
        if request.method =="GET":
            return render_template("adminLogin.html")
        passw = str(request.form.get("password"))
        user = str(request.form.get("username"))
        if passw == params['user-password'] and user == params['user-name']:
            session['user'] = user
            profileData=Profile.query.filter_by().first()
            return render_template("adminProfile.html",profile=profileData)
        else:
            return redirect(url_for("login"))


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
            return redirect(url_for("login"),code=301)
    return render_template("adminLogin.html")


@app.route('/logout', methods=["GET"])
def logout():
    if 'user' in session and session['user'] == params['user-name']:
        session.pop("user")
        return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))


@app.route('/display/<filename>')
def display_image(filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='upload/' + filename), code=301)


@app.route('/get-details-by-category', methods=["POST"])
def get_details():
    if request.json["accesskey"] == params["accesskey"]:
        # if 'category' not in request.form:
        #     return jsonify({"error": True, "data": "Please Enter A category."})
        category_key = request.json["category"]
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
        return redirect(url_for("education"))
    return redirect(url_for("login"))

@app.route("/education",methods=["GET"])
def education():
    if 'user' in session and session['user'] == params['user-name']:
        education = Details.query.filter_by(
                category="education").order_by(desc(Details.id)).all()
        position= Details.query.filter_by(
                category="position").order_by(desc(Details.id)).all()
        awards = Details.query.filter_by(
                category="awards").order_by(desc(Details.id)).all()
        return render_template("adminDetails.html",education=education,position=position,awards=awards)
    return redirect(url_for("login"))
@app.route('/update-details-by-id', methods=["POST"])
def update_details():
    if 'user' in session and session['user'] == params['user-name']:
        id = request.form.get("id")
        detail = Details.query.filter_by(id=id).first()
        detail.first_part = request.form.get("first_part")
        detail.second_part = request.form.get("second_part")
        db.session.commit()
        return redirect(url_for("education"))
    return redirect(url_for("login"))


@app.route('/add-details', methods=["POST"])
def add_details():
    if 'user' in session and session['user'] == params['user-name']:
        detail = Details()
        detail.first_part = request.form.get("first_part")
        detail.second_part = request.form.get("second_part")
        detail.category = request.form.get("category")
        db.session.add(detail)
        db.session.commit()
        return redirect(url_for("education"))
    else:
        return redirect(url_for("login"))


@app.route('/get-gallery', methods=["POST"])
def get_gallery():
    if request.json["accesskey"] == params["accesskey"]:
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

# Indian Railway 
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
            return redirect(url_for("gallery"))
    return redirect(url_for("login"))

@app.route("/gallery",methods=["GET"])
def gallery():
    if 'user' in session and session['user'] == params['user-name']:
        gallery_items = Gallery.query.filter_by().order_by(desc(Gallery.id)).all()
        return render_template("adminGallery.html",gallery_items=gallery_items)
    return redirect(url_for("login"))
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
        return redirect(url_for("gallery"))
    return redirect(url_for("login"))


@app.route('/add-publication', methods=["POST"])
def add_publication():
    if 'user' in session and session['user'] == params['user-name']:
        publication = Publication()
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                if (image and allowed_file(image.filename)):
                    print("souvik")
                    import datetime
                    basename = "publication"
                    suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
                    filename = "_".join([basename, suffix])
                    filename_image = filename + "." + image.filename.rsplit('.', 1)[1].lower()
                    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_image))
                    publication.image_filename= filename_image
                    publication.image=url_for('static', filename='upload/' + filename_image)
                    
                    
        if 'document' in request.files:
            document = request.files['document']
            if document.filename != '':
                if (document and allowed_file(document.filename)):
                    import datetime
                    basename = "publication_document"
                    suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
                    filename = "_".join([basename, suffix])
                    filename_pdf = filename + "." + document.filename.rsplit('.', 1)[1].lower()
                    document.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_pdf))
                    publication.pdf_link = url_for('static', filename='upload/' + filename_pdf)
                    publication.pdf_name = filename_pdf
        publication.title = request.form.get("title")
        publication.author = request.form.get("author")
        publication.ref_no = request.form.get("ref_no")
        db.session.add(publication)
        db.session.commit()
        return redirect(url_for("publication"))
    return redirect(url_for("login"))

@app.route("/publication")
def publication():
    if 'user' in session and session['user'] == params['user-name']:
        publications = Publication.query.filter_by().order_by(desc(Publication.id)).all()
        return render_template("adminPublication.html",publications=publications)
    return redirect(url_for("login"))

@app.route("/get-publication", methods=["POST"])
def get_publication():
    if request.json["accesskey"] == params["accesskey"]:
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


@app.route("/delete-publication-by-id",methods=["POST"])
def delete_publication():
    if 'user' in session and session['user'] == params['user-name']:
        if 'id' not in request.form:
            return jsonify({"error": True, "data": "Please put id"})
        id = request.form.get("id")
        publication = Publication.query.filter_by(id=id).first()
        filename = publication.image_filename
        filename = publication.pdf_name
        db.session.delete(publication)
        db.session.commit()
        return redirect(url_for("publication"))
    return redirect(url_for("login"))


@app.route("/update-publication", methods=["POST"])
def update_publication():
    if 'user' in session and session['user'] == params['user-name']:
        id = request.form.get("id")
        publication = Publication.query.filter_by(id=id).first()
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                if (image and allowed_file(image.filename)):
                    print("souvik")
                    import datetime
                    basename = "publication"
                    suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
                    filename = "_".join([basename, suffix])
                    filename_image = filename + "." + image.filename.rsplit('.', 1)[1].lower()
                    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_image))
                    publication.image_filename= filename_image
                    publication.image=url_for('static', filename='upload/' + filename_image)
                    
                    
        if 'document' in request.files:
            document = request.files['document']
            if document.filename != '':
                if (document and allowed_file(document.filename)):
                    import datetime
                    basename = "publication_document"
                    suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
                    filename = "_".join([basename, suffix])
                    filename_pdf = filename + "." + document.filename.rsplit('.', 1)[1].lower()
                    document.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_pdf))
                    publication.pdf_link = url_for('static', filename='upload/' + filename_pdf)
                    publication.pdf_name = filename_pdf
        
        
        
        
        publication.title = request.form.get("title")
        publication.author = request.form.get("author")
        publication.ref_no = request.form.get("ref_no")
        
        db.session.commit()
        return redirect(url_for("publication"))
    return redirect(url_for("login"))

@app.route("/get-research", methods=["POST"])
def get_reasearch():
    if request.json["accesskey"] == params["accesskey"]:
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
        reasearch = Reasearch()
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != "":
                if (image and allowed_file(image.filename)):
                    import datetime
                    basename = "reasearch"
                    suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
                    filename = "_".join([basename, suffix])
                    filename_image = filename + "." + image.filename.rsplit('.', 1)[1].lower()
                    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_image))
                    reasearch.image_filename = filename_image
                    reasearch.image = url_for('static', filename='upload/' + filename_image)     
        reasearch.title = request.form.get("title")
        reasearch.body = request.form.get("description")
        db.session.add(reasearch)
        db.session.commit()
        return redirect(url_for("research"))
    return redirect(url_for("login"))

@app.route("/research",methods=["GET"])
def research():
    if 'user' in session and session['user'] == params['user-name']:
        researchs = Reasearch.query.filter_by().order_by(desc(Reasearch.id)).all()
        return render_template("adminResearch.html",research=researchs)
    return redirect(url_for("login"))
@app.route("/update-research", methods=["POST"])
def update_reasearch():
    if 'user' in session and session['user'] == params['user-name']:
        id = request.form.get("id")
        res = Reasearch.query.filter_by(id=id).first()
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != "":
                if (image and allowed_file(image.filename)):
                    import datetime
                    basename = "reasearch"
                    suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
                    filename = "_".join([basename, suffix])
                    filename_image = filename + "." + image.filename.rsplit('.', 1)[1].lower()
                    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_image))
                    res.image_filename = filename_image
                    res.image = url_for('static', filename='upload/' + filename_image)
        res.title = request.form.get("title")
        res.body = request.form.get("description")
        db.session.commit()
        return redirect(url_for("research"))
    return redirect(url_for("login"))


@app.route("/delete-research" ,methods=["POST"])
def delete_reasearch():
    if 'user' in session and session['user'] == params['user-name']:
        id = request.form.get("id")
        res = Reasearch.query.filter_by(id=id).first()
        db.session.delete(res)
        db.session.commit()
        return redirect(url_for("research"))
    return redirect(url_for("login"))


@app.route("/goto-reasearch-update", methods=["POST"])
def goto_reasearch_update():
    if 'user' in session and session['user'] == params['user-name']:
        id= request.form.get("id")
        data=Reasearch.query.filter_by(id=id).first()
        return render_template("adminEditResearch.html",data=data)
    return redirect(url_for("login"))
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")