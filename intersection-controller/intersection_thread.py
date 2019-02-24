import logging
import threading

from intersection.intersection import Intersection


class IntersectionThread(threading.Thread):
    def __init__(self, intersection: Intersection):
        super(IntersectionThread, self).__init__()

        self.intersection = intersection

    def run(self):
        logging.debug('Starting intersection thread.')

        self.intersection.run()
