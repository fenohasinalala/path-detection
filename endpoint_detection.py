import requests
port = '5000'
base_url = f'http://localhost:{port}'
wordListFileName = "dir_list.txt"
try:
    wordList = open(wordListFileName, 'r')
except Exception as e:
    print('Word list file cannot be opened:', wordListFileName)
    print('Error:', e)
    exit()

pathList = []

def collectPathList(wordDict):
    for word in wordDict:
        word = word.rstrip()
        print(f'trying {word}')
        url = f'{base_url}/{word}'
        response = requests.get(url)
        if response.status_code == 200 or response.status_code==500:
            pathList.append(url)

collectPathList(wordList)

print("Path available:")
for url in pathList:
    print(url)
