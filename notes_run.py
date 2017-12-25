import os

import fase_run


FASE_SERVER_URL = 'http://fasenotes-env.us-west-2.elasticbeanstalk.com'


def main(argv):
  fase_run.Run(FASE_SERVER_URL)


if __name__ == '__main__':
  main(os.sys.argv)
