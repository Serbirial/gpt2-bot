from gpt import ai

chat = ai.ChatAI()
chat.load_model()
while True:
        inp = input('>')
        resp = chat.get_bot_response("124M", "koya", inp)
        data = resp.split("me:", 1)[1].splitlines()[0]
        print(data)