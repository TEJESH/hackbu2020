from flask import Flask, request, render_template, jsonify
import geopy

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('homes.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['address']
    processed_text = text.upper()
    str1= processed_text
    a = []
    locator = geopy.Nominatim(user_agent = "myGeocoder")
    location = locator.geocode(str1)
    a = [format(location.latitude), format(location.longitude)]
    #print(a)

    print(a)
    return jsonify(a)


if __name__ == '__main__':
    app.run(debug=True)
