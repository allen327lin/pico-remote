import ustruct as struct
import utime
from machine import Pin, SPI
from nrf24l01 import NRF24L01
from micropython import const

# delay between receiving a message and waiting for the next message
POLL_DELAY = const(15)
# Delay between receiving a message and sending the response
# (so that the other pico has time to listen)
SEND_DELAY = const(10)

# Pico pin definition:
spi = SPI(0, sck=Pin(6), mosi=Pin(7), miso=Pin(4))
cfg = {"spi": spi, "csn": 5, "ce": 12}

csn = Pin(cfg["csn"], mode=Pin.OUT, value=1)
ce = Pin(cfg["ce"], mode=Pin.OUT, value=0)
spi = cfg["spi"]
nrf = NRF24L01(spi, csn, ce, channel=60, payload_size=30)

# Addresses
# b"\xe1\xf0\xf0\xf0\xf0", b"\xd2\xf0\xf0\xf0\xf0"
pipes = ("1Node", "2Node") 

nrf.open_tx_pipe(pipes[0])
nrf.open_rx_pipe(1, pipes[1])
nrf.start_listening()

print("nRF24L01 receiver; waiting for the first post...")
led = Pin(25, Pin.OUT)
led.value(0)
while True:
    if nrf.any(): # we received something
        while nrf.any():
            buf = nrf.recv()
            counter = struct.unpack("6s", buf)
            print("message received:", counter[0])
            led.value(1)
            utime.sleep_ms(POLL_DELAY) # delay before next listening
            led.value(0)
        
            
        """response = counter[0]%2 # preparing the response

        utime.sleep_ms(SEND_DELAY) # Give the other Pico a brief time to listen
        nrf.stop_listening()
        try:
            nrf.send(struct.pack("i", response))
        except OSError:
            pass
        print("reply sent:", response)"""
        nrf.start_listening()
print("break")
nrf.set_tx()
