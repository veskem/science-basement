#!/usr/bin/python

import time
import sys
import numpy as np

import pi_spi
import fdc2214 as fdc

enable_plot = False
if (enable_plot):
    import dynamic_plot as dp

fdc2214 = fdc.FDC2214(115200, '/dev/ttyACM0')

C1 = 0.3
C2 = 1

print ("Press CTRL C to exit")
try:
    time_step = 1.0     # sec, plotting takes ~0.4
    buffer_size = 200   # samples

    time_min = 0; time_max = buffer_size * time_step;
    C_min = -3; C_max = 3;

    if (enable_plot):
        buffer = dp.RingBuffer(buffer_size)
        plot = dp.DynamicPlot(np.linspace(time_min, time_max, buffer_size), True, True)
        plot.format_x('Time / sec', time_min, time_max)
        plot.format_y('C / pF') #, C_min, C_max)

    dout = pi_spi.PiSpi_8KO(True)
    dout.write(0)

    keep_looping = True
    while(keep_looping):
        t1 = time.time()

        C = fdc2214.read_ch1()
        if (abs(C) <= C1):
            dout.write(0)
        elif (abs(C) >= C2):
            dout.write(255)

        print("\rC = %.2f pF" % C, end='')
        
        # add measurement to the graph
        if(enable_plot):
            buffer.append(C)
            plot.update_y(buffer.get_lifo())
            keep_looping = plot.opened()

        time.sleep(max(0, time_step - (time.time() - t1)))

            
except KeyboardInterrupt:   # Press CTRL C to exit Program
    fdc.close()
    sys.exit(0)
