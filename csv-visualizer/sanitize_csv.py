#!/usr/bin/python2.4
#
# Copyright 2009 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Sanitize the UReport Uganda CSV data so it can be fed to the visualization
code.  This is a quick-and-dirty implementation which just discards data that
doesn't look right.  (The goal was ease of coding, not including as much data as
possible.)

Usage: ./sanitize_csv.py [dirty csv file] > [clean csv file]
"""

import csv
import logging
import sys

# These are the numbers numbers of the columns in the sample dataset I was
# working with.  You might need to adjust for your dataset.
USED_BEFORE_COL = 0
WAS_USEFUL_COL = 1
PRICE_COL = 3
TRUST_COL = 5
TELL_FRIENDS_COL = 7
LOCATION_COL = 9

YES_NO = {'Yes': True, 'No': False}


def readYesNo(line, column):
  """Read the answer from a column that contains either Yes or No."""
  answer = line[column]
  if answer not in YES_NO:
    return None
  return answer


def readPrice(line, column):
  """Read a price (in ush) from column.  Returns None if the format of the price
  isn't recognized.  """
  price = line[column]
  try:
    stripped = price
    strip = [
      ('.', ''),
      (' ', ''),
      ('sah', ''),
      ('ushs', ''),
      ('shs', ''),
      ('sh', ''),
      ('forfree', '0'),
    ]
    for substring, replacement in strip:
      stripped = stripped.replace(substring, replacement)
    if stripped.startswith('freeof'):
      stripped = '0'
    price = int(stripped)
  except ValueError:
    return None
  return price


def readLocation(line, column):
  """ Return the location from the given column, surrounded with quotes.

  Returns None if the location was empty.
  """
  location = line[column]
  if ',' not in location:
    return None
  return '"%s"' % location


def load(file):
  reader = csv.reader(open(file))
  headers = reader.next()
  data = []
  skipped_lines = 0
  for line in reader:
    result = {'location': readLocation(line, LOCATION_COL)}
    for column in (USED_BEFORE_COL, WAS_USEFUL_COL, TRUST_COL,
                   TELL_FRIENDS_COL):
      question = headers[column]
      result[question] = readYesNo(line, column)
    for column in (PRICE_COL,):
      question = headers[column]
      result[question] = readPrice(line, column)

    if None in result.values():
      skipped_lines += 1
      continue
    data.append(result)
  logging.warning('Skipped %s lines of bad data' % skipped_lines)
  return data


def main():
  in_file = sys.argv[1]
  data = load(in_file)
  keys = data[0].keys()
  keys.sort()
  print ','.join(keys)  # Column headings
  for row in data:
    print ','.join(str(row[key]) for key in keys)


if __name__ == '__main__':
  main()
