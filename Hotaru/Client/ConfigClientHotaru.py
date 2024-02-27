from Mgrs.Client.ConfigClientMgr import ConfigClientMgr
import os
configClientMgr = ConfigClientMgr()

configClientMgr.env = os.environ.copy()
configClientMgr.env['PATH'] = os.path.dirname(configClientMgr.python_exe_path) + ';' + configClientMgr.env['PATH']