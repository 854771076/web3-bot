import os
import sys
import time
from DrissionPage import Chromium,ChromiumOptions
from core.wallet.OKXWallet import login_with_private_key
from loguru import logger
from faker import Faker
from random import randint
import random
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from core.utils import EmailOauth2Sync
from core.bot.basebot import *
#使用okx钱包登陆项目
def login(tab,wallet_tab):
    try:
        tab.get('https://testnet.humanity.org/login?ref=kamibaba')
        tab.ele('@@tag():button@@text():Connect Wallet',timeout=120).click()
        tab.ele('@@tag():button@@text():MetaMask').click()
        logger.info('开始连接钱包')
        wallet_tab.ele('@@tag():button@@text():连接').click()
        tab.ele('@@tag():button@@text():发送消息').click()
        wallet_tab.ele('xpath:/html/body/div[1]/div/div/div/div/div/div[4]/div/button[2]').click()
        logger.success('连接钱包成功')
        time.sleep(5)
    except Exception as e:
        logger.error(e)
        return False
    return True


def register(tab,email:str,
        email_id:str,
        email_refresh_token:str):
    try:
        already_registered = tab.ele('@@tag():p@@text():Loading your profile...')
        if already_registered:
            logger.success('已经注册成功')
            tab.close()
            return True
        faker = Faker()
        num  = str(randint(999,9999))
        firstName = faker.first_name()
        lastName = faker.last_name()
        humanId =firstName+num+lastName
        human_id = tab.ele('@@tag():input@@id=identification.hp_username')
        if human_id:
            human_id.clear()
            human_id.input(humanId)
            time.sleep(2)
        tab.ele('@@tag():button@@text():Next',timeout=300).click()
        logger.info('设置humanID成功')

        first_name = tab.ele('@id=profile.first_name')
        if first_name:
            first_name.clear()
            first_name.input(firstName)
        last_name = tab.ele('@id=profile.last_name')
        if last_name:
            last_name.clear()
            last_name.input(lastName)
        time.sleep(1)
        email_address = tab.ele('xpath:/html/body/div[1]/div/div/div[2]/div/form/div[1]/div[3]/div/input')
        if email_address:
            email_address.clear()
            email_address.input(email)
            time.sleep(random.random())

        confirm_email = tab.ele('xpath:/html/body/div[1]/div/div/div[2]/div/form/div[1]/div[4]/div/input')
        if confirm_email:
            confirm_email.clear()
            confirm_email.input(email)
            time.sleep(random.random())
        next = tab.ele('@@tag():button@@text():Next')
        if next:
            next.click()
        check = tab.ele('@@tag():p@@text():Please enter the code sent to',timeout=120)
        if check:
            time.sleep(3)
            mail=EmailOauth2Sync(email,email_refresh_token,email_id)
            code = mail.listening_unsee_mails(get_code=True)
            if code:
                logger.info('获取验证码成功')
                tab.ele('xpath:/html/body/div[1]/div/div/div[2]/div/div[2]/div/div[2]/div/div[1]/input').input(code)
                logger.info('注册使用的邮箱输入成功')
            else:
                logger.info('使用验证码失败')
                return False
        else:
            logger.info('获取验证码失败')
            return False
        vf = tab.ele('xpath:/html/body/div[1]/div/div[2]/div/div[5]/div/div[3]')
        if vf:
            vf.click()
        return True
    except Exception as e:
        logger.error(e)
        return False


def work(email:str,
        email_id:str,
        email_refresh_token:str,private_key):
    co = ChromiumOptions()
    co.auto_port()
    #添加插件（path放路径）
    co.add_extension(
        path=r"extension/okxWallet/3.37.0_1")
    #配置浏览器信息
    browser = Chromium(addr_or_opts=co)
    #加载浏览器插件时间
    time.sleep(10)

    #钱包的标签页
    tab1 = browser.new_tab()
    browser.close_tabs(tab1, True)
    logger.info('关闭弹出页面')

    #使用私钥导入okx钱包
    wallet_login = login_with_private_key(private_key=private_key,page_info=tab1)
    if not wallet_login:
        browser.quit()
        return False

    #项目页面的标签页
    tab2 = browser.new_tab()
    #实现humanity的登陆
    connect = login(tab=tab2,wallet_tab=tab1)
    if not connect:
        browser.quit()
        return False
    register_vf = register(tab= tab2,email=email,email_id=email_id,email_refresh_token=email_refresh_token)
    if not register_vf:
        browser.quit()
        return False
    browser.quit()
    return email,email_id,email_refresh_token,private_key

def save_data(success):
    df=pd.DataFrame(success)
    df.to_csv('success.csv', index=False)
    logger.success('成功数据已保存')


def concurrent_e(tasks, max_workers, work):
    success = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交任务(多参数为 work ，a， b) work为方法名，data为任务数据
        futures = [executor.submit(work, **data) for data in tasks]
        # 等待所有任务完成
        for future in as_completed(futures):
            try:
                result = future.result()
                if not result:
                    logger.info('注册失败')
                else:
                    success.append(result)
                    logger.success(f'任务完成,私钥： {result}')
                    save_data(success)
            except Exception as e:
                logger.error(e)
    logger.success('Finished All Tasks')


class HumanityManager(BaseBotManager):
    def run_single(self,account):
        work(account['email'],account['email_id'],account['email_refresh_token'],account['private_key'])
       
    def run(self):
        with ThreadPoolExecutor(max_workers=self.config.max_worker) as executor:
            futures = [executor.submit(self.run_single, account) for account in self.accounts if not account.get('x_token_bad')]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logger.error(f"执行过程中发生错误: {e}")


# if __name__ == '__main__':
#     #线程池线程数（建议按照资源尝试修改，默认为单线程）
#     max_workers = 1
#     #账号信息的文件访问（需要修改为自己的文件路径）
#     tasks = pd.read_csv('account.csv').to_dict('records')
#     concurrent_e(tasks, max_workers, work)