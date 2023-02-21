# Import OpenAI and time modules
import openai
import time

# Set OpenAI API key and model engine
api_key = "YOUR API KEY"
openai.api_key = api_key
model_engine = "text-davinci-003"

# Set the names for the bot and human
bot_name = "AI (GPT)"
my_name = "name(Human)"

# Create an OpenAI session
session = openai.Completion(api_key=api_key)

# Define a function to generate a response from OpenAI
def generate_response(prompt, session):
    response = session.create(
        engine=model_engine,
        prompt=prompt,
        temperature=0.4,
        max_tokens=3000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
    )
    bot_response = response["choices"][0]["text"]
    return bot_response

# Initialize variables for keeping the conversation going
keep_prompting = True
context = ""
last_input_time = time.time()

# Start the conversation loop
while keep_prompting:
    # Check if the session has been inactive for 5 minutes
    if time.time() - last_input_time >= 300:
        # Prompt the user to enter a message to keep the session alive
        prompt = "Please enter a message to keep the session alive: "
        user_input = input(prompt)
        last_input_time = time.time()
    else:
        # Prompt the user for input
        prompt = f"{context} {bot_name}: "
        user_input = input(f"{my_name}: ")
        last_input_time = time.time()

    # Log user prompts to chat.log
    with open("chat.log", "a") as f:
        f.write(f"\n{my_name}: {user_input}")

    # End the conversation loop if user enters "quit"
    if user_input == "quit":
        keep_prompting = False
    else:
        # Generate a response from OpenAI
        prompt += user_input
        bot_response = generate_response(prompt, session)

        # Log bot responses to chat.log
        with open("chat.log", "a") as f:
            f.write(f"\n{bot_name}: {bot_response}")

        # Print bot response character-by-character without adding newline or flushing buffer
        print(f"{bot_name}: ", end="")
        for char in bot_response:
            print(char, end="", flush=True,)
            time.sleep(0.05)

        # Update context for next prompt
        context = bot_response
        print('\n')
