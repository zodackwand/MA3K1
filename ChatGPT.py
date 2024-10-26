from openai import OpenAI

def voicetotext():
    client = OpenAI(
        api_key='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')

    audio_file = open("test.m4a", "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )
    print(transcription.text)
    return transcription.text

client = OpenAI(api_key='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')


def live_chat():
    conversation_history = [
        {"role": "system", "content": "Дай ответ True или False, проверяет ли пользователь свою связь"}
    ]  # This sets the initial context

    print("ChatGPT is ready! Type 'exit' to end the chat.\n")

    # Get user input
    user_message = voicetotext()
    if user_message.lower() == "exit":
        print("Ending chat.")

    # Add user's message to the conversation history
    conversation_history.append({"role": "user", "content": user_message})

    # Call the OpenAI API with the conversation history
    completion = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=conversation_history
    )

    # Extract and display the assistant's response
    assistant_message = completion.choices[0].message.content
    print("ChatGPT:", assistant_message)

    # Add ChatGPT's response to the conversation history
    conversation_history.append({"role": "assistant", "content": assistant_message})

# Start the chat
live_chat()
