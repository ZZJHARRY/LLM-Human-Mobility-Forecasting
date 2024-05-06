"""
Define the Prompt class to produce prompts for all use cases so far.
"""

from core.prompt.content import *


class Prompt:
    """
    historical_data:
    X:
    has_duration: indicates whether the current dataset has "duration" information or not
    top_num: the number of predicted place ids we would like LLM to return
    has_temporal_info: indicates whether there are temporal info given in advance for our prediction. In real life, it's likely to be yes.
    """

    def __init__(self, historical_data, X, has_duration=True, top_num=1,
                 has_temporal_info=True):
        self.historical_data = historical_data
        self.X = X
        self.has_duration = has_duration
        self.top_num = top_num
        self.has_temporal_info = has_temporal_info

    def construct_prompt(self):
        prompt = f"""
        {task_specification}
        {data_description}
        {definition_heading if self.has_duration else definition_heading_without_duration}
        {start_time_definition}
        {day_of_week_definition}
        {(duration_definition if self.has_temporal_info else duration_definition_wot) if self.has_duration else ""}
        {place_id_definition}

        {instruction_with_temporal_information if self.has_temporal_info else ""}

        {instruction_guide_model_to_think_top1 if self.top_num == 1 else instruction_guide_model_to_think_top10}
        {consideration_histort_stay}
        {consideration_context_stay}
        {consideration_temporal_information if self.has_temporal_info else ""}

        {instruction_format_output_and_ask_for_explanations_top1 if self.top_num == 1 else instruction_format_output_and_ask_for_explanations_top10}

        {data_heading}
        <history>: {self.historical_data}
        <context>: {self.X['context_stay']}
        {("<target_stay>: " + self.X['target_stay']) if self.has_temporal_info else ""}
        """

        return prompt
