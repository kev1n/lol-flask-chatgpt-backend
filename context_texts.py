import pymongo


mongo_uri = "mongodb+srv://kevin:kevin@cluster0.xyjfa6e.mongodb.net/"
database_name = "users"
collection_name = "messages" 

client = pymongo.MongoClient(mongo_uri)
db = client[database_name]
collection = db[collection_name]

def query_all_messages():
    messagesCursor = collection.find({})
    out = []
    for message in messagesCursor:
        out.append({
            "text" : message["text"],
            "user" : message["user"],
            "timestamp" : message["timestamp"]
        })

    print("------MESSAGES", out)
    return out


def get_context_texts(user_id:str|None=None):
    
    # Query MongoDB for all the texts of the user_id (within last day maybe)
    # convert to same format as sampleTexts if not 
    # (right now there is just support for 1 user at a time)

    return query_all_messages()



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