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

#check with http response status code if the path from request is accessible and not protected
def isAccessiblePath(statusCode):
    #get client error status code, resource protected or type of request not allowed by the server
    if (statusCode in (401,403,404,405,407,410,414,418,421,451)):
        return False
    #get server error status code, need network authentication
    if (statusCode in (511)):
        return False
    #get information response status code   -> (100-199)
    #get successful response status code    -> (200-299)
    #get redirection status code            -> (300-399)
    #get client error status code, need to change to header or the body 
    # -> (400-499) except for (401,403,404,405,407,410,414,418,421,451)
    #get server error status code, implementation error or server connot handle unexpected client request or server not fonctional at the moment 
    # -> (500-599) except for 511
    return True


def collectPathList(wordDict):
    for word in wordDict:
        word = word.rstrip()
        print(f'trying {word}')
        url = f'{base_url}/{word}'
        response = requests.get(url)
        if isAccessiblePath(response.status_code):
            pathList.append(url)

collectPathList(wordList)

print("Accessible paths:")
for url in pathList:
    print(url)
