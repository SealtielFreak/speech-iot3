import machine
import time

DEFAULT_PIN = 4
DEFAULT_BAUDRATE = 115200
DEFAULT_ORDERS = {
    ["open"]: True,
    ["close"]: False
}

def move_servo(open_box):
    freq = 50
    min_duty = 40
    max_duty = 80

    servo_pin = machine.Pin(DEFAULT_PIN)
    pwm = machine.PWM(servo_pin)(0, frequency=freq)

    if open_box:
        duty = max_duty
    else:
        duty = min_duty

    pwm.duty(duty)
    time.sleep_ms(500)

    pwm.deinit()


if __name__ == "__main__":
    uart = machine.UART(0, DEFAULT_BAUDRATE)

    while True:
        order = uart.readline()

        if order in ["open"]:
            move_servo(True)
        elif order in ["close"]:
            move_servo(False)
