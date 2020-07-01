import os
import concurrent.futures

from .core import parser

class Facemock(object):

    def __init__(self, *args, **kwargs):
        pass


    def load_case(self, input="./case", max_workers=None):
        """
        An Executor subclass that executes calls asynchronously
        using a pool of at most max_workers processes. If max_workers
        is None or not given, it will default to the number of processors
        on the machine.
        """
        print("Loading case ...")
        cases =[ "{}/{}".format(input, i) for i in os.listdir(input) if i.endswith(".yaml")]
        with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
            for  i  in zip(cases, executor.map(parser.do_parser, cases)):
                print('Parser return: {}'.format(i))


    def exec_case(self, input="./meta", max_workers=None):
        print("Executing case ...")
        cases =[ "{}/{}".format(input, i) for i in os.listdir(input) if i.endswith(".yaml")]
        with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
            for  i  in zip(cases, executor.map(parser.execute, cases)):
                print('Parser return: {}'.format(i))

    def run(self):
        print("Start ....")
