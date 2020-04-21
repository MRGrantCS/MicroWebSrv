from machine import Pin

def relayOff ():
  relay = Pin(15, Pin.OUT)
  relay.value(1)

def relayOn ():
  relay = Pin(15, Pin.OUT)
  relay.value(0)