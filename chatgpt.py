import os
import sys
import time
import openai
from flask import jsonify
from datetime import datetime, timedelta
from context_texts import get_context_texts


openai.api_key = os.getenv("OPENAI_API_KEY")

systemPrompt = { "role": "system", "content": "You are a helpful assistant that helps look through my text messages." }
# You are a helpful assistant



def get_response(incoming_msg, userId=None):

    context_texts = get_context_texts(userId)

    # Function to format the month day as 1st, 2nd, 3rd, etc.
    def suffix(d):
        return 'th' if 11 <= d <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')

    def custom_strftime(format, t):
        return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))

    # Current time
    current_time = datetime.now()

    context = "Here is the context of the relevant messages.\n" # that your boss sent

    for text in context_texts:
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
        context += f'{text["user"]} told said "{text["text"]}" {friendly_time} ({exact_time}).\n'
    context += f'\n "Prompt: {incoming_msg}"' #I want to know

    print(context)
    data = []
    data.append({"role": "assistant", "content": context})

    messages = [ systemPrompt ]
    messages.extend(data)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", # could change to high token limit model
            messages=messages
        )
        content = response["choices"][0]["message"]["content"]
        data = { 
            "response": content,
            "texts": context_texts 
        } 
        return data
    except openai.error.RateLimitError as e:
        print(e)
        return ""