from threading import Thread


class MyWorker(Thread):
    """
    线程子类
    """
    def __init__(self, func, in_list, out_queue):
        super(MyWorker, self).__init__()
        self.func = func
        self.in_list = in_list
        self.out_queue = out_queue

    def run(self):
        for item in self.in_list:
            result = self.func(item)
            self.out_queue.put(result)
