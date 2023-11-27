from managers.config_manager import config
from managers.translate_manager import _
from managers.screen_manager import screen
from managers.logger_manager import logger
from managers.utils_manager import gu
from managers.automation_manager import auto
import time

def testFun():
    str1 = 'fuck_'
    str2 = '100593155'
    str1, str3 = testFun2(str1, str2)
    print(str1)
    print(str3)

def testFun2(str1,str2):
    str1 += f'hahahaha_{str2}'
    str3 = f'{str1}...good'
    return str1, str3

if __name__ == '__main__':
    testFun()