
import os
import zipfile
import requests
from mailtm import Email
from re import findall
from queue import Queue
import threading
from time import time
from time import sleep
from random import choice
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
ele_appear =  EC.presence_of_element_located



class Reg:
    def __init__(self,driver:webdriver.Chrome):
        self.driver = driver
        self.wait = WebDriverWait(self.driver,10)
        self.email_xpath = '//*[@id="app"]/div[2]/main/div/section/section/div[1]/div/div[2]'
        self.recv = True
        self.email_addr = ""
        self.password = "Admin@2000"
        self.indentify_code = ""
        self.family_name = ["Lê","Nguyễn","Đào","Trịnh"]
        self.names = ["Tuấn","Vy","Ánh","Dương","Ngọc","Sơn"]
        self.fullname = ''
        self.coin = 0
        self.mail = Email()
    
    def Get_indentify_code(self,message):
        if not self.recv:return
        data_recv = message['text'] if message['text'] else message['html']
        self.indentify_code = findall(r'[0-9]{3,}',data_recv)[0]
        print("[ID CODE] :",self.indentify_code)
        self.recv = False
    
    def email_and_indentify_func(self):
        self.mail.register()
        self.email_addr = self.mail.address
        print("email adress:",self.email_addr)
        self.mail.start(self.Get_indentify_code,interval=1)
    
    def fill_info(self):
        email_xpath = '//*[@id="app"]/div[2]/main/div/section/section/div[2]/div[1]/div/label/div[2]/input'
        name_xpath = '//*[@id="app"]/div[2]/main/div/section/section/div[2]/div[3]/label/div[2]/input'
        password_xpath = '//*[@id="app"]/div[2]/main/div/section/section/div[2]/div[4]/label[1]/div[2]/input'
        re_password_xpath = '//*[@id="app"]/div[2]/main/div/section/section/div[2]/div[4]/label[2]/div[2]/input'
        common_btn = "common-button"
        input_code_xpath = '//*[@id="app"]/div[2]/main/div/section/div/label/div[2]/input'
        home_page_url = 'https://ktobongda.com/lobby/'
        giveawayurl = 'https://ktobongda.com/promotion/detail'

        while self.email_addr == "":print("đang đợi email ...")
        self.wait.until(ele_appear((By.XPATH,email_xpath))).send_keys(self.email_addr)
        self.fullname = f"{choice(self.family_name)} {choice(self.names)}"
        self.wait.until(ele_appear((By.XPATH,name_xpath))).send_keys(self.fullname)
        self.wait.until(ele_appear((By.XPATH,password_xpath))).send_keys(self.password)
        self.wait.until(ele_appear((By.XPATH,re_password_xpath))).send_keys(self.password)


        #click verified email
        self.wait.until(ele_appear((By.CLASS_NAME,common_btn))).click()
        #enter code
        while self.indentify_code == "":...
        self.wait.until(ele_appear((By.XPATH,input_code_xpath))).send_keys(self.indentify_code)
        #verify
        self.wait.until(ele_appear((By.CLASS_NAME,common_btn))).click()
        #return home page
        self.wait.until(ele_appear((By.XPATH,'//*[@id="app"]/div[2]/main/div/div/button[2]'))).click()
        self.driver.get(home_page_url)
        sleep(70)
        self.driver.get(giveawayurl)

        #click giveaway
        self.wait.until(ele_appear((By.XPATH,'//*[@id="app"]/div[2]/main/div/section[2]/div[1]/div[2]/div/div[2]'))).click()

        #commit
        try:
            self.wait.until(ele_appear((By.XPATH,'/html/body/div[5]/div/div[2]/button[2]'))).click()
            with open(str(int(time()) +".txt",'w')) as file:
                file.write(f"email: {self.email_addr}\npassword: {self.password}")
            sleep(5) # to load wallet

        except:...



    
    def run(self):
        try:
            self.driver.get("https://ktobongda.com/register/by")
            self.wait.until(ele_appear((By.CLASS_NAME,"common-button"))).click()
            self.wait.until(ele_appear((By.XPATH,self.email_xpath))).click()
            self.fill_info()
        except:
            print("oh cái này lỗi rồi")
        finally:
            self.driver.quit()

        #fill infor







# Khởi tạo hàng đợi công việc
jobs = Queue()

# Đọc danh sách các API keys từ file keys.txt
def read_keys():
    with open('keys.txt', 'r', encoding='utf-8') as f:
        return [line.strip() for line in f.readlines() if line.strip()]


# Lấy proxy mới từ API key
def new_ip(api_key):
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    if ':' in api_key:
        ipp, port, user, pas_ = api_key.split(":")
        ip = f"http://{user}:{pas_}@{ipp}:{port}"
        proxies = {"http": ip, "https": ip}
        return ip, proxies
    elif '-' in api_key:
        while True:
            try:
                ip = requests.get(f"https://wwproxy.com/api/client/proxy/available?key={api_key}&provincedId=-1", headers=headers).json()
                if ip["errorCode"] == 0:
                    ipcc = f"http://{ip['data']['proxy']}"
                    proxies = {"http": ipcc, "https": ipcc}
                    return ipcc, proxies
                elif ip["errorCode"] == 1 and "không tồn tại trên hệ thống" in str(ip):
                    break
                for ll in range(15, -1, -1):
                    print(f"Vui lòng đợi {ll} giây để đổi IP lần nữa", end="\r")
                    sleep(1)
            except Exception:
                continue

        while True:
            try:
                ip_me = requests.get('https://api.ipify.org/?format=json', headers=headers).json()["ip"]
                ip = requests.get(f"https://app.proxydt.com/api/public/proxy/get-new-proxy?license={api_key}&authen_ips={ip_me}", headers=headers).json()
                if ip["code"] == 1:
                    ipcc = ip['data']['http_ipv4']
                    proxies = {"http": ipcc, "https": ipcc}
                    return ipcc, proxies
                elif "Không tìm thấy license" in str(ip) or "Yêu cầu license key & whitelist Ip!" in str(ip) or 'Token không hợp lệ.' in str(ip):
                    print(ip)
                    return "KEYEXPIRED"
                for ll in range(5, -1, -1):
                    print(f"Vui lòng đợi {ll} giây để đổi IP lần nữa", end="\r")
                    sleep(1)
            except Exception:
                continue

    while True:
        try:
            ip = requests.get(f'https://api.kiotproxy.com/api/v1/proxies/new?key={api_key}', headers=headers).json()
            if ip["code"] == 200:
                ipcc = f"http://{ip['data']['http']}"
                proxies = {"http": ipcc, "https": ipcc}
                return ipcc, proxies
            else:
                for ll in range(int(ip['message'].split('sau')[1].split('giây')[0]), -1, -1):
                    print(f"Vui lòng đợi {ll} giây để đổi IP lần nữa", end="\r")
                    sleep(1)
        except Exception:
            continue

# Tạo và cấu hình trình duyệt Chrome với proxy
def get_chromedriver(ipcc=None):
    chrome_options = webdriver.ChromeOptions()
    if ipcc:
        if '@' in ipcc:
            user_pass, ip_host = ipcc.replace('http://', '').split('@')
            PROXY_HOST, PROXY_PORT = ip_host.split(':')
            PROXY_USER, PROXY_PASS = user_pass.split(':')
            manifest_json = """
            {
                "version": "1.0.0",
                "manifest_version": 2,
                "name": "Chrome Proxy",
                "permissions": [
                    "proxy",
                    "tabs",
                    "unlimitedStorage",
                    "storage",
                    "<all_urls>",
                    "webRequest",
                    "webRequestBlocking"
                ],
                "background": {
                    "scripts": ["background.js"]
                },
                "minimum_chrome_version":"22.0.0"
            }
            """
            background_js = """
            var config = {
                mode: "fixed_servers",
                rules: {
                    singleProxy: {
                        scheme: "http",
                        host: "%s",
                        port: parseInt(%s)
                    },
                    bypassList: ["localhost"]
                }
            };

            chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

            function callbackFn(details) {
                return {
                    authCredentials: {
                        username: "%s",
                        password: "%s"
                    }
                };
            }

            chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
            );
            """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

            path = os.path.dirname(os.path.abspath(__file__))
            pluginfile = 'proxy_auth_plugin.zip'

            with zipfile.ZipFile(pluginfile, 'w') as zp:
                zp.writestr("manifest.json", manifest_json)
                zp.writestr("background.js", background_js)
            chrome_options.add_extension(pluginfile)
        else:
            chrome_options.add_argument(f'--proxy-server={ipcc}')
    chrome_options.add_argument('--log-level=3')
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# Hàm thực thi công việc với proxy và mở trang web
def run(location, key):
    ipcc, proxies = new_ip(key)
    if ipcc == "KEYEXPIRED":
        print(f"API key {key} đã hết hạn.")
        return
    driver = get_chromedriver(ipcc)
    driver.set_window_size(500, 900)
    reg = Reg(driver)
    thread = threading.Thread(target= reg.email_and_indentify_func)
    thread.start()
    reg.run()

# Chạy công việc trong các luồng
def do_stuff():
    global jobs
    while not jobs.empty():
        location = jobs.get()
        for key in read_keys():
            run(location, key)
            sleep(2)  # Đợi một chút giữa các lần chạy
        jobs.task_done()

def main():
    # Thay thế 'location_placeholder' bằng thông tin thực tế
    global jobs
    jobs.put('location_placeholder') 

    keys = read_keys()
    num_threads = len(keys)
    
    for i in range(num_threads):
        print(f'Luồng {i}: Bắt đầu tạo chạy!')
        worker = threading.Thread(target=do_stuff)
        worker.start()
    
    jobs.join()

main()