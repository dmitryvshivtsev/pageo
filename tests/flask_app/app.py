from flask import Flask, render_template


def run_flask(queue):
    """
    Функция запускает сервер Flask для выполнения тестов.
    """
    app = Flask(__name__)

    @app.route("/")
    def root():
        return render_template('index.html')

    queue.put(None)

    app.run(port=3000)

