from time import ctime, sleep
import threading

def music(movie):
    print('I listening to music %s %s' %(ctime(),movie))
    sleep(2)

# def homework():
#     print("I doing homework now %s" %ctime())
#     sleep(3)

threads = []
t1 = threading.Thread(target=music,args=('哈哈',))
threads.append(t1)
t2 = threading.Thread(target=music,args=('nnbb',))
threads.append(t2)

if __name__ == '__main__':
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print("over time %s" %ctime())