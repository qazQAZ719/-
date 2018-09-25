# encoding: utf-8
import time, os, sched

# 第一个参数确定任务的时间，返回从某个特定的时间到现在经历的秒数
# 第二个参数以某种人为的方式衡量时间
schedule = sched.scheduler(time.time, time.sleep)


def perform_command(cmd, inc):
    # 安排inc秒后再次运行自己，即周期运行
    schedule.enter(inc, 0, perform_command, (cmd, inc))
    os.system(cmd)


def timeing_exe(cmd, inc=60):
    # enter 用来安排某事件的发生时间，从现在起第n秒开始启动
    schedule.enter(inc, 0, perform_command, (cmd, inc))
    schedule.run()


print("1秒后：")
timeing_exe("python D://Jupyter//数据结构//红包//wxrb.py", 1)