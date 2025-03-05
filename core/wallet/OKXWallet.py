import time
import random
from loguru import logger
from DrissionPage import Chromium,ChromiumOptions
def login_with_private_key(private_key,page_info):


    tab1 = page_info
    logger.debug(type(tab1))
    time.sleep(1)
    tab1.get('chrome-extension://mcohilncbfahbmgdjkbpemcciiolgcge/home.html')
    input_button = tab1.ele('@@tag():button@@text():导入已有钱包')
    if input_button:
        input_button.click()
        time.sleep(random.random())

    private_key_button = tab1.ele('@text():助记词或私钥')
    if private_key_button:
        private_key_button.click()
        time.sleep(random.random())

    #点击私钥按钮，页面元素复杂使用xpath
    private1 = tab1.ele('xpath:/html/body/div/div/div[1]/div/div[2]/div/div[1]/div/div[2]/div/div[2]')
    if private1:
        private1.click()
        time.sleep(random.random())

    private_key_input = tab1.ele('@tag():textarea')
    if private_key_input:
        private_key_input.input(private_key)
        time.sleep(3)

    yes_button = tab1.ele('@@data-testid=okd-button@@text():确认')
    if yes_button:
        yes_button.click()
        time.sleep(2)
        logger.info(f'私钥输入成功')

    yes_button2= tab1.ele('@@data-testid=okd-button@@text():确认')
    if yes_button2:
        yes_button2.click()
        time.sleep(random.random())

    yanzheng_button = tab1.ele('@text():密码验证')
    if yanzheng_button:
        yanzheng_button.click()
        time.sleep(random.random())

    next_step = tab1.ele('@@tag():button@@text():下一步')
    if next_step:
        next_step.click()
        time.sleep(random.random())

    #输入钱包的密码
    input_pwd = tab1.ele('xpath:/html/body/div/div/div[1]/div/div[2]/form/div[1]/div[2]/div/div/div/div/input')
    if input_pwd:
        input_pwd.input('asdfzxcv')
        time.sleep(random.random())
    #确认钱包密码
    input_pwd1 = tab1.ele('xpath:/html/body/div/div/div[1]/div/div[2]/form/div[3]/div[2]/div/div/div/div/input')
    if input_pwd1:
        input_pwd1.input('asdfzxcv')
        time.sleep(random.random())
    #提交
    yes_button3 = tab1.ele('@@data-testid=okd-button@@text():确认')
    if yes_button3:
        yes_button3.click()
        time.sleep(random.random())
        logger.info(f'设置钱包密码成功')

    #选择导入evm网络
    evm_button = tab1.ele('@@tag():span@@text()：EVM 网络')
    if evm_button:
        evm_button.click()
        time.sleep(random.random())

    yes_button3= tab1.ele('@@data-testid=okd-button@@text():确认')
    if yes_button3:
        yes_button3.click()
        time.sleep(random.random())

    # button_final = tab1.ele('@@data-testid=okd-button@@text():开启你的 Web3 之旅')
    # if button_final:
    #     button_final.click()
    logger.success(f'使用私钥登陆okx钱包成功')
    return True


def login_with_key_word(key_word,page_info):

    tab1 = page_info
    time.sleep(1)
    tab1.get('chrome-extension://mcohilncbfahbmgdjkbpemcciiolgcge/home.html')
    input_button = tab1.ele('@@tag():button@@text():导入已有钱包')
    if input_button:
        input_button.click()
        time.sleep(random.random())

    private_key_button = tab1.ele('@text():助记词或私钥')
    if private_key_button:
        private_key_button.click()
        time.sleep(random.random())

    # 键入12个助记词
    str1 = key_word.split()
    try:
        for i in range(1, 13):
            tab1.ele(f'xpath:/html/body/div/div/div[1]/div/div[2]/div/div[2]/div/div/form/div[1]/div[2]/div[{i}]/div[2]/input').input(str1[i - 1])
    except Exception as e:
        print(f"注记词单词输入错误： {e}")

    time.sleep(random.random())
    #助记词输入结束的确认按钮
    yes_button = tab1.ele('@@tag():button@@text():确认')
    if yes_button:
        yes_button.click()
        logger.info(f'输入助记词单词成功')
        time.sleep(random.random())

    yes_button2= tab1.ele('@@data-testid=okd-button@@text():确认')
    if yes_button2:
        yes_button2.click()
        time.sleep(random.random())

    yanzheng_button = tab1.ele('@text():密码验证')
    if yanzheng_button:
        yanzheng_button.click()
        time.sleep(random.random())

    next_step = tab1.ele('@@tag():button@@text():下一步')
    if next_step:
        next_step.click()
        time.sleep(random.random())

    input_pwd = tab1.ele('xpath:/html/body/div/div/div[1]/div/div[2]/form/div[1]/div[2]/div/div/div/div/input')
    if input_pwd:
        input_pwd.input('asdfzxcv')
        time.sleep(random.random())
    input_pwd1 = tab1.ele('xpath:/html/body/div/div/div[1]/div/div[2]/form/div[3]/div[2]/div/div/div/div/input')
    if input_pwd1:
        input_pwd1.input('asdfzxcv')
        time.sleep(random.random())
    #提交
    yes_button3 = tab1.ele('@@data-testid=okd-button@@text():确认')
    if yes_button3:
        yes_button3.click()
        time.sleep(random.random())
        logger.info(f'设置钱包密码成功')

    #选择倒入钱包的网络
    evm_button = tab1.ele('@@tag():span@@text()：EVM 网络')
    if evm_button:
        evm_button.click()
        time.sleep(random.random())

    yes_button3= tab1.ele('@@data-testid=okd-button@@text():确认')
    if yes_button3:
        yes_button3.click()
        time.sleep(random.random())

    button_final = tab1.ele('@@data-testid=okd-button@@text():开启你的 Web3 之旅')
    if button_final:
        logger.success(f'使用助记词登陆okx钱包成功')

    return True

if __name__ == '__main__':
    co = ChromiumOptions()
    co.auto_port()
    # 添加插件（path放路径）
    co.add_extension(
        path=r"../extension/okxWallet/3.37.0_1")
    # 配置浏览器信息
    browser = Chromium(addr_or_opts=co)

    tab = browser.new_tab()
    time.sleep(15)
    login_with_private_key('8c967fcaad98d7d98f858d7ceb6845c79e1320fcae65df8350b0e0e1931dccde',tab)
    time.sleep(100)