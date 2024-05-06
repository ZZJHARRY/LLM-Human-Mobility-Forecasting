"""
This is the function to query the OpenAI and get completion
"""


def get_chat_completion(client, prompt, model="gpt-3.5-turbo-0613", json_mode=False, max_tokens=1200):
    """
    args:
        client: the openai client object (new in 1.x version)
        prompt: the prompt to be completed
        model: specify the model to use
        json_mode: whether return the response in json format (new in 1.x version)
    """
    messages = [{"role": "user", "content": prompt}]
    if json_mode:
        completion = client.chat.completions.create(
            model=model,
            response_format={"type": "json_object"},
            messages=messages,
            temperature=0,  # the degree of randomness of the model's output
            max_tokens=max_tokens  # the maximum number of tokens to generate
        )
    else:
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0,
            max_tokens=max_tokens
        )

    return completion
