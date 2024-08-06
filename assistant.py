from openai import OpenAI
import time #import the time module
import random 
import logging #for error logging
import datetime

log = logging.getLogger("assistant") #basic logging config function

logging.basicConfig(filename = ("assistant.log"), level = logging.INFO) #logging retrieval function

# create the client object
client = OpenAI()

# new function process_run with two parameter
def process_run(thread_id, assistant_id):

    # create a new run
    new_run = client.beta.threads.runs.create( #updated var name
        thread_id = thread_id, #use thread_id to create a run within the specific thread
        assistant_id = assistant_id 
    )

    # Add array of new phrases
    phrases = ["Thinking", "Pondering", "Dotting the i's", "Crossing the t's", "Achieving world peace"]

    # monitor the run status
    while True: #create an infinite loop
        time.sleep(1) #1 equals a 1 second delay, can increase
        # call threads.runs.retrieve
        print(random.choice(phrases) + "...") #randomly select a phrase using random.choice()
        
        # retrieve  and monitor the run status
        run_check = client.beta.threads.runs.retrieve( 
            thread_id = thread_id, #Use thread_id to identify the thread
            run_id = new_run.id #get the run_id from the created run
        )
        # check the run status
        if run_check.status in ["cancelled", "failed", "completed", "expired"]:
             return run_check

# new function to  log the run status and create an error log
def log_run(run_status):
    #conditional for canceled, failed or expired, print an error message
    if run_status in ["cancelled", "failed", "expired"]:
        log.error(str(datetime.datetime.now()) + " Run " + run_status + "\n")

# separate function to get and return the message
def get_message(run_status):
     #handle the object returned by the function
    if run_status == "completed":
    # Display the response to the user, extract the most recent message content when the run is completed  
        thread_messages = client.beta.threads.messages.list(
          thread_id = thread.id
         )
        message = thread_messages.data[0].content[0].text.value

    if run_status in ["cancelled", "failed", "expired"]:
        message = "An error has occurred, please try again."
    
    return message

# create an assistant
assistant = client.beta.assistants.create(
    name = "assistant",
    model = "gpt-3.5-turbo",
    instructions = "You are a helpful assistant for students who are newer to technology. When you answer prompts, do so with simple language suitable for someone learning fundamental concepts.",
    tools = []
)

# create a thread
thread = client.beta.threads.create()

user_input = ""

while True: #new while loop
    # create the prompt for user input
    if (user_input == ""):
        user_input = input("Assistant: Hello there, I'm your helful assistant!  Type exit when you want to end our chat. What is your name?")
    else:
        user_input = input("You: ")
    
    if user_input.lower() == "exit":
        print("Goodbye!")
        exit()
    
    # Use the prompt to create a message with the thread
    message = client.beta.threads.messages.create(
        thread_id = thread.id, #use thread_id to add a message to the thread
        role = "user",
        content = user_input
        )
    #create the run by calling the process_run() function
    run = process_run(thread.id, assistant.id)

    #log error messages
    log_run(run.status)

    message = get_message(run.status)

    print("\nAssistant: " + message + "\n")




