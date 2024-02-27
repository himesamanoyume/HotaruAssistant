from flask import Flask,render_template,request,abort,Response


class WebModule:
    mAppFlask = Flask(__name__, static_folder='../../assets/static', static_url_path='', template_folder='../../assets/templates')

    mAppFlask.config['TEMPLATES_AUTO_RELOAD']=True
    @mAppFlask.template_filter('roundDate')
    def RoundDate(value):
        return round(value, 3)

    mAppFlask.config['TEMPLATES_AUTO_RELOAD']=True
    @mAppFlask.template_filter('universe_number')
    def UniverseNumber(value):
        return f"{value}"

    @mAppFlask.route('/')
    def Index():
        return render_template('test.html')