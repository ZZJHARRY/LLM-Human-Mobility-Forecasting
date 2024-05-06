"""
Main logics for performing the queries.
"""
import os
import ast
import pandas as pd

from utils.helper import get_user_data, load_results
from utils.dataset_preparation import organize_data
from core.prompt.constructor import Prompt
from core.llm_model.model import get_chat_completion


def single_query(client, historical_data, X, has_duration=True, top_num=1, has_temporal_info=True):
    """
    Make a single query.
    param:
    X: one single sample containing context_stay and target_stay
    has_duration: indicates whether the current dataset has "duration" information or not
    top_num: the number of predicted place ids we would like LLM to return
    has_temporal_info: indicates whether there are temporal info given in advance for our prediction. In real life, it's likely to be yes.
    """
    prompt_object = Prompt(historical_data, X, has_duration=has_duration, top_num=top_num, has_temporal_info=has_temporal_info)
    prompt = prompt_object.construct_prompt()
    completion = get_chat_completion(client, prompt)
    return completion


def has_duration_checker(dataset_name):
    has_duration_datasets = {'geolife'}

    return dataset_name in has_duration_datasets


def query_all_user(client, dataname, uid_list, logger, train_data, num_historical_stay,
                   num_context_stay, test_file, top_k, is_wt, output_dir, sleep_query, sleep_crash):
    for uid in uid_list:
        logger.info(f"=================Processing user {uid}==================")
        user_train = get_user_data(train_data, uid, num_historical_stay, logger)
        historical_data, predict_X, predict_y = organize_data(dataname, user_train, test_file, uid, logger, num_context_stay)
        query_a_single_user(client, dataname, uid, historical_data, predict_X, predict_y, logger, top_k=top_k,
                            is_wt=is_wt, output_dir=output_dir, sleep_query=sleep_query, sleep_crash=sleep_crash)
        # TODO - break to save space
        break


# Get the un-queried users for the current dataset by checking the existing works at the ourput directory.
def get_user_list_pending_query(dataname, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    all_user_id = []
    # TODO: Update to not hard code the length.
    if dataname == "geolife":
        all_user_id = [i+1 for i in range(45)]
    elif dataname == "fsq":
        all_user_id = [i+1 for i in range(535)]
    processed_id = set([int(file.split('.')[0]) for file in os.listdir(output_dir) if file.endswith('.csv')])
    remain_pending_user_id_list = [i for i in all_user_id if i not in processed_id]
    print(remain_pending_user_id_list)
    print(f"Number of the remaining pending user id: {len(remain_pending_user_id_list)}")
    return remain_pending_user_id_list


def query_a_single_user(client, dataset_name, uid, historical_data, predict_X, predict_y, logger, top_k, is_wt, output_dir, sleep_query, sleep_crash):
    # Initialize variables
    total_queries = len(predict_X)
    logger.info(f"Total_queries: {total_queries}")

    processed_queries = 0
    current_results = pd.DataFrame({
        'user_id': None,
        'ground_truth': None,
        'prediction': None,
        'reason': None
    }, index=[])

    out_filename = f"{uid:02d}" + ".csv"
    out_filepath = os.path.join(output_dir, out_filename)

    try:
        # Attempt to load previous results if available
        current_results = load_results(out_filepath)
        processed_queries = len(current_results)
        logger.info(f"Loaded {processed_queries} previous results.")
    except FileNotFoundError:
        logger.info("No previous results found. Starting from scratch.")

    # Process remaining queries
    for i in range(processed_queries, total_queries):
        logger.info(f'The {i+1}th sample: ')

        # Process the query at row i.
        # This is the place where we get completions from OpenAI API.
        X = predict_X[i]
        has_duration = has_duration_checker(dataset_name)
        if top_k != 1 and top_k != 10:
            raise ValueError(f"The top_k must be one of 1, 10. However, {top_k} was provided")
        completions = single_query(client, historical_data, X, has_duration=has_duration, top_num=top_k, has_temporal_info=is_wt)

        response = completions.choices[0].message.content

        # Log the prediction results and usage.
        logger.info(f"Pred results: {response}")
        logger.info(f"Ground truth: {predict_y[i]}")
        logger.info(dict(completions).get('usage'))

        res_dict = None
        # This is the place where we process the response from OpenAI API.
        try:
            # This is to convert the response (in a semi-dict format) into an actual dictionary with well interpreted data types for values.
            res_dict = ast.literal_eval(response)  # Convert the string to a dictionary object
            # If top_k != 1, the result included in prediction is a list rather than a single place id, so we need to cast it to a str containing the list to store it in the pd later.
            if top_k != 1:
                res_dict['prediction'] = str(res_dict['prediction'])
            res_dict['user_id'] = uid
            res_dict['ground_truth'] = predict_y[i]
        # This is for the case when there is some exceptions thrown during ast.literal_eval (due to incompatible format)
        except Exception as e:
            res_dict = {'user_id': uid, 'ground_truth': predict_y[i], 'prediction': -100, 'reason': None}
            logger.info(e)
            logger.info(f"API request failed for the {i+1}th query")
            # time.sleep(sleep_crash)
        finally:
            new_row = pd.DataFrame(res_dict, index=[0])  # A dataframe with only one record
            current_results = pd.concat([current_results, new_row], ignore_index=True)  # Add new row to the current df
        # TODO Remove
        return

    # Save the current results
    current_results.to_csv(out_filepath, index=False)
    #save_results(current_results, out_filename)
    logger.info(f"Saved {len(current_results)} results to {out_filepath}")

    # Continue processing remaining queries
    # TODO: Maybe unnecessary since the checking for pending queries has been performed at the beginning of the function.
    if len(current_results) < total_queries:
        logger.info("Restarting queries from the last successful point.")
        query_a_single_user(client, dataset_name, uid, historical_data, predict_X, predict_y,
                            logger, top_k, is_wt, output_dir, sleep_query, sleep_crash)