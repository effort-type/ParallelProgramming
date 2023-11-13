import numpy as np
import sys
import logging
import threading
import math
import time

def Serial_pi(n):
    sum = 0.0
    factor = 1.0

    for i in range(n):
        sum += factor/(2*i + 1)
        factor *= (-1)
    
    return 4.0 * sum


def Thread_sum(my_rank):
    global n, sum
    global flag

    my_n = n / thread_count
    my_first_i = int(my_n * my_rank)
    my_last_i = int(my_first_i + my_n)

    if my_first_i % 2 == 0:
        factor = 1.0
    else:
        factor = -1.0

    for i in range(my_first_i, my_last_i):
        # while flag != my_rank: pass

        sum += factor / (2*i + 1)
        factor *= (-1)
        flag = (flag + 1) % thread_count


if __name__ == '__main__':
    logging.basicConfig(level = logging.INFO)
    logger = logging.getLogger('pth_pi')
    thread_count = 0
    n = 0
    sum = 0.0
    flag = 0

    sys.argv = ["pth_pi_busy1.py", "4", "1_000_000"]
    # sys.argv = ["pth_pi_busy1.py", "4", "1000"]

    if len(sys.argv) < 3:
        logger.error("Wrong number of arguments\n\nUsage : $ python3 pth_pi.py <thread_count> <n>\n")
        sys.exit(-1)

    thread_count = int(sys.argv[1])

    n = int(sys.argv[2])
    logger.info('thread_count = %d, n = %d' % (thread_count, n))
    assert(n % thread_count == 0)

    # thread start
    thread_handles = []
    elapsed_time = np.empty(thread_count)

    start = time.time()
    
    for thread in range(thread_count):
        th = threading.Thread(target = Thread_sum, args = (thread,))
        thread_handles.append(th)
        th.start()

    for thread in range(thread_count):
        thread_handles[thread].join()
    
    finish = time.time()

    elapsed = finish - start

    sum = Serial_pi(n)
    finish = time.time()
    
    print(" Single-threaded estimate of pi = %.15f" % sum)
    print(" Elapsed time = %e seconds" % elapsed)
    print(" Math library estimate of pi = %.15f" % (4.0 * math.atan(1.0)))