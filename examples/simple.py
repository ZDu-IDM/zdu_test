import sys
import time
import os

if __name__ == "__main__":
    print(os.getcwd())
    sleep_time = 5
    time.sleep(sleep_time)
    print("Sleeping for ", sleep_time, " seconds")