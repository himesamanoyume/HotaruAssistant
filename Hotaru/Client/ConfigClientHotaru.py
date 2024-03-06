from Mgrs.Client.ConfigClientMgr import ConfigClientMgr
import os
configClientMgr = ConfigClientMgr()
configClientMgr.env = os.environ.copy()
configClientMgr.env['PATH'] = os.path.dirname(configClientMgr.mConfigModule[configClientMgr.mKey.PYTHON_EXE_PATH]) + ';' + configClientMgr.env['PATH']