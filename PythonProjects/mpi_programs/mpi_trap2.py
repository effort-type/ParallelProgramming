#!/usr/bin/env python3

from mpi4py import MPI
import sys


def f(x):
    return x * x


def Trap(left_endpt, right_endpt, trap_count, base_len):
    estimate = (f(left_endpt) + f(right_endpt)) / 2.0
    
    for i in range(1, trap_count):
        x = left_endpt + i * base_len
        estimate += f(x)
    
    estimate *= base_len
    
    return estimate


def Get_input(comm, my_rank, comm_sz):
    '''
    @return a the start point of an interval
    @return b the end point of an interval
    @return c the number of subintervals
    '''
    
    a = 0.0
    b = 0.0
    n = 0
    
    if my_rank == 0:
        str_a, str_b, str_n = input('Enter a, b, n: ').split()
        a = float(str_a)
        b = float(str_b) 
        n = int(str_n)
        
        for i in range(1, comm_sz):
            comm.send(a, dest = i)
            comm.send(b, dest = i)
            comm.send(n, dest = i)
    else:
        a = comm.recv()
        b = comm.recv()
        n = comm.recv()
    
    return a, b, n
    

if __name__ == '__main__':
        
    comm = MPI.COMM_WORLD
    my_rank = comm.Get_rank()
    comm_sz = comm.Get_size()
    
    a, b, n = Get_input(comm, my_rank, comm_sz)
    
    h = (b - a) / n
    local_n = int(n / comm_sz)
    
    local_a = a + my_rank * local_n * h
    local_b = local_a + local_n * h
    local_int = Trap(local_a, local_b, local_n, h)

    if my_rank != 0:
        comm.send(local_int, dest=0)
    else:
        total_int = local_int
    
        for i in range(1, comm_sz):
            total_int += comm.recv(source = MPI.ANY_SOURCE)
        
    if my_rank == 0:
        print("With n = %d trapezoids, out estimate" % n)
        print("of the integral from %f to %f = %.15e" % (a, b, total_int))
