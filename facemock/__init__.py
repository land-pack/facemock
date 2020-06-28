import os
import concurrent.futures

from .core import parser

class Facemock(object):

    def __init__(self, *args, **kwargs):
        pass

    def load_case(self, input, output, max_workers=None):
        """
        An Executor subclass that executes calls asynchronously
        using a pool of at most max_workers processes. If max_workers
        is None or not given, it will default to the number of processors
        on the machine.
        """
        print("Loading case ...")
        args =[
            ("BAIDU", input, 'A', output),
        ]
        t =[
            "baidu"
        ]
        cases =[ "{}/{}".format(input, i) for i in os.listdir(input) if i.endswith(".yaml")]

        # for i in cases:
        #     print("i -->", i)
        with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
            for  i  in zip(cases, executor.map(parser.do_parser, cases)):
                print('Case:  | output: {}'.format(i))

        # parser.do_parser("BAIDU", input, 'A', output)



    def run(self):
        print("Start ....")
