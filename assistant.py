import time
from openai import OpenAI

client = OpenAI()

#create the assistant
assistant = client.beta.assistants.create(
    name = "Study Buddy",
    model = "gpt-3.5-turbo",
    instructions = "You are a study partner for students who are newer to technology. When you answer prompts, do so with simple language suitable for someone learning fundamental concepts.",
    tools=[]
)

#create a thread
thread = client.beta.threads.create()

#prompt the user to input a message
user_input = input("You: ")
 
#use the prompt to create a message within the thread
message = client.beta.threads.messages.create(
    thread_id = thread.id,
    role = "user",
    content = user_input
)
 
#create a run
run = client.beta.threads.runs.create(
    thread_id = thread.id,
    assistant_id = assistant.id
)
 
#monitor the run status
while True:
    time.sleep(3)
    run_check = client.beta.threads.runs.retrieve(
        thread_id = thread.id,
        run_id = run.id
    )
    if run_check.status == "completed":
        break 

#extract the most recent message content when the run is completed
thread_messages = client.beta.threads.messages.list(
    thread_id = thread.id
)

message_for_user = thread_messages.data[0].content[0].text.value
 
#display the message to the user
print(f"\nAssistant:  {message_for_user}\n")
