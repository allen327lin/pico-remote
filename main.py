import ustruct as struct
import utime
from machine import Pin, SPI
from nrf24l01 import NRF24L01

# delay between receiving a message and waiting for the next message
POLL_DELAY = const(15)
# Delay between receiving a message and sending the response
# (so that the other pico has time to listen)
SEND_DELAY = const(10)

# pin definition for the Raspberry Pi Pico:
spi = SPI(0, sck=Pin(6), mosi=Pin(7), miso=Pin(4))
cfg = {"spi": spi, "csn": 5, "ce": 12}

csn = Pin(cfg["csn"], mode=Pin.OUT, value=1)
ce = Pin(cfg["ce"], mode=Pin.OUT, value=0)
spi = cfg["spi"]
nrf = NRF24L01(spi, csn, ce, channel=60, payload_size=30)

# Addresses (little endian)
pipes = [b"1Node", b"2Node"]

nrf.open_tx_pipe(pipes[0])
nrf.open_rx_pipe(1, pipes[1])

led = Pin(25, Pin.OUT)
led.value(0)

print("Main ready.\n")

nrf.start_listening()

while True:
    if nrf.any(): # we received something
        while nrf.any():
            buf = nrf.recv()
            counter = struct.unpack("6s", buf)[0]
            print("message received:", counter)
            print(type(counter))
            led.value(1)
            utime.sleep_ms(POLL_DELAY) # delay before next listening
            led.value(0)
        
                
        nrf.stop_listening()
        nrf.set_tx_mode()
        utime.sleep_ms(POLL_DELAY)
        
        
        sent = 0
        error_cnt = 0
        while(sent!=1):
            try:
                sending = nrf.send(counter) # sending the message
                print("'{}' sent".format(counter))
                sent = 1
            except OSError:
                error_cnt += 1
                if(error_cnt > 100):
                    print("Send abandoned")
                    break
                # print("Send failed.")
        
            
        nrf.start_listening()