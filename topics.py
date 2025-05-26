import random
from datetime import datetime

def get_seasonal_keywords():
    month = datetime.now().month
    if month == 10:
        return ["Halloween", "ghost", "pumpkin", "witch"]
    elif month == 12:
        return ["Christmas", "snowman", "reindeer", "Santa"]
    elif month == 2:
        return ["Valentine", "hearts", "love", "chocolate"]
    elif month in [6, 7, 8]:
        return ["summer", "beach", "sun", "vacation"]
    else:
        return ["funny", "cute", "animal", "retro"]

subjects = ["cat", "dog", "sushi", "alien", "robot", "frog", "boba tea", "dinosaur", "unicorn", "dragon"]
styles = ["kawaii", "minimalist", "psychedelic", "cyberpunk", "pastel", "vintage", "funny", "grunge"]

def get_random_prompt():
    style = random.choice(styles)
    subject = random.choice(subjects)
    seasonal = random.choice(get_seasonal_keywords())
    return f"{style} {subject} for {seasonal}"
