#!/usr/bin/env python3
import os
import sys

if os.system('pipenv --version') != 0:
  os.system('pip3 install pipenv')

if os.system('pipenv verify') != 0:
  if os.system('pipenv install {}'.format('--dev' if os.getenv('DEV') else '')) != 0:
    print('Failed installing dependencies', file=sys.stderr)
    exit(1)

if os.system('pipenv run python3 src/main.py') != 0:
  print('Failed launching the program', file=sys.stderr)
  exit(2)