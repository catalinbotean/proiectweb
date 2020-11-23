from flask import Flask, render_template, request, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
import os
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://epiz_27286792:6Bwq2IjiZaS8@sql213.byetcluster.com/epiz_27286792_job'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Cata'
app.config['DEBUG'] = True
app.config['TESTING'] = False

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'boteancatalin2@gmail.com'
app.config['MAIL_PASSWORD'] = 'catalinbotean'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
mail = Mail(app)
db = SQLAlchemy(app)


class Proiect(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numeCompanie = db.Column(db.String(100))
    numeJob = db.Column(db.String(100))
    experienta = db.Column(db.Integer)
    tag1 = db.Column(db.String(100))
    tag2 = db.Column(db.String(100))
    tag3 = db.Column(db.String(100))
    filename = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, numeCompanie, numeJob, experienta, tag1, tag2, tag3, filename, email):
        self.numeCompanie = numeCompanie
        self.numeJob = numeJob
        self.experienta = experienta
        self.tag1 = tag1
        self.tag2 = tag2
        self.tag3 = tag3
        self.filename = filename
        self.email = email

    def setNumeCompanie(self, numeCompanie):
        self.numeCompanie = numeCompanie

    def setNumeJob(self, numeJob):
        self.numeJob = numeJob

    def setTag1(self, tag1):
        self.tag1 = tag1

    def setTag2(self, tag2):
        self.tag2 = tag2

    def setTag3(self, tag3):
        self.tag3 = tag3

    def setEmail(self, email):
        self.email = email

    def setFilename(self, filename):
        self.filename = filename

    def setExperienta(self, experienta):
        self.experienta = experienta

    def getNumeCompanie(self):
        return self.numeCompanie

    def getNumeJob(self):
        return self.numeJob

    def getTag1(self):
        return self.tag1

    def getTag2(self):
        return self.tag2

    def getTag3(self):
        return self.tag3

    def getEmail(self):
        return self.email

    def getExperienta(self):
        return self.experienta

    def getFilename(self):
        return self.filename


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    email = db.Column(db.Integer)
    telefon = db.Column(db.String(100))

    def __init__(self, username, password, email, telefon):
        self.username = username
        self.password = password
        self.telefon = telefon
        self.email = email


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/utilizator/<int:id>')
def utilizator(id):
    cont = User.query.filter_by(id=id).first()
    return render_template('utilizator.html', cont=cont)


@app.route('/utilizator/<int:id>/delete')
def deleteCont(id):
    cont = User.query.filter_by(id=id).first()
    db.session.delete(cont)
    db.session.commit()
    return index()


@app.route('/administrare/<int:page_num>/deleteContAdm/<int:id>', methods=['GET', 'POST'])
def deleteContAdm(page_num,id):
    if request.method == "POST":
        cont = User.query.filter_by(id=id).first()
        db.session.delete(cont)
        db.session.commit()
        return administrare(page_num)


@app.route('/editareCont/<int:id>', methods=['GET', 'POST'])
def editareCont(id):
    cont = User.query.filter_by(id=id).first()
    if request.method == "POST":
        cont.username = request.form['username']
        cont.password = request.form['password']
        cont.email = request.form['email']
        cont.telefon = request.form['telefon']
        db.session.commit()
    return render_template("editareProfil.html", cont=cont)


@app.route('/creareCont', methods=['GET', 'POST'])
def creareCont():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        telefon = request.form['telefon']
        cont = User.query.filter_by(username=username).first()
        if cont is not None:
            flash('Username already exist')
            return redirect(request.url)
        else:
            contNou = User(username, password, email, telefon)
            db.session.add(contNou)
            db.session.commit()
            return utilizator(contNou.id)
    else:
        return render_template('creareCont.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/adauga')
def adauga():
    return render_template('adauga.html')


@app.route('/search/<int:id>/<int:page_num>/<string:key>', methods=['GET', 'POST'])
def search(id, page_num, key):
    cont = User.query.filter_by(id=id).first()
    data = Proiect.query.paginate(per_page=4, page=page_num, error_out=True)
    if request.method == "POST" or key !='all':
        if request.method == "POST":
            key = request.form['search']
        data = Proiect.query.filter(
            (Proiect.tag3 == key.lower()) | (Proiect.tag2 == key.lower()) | (Proiect.tag1 == key.lower())).paginate(
            per_page=4, page=page_num, error_out=True)
        if key == 'all':
            data = Proiect.query.paginate(per_page=4, page=page_num, error_out=True)
        next_url = url_for('search', id=id, page_num=page_num + 1,key=key) \
            if data.has_next else None
        prev_url = url_for('search', id=id, page_num=page_num - 1,key=key) \
            if data.has_prev else None
        return render_template("search.html", cont=cont, jobs=data, page_num=page_num, next_url=next_url,
                               prev_url=prev_url, key=key)
    next_url = url_for('search', id=id, page_num=page_num + 1,key=key) \
        if data.has_next else None
    prev_url = url_for('search', id=id, page_num=page_num - 1,key=key) \
        if data.has_prev else None
    return render_template("search.html", cont=cont, jobs=data, page_num=page_num, next_url=next_url, prev_url=prev_url,key=key)


@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == "POST":
        numeCompanie = request.form['numeCompanie']
        numeJob = request.form['numeJob']
        tag1 = request.form['tag1']
        tag2 = request.form['tag2']
        tag3 = request.form['tag3']
        experienta = request.form['experienta']
        upload()
        for file in request.files.getlist("file"):
            filename = file.filename
        email = request.form['description']
        jobNou = Proiect(numeCompanie, numeJob, experienta, tag1, tag2, tag3, filename, email)
        db.session.add(jobNou)
        db.session.commit()
        return adauga()


@app.route('/afisare/<int:page_num>/delete/<int:id>', methods=['GET', 'POST'])
def delete(page_num, id):
    if request.method == "POST":
        job = Proiect.query.get(id)
        db.session.delete(job)
        db.session.commit()
        return afisare(page_num)


@app.route('/afisare/<int:page_num>/editare/<int:id>', methods=['GET', 'POST'])
def editare(page_num, id):
    if request.method == "POST":
        job = Proiect.query.get(id)
        return render_template("editareJob.html", job=job, page_num=page_num)
    return afisare(page_num)


@app.route('/afisare/<int:page_num>/inapoiEditare/<int:id>', methods=['GET', 'POST'])
def inapoiEditare(page_num, id):
    if request.method == "POST":
        return afisare(page_num)
    return editare(page_num, id)


@app.route('/afisare/<int:page_num>/updateJob/<int:id>', methods=['GET', 'POST'])
def updateJob(page_num, id):
    if request.method == "POST":
        job = Proiect.query.filter_by(id=id).first()
        job.numeCompanie = request.form['numeCompanie']
        job.numeJob = request.form['numeJob']
        job.tag1 = request.form['tag1']
        job.tag2 = request.form['tag2']
        job.tag3 = request.form['tag3']
        job.experienta = request.form['experienta']
        for file in request.files.getlist("file"):
            if file.filename != "":
                upload()
                job.filename = file.filename
        job.email = request.form['description']
        db.session.commit()
    return editare(page_num, id)


@app.route('/administrare/<int:page_num>/editareContAdm/<int:id>', methods=['GET', 'POST'])
def updateContAdm(page_num, id):
    cont = User.query.filter_by(id=id).first()
    if request.method == "POST":
        cont.username = request.form['username']
        cont.password = request.form['password']
        cont.email = request.form['email']
        cont.telefon = request.form['telefon']
        db.session.commit()
    return render_template("editareProfilAdm.html", cont=cont, page_num=page_num, id=id)


@app.route('/administrare/<int:page_num>/editareContAdmi/<int:id>', methods=['GET', 'POST'])
def updateContAdmi(page_num, id):
    cont = User.query.filter_by(id=id).first()
    if request.method == "POST":
        return render_template("editareProfilAdm.html", cont=cont, page_num=page_num, id=id)
    return administrare(page_num)


@app.route('/administrare/<int:page_num>/inapoi/<int:id>', methods=['GET', 'POST'])
def backEdit(page_num, id):
    if request.method == "POST":
        return administrare(page_num)
    return updateContAdm(page_num,id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if username == "catalin" and password == "botean":
            return login()
        elif User.query.filter_by(username=username).first() is not None:
            user = User.query.filter_by(username=username).first()
            if user.username == username and user.password == password:
                return utilizator(user.id)
            else:
                flash('Invalid Login Credentials')
                return redirect(request.url)
        else:
            flash('Invalid Login Credentials')
            return redirect(request.url)
    return index()


@app.route('/afisare/<int:page_num>')
def afisare(page_num):
    data = Proiect.query.paginate(per_page=4, page=page_num, error_out=True)
    next_url = url_for('afisare', page_num=page_num + 1) \
        if data.has_next else None
    prev_url = url_for('afisare', page_num=page_num - 1) \
        if data.has_prev else None
    return render_template("afisare.html", jobs=data, page_num=page_num, next_url=next_url, prev_url=prev_url)


@app.route('/administrare/<int:page_num>')
def administrare(page_num):
    data = User.query.paginate(per_page=4, page=page_num, error_out=True)
    next_url = url_for('administrare', page_num=page_num + 1) \
        if data.has_next else None
    prev_url = url_for('administrare', page_num=page_num - 1) \
        if data.has_prev else None
    return render_template("administrare.html", cont=data, page_num=page_num, next_url=next_url, prev_url=prev_url)


@app.route('/search/<int:id>/<int:page_num>/<string:key>/d/<int:idJob>')
def d(id, page_num, key, idJob):
    cont = User.query.filter_by(id=id).first()
    job = Proiect.query.filter_by(id=idJob).first()
    return render_template("detaliiJob.html", cont=cont, id=id, page_num=page_num, key=key, idJob=idJob, job=job)


@app.route('/search/<int:id>/<int:page_num>/<string:key>/detaliu/<int:idJob>', methods=['GET', 'POST'])
def details(id, page_num, key, idJob):
    if request.method == "POST":
        return redirect('/search/'+str(id)+'/'+str(page_num)+'/'+key)
    return d(id, page_num, key, idJob)


@app.route('/search/<int:id>/<int:page_num>/<string:key>/detaliuJob/<idJob>',methods=['GET', 'POST'])
def detailsJob(id,page_num,key,idJob):
    if request.method == "POST":
        return d(id, page_num, key, idJob)
    return search(id, page_num, key)


@app.route('/upload')
def upload():
    target = os.path.join(APP_ROOT, 'static/img/uploads')
    if not os.path.isdir(target):
        os.mkdir(target)
    for file in request.files.getlist("file"):
        filename = file.filename
        destination = "/".join([target, filename])
        file.save(destination)


@app.route('/search/<int:id>/<int:page_num>/<string:key>/aplica/<idJob>',methods=['GET', 'POST'])
def aplica(id,page_num,key,idJob):
    cont = User.query.filter_by(id=id).first()
    job = Proiect.query.filter_by(id=idJob).first()
    if request.method == "POST":
        return a(id, page_num, key, idJob)
    return search(id, page_num, key)


@app.route('/search/<int:id>/<int:page_num>/<string:key>/a/<idJob>', methods=['GET', 'POST'])
def a(id,page_num,key,idJob):
    cont = User.query.filter_by(id=id).first()
    job = Proiect.query.filter_by(id=idJob).first()
    return render_template("aplicare.html", cont=cont, id=id, page_num=page_num, key=key, idJob=idJob, job=job)


@app.route('/search/<int:id>/<int:page_num>/<string:key>/cv/<idJob>', methods=['GET', 'POST'])
def aplicaCV(id,page_num,key,idJob):
    if request.method == "POST":
        cont = User.query.filter_by(id=id).first()
        job = Proiect.query.filter_by(id=idJob).first()
        msq = Message('Proiect-PW', sender='boteancatalin2@gmail.com', recipients=[job.email])
        msq.body = cont.username+' a aplicat pentru pozitia '+job.numeJob+' din cadrul companiei dumneazavoastra. Mai jos aveti atasat cv-ul acestuia'
        cv()
        for file in request.files.getlist("file"):
            filename = file.filename
        with app.open_resource('static/cv/'+filename) as c:
            msq.attach('static/cv/'+filename,'application/pdf',c.read())
        mail.send(msq)
        return a(id, page_num, key, idJob)


@app.route('/cv')
def cv():
    target = os.path.join(APP_ROOT, 'static/cv')
    if not os.path.isdir(target):
        os.mkdir(target)
    for file in request.files.getlist("file"):
        filename = file.filename
        destination = "/".join([target, filename])
        file.save(destination)


if __name__ == "__main__":
    app.run(debug=True)
