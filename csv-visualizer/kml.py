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

"""Simple KML library."""

import sys
import zipfile

# Some pre-defined icons which you can use in Style objects.
WHITE_PIN = 'http://maps.google.com/mapfiles/kml/pushpin/wht-pushpin.png'
BLUE_PIN = 'http://maps.google.com/mapfiles/kml/pushpin/blue-pushpin.png'
RED_PIN = 'http://maps.google.com/mapfiles/kml/pushpin/red-pushpin.png'


def _unique_identifier(x):
  """Return a unique string for object x (based on the object id)."""
  return hex(id(x))[2:].replace('-', 'x')

class Style(object):
  """Represents a <Style> element for a Point."""

  def __init__(self, icon_url, scale=1.0):
    self.icon_url = icon_url
    self.scale = scale

  def id(self):
    return _unique_identifier(self)

  def __str__(self):
    return """
    <Style id="%s">
      <IconStyle>
        <scale>%s</scale>
        <Icon><href>%s</href></Icon>
      </IconStyle>
    </Style>
    """ % (self.id(), self.scale, self.icon_url)



class PolyStyle(object):
  """Represents a <Style> element for a Polygon."""

  def __init__(self, poly_color, line_color=None, line_width=1.0):
    self.poly_color = poly_color
    self.line_color = line_color
    if self.line_color is None:
      self.line_color = poly_color
    self.line_width = line_width

  def id(self):
    return _unique_identifier(self)

  def __str__(self):
    return """
    <Style id="%s">
      <LineStyle>
        <color>%s</color>
        <width>%s</width>
      </LineStyle>
      <PolyStyle>
        <color>%s</color>
      </PolyStyle>
    </Style>
    """ % (self.id(), self.line_color, self.line_width, self.poly_color)


class Point(object):
  """Represents a <Point> element."""

  def __init__(self, lat, lon):
    self.lat = lat
    self.lon = lon

  def __str__(self):
    return """<Point><coordinates>%s,%s,0</coordinates></Point>""" % \
      (self.lon, self.lat)


class Placemark(object):
  """Represents a <Placemark> element."""

  def __init__(self, name, description, point, style=None):
    self.name = name
    self.description = description
    self.point = point
    self.style = style

  def __str__(self):
    style = ''
    if self.style is not None:
      style = '<styleUrl>#%s</styleUrl>' % self.style.id()
    return """
    <Placemark>
      <name>%s</name>
      <description>%s</description>
      %s
      %s
    </Placemark>""" % (self.name, self.description, self.point, style)


class GroundOverlay(object):
  """Represents a <GroundOverlay> element."""

  def __init__(self, name, description, file, scale, rect):
    self.name = name
    self.description = description
    self.file = file
    self.scale = scale
    self.rect = rect

  def __str__(self):
    return """
      <GroundOverlay>
        <name>%s</name>
        <description>%s</description>
        <Icon>
          <href>%s</href>
          <viewBoundScale>%s</viewBoundScale>
        </Icon>
        <LatLonBox>
          <north>%s</north>
          <south>%s</south>
          <east>%s</east>
          <west>%s</west>
        </LatLonBox>
      </GroundOverlay>""" % (self.name, self.description, self.file,
                             self.scale, self.rect.top, self.rect.bottom,
                             self.rect.left, self.rect.right)


class Polygon(object):
  """Represents a simple version of the <Polygon> element.
  (Features like altitudeMode and inner boundries aren't implemetned.)"""

  def __init__(self, coordinates):
    """Coordinates is a list of (lat, lon) tuples.  The first coordinate must
    equal the last coordinate."""
    self.coordinates = coordinates

  def __str__(self):
    return """
      <Polygon>
        <extrude>0</extrude>
        <tessellate>1</tessellate>
        <altitudeMode>clampToGround</altitudeMode>
        <outerBoundaryIs>
          <LinearRing><coordinates>
            %s
          </coordinates></LinearRing>
        </outerBoundaryIs>
      </Polygon>
    """ % ('\n'.join('%s,%s,0' % (lon, lat) for lat, lon in self.coordinates))


class Folder(object):
  """Represents a <Folder> element."""

  def __init__(self, name, styles, elements, visible = True):
    self.name = name
    self.styles = styles
    self.elements = elements
    self.visible = visible

  def __str__(self):
    out = []
    out.append('<Folder>')
    out.append('<name>%s</name>' % self.name)
    visibility = 0
    if self.visible:
      visibility = 1
    out.append('<visibility>%s</visibility>' % visibility)
    for s in self.styles:
      out.append(str(s))
    for e in self.elements:
      out.append(str(e))
    out.append('</Folder>')
    return '\n'.join(out)


def kml(title, objects):
  """ Return a string containing KML data for the given objects."""

  folder = Folder(title, [], objects)
  out = []
  out.append('<?xml version="1.0" encoding="UTF-8"?>')
  out.append('<kml xmlns="http://www.opengis.net/kml/2.2">')
  out.append(str(folder))
  out.append('</kml>')
  return '\n'.join(out)


def write_kmz(filename, kml_data, image_filenames):
  """Creates a kmz file containing the given kml_data (a string) and the given
  image files."""

  file = zipfile.ZipFile(filename, 'w')
  file.writestr('doc.kml', kml_data)
  for i in image_filenames:
    file.write(i)
  file.close()
