import os

import fase_run


FASE_SERVER_URL = 'http://fasehelloworld-env.us-west-2.elasticbeanstalk.com'


def main(argv):
  fase_run.Run(FASE_SERVER_URL)


if __name__ == '__main__':
  main(os.sys.argv)
