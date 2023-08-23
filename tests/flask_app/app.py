from flask import Flask, render_template


def run_flask(queue):
    app = Flask(__name__)

    @app.route("/")
    def root():
        return render_template('index.html')

    queue.put(None)

    app.run(port=8000)

