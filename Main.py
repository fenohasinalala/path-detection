import os
import re
import threading
import time
import requests
import logging
from dotenv import load_dotenv
from WordListFunction import (
    createWordListFromFileList,
    divideList,
    getFilenamesFromDirectory,
)

# Configure logging
logging.basicConfig(
    filename="error.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


# Load environment variables from the .env file
load_dotenv()


# check if url given by user is valid
def isValidUrl(url):
    # Regular expression pattern for matching URLs
    url_pattern = re.compile(
        r"^(?:http|https)://"  # Scheme (http or https)
        r"(?:\w+\.)+\w+"  # Domain name (e.g., example.com)
        r"(?:\:\d+)?"  # Port number (optional)
        r"(?:\/\S*)?"  # Path (optional)
        r"(?:\.\w{2,})?"  # TLD (optional, minimum 2 characters)
        r"$"
    )
    return bool(url_pattern.match(url))


# set base URL from user input and retry if not valid
def setBaseUrlFromUserInput():
    global baseUrl
    try:
        url = input(
            "Enter the base URL (example: http://127.0.0.1:5000 or https://api.publicapis.org) :\n"
        )
        if isValidUrl(url):
            baseUrl = url.strip()
        else:
            print(f"{url} is NOT a valid URL.")
            raise ValueError(f"{url} is NOT a valid URL.")
    except Exception as e:
        logging.error(e)
        setBaseUrlFromUserInput()


# check if the desired thread count is valid number positive and less or equal maximum thread count
def isValidNumber(threadNumber, minThreadCount, maxThreadCount):
    try:
        threadNumber = int(threadNumber)
        if minThreadCount <= threadNumber <= maxThreadCount:
            return True
        return False
    except ValueError:
        return False


# set thread count from user input and retry if not valid thread count
def setThreadCountFromUserInput():
    global threadsCount
    try:
        minThreadCount = 1
        maxThreadCount = os.cpu_count()
        threadNumber = input(
            f"Enter desired thread count between {minThreadCount} and {maxThreadCount} (max thread available):\n"
        )
        if isValidNumber(threadNumber, minThreadCount, maxThreadCount):
            threadsCount = int(threadNumber)
        else:
            print(f"{threadNumber} is NOT valid.")
            raise ValueError(f"{threadNumber} is NOT valid.")
    except Exception as e:
        logging.error(e)
        setThreadCountFromUserInput()


# check with the HTTP response status code if the path from a request is accessible and not protected
def isAccessiblePath(statusCode):
    # get server error status code: need network authentication
    if statusCode == 511:
        return False
    # get client error status code: resource protected or not available; type of request not allowed by the server
    if statusCode in (401, 403, 404, 405, 407, 410, 414, 418, 421, 451):
        return False
    # get information response status code   -> (100-199)
    # get successful response status code    -> (200-299)
    # get redirection status code            -> (300-399)
    # get client error status code: need to change to header or the body
    # -> (400-499) except for (401,403,404,405,407,410,414,418,421,451)
    # get server error status code: implementation error or server cannot handle unexpected client request or server not functional at the moment
    # -> (500-599) except for 511
    return True


# perform requests with different paths (for word from a word list), then collect the accessible and not protected ones
def collectPathList(wordDict, threadNumber):
    global exception_flag  # To access the event flag
    try:
        for word in wordDict:
            word = word.rstrip()
            print(f"Thread {threadNumber} - trying {word}")
            url = f"{baseUrl}/{word}"
            response = requests.get(url)
            if isAccessiblePath(response.status_code):
                # not duplicate path
                if url not in pathList:
                    pathList.append(url)
    except Exception as e:
        logging.error(e)
        print(
            f"Error while sending request to the server {baseUrl} with thread {threadNumber} ",
            url,
        )
        exception_flag.set()  # Set the event flag to indicate an exception
        return  # Exit the function early


##  SPECIFY ALL PARAMS HERE
baseDirectory = os.getenv("baseDirectory", "word_list")
threadsCount = 0  # Number of threads
baseUrl = None
pathList = []
exception_flag = threading.Event()  # Event to signal if an exception occurred
setBaseUrlFromUserInput()
setThreadCountFromUserInput()
start_time = time.time()

wordListFileName = "dir_list.txt"

# create a list of words list from the directory containing words list files
files = getFilenamesFromDirectory(baseDirectory)
wordList = createWordListFromFileList(baseDirectory, files)
# divide the large list into smaller sublists according to the thread count
subList = divideList(wordList, threadsCount)

threads = list()  # Create an empty list of threads
for index in range(threadsCount):  # iterate through the threads count
    # create a new thread for each thread that launches the function collectPathList with the corresponding sublist of paths
    x = threading.Thread(target=collectPathList, args=(subList[index], index))
    # add each Thread to "threads" list
    threads.append(x)
    # then start the task of the thread
    x.start()
# For each thread call the method join(). This ensures that the main thread waits for all the spawned threads to finish before proceeding further.
for index, thread in enumerate(threads):
    thread.join()

# Check if an exception occurred
if exception_flag.is_set():
    print("Application terminated due to an error.")
    print("Enter a working server address")
    exit(1)  # Exit with error code 1

# display all paths collected
print("\n", "Found the following path:")
for url in pathList:
    print(url)

# Track the time spent executing the application after the user inputs to the end of the execution
end_time = time.time()
execution_time = end_time - start_time
print("\n", "Execution time:", execution_time, "seconds", "\n")
