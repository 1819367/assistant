from openai import OpenAI
import time #import the time module

# create the client object
client = OpenAI()

# create an assistant
assistant = client.beta.assistants.create(
    name = "assistant",
    model = "gpt-3.5-turbo",
    instructions = "You are a helpful assistant for students who are newer to technology. When you answer prompts, do so with simple language suitable for someone learning fundamental concepts.",
    tools = []
)

# create a thread
thread = client.beta.threads.create()

# create a prompt
user_input = input("You: ")

# Use the prompt to create a message with the thread
message = client.beta.threads.messages.create(
    thread_id = thread.id,
    role = "user",
    content = user_input
)

# create a run
run = client.beta.threads.runs.create(
    thread_id = thread.id,
    assistant_id = assistant.id
)

# monitor the run status
while True: #create an infinite loop
    time.sleep(1) #1 equals a 1 second delay, can increase
    # call threads.runs.retrieve
    run = client.beta.threads.runs.retrieve(
        thread_id = thread.id,
        run_id = run.id
    )
    if run.status == "completed":
        break

# Display the response to the user, extract the most recent message content when the run is completed
if run.status == "completed":
    thread_messages = client.beta.threads.messages.list(
        thread_id = thread.id
    )

message_for_user = thread_messages.data[0].content[0].text.value

print("\nAssistant: " + message_for_user + "\n")