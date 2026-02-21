from dotenv import load_dotenv
from groq import Groq
import json
import re


class LogClassifier:
    def __init__(self):
        load_dotenv()
        self.groq = Groq()

    def groq_api_call(self, log_msgs):
        try:
            prompt = f'''The given log messages are from linux journalctl.
            Analyze them and find if there is any anomalous behaviour or not.
            Organize the classification results as in the alpaca format given below: 
            The purpose is dataset creation for fine-tuning an llm to classify log messages.
            Give classification for the given sequence of logs as a whole; not for each individual logs.
            {{"instruction": "Analyze the following system logs and classify whether they indicate malicious activity.", "input" : <log sequence -> add all logs in the sequence>, "output": {{"is_anomalous": <0/1>, "component": <component name>,"timestamp":<timestamp>,"reason": <concise description of reason in one or two lines>}}}}
            Log messages: {log_msgs}
            PROVIDE THE OUTPUT STRICTLY IN THE ABOVE JSON FORMAT WITHOUT ANY OTHER EXPLANATIONS, INTRODUCTIONS, CONCLUSIONS, OR FOLLOW-UP QUESTIONS.
            '''

            chat_completion = self.groq.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                temperature=0.1
            )

            content = chat_completion.choices[0].message.content
            return content
        except Exception as e:
            print(f"Error in classification module: {e}")


    def classify(self, input_queue, output_queue):
        while True:
            log_msgs = input_queue.get()
            result = self.groq_api_call(log_msgs)
            output_queue.put(result)