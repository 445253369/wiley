import re
import json

journal_url = []
with open('/Users/heshuwen/Desktop/代码/Wiley_Process/JSR_journal_name.json','r') as file:
    file_info = json.load(file)
    for file_url in file_info:
        file_url = file_url['journal_url']
        journal_url.append(file_url)

journal_urls = []
for ele in journal_url:
    target = 'springer'
    if ele.find(target) >= 0:
        journal_urls.append(ele)
        print(ele)
    else:
        continue

with open('/Users/heshuwen/Desktop/代码/spinger_craw/springer_url','w') as file:
    for line in journal_urls:
        file.write('{}\n'.format(line))


    