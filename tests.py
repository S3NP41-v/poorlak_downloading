from threading import Thread

global x
x = 0


def change_x():
    global x
    x = 42


def test():
    global x
    t = Thread(target=change_x, args=())
    print(x)
    t.start()
    t.join(3)
    print(x)


test()
