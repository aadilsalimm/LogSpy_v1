from dotenv import load_dotenv
from groq import Groq
import json
import re


class LogClassifier:
    def __init__(self):
        load_dotenv()
        self.groq = Groq()

    def groq_api_call(self, log_msgs):

        prompt = f'''The given log messages are from linux journalctl.
        Analyze them and find if there is any anomalous behaviour or not.
        Give a one-word output from either of the following words:
        (1) Anomalous, (2) Normal
        Remember: The output must only contain either of the two words above.
        No explanation is needed.
        Log messages: {log_msgs}'''

        chat_completion = self.groq.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.5
        )

        content = chat_completion.choices[0].message.content
        return content


    def classify(self, input_queue, output_queue):
        while True:
            log_msgs = input_queue.get()
            result = self.groq_api_call(log_msgs)
            output_queue.put(result)