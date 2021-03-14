import random
import time
from pylsl import StreamInfo, StreamOutlet

info = StreamInfo('MyMarkerStream', 'Markers', 1, 0, 'string', 'myuidw43536')

# next make an outlet
outlet = StreamOutlet(info)

print("now sending markers...")
# Test Marker Genearation (send 1 and 2 marker each 1.5s, end after 900s)
timer = 0

while True:
    outlet.push_sample(['1'])
    time.sleep(1.5)
    timer += 1.5

    outlet.push_sample(['2'])
    time.sleep(1.5)
    timer += 1.5

    if timer == 900:
        outlet.push_sample(['end'])
        break


