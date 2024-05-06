import os
import pickle
import time
import ast
import logging
from datetime import datetime
import pandas as pd
from openai import OpenAI

from utils.helper import get_logger, get_dataset, get_user_data
from utils.dataset_preparation import organize_data
from core.query.logic import query_all_user, single_query, get_user_list_pending_query, \
    query_a_single_user


# Helper function
def main():
    # User Input 1: Replace <OpenAI_API_Key> with your OpenAI API key.
    os.environ['OPENAI_API_KEY'] = "<OpenAI_API_Key>"

    client = OpenAI(
        api_key=os.environ['OPENAI_API_KEY']
    )

    # User Input 2: Update the Hyper-Parameters as needed
    """
    dataset_name: specify the name for the dataset, currently including 'geolife' or 'fsq'.
    num_historical_stay: (M) number of historical stays included in the prompt.
    num_context_stay: (N) number of context stays included in the prompt.
    top_k: the number of output place ids
    with_time: whether incorporate temporal information for target stay
    sleep_single_query: the sleep time (in s) between queries
    sleep_if_crash: the sleep time (in s) if the server crashes
    """
    dataset_name = "geolife"
    num_historical_stay = 40
    num_context_stay = 5
    top_k = 10
    with_time = False
    sleep_single_query = 0.1
    sleep_if_crash = 1

    # Output & Logging Directories
    output_dir = f"output/{dataset_name}/top{top_k}" + (
        "_wot" if not with_time else "")  # the output path
    log_dir = f"logs/{dataset_name}/top{top_k}" + (
        "_wot" if not with_time else "")  # the log path

    tv_data, test_file = get_dataset(dataset_name)

    logger = get_logger('my_logger', log_dir=log_dir)

    pending_query_user_list = get_user_list_pending_query(dataset_name, output_dir)
    print(f"Pending Query User Id list: {pending_query_user_list}")

    query_all_user(client, dataset_name, pending_query_user_list, logger, tv_data,
                   num_historical_stay, num_context_stay,
                   test_file, output_dir=output_dir, top_k=top_k, is_wt=with_time,
                   sleep_query=sleep_single_query, sleep_crash=sleep_if_crash)

    print("Query done")


if __name__ == "__main__":
    main()
