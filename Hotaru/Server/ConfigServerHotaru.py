from Mgrs.Server.ConfigServerMgr import ConfigServerMgr
import os

configMgr = ConfigServerMgr()
configMgr.env = os.environ.copy()
configMgr.env['PATH'] = os.path.dirname(configMgr.mConfigModule[configMgr.mKey.PYTHON_EXE_PATH]) + ';' + configMgr.env['PATH']