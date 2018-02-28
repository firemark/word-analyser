#!/usr/bin/python2

from re import compile as re_compile
from sys import argv, stdout
from multiprocessing import Process, Queue, Event
from Queue import Empty

reg = re_compile('\W+')
BANNED_WORDS = {
    'www', 'http', 'https', 'socek', 'pl', 'en', 'us', 'running',
    'utm', 'html', 'gclid', 'source', 'campaign', 'medium', 'all', 'bwe',
    'image', 'kclickdid', 'store', 'content', 'demandware', 'site', 'sites',
    'default', 'gts', 'prefv1', 'prefn1', 'email', 'contact', 'search', 'tid',
    'bta', 'eid', 'and', 'or', 'login', 'gov', 'cart', 'sale',
}
 

def parse(lines):
    for line in lines:
        ip, url = line.split()
        # "URL?params" -> URL
        url, _, _ = url[1:-1].partition('?') 

        # http://url/PATH -> PATH
        try:
            url = url.split('/', 3)[3]
        except IndexError:
            continue
        url = url.lower()

        # get words
        words = [
            word.replace('\n', ' ') for word in reg.split(url)
            if len(word) > 2
            and word not in BANNED_WORDS
            and not word[:5].isdigit()
        ]
        if len(words) == 0:
            continue

        stdout.write(ip + ' ' + ' '.join(words) + '\n')
    stdout.flush()


def chunks(iterable, n):
    buff = []
    i = 0
    for data in iterable:
        buff.append(data)
        i += 1
        if i > n:
            yield buff
            buff = []
            i = 0
    if buff:
        yield buff


def process(queue, event):
    while not event.is_set():
        try:
            parse(queue.get(False, 1))
        except Empty:
            pass


if __name__ == '__main__':
    cores = argv[2] if len(argv) > 2 else 4
    queue = Queue(5000)
    event = Event()
    procs = [Process(target=process, args=(queue, event)) for _ in range(cores)]

    for proc in procs:
        proc.start()

    with open(argv[1]) as f:
        for lines in chunks(f, 1024):
            queue.put(lines)

    queue.close()
    queue.join_thread()
    event.set()

    for proc in procs:
        proc.join()

