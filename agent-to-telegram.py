from uagents import Agent, Context, Bureau, Model
import telegram, asyncio
from uagents.setup import fund_agent_if_low
from ChatGPT import live_chat

class Message(Model):
    message: str

class ContextPrompt(Model):
    context: str
    text: str

class Response(Model):
    text: str

AGENT_MAILBOX_KEY = "c47b2ef5-5750-439c-9eb9-efe08a5af8bf"
SEED_PHRASE = "bike test"

agent = Agent(
    name="mary",
    seed=SEED_PHRASE,
    mailbox=f"{AGENT_MAILBOX_KEY}@https://agentverse.ai",
)
fund_agent_if_low(agent.wallet.address())
print(agent.address)

AI_AGENT_ADDRESS = "agent1q0h70caed8ax769shpemapzkyk65uscw4xwk6dc4t3emvp5jdcvqs9xs32y"

boolie = Agent(name="boolie", seed="boolie recovery phrase")
bob = Agent(name="bob", seed="bob recovery phrase") #he is deciding based on video if need to check

FILE_NAME = "agent_message.txt"
with open(FILE_NAME, "r") as file:
    code = file.read()

prompt = ContextPrompt(
    context="Based on the information provided tell me if the person fell. Return True if they fell and False otherwise.",
    text=code,
)


@agent.on_event("startup")
async def send_message(ctx: Context):
    await ctx.send(AI_AGENT_ADDRESS, prompt)

@agent.on_message(Response)
async def handle_response(ctx: Context, sender: str, msg: Response):
    ctx.logger.info(f"Received response from {sender}: {msg.text}")
    await ctx.send(boolie.address, Message(message=msg.text))



bot_token = "8182349154:AAG2LT6gGfUHVs2fRXdbtmIaGWqqVPUjI18"
chat_id=978673064


async def send_tg(msg, chat_id, token=bot_token):
    bot = telegram.Bot(token=token)
    await bot.sendMessage(chat_id=chat_id, text=msg)
    print('Message Sent!')

 
@boolie.on_message(model=Message) #do we need to ask or not
async def boolie_message_handler(ctx: Context, sender: str, mssg: Message):
    message_text = live_chat()
    if message_text == "True":
        await ctx.send(bob.address, Message(message="True"))
    else:
        print("all is okay")

@bob.on_message(model=Message)
async def bob_message_handler(ctx: Context, sender: str, mssg: Message):
    if mssg.message == "True":
        message_text="Help Requested!!"
        await send_tg(msg=message_text, chat_id=chat_id, token=bot_token)
    else:
        print("Fuck tg bots")



# Message to send

bureau = Bureau()
bureau.add(boolie)
#bureau.add(bob)
bureau.add(agent)
bureau.add(bob)
 
 
# This constructor simply ensure that only this script is running
if __name__ == "__main__":
    bureau.run()
