# aiocqhttp Forward WebSocket Support

This document describes the forward WebSocket support added to aiocqhttp, enabling the library to work as a WebSocket client connecting to OneBot servers.

## Overview

aiocqhttp now supports three connection modes:

1. **HTTP** - Traditional HTTP API calls (existing)
2. **Reverse WebSocket** - OneBot connects to your server (existing)
3. **Forward WebSocket** - Your bot connects to OneBot server (**NEW**)

## Quick Start

### Installation

To use forward WebSocket functionality, install the websockets dependency:

```bash
pip install 'aiocqhttp[forward-ws]'
# or for all optional dependencies:
pip install 'aiocqhttp[all]'
```

### Basic Usage

Simply change your `api_root` from `http://` to `ws://`:

```python
from aiocqhttp import CQHttp

# Before: HTTP mode
# bot = CQHttp(api_root="http://127.0.0.1:5700")

# After: Forward WebSocket mode
bot = CQHttp(api_root="ws://127.0.0.1:3001")

@bot.on_message('private')
async def handle_private_message(event):
    await bot.send(event, f"You said: {event.message}")

# Start the server (for reverse WebSocket/HTTP endpoints)
bot.run(host="127.0.0.1", port=8080)
```

That's it! No other code changes needed.

## Connection Priority

When multiple connection methods are available, aiocqhttp uses this priority:

1. **Forward WebSocket** (highest priority)
2. **Reverse WebSocket**
3. **HTTP** (lowest priority)

This ensures the most efficient connection method is used.

## Features

### API Calls

All existing API methods work exactly the same:

```python
# These work identically in all connection modes
await bot.send_private_msg(user_id=123456, message="Hello")
await bot.get_friend_list()
await bot.set_group_ban(group_id=789, user_id=123456, duration=60)
```

### Event Handling

Events are received and processed through the same event system:

```python
@bot.on_message('group')
async def handle_group_message(event):
    if event.message.startswith('/ping'):
        await bot.send(event, 'Pong!')

@bot.on_notice('group_increase')
async def welcome_new_member(event):
    await bot.send_group_msg(
        group_id=event.group_id,
        message=f"Welcome {event.user_id}!"
    )
```

### Connection Events

Monitor WebSocket connection status:

```python
@bot.on_websocket_connection
async def on_connected(event):
    print("Forward WebSocket connected!")
    # Optionally test the connection
    try:
        login_info = await bot.get_login_info()
        print(f"Connected as: {login_info.get('nickname')}")
    except Exception as e:
        print(f"Connection test failed: {e}")
```

## Configuration

### URL Format

- **WebSocket**: `ws://host:port/path`
- **Secure WebSocket**: `wss://host:port/path`
- **With authentication**: Include `access_token` parameter

```python
# Basic WebSocket
bot = CQHttp(api_root="ws://127.0.0.1:3001")

# Secure WebSocket
bot = CQHttp(api_root="wss://your-server.com:443/ws")

# With authentication
bot = CQHttp(
    api_root="ws://127.0.0.1:3001",
    access_token="your_token_here"
)
```

### Timeout Configuration

Control connection and API call timeouts:

```python
bot = CQHttp(
    api_root="ws://127.0.0.1:3001",
    api_timeout_sec=30  # 30 second timeout for API calls
)
```

## OneBot Server Configuration

Configure your OneBot implementation to enable forward WebSocket:

### go-cqhttp

```yaml
servers:
  - ws:
      host: 127.0.0.1
      port: 3001
```

### NapCat

```json
{
  "http": {
    "enable": false
  },
  "ws": {
    "enable": true,
    "host": "127.0.0.1",
    "port": 3001
  }
}
```

## Migration Guide

### From HTTP

```python
# Old: HTTP mode
bot = CQHttp(api_root="http://127.0.0.1:5700")

# New: Forward WebSocket mode
bot = CQHttp(api_root="ws://127.0.0.1:3001")
```

### From Reverse WebSocket Only

If you were only using reverse WebSocket (no `api_root`), you can now add forward WebSocket:

```python
# Old: Reverse WebSocket only (for events)
bot = CQHttp()  # No API calls possible

# New: Forward WebSocket (events + API calls)
bot = CQHttp(api_root="ws://127.0.0.1:3001")
```

## Troubleshooting

### Import Error

```
ImportError: websockets package is required for forward WebSocket support
```

**Solution**: Install the websockets dependency:
```bash
pip install 'aiocqhttp[forward-ws]'
```

### Connection Failed

```
NetworkError: WebSocket connection failed
```

**Solutions**:
1. Verify OneBot server is running and listening on the specified port
2. Check firewall settings
3. Verify URL format (ws:// or wss://)
4. Check access_token if authentication is required

### No Events Received

**Check**:
1. OneBot server is configured to send events to WebSocket clients
2. Bot has proper permissions in groups/chats
3. Event handlers are properly registered

## Technical Details

### Message Routing

The forward WebSocket implementation automatically routes messages:

- **API Responses**: Messages with `echo` field → API response handling
- **OneBot Events**: Messages with `post_type` field → Event handling

### Connection Management

- Automatic connection on first API call
- Connection reuse for subsequent calls
- Graceful reconnection on connection loss
- Proper cleanup on bot shutdown

### Integration

Forward WebSocket integrates seamlessly with existing aiocqhttp features:

- Event bus system
- Message classes
- Error handling
- Synchronous API wrapper
- Before-sending hooks

## Examples

See `demo_forward_ws.py` for complete examples.

## Compatibility

- Python 3.7+
- OneBot v11/v12 compatible servers
- Works alongside existing HTTP and reverse WebSocket functionality