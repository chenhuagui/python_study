import time
import tkinter as tk

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import wait, ui
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import threading


def execute_it():
    log("Thread Start")
    start_button_text.set("停止任务")
    while task_started:
        log('converting . . .')
        time.sleep(3)
        start_query()
        log('convert finished')
        time.sleep(2)
    log("Thread Stop")
    start_button_text.set("开始任务")


def thread_it(func, *args):
    global task_started
    global main_thread
    task_started = not task_started

    if task_started:
        # 创建线程
        main_thread = threading.Thread(target=func, args=args)
        main_thread.setDaemon(True)
        main_thread.start()
    else:
        log("等待次轮查询完毕，任务即结束")


def start_query():
    if "baidu.com" not in driver.current_url:
        print("初次加载")
        url = 'https://www.baidu.com'
        driver.get(url)
    else:
        print("已加载无需重复加载")

    # 定位输入框
    input_box = driver.find_element(By.XPATH, "//input[@id='kw']")
    try:
        # 输入内容：selenium
        input_box.send_keys('selenium')
        print('搜索关键词：selenium')
    except Exception as e:
        print('fail')

    # 定位搜索按钮
    button = driver.find_element(By.ID, 'su')
    try:
        # 点击搜索按钮
        # button.click()
        input_box.submit()
        log('成功搜索')
    except Exception as e:
        log('fail搜索')

    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "s_is_result_css"))
        );
    except TimeoutException as e:
        log(e)

    try:
        element = driver.find_element(By.ID, "s_is_result_css");
        log(element)
    except Exception as e:
        log(e)

    return True


def log(text):
    print(text)
    hint.set(text)


# 创建浏览器句柄
driver = Chrome()

task_started = False

main_thread = None

# 创建UI界面
window = tk.Tk()
window.title('格式转换')
window.geometry('450x300')
window.resizable(False, False)

version_label = tk.Label(window, text='格式转换').place(x=10, y=10)

uuid_label = tk.Label(window, text='输入文件:').place(x=10, y=50)

start_button_text = tk.StringVar()
start_button = tk.Button(window, textvariable=start_button_text, command=lambda: thread_it(execute_it)).place(x=150, y=100)
start_button_text.set("开始任务")

# 日志打印
hint = tk.StringVar()
hint.set('')
tk.Label(window, textvariable=hint).place(x=10, y=140)

window.mainloop()
