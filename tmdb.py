# !pip install langchain
# !pip  install OpenAI

from langchain.llms import OpenAI
import requests
import os
import openai
#  Set the open API key
os.environ["OPENAI_API_KEY"] = "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"
# Set the TMDB API key
os.environ['TMDB_API_KEY']= "f71f3c34619b78598760fbd515bf4c07"
# Set the movie title
# movie_title = "The Matrix"
movie_title="Titanic"

# movie_title = "Dilwale Dulhania Le Jayenge"


# Get movie information from the TMDB API
tmdb_url = f"https://api.themoviedb.org/3/search/movie?api_key={os.getenv('TMDB_API_KEY')}&query={movie_title}"
response = requests.get(tmdb_url)
data = response.json()

# Get the movie overview from the TMDB API
tmdb_url = f"https://api.themoviedb.org/3/movie/{data['results'][0]['id']}?api_key={os.getenv('TMDB_API_KEY')}"
response = requests.get(tmdb_url)
movie_data = response.json()
overview = movie_data['overview']

# Set up the OpenAI API
OpenAI.api_key = "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"
prompt = f"Generate 5 multiple-choice questions using OpenAI and their correct answers using TMDB API based on the movie '{movie_title}'.\n\n"

# Generate the quiz questions and answers
for i in range(5):
    # Generate the question using OpenAI
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.5,
        max_tokens=60,
    )
    question = response.choices[0].text.strip()

    # Get the correct answer using TMDB API
    answer = overview

    # Generate the multiple choice question and answer options
    prompt += f"Question {i+1}: {question}\n"
    options = [answer]
    for j in range(3):
        wrong_answer = overview[:50] + "..." + str(j)
        options.append(wrong_answer)
    options = sorted(options)
    for j, option in enumerate(options):
        prompt += f"{chr(97+j)}) {option}\n"
    prompt += f"Correct answer: {chr(97+options.index(answer))}\n\n"

print(prompt)
