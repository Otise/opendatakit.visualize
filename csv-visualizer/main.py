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

"""Plot ureport data on a heatmap."""

import sys

import boolean_data
import geo
import kml
import numeric_data
import ureport_csv
import overlay


UGANDA_RECT = geo.Rect(
  left = 29.476961,
  right = 35.098989,
  top = 4.267966,
  bottom = -1.539426,
)


def yesno_layers(layer_title, data):
  """Return a list of KML layers which make sense for boolean data stored
  as "yes" or "no" strings."""
  low_res = geo.aggregate_grid(UGANDA_RECT, 20, 20, data)
  hi_res = geo.aggregate_grid(UGANDA_RECT, 120, 120, data)

  return [
    overlay.placemark_layer(low_res, boolean_data.placemark_from_aggregate,
                            layer_title),
    overlay.polygon_layer(low_res, boolean_data.polygon_from_aggregate,
                            layer_title + ' low-res'),
    overlay.polygon_layer(hi_res, boolean_data.polygon_from_aggregate,
                            layer_title + ' hi-res'),
    overlay.heatmap_layer(UGANDA_RECT, 20, 20, low_res, layer_title, 'low-res'),
    overlay.heatmap_layer(UGANDA_RECT, 120, 120, hi_res, layer_title, 'hi-res'),
  ]


def numeric_layer(layer_title, data):
  """Return a KML layer summarizing numeric survey data."""
  data = geo.aggregate_grid(UGANDA_RECT, 20, 20, data)
  return overlay.placemark_layer(data, numeric_data.placemark_from_aggregate,
                                 layer_title)


def make_kml(in_file, out_file, location_column, columns, column_types):
  """Create and save a KML file from the given CSV data and desired columns."""
  data = ureport_csv.load(in_file, location_col=location_column,
                          target_cols=columns)
  layers = []
  for column, type in zip(columns, column_types):
    question = data[0].questions[column]
    print question

    column_data = []
    for d in data:
      point = geo.Point(d.point.lat, d.point.lon)
      point.value = d.answers[column]
      if type == 'yesno':
        point = boolean_data.yes_no_to_boolean(point)
      elif type == 'numeric':
        point.value = float(point.value)
      column_data.append(point)

    if type == 'yesno':
      layers.extend(yesno_layers(question, column_data))
    elif type == 'numeric':
      layers.append(numeric_layer(question, column_data))
    else:
      raise RuntimeError('Unknown column type [%s]' % type)


  files = [layer.file for layer in layers if hasattr(layer, 'file')]
  kml.write_kmz(out_file, kml.kml('UReport', layers), files)


def n_at_a_time(list, n):
  """ Split list into tuples of lenth n.  For example:
    >>> n_at_a_time((0, 1, 2, 3, 4, 5), 2)
    ((0, 1), (2, 3), (4, 5))
  """
  if len(list) % 2 != 0:
    raise RuntimeError("Don't use an odd-length list.")
  out = []
  i = 0
  while i < len(list) - 1:
    out.append((list[i], list[i+1]))
    i += 2
  return out


def usage():
  print """Usage: %s <in file> <out file> <location column> [column/type pairs...]
  in file: Filename of a file containing sanitized CSV data.
  out file: Filename to write the resulting KMZ data to.
  location column: index of the column containing lat,lon information
  column/type pairs: alternating list of column index and data types for the
    columns you want included in the KMZ file.

Valid types for columns:
  numeric: float or integer data
  yesno: column contains either "yes" or "no"

Column indexes start at 0.

Example:
  %s data.csv output.kmz 5 0 yesno 2 numeric

  """ % (sys.argv[0], sys.argv[0])


def main():
  try:
    in_file, out_file, location_column = sys.argv[1:4]
    column_type_pairs = sys.argv[4:]
  except ValueError:
    usage()
    sys.exit(1)

  location_column = int(location_column)
  print column_type_pairs
  columns, column_types = zip(*n_at_a_time(column_type_pairs, 2))
  columns = [int(c) for c in columns]

  make_kml(in_file, out_file, location_column, columns, column_types)


if __name__ == '__main__':
  main()
