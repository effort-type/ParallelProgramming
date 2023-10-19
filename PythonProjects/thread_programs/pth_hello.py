#!/usr/bin/env python3

import threading
import sys
import time


def Hello(rank):
    global thread_count
    print('Hello from thread %d of %d' % (rank, thread_count))
    time.sleep(1)
    

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: $ python3 pth_hello.py n(# of threads)')
        sys.exit(-1)
    
    thread_count = int(sys.argv[1])
    thread_handles = []
    
    for thread in range(thread_count):
        th = threading.Thread(target=Hello, args=(thread,))
        thread_handles.append(th)
        th.start()
        
    #print(thread_handles)
    print('Hello from the main thread : active_count = %d' % threading.active_count())
    
    for thread in range(thread_count):
        thread_handles[thread].join()
    
    #print(thread_handles)
    print('end of pth_hello')
    

