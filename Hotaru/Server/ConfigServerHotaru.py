from Mgrs.Server.ConfigServerMgr import ConfigServerMgr
import os
configServerMgr = ConfigServerMgr()

configServerMgr.env = os.environ.copy()
# configServerMgr.env['PATH'] = os.path.dirname(configServerMgr.m) + ';' + configServerMgr.env['PATH']
configServerMgr.env['PATH'] = os.path.dirname(configServerMgr.mConfig[configServerMgr.mKey.PYTHON_EXE_PATH]) + ';' + configServerMgr.env['PATH']