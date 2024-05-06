"""
This is the file containing main content of the prompts.
"""

task_specification = "Your task is to predict a user's next location based on his/her activity pattern."

data_description = "You will be provided with <history> which is a list containing this user's historical stays, then <context> which provide contextual information about where and when this user has been to recently. Stays in both <history> and <context> are in chronological order."

definition_heading = "Each stay takes on such form as (start_time, day_of_week, duration, place_id). The detailed explanation of each element is as follows:"
definition_heading_without_duration = "Each stay takes on such form as (start_time, day_of_week, place_id). The detailed explanation of each element is as follows:"
start_time_definition = "start_time: the start time of the stay in 12h clock format."
day_of_week_definition = "day_of_week: indicating the day of the week."
duration_definition = "duration: an integer indicating the duration (in minute) of each stay. Note that this will be None in the <target_stay> introduced later."
duration_definition_wot = "duration: an integer indicating the duration (in minute) of each stay."
place_id_definition = "place_id: an integer representing the unique place ID, which indicates where the stay is."

instruction_with_temporal_information = "Then you need to do next location prediction on <target_stay> which is the prediction target with unknown place ID denoted as <next_place_id> and unknown duration denoted as None, while temporal information is provided."

instruction_guide_model_to_think_top1 = "Please infer what the <next_place_id> is (i.e., the most likely place ID), considering the following aspects:"
instruction_guide_model_to_think_top10 = "Please infer what the <next_place_id> might be (please output the 10 most likely places which are ranked in descending order in terms of probability), considering the following aspects:"

consideration_histort_stay = "1. the activity pattern of this user that you learned from <history>, e.g., repeated visits to certain places during certain times;"
consideration_context_stay = "2. the context stays in <context>, which provide more recent activities of this user;"
consideration_temporal_information = "3. the temporal information (i.e., start_time and day_of_week) of target stay, which is important because people's activity varies during different times (e.g., nighttime versus daytime) and on different days (e.g., weekday versus weekend)."

instruction_format_output_and_ask_for_explanations_top1 = "Please organize your answer in a JSON object containing following keys: \"prediction\" (place ID) and \"reason\" (a concise explanation that supports your prediction). Do not include line breaks in your output."
instruction_format_output_and_ask_for_explanations_top10 = """Please organize your answer in a JSON object containing following keys:
    "prediction" (the ID of the ten most probable places in descending order of probability) and "reason" (a concise explanation that supports your prediction). Do not include line breaks in your output."""

data_heading = "The data are as follows:"