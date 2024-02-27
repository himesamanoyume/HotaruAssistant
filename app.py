from flask import Flask,render_template,request,abort,Response


# class WebModule:
mApp = Flask(__name__)
mApp.config['TEMPLATES_AUTO_RELOAD']=True
@mApp.template_filter('roundDate')
def RoundDate(value):
    return round(value, 3)

mApp.config['TEMPLATES_AUTO_RELOAD']=True
@mApp.template_filter('universe_number')
def UniverseNumber(value):
    return f"{value}"

@mApp.route('/')
def index():
    return render_template('test.html')

if __name__ == "__main__":
    mApp.run(host='0.0.0.0')