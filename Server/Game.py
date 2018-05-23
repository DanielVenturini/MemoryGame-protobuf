# -*- coding:ISO-8859-1 -*-

from threading import Thread

class Game(Thread):

    def __init__(self, conn1, conn2):
        Thread.__init__(self)

        self.conn1 = conn1
        self.conn2 = conn2