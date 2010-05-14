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

"""Module to load data from sanitized CSV files with results from the Uganda
deployment."""

import csv
import logging

import geo


class Result(object):
  """A survey result.  It holds a geo.Point, along with a list of questions
  and answers.
  """
  def __init__(self, point):
    self.point = point
    self.questions = {}
    self.answers = {}


def load(file, location_col, target_cols):
  """Load Result objects from file.
    file:  filename of csv file to load from
    location_col: index of the column holding location (as "<lat>,<lon>")
    target_cols: indices of the columns to load questions & answers from.
  """
  reader = csv.reader(open(file))
  headers = reader.next()
  data = []
  for line in reader:
    lat, lon = _readLocation(line, location_col)
    result = Result(geo.Point(lat, lon))
    for col in target_cols:
      question = headers[col]
      result.questions[col] = question
      result.answers[col] = line[col]
    data.append(result)
  return data


def _readLocation(line, column):
  location = line[column]
  location = location.split(',')
  if len(location) != 2:
    return None, None
  lat = float(location[0])
  lon = float(location[1])
  return lat, lon
