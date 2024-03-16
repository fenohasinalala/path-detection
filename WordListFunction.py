##  FUNCTIONS DEFINITION


def createWordListFromFile(filename):
    wordlist = []
    try:
        with open(filename, "r") as file:
            for line in file:
                # Remove leading and trailing whitespace, then append to the list
                wordlist.append(line.strip())
        return wordlist
    except Exception as e:
        print("Word list file cannot be opened:", filename)
        print("Error:", e)
        exit()


# divide a list into x sub-lists, here x represents the threads number and the list is the words list
def divideList(word_list, x):
    # Calculate the length of each sublist
    sublist_length = (len(word_list) + x - 1) // x  # Round up division
    # Create sublists using list comprehension
    sublists = [
        word_list[i : i + sublist_length]
        for i in range(0, len(word_list), sublist_length)
    ]
    return sublists
