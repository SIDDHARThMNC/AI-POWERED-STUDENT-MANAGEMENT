from textblob import TextBlob


# Sentiment Analysis
def analyze_sentiment(text: str):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0:
        sentiment = "Positive 😊"
    elif polarity < 0:
        sentiment = "Negative 😔"
    else:
        sentiment = "Neutral 😐"

    return {
        "polarity": polarity,
        "sentiment": sentiment
    }


# ✅ Smart Search Function
def smart_search(students, query: str):
    query = query.lower()
    results = []

    for student in students:
        if (
            query in student.name.lower()
            or query in student.course.lower()
        ):
            results.append(student)

    return results
