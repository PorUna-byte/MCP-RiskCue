# chatbot.py
import asyncio
from dotenv import load_dotenv
from client.agent import MCPAgent


class ChatBot:
    def __init__(self, agent: MCPAgent):
        self.agent = agent

    async def chat_loop(self):
        print("\nMCP Client Started!  (type 'quit' to exit)")
        while True:
            try:
                query = input("\nQuery: ").strip()
                if query.lower() == "quit":
                    break
                reply = await self.agent.process_query(query)
                print("\n" + reply)
            except Exception as e:
                print(f"\n[Error] {e}")

        print(self.agent.history)

async def main():
    load_dotenv()
    async with MCPAgent() as agent:      # <— 关键：统一 context 管理
        bot = ChatBot(agent)
        await bot.chat_loop()


if __name__ == "__main__":
    asyncio.run(main())
