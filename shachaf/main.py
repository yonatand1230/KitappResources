import shachaf, time, json
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from clipboard import copy


# init selenium
driver = webdriver.Chrome('chromedriver.exe')
url = "https://yba-gs.iscool.co.il/default.aspx"
driver.get(url)
time.sleep(1)

# select class
dropdown = driver.find_element(By.ID, 'dnn_ctr30678_TimeTableView_ClassesList')
select = Select(dropdown)
select.select_by_visible_text('י - 1')

# select schedule
btn = driver.find_element(By.ID, "dnn_ctr30678_TimeTableView_btnChangesTable")
btn.click()
time.sleep(1)

# get page html
html = driver.page_source

# get changes+holidays as dict using shachaf api
holidays = shachaf.get_holidays(html)
changes = shachaf.get_changes(html)

# dump all info into a json file
final = {
    'holidays': holidays,
    'changes': changes
    }

with open('changes.json', 'w') as f:
    f.write(json.dumps(final))
