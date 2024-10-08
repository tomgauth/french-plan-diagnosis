level_data = {
    "A0.1": {"words": 125, "frequent_words": 100, "MIPs": 63, "reading_comp": 188},
    "A0.2": {"words": 250, "frequent_words": 200, "MIPs": 125, "reading_comp": 375},
    "A0.3": {"words": 350, "frequent_words": 280, "MIPs": 175, "reading_comp": 525},
    "A1": {"words": 500, "frequent_words": 400, "MIPs": 250, "reading_comp": 750},
    "A1.1": {"words": 625, "frequent_words": 500, "MIPs": 313, "reading_comp": 938},
    "A1.2": {"words": 750, "frequent_words": 600, "MIPs": 375, "reading_comp": 1125},
    "A1.3": {"words": 875, "frequent_words": 700, "MIPs": 438, "reading_comp": 1313},
    "A2": {"words": 1000, "frequent_words": 800, "MIPs": 500, "reading_comp": 1500},
    "A2.1": {"words": 1250, "frequent_words": 1000, "MIPs": 625, "reading_comp": 1875},
    "A2.2": {"words": 1500, "frequent_words": 1200, "MIPs": 750, "reading_comp": 2250},
    "A2.3": {"words": 1750, "frequent_words": 1400, "MIPs": 875, "reading_comp": 2625},
    "B1": {"words": 2000, "frequent_words": 1600, "MIPs": 1000, "reading_comp": 3000},
    "B1.1": {"words": 2500, "frequent_words": 2000, "MIPs": 1250, "reading_comp": 3750},
    "B1.2": {"words": 3000, "frequent_words": 2400, "MIPs": 1500, "reading_comp": 4500},
    "B1.3": {"words": 3500, "frequent_words": 2800, "MIPs": 1750, "reading_comp": 5250},
    "B2": {"words": 4000, "frequent_words": 3200, "MIPs": 2000, "reading_comp": 6000},
}

conversation_data = {
    "Introduce yourself and talk about your life": {"min_phrases": 100, "max_phrases": 500},
    "Talk about your weekend": {"min_phrases": 100, "max_phrases": 500},
    "Explain in detail your journey learning French": {"min_phrases": 100, "max_phrases": 300},
    "Make a presentation at work": {"min_phrases": 200, "max_phrases": 500},
    "Small talk with in-laws": {"min_phrases": 100, "max_phrases": 500},
    "Be ready as an expat for doctor, post office, school, everyday things": {"min_phrases": 100, "max_phrases": 300},
    "Order in cafes and restaurants": {"min_phrases": 10, "max_phrases": 100},
    "Speak French most of the time at home with my partner": {"min_phrases": 200, "max_phrases": 1000},
}


def calculate_phrases_to_learn(current_level, conversations):
    """
    Calculate the total number of phrases needed to learn based on the user's current level and selected conversation goals.
    If level is A2 or below, use min_phrases. If B1 or higher, use max_phrases.
    """
    total_phrases = 0
    for conversation in conversations:
        if current_level in ["A0.1", "A1", "A2"]:
            total_phrases += conversation_data[conversation]["min_phrases"]
        else:
            total_phrases += conversation_data[conversation]["max_phrases"]
    
    return total_phrases

learning_speed_data = {
    "Flashcards": 1 / 2.5,  # 1 phrase every 2.5 minutes
    "Self-study (books/videos)": 1 / 15,  # 1 phrase every 15 minutes
    "Conversation lessons": 10 / 60,  # 10 phrases per hour of lesson
    "Other": 1 / 15  # Default: self-study rate (15 minutes per phrase)
}

def calculate_learning_speed(learning_method, taking_lessons):
    """
    Determine the learning speed based on the learning method using a dict.
    """
    if learning_method == "Conversation lessons" and taking_lessons == "Yes":
        return learning_speed_data["Conversation lessons"]
    
    return learning_speed_data.get(learning_method, learning_speed_data["Other"])

def calculate_time_to_goal(total_phrases, study_time, learning_speed):
    """
    Calculate how long (in days and weeks) it will take the user to reach their goal based on their daily study time.
    """
    phrases_per_day = study_time * learning_speed  # Phrases learned per day
    days_to_goal = total_phrases / phrases_per_day
    weeks_to_goal = days_to_goal / 7  # Convert days to weeks
    
    return days_to_goal, weeks_to_goal


def calculate_score(current_level, target_level, conversations, improvements):
    # Calculate level score based on user input
    level_score = abs(["A1", "A2", "B1", "B2", "C1", "C2"].index(target_level) - ["A1", "A2", "B1", "B2", "C1", "C2"].index(current_level))
    
    # Example score calculation for conversations and improvements
    conv_score = len(conversations) * 2
    imp_score = len(improvements) * 3
    
    # Calculate total score
    total_score = level_score + conv_score + imp_score
    
    return total_score


def generate_learning_plan(score):
    # Generate a learning plan based on the score
    if score <= 10:
        return "You’ll need a 3-month plan focusing on vocabulary and confidence."
    elif score <= 15:
        return "Your plan will take 6 months, focusing on comprehension and conversation practice."
    else:
        return "You may need a 9-month comprehensive learning plan."



def calculate_words_for_conversations(conversations, target_level):
    target_words = level_data[target_level]["words"]
    total_phrases = sum(conversation_data[conv]["max_phrases"] for conv in conversations)
    
    # Compare the number of target words and needed phrases
    return min(total_phrases, target_words)


def estimate_learning_duration(current_level, target_level, lessons_per_week, hours_per_week):
    current_words = level_data[current_level]["words"]
    target_words = level_data[target_level]["words"]
    words_to_learn = target_words - current_words
    
    # Estimation of words learned per lesson or self-study hour (e.g., 50 words per lesson, 30 words per hour self-study)
    words_per_lesson = 50
    words_per_hour_study = 30
    
    # Calculate total progress with lessons and study time
    total_lessons = lessons_per_week * (words_to_learn // words_per_lesson)
    total_study_hours = hours_per_week * (words_to_learn // words_per_hour_study)
    
    return total_lessons, total_study_hours