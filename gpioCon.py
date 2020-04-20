from machine import Pin
from time import sleep

def relayOn ():
  relay = Pin(15, Pin.OUT)
  relay.value(1)

def relayOut ():
  relay = Pin(15, Pin.OUT)
  relay.value(0)