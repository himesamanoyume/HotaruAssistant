from Mgrs.Server.ConfigServerMgr import ConfigServerMgr
import os

configServerMgr = ConfigServerMgr()
configServerMgr.env = os.environ.copy()
configServerMgr.env['PATH'] = os.path.dirname(configServerMgr.mConfigModule[configServerMgr.mKey.PYTHON_EXE_PATH]) + ';' + configServerMgr.env['PATH']