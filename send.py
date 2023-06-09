"""
nRF24L01 transmitter
Raspberry Pi Pico and nRF24L01 module
Once per second, a numerical value is sent, and we
checks if we receive a response.
For more info:
www.bekyelectronics.com/raspberry-pico-nrf25l01-micropython/
"""
import ustruct as struct
import utime
from machine import Pin, SPI
from nrf24l01 import NRF24L01

# pin definition for the Raspberry Pi Pico:
spi = SPI(0, sck=Pin(6), mosi=Pin(7), miso=Pin(4))
cfg = {"spi": spi, "csn": 5, "ce": 12}

csn = Pin(cfg["csn"], mode=Pin.OUT, value=1)
ce = Pin(cfg["ce"], mode=Pin.OUT, value=0)
spi = cfg["spi"]
nrf = NRF24L01(spi, csn, ce, channel=60, payload_size=30)

# Addresses (little endian)
pipes = ("1Node", "2Node")

print("NRF24L01 transmitter\n")

nrf.open_tx_pipe(pipes[0])
nrf.open_rx_pipe(1, pipes[1])
nrf.stop_listening()





nrf.set_tx_mode()






counter = 0
while True:
    # allen-remote
    uuid = "17acb8"
    
    print("sending: '{}'".format(uuid))
    
    sent = 0
    error_cnt = 0
    while(sent!=1):
        try:
            sending = nrf.send(struct.pack("6s",  uuid)) # sending the message
            print("'{}' sent".format(uuid))
            sent = 1
        except OSError:
            error_cnt += 1
            if(error_cnt > 100):
                print("Send abandoned")
                break
            # print("Send failed")






    

    start_time = utime.ticks_ms()
    
    nrf.start_listening()
    
    timeout = False
    while not nrf.any() and not timeout:
        if utime.ticks_diff(utime.ticks_ms(), start_time) > 100:
            timeout = True

    if timeout:  # no response received
        print("\nNo response")

    else:  # a response has been received
        buf = nrf.recv()
        response = struct.unpack("6s", buf)[0]
        print("message received:", response)
        

    nrf.stop_listening()







    print("\n----------\n")
    utime.sleep_ms(1000)