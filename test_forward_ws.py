#!/usr/bin/env python3
"""
Basic test script for forward WebSocket functionality.
"""

import asyncio
import logging
from aiocqhttp import CQHttp

# Configure logging
logging.basicConfig(level=logging.DEBUG)

async def test_http_mode():
    """Test that HTTP mode still works."""
    print("Testing HTTP mode...")
    bot = CQHttp(api_root="http://127.0.0.1:5700")
    assert hasattr(bot._api, '_http_api')
    assert bot._api._http_api is not None
    assert bot._api._wsf_api is None
    print("✓ HTTP mode configuration works")

async def test_websocket_detection():
    """Test that WebSocket URL detection works."""
    print("Testing WebSocket URL detection...")

    try:
        # This should create WebSocketForwardApi
        bot = CQHttp(api_root="ws://127.0.0.1:8080")
        assert hasattr(bot._api, '_wsf_api')
        assert bot._api._wsf_api is not None
        assert bot._api._http_api is None
        print("✓ WebSocket mode configuration works")

        # Clean up
        if bot._api._wsf_api:
            await bot._api._wsf_api.close()

    except ImportError as e:
        print(f"! WebSocket functionality requires 'websockets' package: {e}")
        print("  Install with: pip install 'aiocqhttp[forward-ws]'")

async def test_wss_detection():
    """Test that WSS (secure WebSocket) detection works."""
    print("Testing WSS URL detection...")

    try:
        bot = CQHttp(api_root="wss://example.com:8080")
        assert hasattr(bot._api, '_wsf_api')
        assert bot._api._wsf_api is not None
        print("✓ WSS mode configuration works")

        # Clean up
        if bot._api._wsf_api:
            await bot._api._wsf_api.close()

    except ImportError as e:
        print(f"! WebSocket functionality requires 'websockets' package: {e}")

async def test_backward_compatibility():
    """Test that existing functionality isn't broken."""
    print("Testing backward compatibility...")

    # Test default (no api_root)
    bot = CQHttp()
    assert hasattr(bot._api, '_http_api')
    print("✓ Default configuration works")

    # Test None api_root
    bot2 = CQHttp(api_root=None)
    assert hasattr(bot2._api, '_http_api')
    print("✓ None api_root works")

async def main():
    """Run all tests."""
    print("Testing aiocqhttp forward WebSocket implementation...\n")

    await test_backward_compatibility()
    await test_http_mode()
    await test_websocket_detection()
    await test_wss_detection()

    print("\n✓ All tests completed!")

if __name__ == "__main__":
    asyncio.run(main())