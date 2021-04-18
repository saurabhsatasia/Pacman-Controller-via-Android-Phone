import socket
import argparse
from pynput.keyboard import Key, Controller

keyboard = Controller()
# host = '192.168.137.1' # 150.254.5.4
# port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

def control(signals):
    for signal in signals["signal_release"]:
        keyboard.release(signal)
    keyboard.press(signals["signals_on"])


def main(host, port):
    print(f"host::{host} , port::{port}")
    s.bind((host, port))
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
                print(f"g_x::{g_x}, g_y::{g_y}, g_z::{g_z}")

                # we need only x and y to control pacman
                # halt
                if (-3 < g_x < 3) and (-3 < g_y < 3):
                    print("HALT")
                    signals_dict = {"signal_release": [Key.up, Key.down, Key.left, Key.right],
                                    "signal_on": Key.Space}
                    control(signals=signals_dict)

                # forward
                elif (-4 > g_x) and (-3 < g_y < 3):
                    print("FORWARD")
                    signals_dict = {"signal_release": [Key.space, Key.down, Key.left, Key.right],
                                    "signal_on": Key.up}
                    control(signals=signals_dict)

                # retreat
                elif (4 < g_x) and (-3 < g_y < 3):
                    print("RETREAT")
                    signals_dict = {"signal_release": [Key.up, Key.space, Key.left, Key.right],
                                    "signal_on": Key.down}
                    control(signals=signals_dict)

                # left
                elif (-3 < g_x < 3) and (-4 > g_y):
                    print("LEFT")
                    signals_dict = {"signal_release": [Key.up, Key.down, Key.space, Key.right],
                                    "signal_on": Key.left}
                    control(signals=signals_dict)

                # right
                elif (-3 < g_x < 3) and (4 < g_y):
                    print("RIGHT")
                    signals_dict = {"signal_release": [Key.up, Key.down, Key.left, Key.space],
                                    "signal_on": Key.right}
                    control(signals=signals_dict)

        except (KeyboardInterrupt, SystemExit):
            raise  # -0.060,  1.687,  9.660
        except Exception as e:
            print(e)


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--port', default=5555)
    args.add_argument('--host', default="192.168.137.1")
    # args.add_argument('--csv', default="signal_data.csv")
    parsed_args = args.parse_args()
    main(parsed_args.host, parsed_args.port)

