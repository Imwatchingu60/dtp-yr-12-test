from flask import Flask, render_template

app = Flask(__name__, template_folder='.')

FLOWERS={'id':1,'name':'Sunflower','latin':'Helianthus annuus','season':'Summer','sunlight':'Full Sun','watering':'Medium','difficulty': 'Easy'},{'id':2, 'name':'Rose','latin':'Rosa','season':'Spring-Autumn','sunlight':'Full Sun','watering':'Medium','difficulty':'Hard'},{'id':3,'name':'Lavender','latin':'lavare','season':'Summer','sunlight':'Full Sun','watering':'Low','difficulty':'Easy'},


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/flowers')
def flowers():
    return render_template('flowers.html',flowers=FLOWERS)


@app.route('/flower/<int:id>')
def flower_detail(id):
    flower = None
    for f in FLOWERS:
        if f['id'] == id:
            flower = f
    return render_template('flower.html', flower=flower)

if __name__ =='__main__':
    app.run(debug=True)