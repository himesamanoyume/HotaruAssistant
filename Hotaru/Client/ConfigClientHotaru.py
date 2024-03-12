from Mgrs.Client.ConfigClientMgr import ConfigClientMgr
import os
configMgr = ConfigClientMgr()
configMgr.env = os.environ.copy()
configMgr.env['PATH'] = os.path.dirname(configMgr.mConfig[configMgr.mKey.PYTHON_EXE_PATH]) + ';' + configMgr.env['PATH']