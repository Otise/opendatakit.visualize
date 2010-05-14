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

"""Helpful functions/classes for working with geo data."""

import logging
import math


class Point(object):
  """A point on a map with latitude and longitude."""

  def __init__(self, lat, lon):
    self.lat = lat
    self.lon = lon

  def __repr__(self):
    return '%sx%s' % (self.lat, self.lon)


class AggregatePoint(Point):
  """ A collection of other points. This has its own lat/lon because it
  is intended to be used to summarize/bundle other points into a single
  point.
  """

  def __init__(self, lat, lon, points):
    self.lat = lat
    self.lon = lon
    self._points = points
    self.count = len(points)

  def __len__(self):
    return len(self._points)

  def __getitem__(self, index):
    return self._points[index]


class Rect(object):
  """A rectangle, intended to be used to define an area of interest on a map.
  Top & bottom are latitude, while left & right are longitude.
  """

  def __init__(self, top, right, bottom, left):
    self.top = top
    self.right = right
    self.bottom = bottom
    self.left = left


def grid(rect, num_rows, num_cols, points):
  """Group the points into a grid, with a list of points per grid cell.
  Points outside the grid are discarded.

  left, right: longitude of left & right sides
  top, bottom: latitude of top & bottom
  num_rows, num_cols: how many rows/cols to have
  points: list of objects with x.lat and x.lon.
  returns: a grid, represented as a list (arranged so the cells for the first
    row are immediately followed by the cells from the 2nd row, and so on).
    Each cell is represented as a list.  So, grid()[0] is the list of points in
    the top-left cell, grid()[-1] is the list of points in the bottom right
    cell.
  """
  left = rect.left
  right = rect.right
  top = rect.top
  bottom = rect.bottom
  skip_count = 0
  out = [[] for i in range(num_rows * num_cols)]
  width = right-left
  height = top - bottom
  dx = width / num_cols
  dy = height / num_rows
  assert(dx > 0)
  assert(dy > 0)
  for p in points:
    from_left = p.lon - left
    from_bottom = p.lat - bottom
    x = int(from_left / dx)
    y = int(from_bottom / dy)
    if x < 0 or x >= num_cols or y < 0 or y >= num_cols:
      skip_count += 1
      continue
    y = -y  # (0, 0) is top-left
    out[y*num_cols + x].append(p)
  if skip_count:
    logging.warn('skipping %s results outside of area' % skip_count)
  return out


def aggregate_grid(rect, num_rows, num_cols, points):
  """Divide the points into a grid of AggregatePoints.
  Points outside the grid are discarded.

  left, right: longitude of left & right sides
  top, bottom: latitude of top & bottom
  num_rows, num_cols: how many rows/cols to have
  points: list of objects with x.lat and x.lon.
  returns: a list of AggregatePoints, same layout as grid uses.
  """
  dx = (rect.right - rect.left)/num_cols
  dy = (rect.top - rect.bottom)/num_rows
  aggregates = []
  for i, points_in_cell in enumerate(grid(rect, num_cols, num_rows, points)):
    row = i / num_cols
    col = i % num_cols
    lat = rect.top - row * dy + dy/2.0
    lon = rect.left + col * dx + dx/2.0
    aggregates.append(AggregatePoint(lat, lon, points_in_cell))
  return aggregates


def distance(a, b):
  """Calculate distance in nautical miles between (lat, lon) tuples a and b.

  Simple approximation, won't work for large distances.
  """
  nautical_miles_per_degree = 60
  lat_a, lon_a = a
  lat_b, lon_b = b

  y = (lat_b - lat_a) * nautical_miles_per_degree
  # Correct for longitude lines getting closer together near the poles.
  lon_ratio = (math.cos(math.radians(lat_a)) + math.cos(math.radians(lat_b)))/2
  x = lon_ratio * (lon_b - lon_a) * nautical_miles_per_degree
  return math.sqrt(x**2 + y**2)
