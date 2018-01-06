import time
import button
import data
import display


def q23_request(led_matrix):
    raw_response = data.make_request('MTABC_Q23', 503862)
    valid_until, json_buses = data.parse_data(raw_response)
    buses = data.simplify_parsed_data(json_buses)

    led_matrix.device.contrast(32)
    led_matrix.print_msg(str(buses[0]))

if __name__ == '__main__':
    leds = display.Matrix()
    b = button.Button(18)
    b.on_press(lambda pin: q23_request(leds))
    while True:
        time.sleep(1)
