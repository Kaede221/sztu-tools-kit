from selenium import webdriver
from win11toast import toast
from selenium.webdriver.common.by import By
import requests
import time
import yaml

username = ""
password = ""
outtime = 0

# 读取配置文件
with open("./config.yml", "r", encoding="utf-8") as f:
    res = yaml.load(f.read(), Loader=yaml.FullLoader)
    username = res["username"]
    password = res["password"]
    outtime = res["outtime"]
    print(
        f"配置文件读取成功! \t用户名: {username}\t密码: {password}\t超时时间: {outtime}"
    )

toast("运行成功!", "请保证连接到SZTU哦(否则无法判断)")


# 重连逻辑函数
def reconnect():
    # 这里才打开浏览器, 重新登陆
    driver = webdriver.Edge()
    driver.get("http://172.19.0.5/")
    driver.set_window_size(30, 30)

    # 找到输入框
    user_input = driver.find_element(By.ID, value="username")
    user_password = driver.find_element(By.ID, value="password")
    login_btn = driver.find_element(By.ID, value="login-account")
    time.sleep(1)

    # 输入账号密码
    user_input.send_keys(username)
    user_password.send_keys(password)
    time.sleep(1)

    # 登录
    login_btn.click()
    time.sleep(5)
    driver.close()


while True:
    # 60秒检查一次网络连接
    for i in range(outtime):
        time.sleep(1)
    # 判断网络状态
    try:
        r = requests.get("https://cn.bing.com/", timeout=(2, 3))
    except requests.exceptions.Timeout:
        reconnect()
