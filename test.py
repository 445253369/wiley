import re
article_url = 'https://onlinelibrary.wiley.com/journal/1600079x'
mode = r'https://.*?/journal/(\w+)'
pattern = re.compile(mode)
article_id = pattern.match(article_url).group(1)
print(article_id)