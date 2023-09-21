# Usage: mpirun -n python3 mpi_hello.py

"""

"""

from mpi4py import MPI

if __name__ == '__main__':
    comm = MPI.COMM_WORLD
    comm_sz = comm.Get_size()
    my_rank = comm.Get_rank()
    
    if my_rank != 0:
        greeting = "Greetings from process %d of %d!" % (my_rank, comm_sz)
        comm.send(greeting, dest = 0)
    else:
        print("Greetings from process %d of %d!" % (my_rank, comm_sz))
        
        for i in range(1, comm_sz):
            greeting = comm.recv(source = MPI.ANY_SOURCE)
            print(greeting)
