import openai, json, sys
from client.client import MCPClient
from client.agent import MCPAgent
import asyncio
from dotenv import load_dotenv

class ChatBot:
    def __init__(self):
        self.MCPAgent = MCPAgent()

    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")

        while True:
            try:
                query = input("\nQuery: ").strip()

                if query.lower() == 'quit':
                    break

                response = await self.MCPAgent.process_query(query)
                print("\n" + response)

            except Exception as e:
                print(f"\nError: {str(e)}")

    async def cleanup(self):
        """Clean up resources"""
        await self.MCPAgent.cleanup()
    

async def main():
    load_dotenv()
    chatbot = ChatBot()
    try:
        await chatbot.MCPAgent.setup()
        await chatbot.chat_loop()
    finally:
        pass

if __name__ == "__main__":
    asyncio.run(main())