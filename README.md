Arcade Machine Controller
=========================

This code is quite niche but contains some aspects that may be useful for some people.

This is a Micropython project that is used to control the hardware in a custom
built RetroPi (Raspberry Pi based emulator for MAME and other consoles) build.

This code is designed to work on an ESP32 microcontroller running Micropython.

What is here?
-------------

The ESP32 controls a few bits of hardware:

* A 4 channel power relay which switches:
    * Power to the Raspeberry Pi 4 (5VDC)
    * Power to the monitor (12VDC)
    * Power to the audio amplifier (12VDC)
    * Power to a 40x8 WS2812B LED array (5VDC) - More on this later
* An SD Card reader
* Sending data to a 40x8 WS2812B LED array
* 16 Microswitch LEDs through two linked shift registers
* A bell (A solenoid and a bicycle bell)
* The mains switch for a D19 plug panel
* Safely switching the Raspberry Pi off
* A threaded Moore Finite State Machine

The 4 Channel Relay Board
-------------------------

This is a 5VDC board with 4 SRD-05VDC-SL-C relays. There is a single dual rail arcade
power supply which supplies both 12VDC and 5VDC (+/- @ 1A and 16A). As soon as the
PSU is plugged into the power, the ESP32 is immediately running and monitoring the
power switch on an interrupt.

If an on signal from the switch is detected, the ESP32 then triggers the relays to start
the system.

If an off signal is detected, the ESP32 will switch everything off with the exception of
the Raspberry Pi, which it will instruct to power down safely. Once off, it will shut off
the power totally leaving the ESP32 in lower power mode waiting for the next on signal.

This enables the system to delay the power feeds for each component as everything switches
on or off.

The SD Card Reader
------------------

This is a simple SPI based card reader which has the card detection facility attached to
a pin interrupt. This means that we can auto-mount the SD card.

WS2812B LED Array
-----------------

The ESP32 contains a built in NeoPixel library which provides very basic communication
to the LEDs. This library expands the capability by adding several abstractions to
deal with images.

A NeoDevice which is used to control the boards directly. It understands the layout of
the board, such as if the LED arrangement is zig-zag or in an snake arrangement. It
will translate x/y coordinates to the physical position on the array.

An image handling library which allows:
* Loading images from file

A viewport library which can provide a canvas larger than the device, allowing panning
across an image.

A basic drawing library with the ability to draw lines, circles, rectangles, fills etc.

A typeface library and a text renderer.

Microswitch LED Controls
------------------------

This library allows the control of many LEDs through an arrangement of shift registers
attached to the ESP32. With many shift registers attached to each other any number
of LEDs can be controlled through only 4 pins on the ESP32.

The Bell
--------

This is a bicycle bell and a solenoid. The library deals with the signalling necessary
to make it ring. It has all the timing plus it has some monotonic tunes built in.

The Finite State Machine
------------------------

Although this is not a hardware controller, it is important in that it uses the
under-documented Micropython _thread library to provide a Moore based FSM.

This class allows the definition of states and transitions by Micropython callables
defined in a simple dictionary object. Each state transition includes three phases:

1. Exiting a previous state
2. Entering the new state
3. Looping while in the current state

Along with this, there is a timer based event system for traversing the FSM. It will
also allow interrupts from the ESP32 pins.

Transferring to the ESP32
=========================

You will need a Micropython firmware and esptool.py

There are plenty of resources available online to perform the upload.