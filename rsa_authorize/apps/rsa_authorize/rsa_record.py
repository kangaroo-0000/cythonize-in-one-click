from utils.logger import Logger
import os
import sys
import traceback
import datetime

logger = Logger(__name__, os.getenv('log_path'))


def add_authorize_time(current_data: str, time_range: int):
    try:
        today = datetime.datetime.strptime(current_data, "%Y/%m/%d-%H:%M:%S")
        authorize_time_datetime = today + datetime.timedelta(days=time_range)
        # authorize_time = authorize_time_datetime.strftime("%Y/%m/%d-%H:%M:%S")
        return(authorize_time_datetime)
    except:
        message = " 處理授權日期時發生意外錯誤 "
        logger.debug(message)
        logger.debug(sys.exc_info())
        logger.debug(traceback.format_exc(1))
        return False
