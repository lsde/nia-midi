#!/usr/bin/env python3
import pyglet
import sys
import threading
import time
import nia as NIA
import rtmidi

# global scope stuff
nia = None
nia_data = None

def update(x):
    """
        The main pyglet loop. This function starts a data collection thread,
        whilst processing and displying the previously collected data. At the
        end of the loop the threads are joined
    """

    # kick-off processing data from the NIA
    data_thread = threading.Thread(target=nia_data.get_data)
    data_thread.start()

    # get the fourier data from the NIA
    data, steps = nia_data.fourier(nia_data)
    print(steps)
    for step in steps:
        nia_note = int(step) * 12
        note_on = [0x90, nia_note, 112] # channel 1, XXX, velocity 112
        note_off = [0x80, nia_note, 0]
        midiout.send_message(note_on)
        time.sleep(0.01)
        midiout.send_message(note_off)
        time.sleep(0.01)

    # wait for the next batch of data to come in
    data_thread.join()

    # exit if we cannot read data from the device
    if nia_data.AccessDeniedError:
        sys.exit(1)

if __name__ == "__main__":
    """
        The main function opens the NIA, creates a pyglet window, and then
        enters the main pyglet loop (update). When the main pyglet loop exits,
        the NIA is closed out and the programs exits successfully.
    """
    # open the NIA, or exit with a failure code
    nia = NIA.NIA()
    if not nia.open():
        sys.exit(1)

    midiout = rtmidi.MidiOut()
    available_ports = midiout.get_ports()
    print(available_ports)

    if available_ports: midiout.open_port(1)
    else: midiout.open_virtual_port("nia-midi")

    # start collecting data
    milliseconds = 250
    nia_data = NIA.NiaData(nia, milliseconds)

    # open a window and schedule continuous updates
    with midiout:
        pyglet.clock.schedule(update)
        pyglet.app.run()

    # when pyglet exits, close out the NIA and exit gracefully
    del midiout
    nia.close()
    sys.exit(0)
