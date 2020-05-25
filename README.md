# PyPinger

A simple python command-line tool to graph real-time ping latency. I just made this tool for fun. Feel free to clone the repository for use.

## Usage

```sh
Usage: python main.py [-h] [-H HOST] [-i INTERVAL] [-l LIMIT] [-t TIMEOUT]

Plots a real-time graph of ping latency.

optional arguments:
  -h, --help            show this help message and exit
  -H HOST, --host HOST  the host to ping
  -i INTERVAL, --interval INTERVAL
                        the interval (in ms) between consecutive ping calls
  -l LIMIT, --limit LIMIT
                        max number of data points to display
  -t TIMEOUT, --timeout TIMEOUT
                        max ping timeout (in ms)
```

## Requirements

[Python v3+](https://www.python.org/) is required to run the tool, with additional libraries:

- [matplotlib](https://pypi.org/project/matplotlib/)
- [pythonping](https://pypi.org/project/pythonping/)

You can also install all of them using:

```sh
pip install -r requirements.txt
```
