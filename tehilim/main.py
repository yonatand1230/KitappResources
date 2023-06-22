import bs4, requests, json, clipboard

### TEHILIM ###
print("-- TEHILIM --")
# Step 1 - GET HTML
print("Getting Remote HTML...")
response = requests.get("https://tehilim.co")
html = response.text


# Step 2 - SCRAP INFO
print("Scrapping...")
page = bs4.BeautifulSoup(html,features="html.parser")
l = page.find_all('h2')


# Step 3 - FILTER
print("Filtering...")
final = []

for i in l: 
    # i.next_sibling
    if "פרק " in i.text:
        final.append(i)

final2 = []

for i in final:
    if i['id'].strip()[:2] == 'cc':
        final2.append(i)
        print(i)

# Step 4 - Get final result
print("Getting final result...")

prakim = {}
for i in final2:
    prakim[i.get_text()] = i.next_sibling.get_text()


##########################


# Step 1 - Get HTML
print("-- AVOT --")
print("Getting Remote HTML...")
response = requests.get('https://oraita.net/avot/')
html = response.text

# Step 2 - Scrap
print("Scrapping...")
page = bs4.BeautifulSoup(html,features="html.parser")

ar = page.find('article')

number = ar.find('h1').get_text().strip()


p = ar.find('p')
for t in p.find_all('sup'):
    t.extract()

text = p.get_text().strip()

avot_final = {
    number: text
}


##########################


final = {
    "tehilim": prakim,
    "avot": avot_final
}

print("converting to json object...")
j = json.dumps(final, ensure_ascii=False, indent=2)

print("writing to file...")
with open('tehilim.json', 'w', encoding="utf-8") as f:
    f.write(j)

print("Done!")
