#!/usr/bin/python

import os
import sys

def main(argv):
    line = 'environment = PRODUCTION=True,VAULT_PASSWORD=%s\n' % os.environ['VAULT_PASSWORD']  

    with open(argv[0], "a") as myfile:
        myfile.write(line)

if __name__ == "__main__":
    main(sys.argv[1:])
