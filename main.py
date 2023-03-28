from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
import wtforms
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, URL
import csv
import os


SECRET_KEY = os.environ['SECRET_KEY']
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = wtforms.StringField('Cafe name', validators=[DataRequired()])
    GoogleLocation = URLField('Location', validators=[DataRequired(), URL()])
    OpenTime = wtforms.TimeField('Opening time', validators=[DataRequired()])
    ClosingTime = wtforms.TimeField('Closing time', validators=[DataRequired()])
    CoffeeRating = wtforms.SelectField('Coffee Rating', choices=['✘', '☕', '☕☕', '☕☕☕', '☕☕☕☕'])
    WifiRating = wtforms.SelectField('Wifi', choices=['✘', '💪', '💪💪', '💪💪💪', '💪💪💪💪'])
    GPORating = wtforms.SelectField('Power outlets', choices=['✘', '🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌'])
    submit = wtforms.SubmitField('Save')




# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
# e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.




# Cafe Name,Location,Open,Close,Coffee,Wifi,Power
# Lighthaus,https://goo.gl/maps/2EvhB4oq4gyUXKXx9,11AM, 3:30PM,☕☕☕☕️,💪💪,🔌🔌🔌
# Esters,https://goo.gl/maps/13Tjc36HuPWLELaSA,8AM,3PM,☕☕☕☕,💪💪💪,🔌
# Ginger & White,https://goo.gl/maps/DqMx2g5LiAqv3pJQ9,7:30AM,5:30PM,☕☕☕,✘,🔌
# Mare Street Market,https://goo.gl/maps/ALR8iBiNN6tVfuAA8,8AM,1PM,☕☕,💪💪💪,🔌🔌🔌



# NEED TO INCLUDE A HOME RENDER
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        data = request.form
        newCafe = (list(data.values()))
        with open(r'cafe-data.csv', 'a', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(newCafe[1:-1])
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('home.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
