#!/usr/bin/env python3
"""
Example usage of aiocqhttp with forward WebSocket support.
"""

import asyncio
import logging
from aiocqhttp import CQHttp

# Configure logging to see what's happening
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def demo_forward_websocket():
    """
    Demo showing how to use forward WebSocket with aiocqhttp.
    """
    print("=== aiocqhttp Forward WebSocket Demo ===\n")

    # Create bot with forward WebSocket
    # Replace with your actual OneBot server URL
    bot = CQHttp(api_root="ws://127.0.0.1:3001")

    @bot.on_message('private')
    async def handle_private_message(event):
        logger.info(f"Received private message: {event.message}")
        # Echo the message back
        await bot.send(event, f"You said: {event.message}")

    @bot.on_message('group')
    async def handle_group_message(event):
        logger.info(f"Received group message: {event.message}")
        if str(event.message).startswith("/echo"):
            await bot.send(event, f"Echo: {str(event.message)[5:]}")

    @bot.on_websocket_connection
    async def on_connected(event):
        logger.info("Forward WebSocket connected!")
        # Test API call
        try:
            login_info = await bot.get_login_info()
            logger.info(f"Bot login info: {login_info}")
        except Exception as e:
            logger.error(f"Failed to get login info: {e}")

    print("Bot configured with forward WebSocket!")
    print("Features:")
    print("- Automatically connects to OneBot server as WebSocket client")
    print("- Receives OneBot events (messages, notices, etc.)")
    print("- Can make API calls through the same WebSocket connection")
    print("- Falls back to reverse WebSocket/HTTP if forward WebSocket fails")
    print("\nNote: This demo requires a running OneBot server at ws://127.0.0.1:3001")
    print("Examples: go-cqhttp, NapCat, or other OneBot implementations")

    # In a real application, you would start the bot server:
    # await bot.run_task(host="127.0.0.1", port=8080)

async def demo_migration_example():
    """
    Show how existing code can easily migrate to forward WebSocket.
    """
    print("\n=== Migration Example ===\n")

    print("Before (HTTP):")
    print('bot = CQHttp(api_root="http://127.0.0.1:5700")')

    print("\nAfter (Forward WebSocket):")
    print('bot = CQHttp(api_root="ws://127.0.0.1:3001")')

    print("\nThat's it! No other code changes needed.")
    print("- Same API methods (bot.send_private_msg, etc.)")
    print("- Same event handlers (@bot.on_message, etc.)")
    print("- Same configuration options")

async def demo_unified_api():
    """
    Show how UnifiedApi prioritizes different connection types.
    """
    print("\n=== UnifiedApi Priority Demo ===\n")

    # This would try forward WebSocket, then reverse WebSocket, then HTTP
    # (In practice, you'd only configure one at a time)
    print("Priority order:")
    print("1. Forward WebSocket (ws://... or wss://...)")
    print("2. Reverse WebSocket (when OneBot connects to your server)")
    print("3. HTTP (http://... or https://...)")
    print("\nThis ensures the best available connection method is used.")

if __name__ == "__main__":
    async def main():
        await demo_forward_websocket()
        await demo_migration_example()
        await demo_unified_api()

    asyncio.run(main())