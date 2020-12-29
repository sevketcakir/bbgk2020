from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notlar.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'bu anahtarı değiştirin....'
bootstrap = Bootstrap(app)

class Ogrenci(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ogr_no = db.Column(db.String(8), nullable=False)
    adi = db.Column(db.String(25), nullable=False)
    soyadi = db.Column(db.String(25), nullable=False)

    def __repr__(self):
        return f"<Ogrenci: {self.ogr_no} {self.adi} {self.soyadi}>"

class OgrenciForm(Form):
    ogr_no = StringField('Öğrenci numarası', validators=[DataRequired()])
    adi = StringField('Adı', validators=[DataRequired()])
    soyadi = StringField('Soyadı', validators=[DataRequired()])
    gonder = SubmitField('Gönder')



class Not(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ders_adi = db.Column(db.String(30), nullable=False)
    notu = db.Column(db.Integer, nullable=False)
    ogrenci_id = db.Column(db.Integer, db.ForeignKey('ogrenci.id'), nullable=False)
    ogrenci = db.relationship('Ogrenci', backref=db.backref('notlar'))

    def __repr__(self):
        return f"<Not: {self.ogrenci} {self.ders_adi} {self.notu}>"



@app.route('/ogrenci/<int:ogr_id>', methods=['GET', 'POST'])
def ogrenci(ogr_id):
    ogrenci = Ogrenci.query.get(ogr_id)
    return render_template('ogrenci.html', ogrenci=ogrenci)

@app.route('/ogrenci/ekle', methods=['GET', 'POST'])
def ogrenci_ekle():
    form = OgrenciForm()
    if form.validate_on_submit():
        ogr_no = form.ogr_no.data
        adi = form.adi.data
        soyadi = form.soyadi.data
        o = Ogrenci(ogr_no=ogr_no, adi=adi, soyadi=soyadi)
        db.session.add(o)
        db.session.commit()
        return render_template('ogrenci.html', ogrenci=o)
    return render_template('ogrenciekle.html', form=form)

app.run(debug=True)