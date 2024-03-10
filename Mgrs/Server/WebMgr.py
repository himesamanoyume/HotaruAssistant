from Modules.Server.WebModule import WebModule
import threading

class WebMgr:
    mInstance = None
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mWebModule = WebModule().mAppFlask

        return cls.mInstance
    
    def StartWeb(self):
        flaskThread = threading.Thread(target=self.RunFlask)
        flaskThread.start()
        import webbrowser
        webbrowser.open('http://127.0.0.1:5000')

    def StartDebugWeb(self):
        self.mWebModule.run(host='0.0.0.0',debug=True)

    def RunFlask(self):
        self.mWebModule.run(host='0.0.0.0')
