#!/usr/bin/python

# MIT License
# 
# Copyright (c) 2020 Ryo Okazaki
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import time
import VL53L0X
import argparse
from pythonosc import udp_client

if __name__ == "__main__":
    # Create a VL53L0X object
    tof = VL53L0X.VL53L0X()
    
    # Start ranging
    tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
    
    timing = tof.get_timing()
    if (timing < 20000):
        timing = 20000
    print ("Timing %d ms" % (timing/1000))

    # Parse args
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1", help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=5005, help="The port the OSC server is listening on")
    args = parser.parse_args()

    client = udp_client.SimpleUDPClient(args.ip, args.port)
    
    try:
        while (1):
            distance = tof.get_distance()
            if (distance > 0):
                print ("%d mm, %d cm" % (distance, distance/10))
                client.send_message("/distance", distance)
        
            time.sleep(0.5)
    except KeyboardInterrupt:
        tof.stop_ranging()
