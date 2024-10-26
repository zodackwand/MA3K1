from uagents import Agent, Context, Bureau, Model
import telegram, asyncio

class Message(Model):
    message: str
 
alice = Agent(name="alice", seed="alice recovery phrase")
bob = Agent(name="bob", seed="bob recovery phrase")

bot_token = "8182349154:AAG2LT6gGfUHVs2fRXdbtmIaGWqqVPUjI18"
message_text = input("Enter the message you want to send: ")
chat_id=978673064



async def send(msg, chat_id, token=bot_token):
    bot = telegram.Bot(token=token)
    await bot.sendMessage(chat_id=chat_id, text=msg)
    print('Message Sent!')

@bob.on_event("startup")
async def introduce_agent(ctx: Context):
    ctx.logger.info(f"Hello, I'm agent {bob.name} and my address is {bob.address}.")
    await ctx.send(alice.address, Message(message=message_text))

@alice.on_message(model=Message)
async def alice_message_handler(ctx: Context, sender: str, mssg: Message):
    ctx.logger.info(f"Hello, I'm agent {alice.name} and my address is {alice.address}.")
    await send(msg=mssg.message, chat_id=chat_id, token=bot_token)



#bot = Bot(token=bot_token)

# Message to send

bureau = Bureau()
bureau.add(alice)
bureau.add(bob)
 
 
# This constructor simply ensure that only this script is running
if __name__ == "__main__":
    bureau.run()
