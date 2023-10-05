#!/usr/bin/evn python3

from mpi4py import MPI

if __name__=='__main__':
    comm = MPI.COMM_WORLD
    comm_sz = comm.Get_size()
    my_rank = comm.Get_rank()

    print('Proc %d of %d > Does anynoe have a toothpick?' %(my_rank, comm_sz))

