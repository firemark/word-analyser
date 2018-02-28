#!/usr/bin/python2

from re import compile as re_compile
from itertools import groupby
from sys import argv, stdout
from multiprocessing import Process, Queue, Event
from Queue import Empty


def parse(data):
    for group_words in data:
        stdout.write(' '.join(o[1] for o in group_words) + '\n')
    stdout.flush()


def process(queue, event):
    while not event.is_set():
        try:
            parse(queue.get(False, 1))
        except Empty:
            pass


def chunks(iterable, n):
    buff = []
    i = 0
    for key, data in iterable:
        buff.append(list(data))
        i += 1
        if i > n:
            yield buff
            buff = []
            i = 0
    if buff:
        yield buff


def get_data():
    with open(argv[1]) as f:
        for line in f:
            ip, _, words = line.strip().partition(' ')
            yield ip, words


if __name__ == '__main__':
    cores = argv[2] if len(argv) > 2 else 4
    queue = Queue(1000)
    event = Event()
    procs = [Process(target=process, args=(queue, event)) for _ in range(cores)]

    for proc in procs:
        proc.start()

    data = groupby(get_data(), lambda o: o[0])
    for obj in chunks(data, 256):
        queue.put(obj)

    queue.close()
    queue.join_thread()
    event.set()

    for proc in procs:
        proc.join()
