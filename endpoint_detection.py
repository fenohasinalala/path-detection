import requests
import os
import threading
import time

start_time = time.time()

##  FUNCTIONS DEFINITION

#open a text file, and create create a list of words from it
def createWordListFromFile(filename):
    wordlist = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                # Remove leading and trailing whitespace, then append to the list
                wordlist.append(line.strip())
        return wordlist
    except Exception as e:
        print('Word list file cannot be opened:', filename)
        print('Error:', e)
        exit()


#divide a list into x sub-lists, here x represents the threads number and the list is the words list
def divideList(word_list, x):
    # Calculate the length of each sublist
    sublist_length = (len(word_list) + x - 1) // x  # Round up division
    # Create sublists using list comprehension
    sublists = [word_list[i:i+sublist_length] for i in range(0, len(word_list), sublist_length)]
    return sublists


#check with http response status code if the path from request is accessible and not protected
def isAccessiblePath(statusCode):
    #get client error status code: resource protected or not available ; type of request not allowed by the server
    if (statusCode in (401,403,404,405,407,410,414,418,421,451)):
        return False
    #get server error status code: need network authentication
    if (statusCode == 511):
        return False
    #get information response status code   -> (100-199)
    #get successful response status code    -> (200-299)
    #get redirection status code            -> (300-399)
    #get client error status code: need to change to header or the body 
    # -> (400-499) except for (401,403,404,405,407,410,414,418,421,451)
    #get server error status code: implementation error or server connot handle unexpected client request or server not fonctional at the moment 
    # -> (500-599) except for 511
    return True

pathList = []


#perform request with different path (for word from a word list), then collect the accessible and not protected ones
def collectPathList(wordDict, threadNumber):
    for word in wordDict:
        word = word.rstrip()
        print(f'Thread {threadNumber} - trying {word}')
        url = f'{baseUrl}/{word}'
        response = requests.get(url)
        if isAccessiblePath(response.status_code):
            pathList.append(url)

##  SPECIFY ALL PARAMS HERE
port = '5000'
baseUrl = f'http://127.0.0.1:{port}'
wordListFileName = "dir_list.txt"
desiredThreadsCount = 3 #specify the number of threads you want
threadsCount = min(max(1,desiredThreadsCount), os.cpu_count()) #the thread number is between 1 and cpu max threads count

## MAIN APP START
# create a list of words list from filename
wordList = createWordListFromFile(wordListFileName)
# divide the large list into smaller sublists according to the thread count
subList = divideList(wordList,threadsCount)

threads = list() #create an empty list of threads
for index in range(threadsCount): #iterate through the threads count
    #create a new thread for each thread that launch the function collectPathList with the corresponding sublist of paths
    x = threading.Thread(target=collectPathList, args=(subList[index],index))
    #add each Thread to "threads" list
    threads.append(x)
    #then start the task of the thread
    x.start()
#for each thread call the method join(). This ensures that the main thread waits for all the spawned threads to finish before proceeding further.
for index, thread in enumerate(threads):
    thread.join()

#Track the time spent executing the application
end_time = time.time()
execution_time = end_time - start_time
print("\n","Execution time:", execution_time, "seconds","\n")

# display all paths collected
print("Found the following path:")
for url in pathList:
    print(url)