import websocket
import _thread
import time
import json

previous_len = None


def get_color(number):
    colors = {
        0: "Branco",
        1: "Vermelho",
        2: "Preto"
    }
    return colors.get(number,)


def on_message(ws, message):
    global previous_len
    if "roulette.update" in message:
        data = json.loads(message.replace('42["', '["'))[1]["payload"]
        if data["roll"] == 0 and len(data.get("bets")) != previous_len:
            print(fr'Giro anterior {data["roll"]}, cor {get_color(data["color"])}')
            previous_len = len(data.get("bets"))
        elif data.get("roll") and len(data.get("bets")) > 0 and len(data.get("bets")) != previous_len:
            print(fr'Giro anterior {data["roll"]}, cor {get_color(data["color"])}')
            previous_len = len(data.get("bets"))

        ws.send('2')

    # print(message)


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


def on_open(ws):

    def run(*args):
        time.sleep(1)
        message = '%d["cmd", {"id": "subscribe", "payload": {"room": "roulette"}}]' % 420
        ws.send(message)
        time.sleep(0.1)
        message = '%d["cmd", {"id": "subscribe", "payload": {"room": "chat_room_2"}}]' % 421
        ws.send(message)

    _thread.start_new_thread(run, ())


if __name__ == "__main__":
    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://api-v2.blaze.com/replication/?EIO=3&transport=websocket",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close
                                )

    ws.run_forever()
