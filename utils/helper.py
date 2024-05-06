"""
The helper functions
"""


import pandas as pd
import pickle
import os
import logging
import datetime


# This is the function to load dataset.
# Maybe we can refactor to also include path to the dataset.
def get_dataset(dataname):

    # Get training and validation set and merge them
    train_data = pd.read_csv(f"data/{dataname}/{dataname}_train.csv")
    valid_data = pd.read_csv(f"data/{dataname}/{dataname}_valid.csv")

    # Get test data
    with open(f"data/{dataname}/{dataname}_testset.pk", "rb") as f:
        test_file = pickle.load(f)  # test_file is a list of dict

    # merge train and valid data
    tv_data = pd.concat([train_data, valid_data], ignore_index=True)
    tv_data.sort_values(['user_id', 'start_day', 'start_min'], inplace=True)
    if dataname == 'geolife':
        tv_data['duration'] = tv_data['duration'].astype(int)

    print("Number of total test sample: ", len(test_file))
    return tv_data, test_file


def convert_to_12_hour_clock(minutes):
    if minutes < 0 or minutes >= 1440:
        return "Invalid input. Minutes should be between 0 and 1439."

    hours = minutes // 60
    minutes %= 60

    period = "AM"
    if hours >= 12:
        period = "PM"

    if hours == 0:
        hours = 12
    elif hours > 12:
        hours -= 12

    return f"{hours:02d}:{minutes:02d} {period}"


def int2dow(int_day):
    tmp = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday',
           3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    return tmp[int_day]


# This is the function to create a logger.
# Comment: Pretty useful, and consider adding it to my project.
def get_logger(logger_name, log_dir='logs/'):
    # Create log dir
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create a logger instance
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # Create a console handler and set its log level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # Create a file handler and set its log level
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y%m%d_%H%M%S")
    # Here is the log file name.
    log_file = 'log_file_' + formatted_datetime + '.log'
    log_file_path = os.path.join(log_dir, log_file)
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.DEBUG)

    # Create a formatter and add it to the handlers
    formatter = logging.Formatter('%(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


def get_user_data(train_data, uid, num_historical_stay, logger):
    user_train = train_data[train_data['user_id']==uid]
    logger.info(f"Length of user {uid} train data: {len(user_train)}")
    # tail is to get the last num_historical_stay number of data points.
    user_train = user_train.tail(num_historical_stay)
    logger.info(f"Number of user historical stays: {len(user_train)}")
    return user_train


def load_results(filename):
    # Load previously saved results from a CSV file
    results = pd.read_csv(filename)
    return results
