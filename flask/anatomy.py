from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bu anahtari degistirin...'
bootstrap = Bootstrap(app)

class NameForm(Form):
    name = StringField('İsminiz nedir?', validators=[DataRequired()])

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    #yorum
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('index.html', form=form, isim=name)


if __name__ == '__main__':
    app.run(debug=True)
