#!/usr/bin/env python3

import numpy as np
import sys
import logging
import random
import threading
import time


def Gen_matrix(A):
    m, n = A.shape
    random.seed()

    for i in range(m):
        for j in range(n):
            A[i][j] = random.randint(0, 9)


def Gen_vector(x):
    n = x.size
    
    for i in range(n):
        x[i] = random.randint(0, 9)


def Pth_mat_vect(my_rank):
    global A, x, y, m, n, thread_count
    global logger
    global elaspsed_time

    local_m = m / thread_count
    my_first_row = int(my_rank * local_m)
    my_last_row = int(my_first_row + local_m)

    start = time.time()
    for i in range(my_first_row, my_last_row):
        for j in range(n):
            y[i] += A[i][j] * x[j]
    
    finish = time.time()
    elaspsed_time[my_rank] = finish - start
    logger.info('Thread %d > Elapsed time = %e seconds' % (my_rank, elaspsed_time[my_rank]))


if __name__ == '__main__':
    logging.basicConfig(level = logging.INFO)
    logger = logging.getLogger('pth_mat_vect')
    thread_count = 0
    m = n = 0

    if len(sys.argv) < 4:
        logger.error('Wrong number of arguments\n\nUsage : $ python3 pth_mat_vec_rand_split.py <thread_count> <m> <n>\n')
        sys.exit(-1)

    thread_count = int(sys.argv[1])
    m = int(sys.argv[2])
    n = int(sys.argv[3])
    logger.info('thread_count = %d, m = %d, n = %d' % (thread_count, m, n))
    
    assert(m % thread_count == 0)

    # matrix, vector create
    A = np.empty(m*n, dtype = 'float').reshape(m, n)
    x = np.empty(n, dtype = 'float')
    y = np.zeros(m, dtype = 'float')

    Gen_matrix(A)
    logger.debug('A = \n%s' % A)

    Gen_vector(x)
    logger.debug('x = \n%s', x)

    # thread start
    thread_handles = []
    elaspsed_time = np.empty(thread_count)

    for thread in range(thread_count):
        th = threading.Thread(target = Pth_mat_vect, args = (thread, ))
        thread_handles.append(th)
        th.start()
    logger.debug('y = %s' % y)

    for thread in range(thread_count):
        thread_handles[thread].join()

    # total time
    total_time = 0.0
    for i in range(thread_count):
        total_time += elaspsed_time[i]
    
    logger.info('total elapsed time = %.6f' % total_time)