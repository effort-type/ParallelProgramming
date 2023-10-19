import threading


class MyClass(threading.Thread):
    def __init__(self, rank):
        super().__init__()
        self.rank = rank
        
        
    def run(self):
        print("Hello from %s" % threading.get_ident())
        
        
if __name__ == "__main__":
    th_list = []
    for i in range(4):
        th = MyClass(i)
        th_list.append(th)    
        th.start()
    

    for th in th_list:
        th.join()
        
    print("end of thread_ex01")
