from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low


class ContextPrompt(Model):
    context: str
    text: str


class Response(Model):
    text: str


AGENT_MAILBOX_KEY = "c47b2ef5-5750-439c-9eb9-efe08a5af8bf"
SEED_PHRASE = "bike test"
 
# Now your agent is ready to join the agentverse!
agent = Agent(
    name="mary",
    seed=SEED_PHRASE,
    mailbox=f"{AGENT_MAILBOX_KEY}@https://agentverse.ai",
)
fund_agent_if_low(agent.wallet.address())
print(agent.address)

AI_AGENT_ADDRESS = "agent1q0h70caed8ax769shpemapzkyk65uscw4xwk6dc4t3emvp5jdcvqs9xs32y"


code = "Mary fell of her bike."

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


if __name__ == "__main__":
    agent.run()