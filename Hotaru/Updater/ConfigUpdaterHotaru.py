from Mgrs.Updater.ConfigUpdaterMgr import ConfigUpdaterMgr
import os
configMgr = ConfigUpdaterMgr()
configMgr.env = os.environ.copy()
configMgr.env['PATH'] = os.path.dirname(configMgr.mConfig[configMgr.mKey.PYTHON_EXE_PATH]) + ';' + configMgr.env['PATH']