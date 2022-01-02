from flask import render_template
import os


class MainViews:
    @staticmethod
    def main_display(responce=None):
        return render_template("index.html", data={"title": "Slash92"})

    @staticmethod
    def error_404_display(error):
        return render_template("error.html", data={"title": "404", "code": 404, "error": "Пуся, некорректный адрес)"})

    @staticmethod
    def error_500_display(error):
        return render_template("error.html", data={"title": "500", "code": 500, "error": "Чот на серваке, лол..."})
