import asyncio
import websockets
import json


async def main():
    uri = "ws://localhost:6123"

    async with websockets.connect(uri) as websocket:
        await websocket.send("sub -e window_managed")

        while True:
            json_response = {}
            response = await websocket.recv()
            try:
                if not response:
                    raise ValueError("response is empty")
                json_response = json.loads(response)
                    
                sizePercentage = json_response.get("data",{}).get("managedWindow",{}).get(
                    "tilingSize", None
                ) 
                if sizePercentage is not None and sizePercentage <= 0.5:
                    await websocket.send('command toggle-tiling-direction')
            except KeyError:
                pass


if __name__ == "__main__":
    asyncio.run(main())