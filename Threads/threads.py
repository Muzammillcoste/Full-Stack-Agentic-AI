from threading import Thread, Lock
import time

def learn(range_:int, name:str)->None:
    counter=0
    print(f"start",name)
    for i in range(range_):
        counter+=1
        print(counter)
    print(f"end",name)

t1= Thread(target=learn, args=(5000,'first',))
t2= Thread(target=learn, args=(10000,'second',))
start=time.time()
t1.start()
t2.start()
t1.join()
t2.join()
end=time.time()
print(f"Total time taken in threads: {end-start} seconds")