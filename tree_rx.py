import socket
import argparse
import joblib
from pynput.keyboard import Key, Controller

keyboard = Controller()
# host = '192.168.137.1' # 150.254.5.4
# port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

def control(signals):
    print(signals["control"])
    for signal in signals["signal_release"]:
        keyboard.release(signal)
    keyboard.press(signals["signals_on"])


def main(host, port, model):
    print(f"host::{host} , port::{port}")
    s.bind((host, port))
    loaded_model = joblib.load(model)
    while True:
        try:
            BYTE = 8192
            message, address = s.recvfrom(BYTE)
            LIST_DATA = str(message).split(",")
            # print(str(message).split(","))
            received_length = len(LIST_DATA) # sometimes 13 or 17
            expected_length = 17
            if received_length == expected_length:
                gravity_data = LIST_DATA[-3:]
                for idx, gravity in enumerate(gravity_data):
                    gravity_data[idx] = float(gravity.strip()[:-1])
                # print(gravity_data)  # --> [-2.86, 3.49, 8.704]
                g_x, g_y, g_z = gravity_data

                result = loaded_model.predict([gravity_data[:-1]])[0]  # [[], []]

                tally = [
                    {
                        "signal_release":[Key.up, Key.down, Key.left, Key.right],
                        "signal_on":Key.space,
                        "control": "halt"
                    },
                    {
                        "signal_release": [Key.space, Key.down, Key.left, Key.right],
                        "signal_on": Key.up,
                        "control": "forward"
                    },
                    {
                        "signal_release": [Key.up, Key.space, Key.left, Key.right],
                        "signal_on": Key.down,
                        "control": "retreat"
                    },
                    {
                        "signal_release": [Key.up, Key.down, Key.space, Key.right],
                        "signal_on": Key.left,
                        "control": "left"
                    },
                    {
                        "signal_release": [Key.up, Key.down, Key.left, Key.space],
                        "signal_on": Key.right,
                        "control": "right"
                    }
                ]

                control(signals=tally[result])

        except (KeyboardInterrupt, SystemExit):
            raise  # -0.060,  1.687,  9.660
        except Exception as e:
            print(e)


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--port', default=5555)
    args.add_argument('--host', default="192.168.137.1")
    args.add_argument('--model', default="tree_clf.model")
    parsed_args = args.parse_args()
    main(parsed_args.host, parsed_args.port, parsed_args.model)

