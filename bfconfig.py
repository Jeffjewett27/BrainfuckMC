import argparse
import json
import re

class BfConfig:
    CONFIG_FILE = 'config.json'

    def __init__(self, config_dict):
        self.__dict__.update(config_dict)

    def __str__(self) -> str:
        return f'Config[{str(self.__dict__)}]'

    @staticmethod
    def parseConfig(parseJson=True, parseArgs=True):
        config_dict = {
            "program": None,
            "brainfile": None,
            "input": None,
            "inputfile": None,
            "log": False,
            "max": 1000,
            "wrap": False,
            "animate": False
        }

        if parseJson:
            try:
                with open(BfConfig.CONFIG_FILE, 'r') as json_file:
                    baseConfig = json.load(json_file)
                    config_dict.update(baseConfig['engine'])
                    config_dict.update(baseConfig['program'])
                    config_dict.update(baseConfig['execution'])
            except:
                pass

        if parseArgs:
            parser = argparse.ArgumentParser()

            parser.add_argument("-p", "--program", help="Brainfuck program text")
            parser.add_argument("-b", "--brainfile", help="Brainfuck program file")
            parser.add_argument("-i", "--input", help="Input digit string")
            parser.add_argument("-d", "--inputfile", help="Input file")
            parser.add_argument("-l", "--log", help="debug statements", action='store_true', default=None)
            parser.add_argument("-m", "--max", help="max num instructions")
            parser.add_argument("-w", "--wrap", help="whether can underflow and overflow", action='store_true', default=None)
            parser.add_argument("-a", "--animate", help="do animation", action='store_true', default=None)
            args = parser.parse_args()

            for key, value in vars(args).items():
                if key not in config_dict or value is not None:
                    config_dict[key] = value

        config = BfConfig(config_dict)

        print(config_dict)

        if config.program is None:
            with open(config.brainfile, "r") as f:
                config.program = f.read()

        if config.input is None:
            if config.inputfile is not None:
                with open(args.inputfile, "r") as f:
                    config.input = f.read()

        config.program = re.sub('[^\.,\+\-<>|#\[\]&]', '', config.program or '')
        if config.animate:
            config.program = re.sub('[^\.,\+\-<>|\[\]]', '', config.program or '')
        config.input = re.sub('[^0-9]', '', config.input or '')

        return config