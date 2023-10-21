import os
import sys
import time
import openai
from flask import jsonify
from datetime import datetime, timedelta


openai.api_key = os.getenv("OPENAI_API_KEY")

systemPrompt = { "role": "system", "content": "You are a helpful assistant." }

def get_response(incoming_msg):
    sampleTexts = [
      {
        "text": 'Happy Birthday! Hope your day is as amazing as you are!',
        "user": 'JohnDoe',
        "timestamp": 1671619200
      },
      {
        "text": 'Wishing you all the happiness on your special day! 🎉',
        "user": 'JaneDoe',
        "timestamp": 1671622800, 
      },
      {
        "text": "HBD! Can't wait to celebrate with you tonight!",
        "user": 'Mike_Smith',
        "timestamp": 1671626400, 
      },
      {
        "text": 'Haha, I still hate you',
        "user": 'SarahP',
        "timestamp": 1671630000, 
      },
      {
        "text": "Happy Birthday! Let's make this year the best one yet!",
        "user": 'Tom_Jones',
        "timestamp": 1671633600, 
      },
      {
        "text": 'Another year older, wiser, and even more awesome. Happy Birthday!',
        "user": 'JenniferM',
        "timestamp": 1671637200, 
      },
      {
        "text": 'Hope your birthday is just the beginning of a year full of happiness!',
        "user": 'AlexW',
        "timestamp": 1671640800, 
      },
      {
        "text": 'Have a wonderful birthday, my dear! You deserve all the joy in the world 🎈',
        "user": 'ChrisF',
        "timestamp": 1671644400, 
      },
      {
        "text": 'Happy Birthday! 🎁 Enjoy this day to the fullest!',
        "user": 'PatriciaH',
        "timestamp": 1671648000, 
      },
      {
        "text": 'Worst wishes on your birthday! I hate you still!',
        "user": 'Bill_S',
        "timestamp": 1671651600, 
      },
    ]
    # Function to format the month day as 1st, 2nd, 3rd, etc.
    def suffix(d):
        return 'th' if 11 <= d <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')

    def custom_strftime(format, t):
        return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))

    # Current time
    current_time = datetime.now()

    context = "Here is the context of the relevant messages that your boss sent.\n"

    for text in sampleTexts:
        # Convert the timestamp to a datetime object
        message_time = datetime.fromtimestamp(text["timestamp"])
        
        # Calculate how long ago the message was sent
        time_diff = current_time - message_time
        
        # String representation of the exact time
        exact_time = custom_strftime('%B {S} at %I:%M %p', message_time)  # E.g., "July 29th at 3:34 AM"

        # Friendly string representation of the time difference
        if time_diff.days > 0:
            friendly_time = f"{time_diff.days} days ago"
        else:
            hours = time_diff.seconds // 3600  # Convert seconds to hours
            if hours > 0:
                friendly_time = f"{hours} hours ago"
            else:
                minutes = time_diff.seconds // 60  # Remaining seconds converted to minutes
                if minutes > 0:
                    friendly_time = f"{minutes} minutes ago"
                else:
                    friendly_time = "just now"
        
        # Add this text to the context, including both time representations
        context += f'{text["user"]} told your boss "{text["text"]}" {friendly_time} ({exact_time}).\n'
    context += f'\nYour boss asks you "{incoming_msg}"'

    print(context)
    data = []
    data.append({"role": "assistant", "content": context})

    messages = [ systemPrompt ]
    messages.extend(data)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        content = response["choices"][0]["message"]["content"]
        data = { 
            "response": content,
            "texts": sampleTexts 
        } 
        return data
    except openai.error.RateLimitError as e:
        print(e)
        return ""