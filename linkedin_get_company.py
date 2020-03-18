from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from getpass import getpass
import requests
import pprint
import time,random
import sys
import argparse

options = Options()
options.add_argument('--disable-infobars')
options.add_argument("--disable-extensions")
# options.add_argument("--no-sandbox")  # only needed if running as root

# need to make this an option
options.add_argument("--user-data-dir=/tmp/");
# options.add_argument("--profile-directory=Default");



def get_details(driver):
    # results = driver.find_elements_by_class_name("search-result__wrapper")
    results = driver.find_elements_by_class_name("search-result__wrapper")
    for r in results:
        line = ''.join(r.text.split(',')).split('\n')
        x = ','.join(line).split('/n')
        if '2nd' in x[0]:
            x = x[0].replace(',2nd degree connection,2nd', '')
        elif '3rd' in x[0]:
            x = x[0].replace(',3rd degree connection,3rd', '')
        else:
            x = x[0]
        people_list.append(x)


def writeout(line):
    with open('./outfile.txt','a+') as f:
        f.write(line)




if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-id", "--companyid", required=True, help="Company ID number eg: 121247 ")
    ap.add_argument("-u", "--username", required=True, help="Linkedin Username")
    ap.add_argument("-p", "--password", required=False, type=int, help="Linkedin Password")
    ap.add_argument("-c", "--chromepath", required=True, help="Path to the chrome driver ")
    args = vars(ap.parse_args())

    if not args['companyid']:
        print(" You  must enter a company ID. This can be found manually by searching for the company\
            in Linkedin, clicking see all people, and copying the 'facetCurrentCompany' digits.")

    compID = args['companyid']
    username = args['username']

    if args['password'] is None:
        password = getpass('Enter your Linkedin password: ')
    else:
        print('password')
        password = args['password']



    chrome_path = args['chromepath']
    driver = webdriver.Chrome(chrome_path,chrome_options=options)
    driver.get("https://linkedin.com")

    try:
        driver.find_element_by_xpath("""/html/body/nav/a[3]""").click()
        driver.find_element_by_xpath("""//*[@id="username"]""").send_keys(username)
        driver.find_element_by_xpath("""//*[@id="password"]""").send_keys(password)
        driver.find_element_by_xpath("""//*[@id="app__container"]/main/div/form/div[4]/button""").click()
        driver.get('https://www.linkedin.com/search/results/people/?facetCurrentCompany={}'.format(compID))

        # Get the final page of people
        ep = driver.find_element_by_xpath("""/html/body/div[5]/div[3]/div[3]/div/div[2]/div/div[2]/div/div/div/div/div[2]/artdeco-pagination/ul""").text.split('\n')[-1]
        ep = int(ep)
        print('[+] Getting {} pages'.format(ep))

        i = 1
        while i <= ep:
            people_list = []
            driver.get('https://www.linkedin.com/search/results/people/?facetCurrentCompany={}&page={}'.format(compID,str(i)))
            get_details(driver)
            i+=1
            time.sleep(random.randrange(10,30))

            for r in people_list:
                writeout(r+"\n")

    except Exception as e:
        print(str(e))
        # import pdb
        # pdb.set_trace()
        # input('waiting')



# notes
# if using snap version of chromium, must use snap driver at /snap/bin/chromium.chromedriver
# if root, must use --no-sandbox options

#chrome_path = './win_chromedriver_77.exe'
# chrome_path = './chromedriver_79'
# chrome_path = '/snap/bin/chromium.chromedriver'