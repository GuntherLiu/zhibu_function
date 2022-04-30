from func_do import do
import schedule
import time
import logger
import random


def main():
    sleep_sec = random.randint(10 * 60, 40 * 60)
    time.sleep(sleep_sec)
    logger.logger("----- begin ----")
    do()
    logger.logger("----- end -----")


if __name__ == '__main__':
    schedule.every().day.at("06:00").do(main)
    while True:
        schedule.run_pending()
        time.sleep(58)
