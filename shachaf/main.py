import time, json
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from clipboard import copy
from shachaf import Shachaf

def sort(lst):
    final = {}

    for d in lst:
        day_number = d.get("day")
        hour = d.get("hour")
        body = d.get("body")
        if day_number not in final:
            final[day_number] = {}
        final[day_number][hour] = body
    return final


# init selenium
driver = webdriver.Chrome('chromedriver.exe')
url = "https://yba-gs.iscool.co.il/default.aspx"
driver.get(url)

# wait for the page to load
is_document_ready = driver.execute_script("return document.readyState === 'complete';")
while not is_document_ready:
    is_document_ready = driver.execute_script("return document.readyState === 'complete';")

# select grade
dropdown = driver.find_element(By.ID, 'dnn_ctr30678_TimeTableView_ClassesList')
select = Select(dropdown)

final = {} # init dict for final changes

options = select.options
x=1
for i in range(18, 24): # loop through yud 1 - yud 6
    ## STEP 1: GET PAGE HTML ##
    # select grade
    print("finding dropdown...")
    dropdown = driver.find_element(By.ID, 'dnn_ctr30678_TimeTableView_ClassesList') # find dropdown
    select = Select(dropdown)
    options = select.options # refresh options
    
    current_value = options[i].get_attribute('value')
    select.select_by_value(current_value)
    print("Grade selected! value=" + str(current_value)) #+ " text=" + options[i].get_attribute('text'))
    
    # select schedule
    print("opening schedule...")
    btn = driver.find_element(By.ID, "dnn_ctr30678_TimeTableView_btnChangesTable")
    btn.click()
    
    # wait for the page to load
    print("waiting for the page to load...")
    is_document_ready = driver.execute_script("return document.readyState === 'complete';")
    while not is_document_ready:
        is_document_ready = driver.execute_script("return document.readyState === 'complete';")
    print("page loaded!")
    
    # get page html
    print("Getting driver's html...")
    html = driver.page_source
    
    # need to rewrite this section - to make sure the page loaded correctly.
    """ 
    # make sure the page loaded correctly
    while 'Too many requests' in driver.page_source:
        print("too many requests. waiting for reload")
        time.sleep(20) # wait the appropriate time for the server to allow more requests
        print("reloading...")
        driver.refresh() # reload
        if not 'Too many requests' in driver.page_source:
            print("loaded correctly!")
            html = driver.page_source 
            print(html)
            dropdown = driver.find_element(By.ID, 'dnn_ctr30678_TimeTableView_ClassesList') # find dropdown
            select = Select(dropdown) # init dropdown
            options = select.options # get options
            current_value = options[i].get_attribute('value') # check for the desired grade
            select.select_by_value(current_value) # select the wanted option
            
            btn = driver.find_element(By.ID, "dnn_ctr30678_TimeTableView_btnChangesTable")
            btn.click()
    """    
    
    ## STEP 2: GET CHANGES+HOLIDAYS FROM HTML ##     
    print("finding changes and holidays...")
    holidays = Shachaf.get_holidays(html)
    changes = Shachaf.get_changes(html)

    # get current grade again (Refresh options)
    print("finding dropdown...")
    dropdown = driver.find_element(By.ID, 'dnn_ctr30678_TimeTableView_ClassesList')
    select = Select(dropdown)
    
    print("refreshing options...")
    options = select.options # refresh options
    current_grade = options[i].get_attribute('text')
    
    # replace grade name:
    shichva = current_grade[0]
    mispar_kita = current_grade[-1]
    
    current_grade = "כיתה " + shichva + "'" + mispar_kita
    
    # add all of the info to the final dict
    print("updating dict for grade: " + current_grade)
    final.update({
        current_grade: {
        'holidays': holidays,
        'changes': changes
        }
        })
    #if current_value == 35:
    time.sleep(3)
    print("\n\n") # a few blank lines before the next grade
    
# convert list of changes to a dict 
print("sorting dict...")
for i in list(final):
    changes = final[i]['changes'] # list of changes
    new_changes = sort(changes)
    final[i]['changes'] = new_changes


# dump all info into changes.json file
print("converting to json object...")
j = json.dumps(final, ensure_ascii=False, indent=2)

print("writing to file...")
with open(r'changes.json', 'w', encoding="utf-8") as f:
    f.write(j)
