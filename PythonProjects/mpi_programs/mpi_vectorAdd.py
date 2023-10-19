from mpi4py import MPI
import numpy as np
import time


def Parallel_vector_sum(local_x, local_y):
    local_z = np.empty(len(local_x), dtype = 'int')
    
    for i in range(len(local_x))


if __name__ == '__main__':
    comm = MPI.COMM_WORLD
    comm_sz = comm.Get_size()
    my_rank = comm.Get_rank()
    
    n, local_n = Read_n(comm, comm_sz, my_rank)
    # local_x, local_y, local_z = Allocate_vectors(local_n)
    
    local_x = Read_vector(n, 'x', comm_sz, my_rank)
    Print_vector(local_x, n, 'x is', my_rank, comm)
    
    local_y = Read_vector(n, 'y', comm_sz, my_rank)
    Print_vector(local_y, n, 'y is', my_rank, comm)
    
    local_z = Parallel_vector_sum(local_x, local_y)
    Print_vector(local_z, n, 'z is', my_rank, comm)
    
    time.sleep(1)
   
    
