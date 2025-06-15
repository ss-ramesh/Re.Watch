from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def analyze_and_summarize(transcript):
    prompt = (
        "Analyze this transcript and write a clear, human-readable summary of what the speaker is saying. "
        "Include key points, arguments, and overall message:\n\n" + transcript
    )
    result = summarizer(prompt, max_length=300, min_length=80, do_sample=False)
    return result[0]['summary_text']