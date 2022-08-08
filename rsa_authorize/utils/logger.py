import logging
from logging.handlers import RotatingFileHandler

# 定義顏色
FOREGROUND_WHITE = 0x0007
FOREGROUND_BLUE = 0x01  # text color contains blue.
FOREGROUND_GREEN = 0x02  # text color contains green.
FOREGROUND_RED = 0x04  # text color contains red.
FOREGROUND_YELLOW = FOREGROUND_RED | FOREGROUND_GREEN

class Logger:
    #clevel => cmd level, Flevel => File level
    def __init__(self, name, path='./logs/record.log', Flevel=logging.DEBUG):
        try:
            fmt = '[ %(asctime)20s ]-[%(levelname)s]-[{name}]-%(message)s'.format(name=name)# 輸出格式
            self.logger = logging.getLogger(name)
            
            # 如果已經建立過相名字的 logger , 則不用再追加 handler
            if not self.logger.handlers:
                self.logger.setLevel(Flevel) # 設定要寫入的資訊層級  CRITICAL > ERROR > WARNING > INFO > DEBUG
                # 文件日誌
                fh = RotatingFileHandler(filename=path, mode="a+", maxBytes=1024*1024, backupCount=1, encoding=None, delay=0)# 指定要寫入 log 檔的路徑
                fh.setFormatter(logging.Formatter(fmt))
                fh.setLevel(Flevel)
                self.logger.addHandler(fh)
        except:
            print(name)
            print("The log setting is failed")

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def war(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def cri(self, message):
        self.logger.critical(message)

# 記錄會到 logs 中的 record 中（P.S：注意相對路徑 "./logs/record.log" ）
# 基本使用
# from uvicore.logger import Logger
# log = Logger(Flevel=logging.DEBUG)
# log.debug(" Get_Files is Fail ")
# message = " Something bad is happend "
# raise HTTPException(status_code=500, detail=message)

# message = (" 取得單頁資料失敗 ")
# record_program_process(log, message)
# log.debug(sys.exc_info())
# log.debug(traceback.format_exc(1))