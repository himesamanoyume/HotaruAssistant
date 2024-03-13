from Modules.Server.WebModule import WebModule
import threading

class WebMgr:
    mInstance = None
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mWebModule = WebModule().mAppFlask

        return cls.mInstance
    
    def StartWeb(self, isDebug=False):
        if isDebug:
            self.RunFlask(isDebug)
        else:
            flaskThread = threading.Thread(target=self.RunFlask, args=(isDebug, ))
            flaskThread.start()
            import webbrowser
            webbrowser.open('http://127.0.0.1:5000')

    def RunFlask(self, isDebug=False):
        self.mWebModule.run(host='0.0.0.0',debug=isDebug)
