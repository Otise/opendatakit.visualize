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

"""Code for generating different kinds of overlay layers in KML."""

import random
import string

from PIL import Image

import boolean_data
import geo
import kml


def placemark_layer(points, placemark_maker, layer_title):
  """ Return a KML Folder containing placemarks for the given points.
    points: a list of point objects
    placemark_maker: Callback used to create a placemark from a point object.
        Args: layer_title, point, max_num_responses.
    layer_title: Title to use for the layer.
    returns: KML Folder containing placemarks.
  """
  elements = []
  styles = []
  max_num_responses = max(x.count for x in points)
  for point in points:
    if point.count > 0:
      p = placemark_maker(layer_title, point, max_num_responses)
      styles.append(p.style)
      elements.append(p)
  return kml.Folder('%s (placemarks)' % layer_title, styles, elements)


def create_image(points, pixel_maker, width, height):
  """ Create and return an image from the given points.
    points: list of point objects
    pixel_maker: callback for making a pixel tuple from a point
    width, height: dimensions of the grid of points (not the final image)
  """
  i = Image.new('RGBA', (width, height))
  pixels = []
  for point in points:
    if len(point) > 0:
      pixels.append(pixel_maker(point))
    else:
      pixels.append((0, 0, 0, 0))
  i.putdata(pixels)
  i = i.resize((width*10, height*10))
  return i


def heatmap_layer(rect, width, height, points, layer_title, res):
  """Return a KML GroundOverlay for the given points.  Currently saves the
  image under a random filename in the current directory.
  """
  # TODO(mivey): Find a better place to save, use mktemp to get a better name.
  filename = ''.join(random.choice(string.lowercase) for x in range(10))
  filename += '.png'
  dx = (rect.right - rect.left)/width
  dy = (rect.top - rect.bottom)/height
  image = create_image(points, boolean_data.make_boolean_pixel, width, height)
  image.save(filename)
  return kml.GroundOverlay('%s (%s overlay)' % (layer_title, res), '',
      filename, 1,
      geo.Rect(rect.top+dy, rect.right, rect.bottom+dy, rect.left))


def polygon_layer(points, polygon_maker, layer_title):
  """ Return a KML Folder containing polygons for the given points.
    points: a list of point objects
    polygon_maker: Callback used to create a polygon from a point object.
        Args: layer_title, point, max_num_responses.
    layer_title: Title to use for the layer.
    returns: KML Folder containing polygons.
  """
  elements = []
  styles = []
  max_num_responses = max(x.count for x in points)
  for point in points:
    if point.count > 0:
      p = polygon_maker(layer_title, point, max_num_responses)
      styles.append(p.style)
      elements.append(p)
  return kml.Folder('%s (polygons)' % layer_title, styles, elements)

  dx = (rect.right - rect.left)/width
  dy = (rect.top - rect.bottom)/height
  image = create_image(points, boolean_data.make_boolean_pixel, width, height)
  image.save(filename)
  return kml.GroundOverlay('%s (%s overlay)' % (layer_title, res), '',
      filename, 1,
      geo.Rect(rect.top+dy, rect.right, rect.bottom+dy, rect.left))
