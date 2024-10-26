from openai import OpenAI

client = OpenAI(
    api_key='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')

audio_file = open("test.m4a", "rb")
transcription = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file
)
print(transcription.text)
