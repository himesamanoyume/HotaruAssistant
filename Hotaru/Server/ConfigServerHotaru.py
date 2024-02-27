from Mgrs.Server.ConfigServerMgr import ConfigServerMgr
import os
configServerMgr = ConfigServerMgr()

configServerMgr.env = os.environ.copy()
configServerMgr.env['PATH'] = os.path.dirname(configServerMgr.python_exe_path) + ';' + configServerMgr.env['PATH']