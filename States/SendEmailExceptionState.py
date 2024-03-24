from States import *
from Hotaru.Client.DataClientHotaru import dataMgr
from Hotaru.Client.OcrHotaru import ocrMgr
from Hotaru.Client.ScreenHotaru import screenMgr
import os,sys,time,psutil,pyautogui
from Modules.Utils.Retry import Retry
from .BaseNotifyState import BaseNotifyState

class SendEmailExceptionState(BaseNotifyState):

    mStateName = 'SendEmailExceptionState'

    def OnBegin(self):
        return False

    def OnRunning(self):
        return False

    def OnExit(self):
        return False