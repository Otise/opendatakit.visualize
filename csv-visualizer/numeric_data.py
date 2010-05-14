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

"""Helpers for dealing with numeric data."""

import geo
import kml


def placemark_from_aggregate(layer_title, point, max_num_responses):
  """ Make a placemark from an AggregatePoint containing numeric data."""
  count = len(point)
  if count == 0:
    return kml.Placemark('No Data', 'No Data', kml.Point(point.lat, point.lon))
  values = [p.value for p in point]
  avg = int(sum(values)/float(count))
  med = int(sorted(values)[count/2])
  desc = '%s responses\nAverage: %s\nMedian: %s' % (count, avg, med)
  p = kml.Placemark('%s/%s' % (avg, med), desc, kml.Point(point.lat, point.lon))
  scale = (count/ float(max_num_responses)) * 1.5 + 0.8
  p.style = kml.Style(kml.WHITE_PIN, scale)
  return p
