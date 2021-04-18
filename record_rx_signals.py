import socket
import argparse

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)


def record_data(signals, csv_file):
    with open(csv_file, "a") as f:
        string = ""
        for signal in signals["dependent_var"]:
            string += f"{signal},"
        string += f"{signals['target']}\n"
        f.writelines(string)


def rule_based_module(gravity_data, csv):
    g_x, g_y, g_z = gravity_data
    print(f"g_x::{g_x}, g_y::{g_y}, g_z::{g_z}")

    # we need only x and y to control pacman
    # halt
    if (-3 < g_x < 3) and (-3 < g_y < 3):
        print("HALT")
        signals_dict = {"dependent_var": gravity_data[:-1],
                        "target": "0"}
        record_data(signals_dict, csv)

    # forward
    elif (-4 > g_x) and (-3 < g_y < 3):
        print("FORWARD")
        signals_dict = {"dependent_var": gravity_data[:-1],
                        "target": "1"}
        record_data(signals_dict, csv)

    # retreat
    elif (4 < g_x) and (-3 < g_y < 3):
        print("RETREAT")
        signals_dict = {"dependent_var": gravity_data[:-1],
                        "target": "2"}
        record_data(signals_dict, csv)

    # left
    elif (-3 < g_x < 3) and (-4 > g_y):
        print("LEFT")
        signals_dict = {"dependent_var": gravity_data[:-1],
                        "target": "3"}
        record_data(signals_dict, csv)

    # right
    elif (-3 < g_x < 3) and (4 < g_y):
        print("RIGHT")
        signals_dict = {"dependent_var": gravity_data[:-1],
                        "target": "4"}
        record_data(signals_dict, csv)


def init_csvFile(csv_file):
    with open(csv_file, "a") as f:
        string = "g_x, g_y, TARGET\n"
        f.writelines(string)


def main(host, port, csv):
    print(f"host::{host} , port::{port}")
    s.bind((host, port))
    init_csvFile(csv)
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
                rule_based_module(gravity_data, csv)


        except (KeyboardInterrupt, SystemExit):
            raise  # -0.060,  1.687,  9.660
        except Exception as e:
            print(e)


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--port', default=5555)
    args.add_argument('--host', default="192.168.137.1")
    args.add_argument('--csv', default="signal_data.csv")
    parsed_args = args.parse_args()
    main(parsed_args.host, parsed_args.port, parsed_args.csv)

