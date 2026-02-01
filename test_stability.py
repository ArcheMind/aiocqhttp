#!/usr/bin/env python3
"""
Test for timing and attribute access safety.
"""

import asyncio
from aiocqhttp import CQHttp

async def test_early_api_access():
    """Test that self.api is always accessible, even before _configure."""
    print("Testing early API access safety...")

    # This should work without errors
    bot = CQHttp()

    # Should be accessible immediately after __init__
    api = bot.api
    assert api is not None
    print("✓ bot.api accessible immediately after __init__")

    # Should handle calls gracefully (though they may fail due to no config)
    try:
        # This will likely fail due to no api_root, but should not crash
        await bot.get_login_info()
    except Exception as e:
        # Expected - no api_root configured
        print(f"✓ API call fails gracefully: {type(e).__name__}")

    print("✓ Early API access safety test passed")

async def test_inheritance_safety():
    """Test that inheritance scenarios work."""
    print("Testing inheritance safety...")

    class CustomBot(CQHttp):
        def __init__(self):
            super().__init__()
            # This should work - accessing api in child __init__
            self.my_api = self.api
            assert self.my_api is not None

    bot = CustomBot()
    print("✓ Inheritance with early API access works")

async def test_reconfiguration():
    """Test that API can be reconfigured multiple times."""
    print("Testing reconfiguration safety...")

    bot = CQHttp()
    original_api = bot.api

    # Reconfigure to HTTP
    bot._configure(api_root="http://127.0.0.1:5700")
    assert bot.api is original_api  # Same object
    assert bot.api._http_api is not None
    print("✓ HTTP reconfiguration works")

    # Reconfigure to WebSocket
    bot._configure(api_root="ws://127.0.0.1:3001")
    assert bot.api is original_api  # Still same object
    assert bot.api._wsf_api is not None
    print("✓ WebSocket reconfiguration works")

    # Clean up
    if bot.api._wsf_api:
        await bot.api._wsf_api.close()

async def main():
    print("Testing SDK stability and timing safety...\n")

    await test_early_api_access()
    await test_inheritance_safety()
    await test_reconfiguration()

    print("\n✓ All stability tests passed!")

if __name__ == "__main__":
    asyncio.run(main())