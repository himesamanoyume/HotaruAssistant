from Modules.Server.WebModule import WebModule
import threading

class WebMgr:
    mInstance = None
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mWebModule = WebModule().mAppFlask

        return cls.mInstance
    
    @classmethod
    def StartWeb(cls):
        flaskThread = threading.Thread(target=cls.RunFlask)
        flaskThread.start()
        # import webbrowser
        # webbrowser.open('http://127.0.0.1:5000')

    @classmethod
    def RunFlask(cls):
        cls.mWebModule.run(host='0.0.0.0')
