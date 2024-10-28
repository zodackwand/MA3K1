This project was created during WHACK 2024 (University of Warwick Hackathon). 

**Project Concept** 

*The problem:* if a cyclists gets into an accident in the rural countryside, depending on the severity of the accident, they may not be able to request help. This means that it is quite likely that emergency services will get to the person too late.

*The solution:* a video monitoring tool, which communicates with the user via audio to check whether assitance is required. This tool consists of three fetch.ai agents:<br>Agent 1: monitors cyclist's pov, creates a transcipt of what is happening in the video and based on it determines whether something out of the ordinary happened. The verdict is sent to Agent 2.<br>Agent 2: if the verdict recieved implies that the cyclist may require help asks using audio whether help is indeed needed, then waits for a response. If the speech response received from cyclist implies that assistance is required, or if there simply was no response, Agent 2 passes the relevant verdict to Agent 3.<br>Agent 3: if based on the information from Agent 2 help is required, a message is sent to emergency services. 

In the demo the emergency service is modelled by a Telegram bot.

Runs smoothly on Windows

1. Install the requirements
   pip install -r requirements.txt

2. Set the environment variable
   $env:GOOGLE_APPLICATION_CREDENTIALS="service-account-file.json"

3. Run agent_to_telegram.py
