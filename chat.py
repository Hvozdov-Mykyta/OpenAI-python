from openai import OpenAI


def get_api_key(path) -> tuple[bool, str]:
    try:
        with open(path, 'rt') as file:
            api_key = file.read()
        return True, api_key
    except FileNotFoundError:
        return False, 'Invalid api_key file path'


def get_openai_response(client, chat_history) -> tuple[bool, str]:
    try:
        response = client.chat.completions.create(model = 'gpt-4o-mini', messages = chat_history)
        return True, response['choices'][0]['message']['content']
    except Exception as e:
        return False, str(e)


def main():
    api_key_path = input('\n API_KEY file path:    ')
    api_key_tuple = get_api_key(api_key_path)

    if not api_key_tuple[0]:
        print(f'\n Error: {api_key_tuple[1]}')
        return

    client = OpenAI(api_key=api_key_tuple[1])
    chat_history = [{'role': 'system', 'content': 'You are an assistant for regular conversation.'}]

    while True:
        user_input = input('\n You:   ')
        if user_input == 'exit':
            return
        
        chat_history.append({'role': 'user', 'content': [{'type': 'text', 'text': user_input}]})
        response_tuple = get_openai_response(client, chat_history)

        if not response_tuple[0]:
            print(f'\n Error: {response_tuple[1]}')
            return
        
        chat_history.append({'role': 'system', 'content': response_tuple[1]})
        print(f' Chat:  {response_tuple[1]}')



if __name__ == '__main__':
    main()