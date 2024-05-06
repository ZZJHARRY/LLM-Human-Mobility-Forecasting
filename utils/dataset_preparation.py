"""
Process the datasets further according to user-specific hyperparameters.
"""
import pandas as pd

from utils.helper import convert_to_12_hour_clock, int2dow


# Can expand to more datasets, and use a separate function to process.
# Organising data
# This function is to process the train and test dataset.
def organize_data(dataset_name, user_train, test_file, uid, logger, num_context_stay=5):
    # Use another way of organising data
    historical_data = []

    if dataset_name == 'geolife':
        for _, row in user_train.iterrows():
            historical_data.append(
                (convert_to_12_hour_clock(int(row['start_min'])),
                int2dow(row['weekday']),
                int(row['duration']),
                row['location_id'])
                )
    elif dataset_name == 'fsq':
        for _, row in user_train.iterrows():
            historical_data.append(
                (convert_to_12_hour_clock(int(row['start_min'])),
                int2dow(row['weekday']),
                row['location_id'])
                )

    logger.info(f"historical_data: {historical_data}")
    logger.info(f"Number of historical_data: {len(historical_data)}")

    # This function is to iterate through all the test_file and get data points for user with uid.
    # Get user ith test data
    list_user_dict = []
    for i_dict in test_file:
        if dataset_name == 'geolife':
            i_uid = i_dict['user_X'][0]
        elif dataset_name == 'fsq':
            i_uid = i_dict['user_X']
        if i_uid == uid:
            list_user_dict.append(i_dict)

    predict_X = []
    predict_y = []
    for i_dict in list_user_dict:
        construct_dict = {}
        if dataset_name == 'geolife':
            context = list(zip([convert_to_12_hour_clock(int(item)) for item in i_dict['start_min_X'][-num_context_stay:]],
                            [int2dow(i) for i in i_dict['weekday_X'][-num_context_stay:]],
                            [int(i) for i in i_dict['dur_X'][-num_context_stay:]],
                            i_dict['X'][-num_context_stay:]))
        elif dataset_name == 'fsq':
            context = list(zip([convert_to_12_hour_clock(int(item)) for item in i_dict['start_min_X'][-num_context_stay:]],
                            [int2dow(i) for i in i_dict['weekday_X'][-num_context_stay:]],
                            i_dict['X'][-num_context_stay:]))
        # Target is the target we want to predict, and we can see that it contains four elements:
        # 1. the timeslot
        # 2. day of week
        # 3. None, the duration is not important (?)
        # 4. The <next_place_id> token: which is what we want to predict.
        target = (convert_to_12_hour_clock(int(i_dict['start_min_Y'])), int2dow(i_dict['weekday_Y']), None, "<next_place_id>")
        construct_dict['context_stay'] = context
        construct_dict['target_stay'] = target
        predict_y.append(i_dict['Y'])
        predict_X.append(construct_dict)

    logger.info(f"Number of predict_data: {len(predict_X)}")
    logger.info(f"predict_y: {predict_y}")
    logger.info(f"Number of predict_y: {len(predict_y)}")
    return historical_data, predict_X, predict_y