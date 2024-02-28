from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import json
import sys

type_dict={}

# 读入json文件
with open('type.json', 'r', encoding='utf-8') as file:
    type_dict = json.load(file)

print(type_dict)
def get_forex_rate(date, currency_code):

    driver = webdriver.Chrome()
    try:
        # 打开目标页面
        driver.get("https://www.boc.cn/sourcedb/whpj/")

        # 输入日期
        date_input = driver.find_element(By.NAME, "erectDate")
        date_input.clear()
        date_input.send_keys(date)

        # 清空另一个日期输入框并输入相同的日期
        date_input = driver.find_element(By.NAME, "nothing")
        date_input.clear()
        date_input.send_keys(date)

        # 定位货币类型选择框
        pjname = driver.find_element(By.NAME, 'pjname')

        # 移动鼠标到货币类型选择框并点击
        actions = ActionChains(driver)
        actions.move_to_element(pjname).click().perform()

        # 获取货币类型选择框中的所有选项
        options = pjname.find_elements(By.TAG_NAME, 'option')

        # 构建货币类型和选项索引的映射关系字典
        options_dict = {option.text: i for i, option in enumerate(options)}

        # 选择指定货币类型
        select = Select(pjname)
        select.select_by_index(options_dict[type_dict[currency_code]])

        # 点击查询按钮
        search_button = driver.find_element(By.XPATH, '//*[@id="historysearchform"]/div/table/tbody/tr/td[7]/input')
        search_button.click()

        # 等待页面加载完成
        time.sleep(1)

        # 获取页面源代码
        html = driver.page_source

        return html

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        driver.quit()

date = sys.argv[1]
currency_code = sys.argv[2]

forex_rate = get_forex_rate(date, currency_code)
soup=BeautifulSoup(forex_rate,"html.parser")

table=soup.find('table',{'cellpadding': '0', 'align': 'left', 'cellspacing': '0', 'width': '100%'})
tr=table.find_all('tr')[1] 
td=tr.find_all('td')[3]

with open("result.txt", "w", encoding="utf-8") as file:
    file.write(forex_rate)
print(td.text.strip())