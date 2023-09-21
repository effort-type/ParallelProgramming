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


if __name__ == '__main__':
    a = 0.0
    b = 3.0
    n = 1024
    
    if len(sys.argv) < 4:
        print("Usage: mpirun -n 4 python3 mpi_trap1.py 0 3 1000")
    else:
        a = float(sys.argv[1])
        b = float(sys.argv[2])
        n = int(sys.argv[3])
        
    comm = MPI.COMM_WORLD
    my_rank = comm.Get_rank()
    comm_sz = comm.Get_size()
    
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
