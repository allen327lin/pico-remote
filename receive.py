"""
nRF24L01 receiver
Raspberry Pi Pico and nRF24L01 module.
If an integer is received, it is acknowledged by flipping its modulo.
For more info:
www.bekyelectronics.com/raspberry-pico-nrf25l01-micropython/
"""
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

# pin definition for the Raspberry Pi Pico:
spi = SPI(0, sck=Pin(6), mosi=Pin(7), miso=Pin(4))
cfg = {"spi": spi, "csn": 5, "ce": 12}

csn = Pin(cfg["csn"], mode=Pin.OUT, value=1)
ce = Pin(cfg["ce"], mode=Pin.OUT, value=0)
spi = cfg["spi"]
nrf = NRF24L01(spi, csn, ce, channel=60, payload_size=30)

# Addresses (little endian)
pipes = (b"\xe1\xf0\xf0\xf0\xf0", b"\xd2\xf0\xf0\xf0\xf0")

nrf.open_tx_pipe(pipes[1])
nrf.open_rx_pipe(1, pipes[0])



# buf = struct.pack("i", 0)
# print(buf)






print("nRF24L01 receiver; waiting for the first post...\n")


nrf.start_listening()
while True:
    buf = nrf.recv()
    counter = struct.unpack("i", buf)
    if(counter[0]!=0):
        print("message received:", counter[0])
        print("buf:", buf)
    
    if nrf.any():
        nrf.stop_listening()
        
        
        buf = nrf.recv()
        counter = struct.unpack("i", buf)
        print(counter)
        print("message received:", counter[0])
        print("buf:", buf)
        
        
        
        
        
        
        # utime.sleep_ms(POLL_DELAY) # delay before next listening
            
        response = counter[0]

        # utime.sleep_ms(SEND_DELAY) # Give the other Pico a brief time to listen
        
        
        
        
        
        
        
        sent = 0
        error_cnt = 0
        while(sent!=1):
            try:
                nrf.send(struct.pack("i", response))
                print("reply sent:", response)
                sent = 1
            except OSError:
                error_cnt += 1
                if(error_cnt > 100):
                    print("Send abandoned")
                    break
                # print("Send failed")
        
        
        
        
        
        print("\n----------\n")
        nrf.start_listening()