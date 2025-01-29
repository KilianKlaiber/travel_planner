import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def find_country(landmark: str) -> str:
    """Retrieve country of origin of landmark

    Args:
        landmark (str): Landmark like the Eiffel Tower

    Returns:
        str: Country of origin of the landmark, like France"""

    client = Groq(
        api_key=os.getenv("API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Tell me, in which country the {landmark} is located. Answer with the sentence: The {landmark} is in ... ",
            }
        ],
        model="llama3-8b-8192",
    )


    groq_answer = chat_completion.choices[0].message.content
    word_list = groq_answer.split()
    last_word = word_list[-1]

    # Test whether groq has finished the sentence with a point or other non-alphabetic character.
    # If so, then delete this character from the answer.
    if not last_word[-1].isalpha():
        country = last_word[0:-1]
    else:
        country = last_word

    return country


if __name__ == "__main__":
    print(find_country("Tower Bridge"))
