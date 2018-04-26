from flask import Flask, render_template
import json

app = Flask(__name__)


@app.route('/')
def sports_capital():
    with open('data/grants_2017.json') as json_data:
        grant_data = json.loads(json_data)
    return render_template('dash.html', grant_data=grant_data)


if __name__ == '__main__':
    app.run()
