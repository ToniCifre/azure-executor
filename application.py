from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html")


@app.route('/toni', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':

        return jsonify(result="comemela", probability="por_los_dos_lados")

    return render_template("error/404.html")

