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

"""Tests for geo.py"""

import unittest

import geo


class GeoTest(unittest.TestCase):

  def testDistanceWithRealworldData(self):
    """ Test the distance function using data I gathered from Google Earth."""
    alcatraz = (37.825685, -122.422586)
    sfo = (37.619057, -122.375483)
    mono_lake = (37.998619, -119.028868)
    nyc = (40.577485, -73.975278)
    gibralter = (35.904513, -5.562047)
    mumbai = (19.010173, 72.910176)

    self.assertAlmostEqual(geo.distance(alcatraz, sfo), 12.5, .1)
    self.assertAlmostEqual(geo.distance(alcatraz, mono_lake), 162, 2)
    self.assertAlmostEqual(geo.distance(alcatraz, nyc), 2233, 25)
    self.assertAlmostEqual(geo.distance(alcatraz, gibralter), 5163, 450)
    self.assertAlmostEqual(geo.distance(nyc, gibralter), 3148, 90)
    self.assertAlmostEqual(geo.distance(mumbai, gibralter), 4193, 65)

    # Here's one that is wildly inaccurate, just as an example.  (The algorithm
    # uses an approximation that's only valid for shorter distances.)
    self.assertAlmostEqual(geo.distance(alcatraz, mumbai), 7291, 3000)

  def testAggregatePointHasLength(self):
    points = [geo.Point(x, x) for x in range(4)]
    aggregate = geo.AggregatePoint(9, 9, points)
    self.assertEqual(len(points), len(aggregate))

  def testAggregatePointAllowsArrayStyleAccess(self):
    points = [geo.Point(x, x) for x in range(4)]
    aggregate = geo.AggregatePoint(9, 9, points)
    self.assertEqual(points[0], aggregate[0])
    self.assertEqual(points[3], aggregate[3])

  def testGridSimple(self):
    points = self.makePoints((0, 0), (0, 1),
                             (1, 0), (1, 1))
    grid = geo.grid(geo.Rect(2, 2, 0, 0), 2, 2, points)
    self.assertEqual([[points[0]], [points[1]], [points[2]], [points[3]]],
                      grid)

  def testGridComplex(self):
    top_left      = self.makePoints((0, 0), (0, 1),
                                    (1, 0), (1, 1),
                                    (2, 0), (2, 1))
    top_middle    = self.makePoints((0, 2), (0, 3),
                                    (1, 2), (1, 3),
                                    (2, 2), (2, 3))
    top_right     = self.makePoints((0, 4), (0, 5),
                                    (1, 4), (1, 5),
                                    (2, 4), (2, 5))
    bottom_left   = self.makePoints((3, 0), (3, 1),
                                    (4, 0), (4, 1),
                                    (5, 0), (5, 1))
    bottom_middle = self.makePoints((3, 2), (3, 3),
                                    (4, 2), (4, 3),
                                    (5, 2), (5, 3))
    bottom_right  = self.makePoints((3, 4), (3, 5),
                                    (4, 4), (4, 5),
                                    (5, 4), (5, 5))

    points = (top_left + top_middle + top_right +
              bottom_left + bottom_middle + bottom_right)
    grid = geo.grid(geo.Rect(6, 6, 0, 0), 2, 3, points)

    self.assertEqual([top_left, top_middle, top_right,
                      bottom_left, bottom_middle, bottom_right], grid)

  def testGridDiscardsPointsOutsideArea(self):
    points = self.makePoints((0, 0),  # The only point inside the area.
                             (-10, 0), (10, 0), (0, -10), (0, 10))
    grid = geo.grid(geo.Rect(1, 1, -1, -1), 1, 1, points)
    self.assertEqual([[points[0]]], grid)

  def testAggregateGridSimple(self):
    points = self.makePoints((0, 0), (0, 1),
                             (1, 0), (1, 1))
    grid = geo.aggregate_grid(geo.Rect(2, 2, 0, 0), 2, 2, points)
    self.assertEqual(4, len(grid))
    self.assertEqual(1, len(grid[0]))
    self.assertEqual(1, len(grid[1]))
    self.assertEqual(1, len(grid[2]))
    self.assertEqual(1, len(grid[3]))
    self.assertEqual(points[0], grid[0][0])
    self.assertEqual(points[1], grid[1][0])
    self.assertEqual(points[2], grid[2][0])
    self.assertEqual(points[3], grid[3][0])

  def assertAlmostEqual(self, actual, expected, epsilon):
    """Assert that expected is within +/- epsilon of actual."""
    delta = abs(actual - expected)
    if delta > epsilon:
      raise AssertionError('%s != %s +/- %s (difference: %s)' % (actual,
        expected, epsilon, delta))

  def makePoints(self, *coordinates):
    """Return a list of geo.Point() objects for the given coordinates"""
    return [geo.Point(lat, lon) for lat, lon in coordinates]


if __name__ == '__main__':
  unittest.main()
