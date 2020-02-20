import requests

user = 'alvinpastore'
url = 'https://api.github.com/'
with open('../misc/git_token', 'r') as api_token_file:
    api_token = api_token_file.readline()

headers = {'Authorization': 'token ' + api_token}
r = requests.get(url, headers=headers)

print(r.status_code)
print(r.headers['content-type'])
print(r.encoding)
print(r.text)
print(r.json())
