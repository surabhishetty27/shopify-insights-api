from openai import OpenAI

def clean_faqs(raw_text):
    prompt = f"Extract question-answer pairs from the following FAQ section:\n\n{raw_text}"
    response = OpenAI().chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
