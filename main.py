import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPEN_API_KEY'))
import pinecone


def get_openai_response(prompt, model="gpt-3.5-turbo", temperature=0.7):
    """Get a response from OpenAI's GPT model."""
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error in getting response: {e}")
        return ""

def __main(user_input):
    index = pinecone.Index('pineconedbname')
    MODEL = "text-embedding-ada-002"

    query = user_input
    print(query)

    xq = client.embeddings.create(input=query, engine=MODEL)['data'][0]['embedding']  # transforms query into embedding

    res = index.query([xq], top_k=5,
                      include_metadata=True)  # similaritysearch your db with your question, returns 5 chunks in lists of dictionaries

    combined_context = " "
    #go through the 5 similar results dictionary and add only the text
    for chunks in res['matches']:
        # Combine all texts to form the context
        combined_context += chunks['metadata']['text']
        print(f"{chunks['score']:.2f}: {chunks['metadata']['text']}") #replace print with app.logger.info for render



    # Start the conversation
    print("Starting the conversation. Type 'exit' to end.")
    while True:
        #user_input = input("You: ")
        if user_input.lower() == 'exit':
            break

        # Combine context with user input for the prompt
        prompt = combined_context + "\n\n" + user_input

        # Get the model's response
        response = get_openai_response(prompt)
        return response
        print("ChatGPT:", response)

if __name__ == '__main__':
    __main()