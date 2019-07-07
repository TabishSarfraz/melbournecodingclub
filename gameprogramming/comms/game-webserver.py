#!/usr/bin/env python

# WS server example

import asyncio
import websockets
import json

USERS = set()

def users_event():
    return json.dumps({'type': 'users', 'count': len(USERS)})

async def notify_users():
    if USERS:       # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])

async def register(websocket):
    USERS.add(websocket)
    print(USERS)
    await notify_users()

async def hello(websocket, path):
    await register(websocket)
    name = await websocket.recv()
    print(f"< {name}")

    greeting = f"Hello {name}!"

    async for message in websocket:
        await websocket.send(greeting)
    print(f"> {greeting}")

start_server = websockets.serve(hello, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
