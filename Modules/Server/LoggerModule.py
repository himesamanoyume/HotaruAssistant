from datetime import datetime
import logging,os,glob
from colorama import init

class LoggerModule:

    mInstance = None

    def __new__(cls, level="INFO"):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mInstance.InitLogger(level)
        return cls.mInstance
    
    def InitLogger(self, level="INFO"):
        self.logger = logging.getLogger("HotaruAssistant")
        self.logger.propagate = False
        self.logger.setLevel(level)

        if not os.path.exists("logs"):
            os.makedirs("logs")

        self.ClearLog("./logs")
        
        file_handler = logging.FileHandler(f"./logs/{self.CurrentDatetime()}.log", encoding="utf-8")
        file_formatter = logging.Formatter('├ %(levelname)s|%(asctime)s|%(filename)s:%(lineno)d\n└ %(message)s')
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_formatter = ColoredFormatter('├ %(levelname)s|%(asctime)s|%(filename)s:%(lineno)d\n└ %(message)s')
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        self.logger.hr = TitleFormatter.format_title

        return self.logger
    
    def CurrentDatetime(self):
        return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    def ClearLog(self, directory):
        files = glob.glob(directory + '/*')
        for f in files:
            if os.path.isfile(f):
                if os.path.getsize(f) <= 2048:
                    os.remove(f)

    def GetLogger(self):
        return self.logger
    
    def Info(self, msg, *args, **kwargs):
        self.GetLogger().info(msg, *args, **kwargs)

    def Error(self, msg, *args, **kwargs):
        self.GetLogger().error(msg, *args, **kwargs)

    def Warning(self, msg, *args, **kwargs):
        self.GetLogger().warning(msg, *args, **kwargs)

class ColoredFormatter(logging.Formatter):
    init(autoreset=True)
    COLORS = {
        'DEBUG': '\033[94m',  # 蓝色
        'INFO': '\033[92m',   # 绿色
        'WARNING': '\033[93m',  # 黄色
        'ERROR': '\033[91m',   # 红色
        'CRITICAL': '\033[91m',  # 红色
        'RESET': '\033[0m'   # 重置颜色
    }

    def format(self, record):
        log_level = record.levelname
        color_start = self.COLORS.get(log_level, self.COLORS['RESET'])
        color_end = self.COLORS['RESET']
        record.levelname = f"{color_start}{log_level}{color_end}"
        return super().format(record)

class TitleFormatter:
    @staticmethod
    def custom_len(s):
        length = 0
        for char in s:
            # 判断是否是中文字符和全角符号的Unicode范围
            if (ord(char) >= 0x4E00 and ord(char) <= 0x9FFF) or (ord(char) >= 0xFF00 and ord(char) <= 0xFFEF):
                length += 2
            else:
                length += 1
        return length

    @staticmethod
    def format_title(title, level=0):
        try:
            separator_length = 115
            title_lines = title.split('\n')
            separator = '+' + '-' * separator_length + '+'
            title_length = TitleFormatter.custom_len(title)
            half_separator_left = (separator_length - title_length) // 2
            half_separator_right = separator_length - title_length - half_separator_left

            if level == 0:
                formatted_title_lines = []

                for line in title_lines:
                    title_length_ = TitleFormatter.custom_len(line)
                    half_separator_left_ = (separator_length - title_length_) // 2
                    half_separator_right_ = separator_length - title_length_ - half_separator_left_

                    formatted_title_line = '|' + ' ' * half_separator_left_ + line + ' ' * half_separator_right_ + '|'
                    formatted_title_lines.append(formatted_title_line)

                print(separator)
                print('\n'.join(formatted_title_lines))
                print(separator)
            elif level == 1:
                formatted_title = '=' * half_separator_left + ' ' + title + ' ' + '=' * half_separator_right
                print(f"{formatted_title}")
            elif level == 2:
                formatted_title = '-' * half_separator_left + ' ' + title + ' ' + '-' * half_separator_right
                print(f"{formatted_title}")
        except:
            pass