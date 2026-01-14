# pip install croniter

from croniter import croniter
from datetime import datetime
from feishu_demo import send_feishu_msg
import time
# CRON 表达式：每周一到周五的晚上 8:55 执行
# cron_expr = "55 20 * * 1-5"

cron_expr = "*/5 * * * 1-5"
base_time = datetime.now()  # 当前时间作为基准时间
iter = croniter(cron_expr, base_time)

while True:
    # 获取下一个执行时间
    next_time = iter.get_next(datetime)
    print("下一次执行时间:", next_time)
    now = datetime.now()
    wait_time = (next_time - now).total_seconds()
    
    # 如果等待时间小于0，说明已经错过了这个时间点，跳过
    if wait_time < 0:
        continue
    
    # 等待直到下一个执行时间
    time.sleep(wait_time)
    
    send_feishu_msg()
