# ===============================================
# Sample code to receive measurements from LDC1000, FDC2214 and DrDaq modules
# (c) 2017 Mihkel Veske
# ===============================================

import time
import signal

import fdc2214
import ldc1000
import drdaq
import tools
import constants as const

# ===============================================
# === Some simple macros
# ===============================================

# apply formatting for measured values
def format_f(value):
    return ", %.3f" % value
    
def format_i(value):
    return ", %d" % value    

def signal_handler(signum, stack):
    global keep_running
    keep_running = False

# ===============================================
# === Code itself
# ===============================================

signal.signal(signal.SIGINT, signal_handler)
keep_running = True
full_functional = True

print("T[degC], C[pF], dC[pF], L[uH],  Z[kOHm]")

# Initialize
if (full_functional):
    ldc1000.config()
    fdc2214.config()
    drdaq.init()

# Loop; break the loop with a keystroke
while(keep_running):
    results = ""
    
    # measure data
    if (full_functional):
        results += format_f( drdaq.get_ext1() )          # temperature [degC]
        results += format_f( fdc2214.read_ch1() )        # capacitance [pF]
        results += format_f( fdc2214.read_ch10() )       # capacitance diffrence [pF]
        results += format_f( ldc1000.read_inductance() ) # inductance [uH]
        results += format_f( ldc1000.read_impedance() )  # impedance [kOhm]
    else:
        results += format_f( tools.get_random() )
        results += format_f( tools.get_random() )
        results += format_f( tools.get_random() )
        results += format_f( tools.get_random() )
        results += format_f( tools.get_random() )
    
    # output data
    print(results[1:])

    # write data to Wolfram Datadrop
    tools.write_datadrop( drdaq.get_ext1(), fdc2214.read_ch1() )
    
    # give CPU some time before looping again
    # drivers need 0.01 sec for one measurement
    for i in range(30):
        print('Time since next measurement: %d sec' % (30-i), end='\r', flush=True)
        time.sleep(1)
