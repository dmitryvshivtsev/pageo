from flask import Flask, render_template


def run_flask():
    app = Flask(__name__)

    @app.route("/")
    def root():
        return render_template('index.html')

    app.run(port=8000)

