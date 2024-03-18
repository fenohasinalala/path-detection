# PATH DETECTION

## Description

This path detection application is designed for terminal use (CLI). It looks for a list of URLs accessible in a server by mapping each word present in multiple word list files.

This application can look for words in every word list file placed in a specified directory.

The user can specify the desired theard to use; the max thread capacity of the CPU is shown at the input.  

## Other aspects

This application also has a logger for errors, all errors that occur are logged in the 'error.log' file.

It follows the coding standard PEP8 for Python and uses Ruff as a linter and formatter.
Here is how to use Ruff:

- to install :

```bash
pip install ruff
```

- to lint :

```bash
ruff check . # can add '--fix' parameter for small fix
```

- to format :

```bash
ruff format .
```

## Requirement

### Python Installation

Depending on the OS:

[Download and install](https://www.python.org/downloads/) Python 3.10 or higher

### Dependencies Installation

```bash
# Clone the project
git clone https://github.com/fenohasinalala/path-detection.git
cd path-detection
# To install dependencies
pip install -r requirements.txt
```

## Usage

1- Configuration :

- can custom the base directory where all wordlist files should be stored, with a '.env' file (or stay with default directory: word_list)
- add as many wordlist files as you want in the specified base directory

2- Before launching the application, make sure that the server is running correctly.

3- Launch the application as follows:

```bash
# To run the application
python Main.py
```

4- Enter the two following parameters:

- base URL as an example: '<http://127.0.0.1:5000>'
- desired thread count between 1 and max CPU thread count (depending on the computer)

## License

This project is licensed under the [MIT License](LICENSE.md)

## About the author

Name: Lova Fenohasina Lala RAFANOMEZANTSOA

Email: <hei.lova.31@gmail.com>

STD Reference: STD21107
