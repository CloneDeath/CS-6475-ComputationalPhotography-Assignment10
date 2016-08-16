import time
import os
import sys
import argparse
import json
from bonnie.submission import Submission

LATE_POLICY = \
"""Late Policy: I have read the late policy for CS6475. I understand that only my 
last commit before the late submission deadline will be accepted and that late 
penalties apply if any part of the assignment is submitted late."""

HONOR_PLEDGE = "Honor Pledge: I have neither given nor received aid on this assignment."

def require_pledges():
  print(LATE_POLICY)
  ans = raw_input("Please type 'yes' to agree and continue>")
  if ans != "yes":
    raise RuntimeError("Late policy not accepted.")

  print(HONOR_PLEDGE)
  ans = raw_input("Please type 'yes' to agree and continue>")
  if ans != "yes":
    raise RuntimeError("Honor pledge not accepted")


def main():
  parser = argparse.ArgumentParser(description='Submits code to the Udacity site.')
  parser.add_argument('--provider', choices = ['gt', 'udacity'], default = 'gt')
  parser.add_argument('--environment', choices = ['local', 'development', 'staging', 'production'], default = 'production')
  parser.add_argument('--writeup', action='store_true', default=False)

  args = parser.parse_args()

  require_pledges()

  quiz = 'assignment10'
  filenames = ["assignment10.pdf"]

  if not os.path.isfile(filenames[0]):
    print "%s is not present in the directory." %  filenames[0]
    return
  elif (os.stat(filenames[0]).st_size >> 20) >= 6:
    print "Please keep your files under 6MB."
    return

  submission = Submission('cs6475', quiz, 
                          filenames = filenames, 
                          environment = args.environment, 
                          provider = args.provider)

  while not submission.poll():
    time.sleep(3.0)

  if submission.result():
    result = submission.result()
    print json.dumps(result, indent=4)
  elif submission.error_report():
    error_report = submission.error_report()
    print json.dumps(error_report, indent=4)
  else:
    print "Unknown error."

if __name__ == '__main__':
  main()
