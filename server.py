from quart import Quart, websocket, render_template, g
import aioredis
import asyncio
import json

app = Quart(__name__)


@app.route("/", methods=["GET"])
async def home():
    g.cfg = {}
    return await render_template("home.jinja2")


@app.websocket("/ws")
async def ws():
    sub = await aioredis.create_redis("redis://localhost/4")

    res = await sub.subscribe("chan:1")
    ch1 = res[0]
    while True:
        # print('inner infinite loop')
        await asyncio.sleep(2)
        while await ch1.wait_message():
            # print('as here')
            msg = await ch1.get_json()
            # print(f"Sending to WS: {msg}, {type(msg)}")
            await websocket.send(json.dumps(msg))


if __name__ == "__main__":
    app.run(port=5000)
