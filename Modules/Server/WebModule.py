from flask import Flask,render_template,request,abort,Response


class WebModule:
    mAppFlask = Flask(__name__)

    @mAppFlask.route('/')
    def index():
        return ''