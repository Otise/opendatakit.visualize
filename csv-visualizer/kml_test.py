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

"""Tests for kml.py"""

import unittest

import geo
import kml


class KmlTest(unittest.TestCase):

  def testPoint(self):
    self.assertEqual(u'<Point><coordinates>8,7,0</coordinates></Point>',
                     str(kml.Point(7, 8)))
    self.assertEqual(u'<Point><coordinates>99,-5,0</coordinates></Point>',
                     str(kml.Point(-5, 99)))

  def testStyle(self):
    style = kml.Style('http://example.com', 78)
    self.assertIn('<href>http://example.com</href>', str(style))
    self.assertIn('<scale>78</scale', str(style))
    self.assertIn('id="%s"' % style.id(), str(style))

  def testStylesHaveUniqueIds(self):
    style1 = kml.Style("url")
    style2 = kml.Style("url")
    self.assertNotEqual(style1.id(), style2.id())

  def testPlacemark(self):
    x = kml.Placemark('Store', 'You can buy stuff here', kml.Point(55, 10))
    self.assertIn('<name>Store</name>', str(x))
    self.assertIn('<description>You can buy stuff here</description>', str(x))
    self.assertIn('<Point><coordinates>10,55,0</coordinates></Point>', str(x))

  def testGroundOverlay(self):
    overlay = kml.GroundOverlay('population', 'from census data',
                                'image.png', 1.0, geo.Rect(4, 3, 2, 1))
    self.assertIn('<name>population</name>', str(overlay))
    self.assertIn('<description>from census data</description>', str(overlay))
    self.assertIn('<href>image.png</href>', str(overlay))
    self.assertIn('<viewBoundScale>1.0</viewBoundScale>', str(overlay))
    self.assertIn('<north>4', str(overlay))
    self.assertIn('<west>3', str(overlay))
    self.assertIn('<south>2', str(overlay))
    self.assertIn('<east>1', str(overlay))

  def testFolder(self):
    style1 = kml.Style(kml.WHITE_PIN)
    style2 = kml.Style(kml.BLUE_PIN)
    point = kml.Point(0, 1)
    placemark = kml.Placemark('house', 'where I live', kml.Point(5, 9))
    folder = kml.Folder('example', [style1, style2], [point, placemark])
    self.assertIn('<name>example</name>', str(folder))
    self.assertIn(str(point), str(folder))
    self.assertIn(str(placemark), str(folder))
    self.assertIn(str(style1), str(folder))
    self.assertIn(str(style2), str(folder))

  def testKml(self):
    house = kml.Placemark('house', '', kml.Point(5, 9))
    work = kml.Placemark('work', '', kml.Point(1, 2))
    kml_data = kml.kml('title', [house, work])

    self.assertEqual("""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Folder>
<name>title</name>
<visibility>1</visibility>
%s
%s
</Folder>
</kml>""" % (str(house), str(work)), kml_data)

  def assertIn(self, a, b):
    """Asserts that "a in b" is true."""
    assert a in b, "%s was not found in %s" % (a, b)


if __name__ == '__main__':
  unittest.main()
