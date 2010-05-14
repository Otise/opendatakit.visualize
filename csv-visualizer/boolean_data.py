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

"""Helpers for working with boolean data."""

import math

import geo
import kml


def make_boolean_pixel(points):
  """ Return a PIL pixel tuple for the given points."""
  point = _BooleanSummary(points)
  red = int((1 - point.true_false_ratio) * 255)
  green = 0
  blue = int(point.true_false_ratio * 255)
  alpha = int(point.count/2.0 + 128)
  return (red, green, blue, alpha)


def yes_no_to_boolean(yes_no_point):
  """ Make a geo.Point containing boolean data from one containing "yes" or "no"
  strings."""
  bool_point = geo.Point(yes_no_point.lat, yes_no_point.lon)
  bool_point.value = _convert_yes_no(yes_no_point.value)
  return bool_point


def placemark_from_aggregate(layer_title, point, max_num_responses):
  """ Make a point-based kml.Placemark from an AggregatePoint containing
  boolean data."""
  summary = _BooleanSummary(point)
  if summary.count == 0:
    return kml.Placemark('No Data', 'No Data', kml.Point(point.lat, point.lon))
  desc = '%s\n%s responses.  %s affirmative' % (layer_title, summary.count,
                                                summary.percent_true)
  p = kml.Placemark('%s/%s' % (summary.true, summary.count), desc,
                    kml.Point(point.lat, point.lon))
  scale = (summary.count/ float(max_num_responses)) * 1.5 + 0.8
  if summary.true_false_ratio > 0.5:
    style = kml.Style(kml.BLUE_PIN, scale)
  else:
    style = kml.Style(kml.RED_PIN, scale)
  p.style = style
  return p


def polygon_from_aggregate(layer_title, point, max_num_responses):
  """ Make a polygon-based kml.Placemark from an AggregatePoint containing
  boolean data."""
  lat = point.lat
  lon = point.lon
  summary = _BooleanSummary(point)
  if summary.count == 0:
    return kml.Placemark('No Data', 'No Data', kml.Polygon([(lat, lon)]))
  desc = '%s\n%s responses.  %s affirmative' % (layer_title, summary.count,
                                                summary.percent_true)
  percent_of_total_responses = summary.count/ float(max_num_responses)
  min_circle_size = 0.025
  circle_scale = .15
  num_segments = 32
  radius = percent_of_total_responses * circle_scale + min_circle_size

  points = []
  for n in range(num_segments):
    rad = 2 * math.pi * n / num_segments
    points.append((lat + (math.cos(rad) * radius),
                   lon + (math.sin(rad) * radius)))
  points.append(points[0])  # Make last == first
  polygon = kml.Polygon(points)
  p = kml.Placemark('%s/%s' % (summary.true, summary.count), desc, polygon)
  red, green, blue, alpha = list(make_boolean_pixel(point))
  alpha = 255
  colors = (alpha, blue, green, red)  # KML does colors backwards.
  p.style = kml.PolyStyle(''.join('%02x' % x for x in colors))
  return p


def _convert_yes_no(input):
  """ Convert the string "yes" to True and "no" to False."""
  input = input.lower()
  if input == 'yes':
    return True
  elif input == 'no':
    return False
  else:
    raise AssertionError('Invalid input %s' % input)


class _BooleanSummary(object):
  """ Wrapper which summarizes the boolean points it contains."""
  def __init__(self, points):
    values = [p.value for p in points]
    self.count = len(values)
    self.true = 0
    self.false = 0
    for x in values:
      if x:
        self.true += 1
      else:
        self.false += 1
    if self.count != 0:
      self.true_false_ratio = self.true / float(self.count)
    else:
      self.true_false_ratio = 0
    self.percent_true = '%d%%' % (self.true_false_ratio * 100)
