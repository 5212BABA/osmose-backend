#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2012                                      ##
##                                                                       ##
## This program is free software: you can redistribute it and/or modify  ##
## it under the terms of the GNU General Public License as published by  ##
## the Free Software Foundation, either version 3 of the License, or     ##
## (at your option) any later version.                                   ##
##                                                                       ##
## This program is distributed in the hope that it will be useful,       ##
## but WITHOUT ANY WARRANTY; without even the implied warranty of        ##
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         ##
## GNU General Public License for more details.                          ##
##                                                                       ##
## You should have received a copy of the GNU General Public License     ##
## along with this program.  If not, see <http://www.gnu.org/licenses/>. ##
##                                                                       ##
###########################################################################

from modules.OsmoseTranslation import T_
from .Analyser_Osmosis import Analyser_Osmosis
from modules.Stablehash import stablehash64

sql10 = """
CREATE TEMP TABLE commune AS
SELECT
    relations.id AS id,
    relations.tags->'ref:INSEE' AS ref,
    ST_Buffer(ST_Polygonize(ways.linestring), 0) AS polygon
FROM
    relations
    JOIN relation_members ON
        relation_members.relation_id = relations.id AND
        relation_members.member_type = 'W'
    JOIN ways ON
        ways.id = relation_members.member_id AND
        ST_NPoints(ways.linestring) > 1
WHERE
    relations.tags?'type' AND
    relations.tags->'type' = 'boundary' AND
    relations.tags?'boundary' AND
    relations.tags->'boundary' = 'administrative' AND
    relations.tags?'admin_level' AND
    relations.tags->'admin_level' = '{0}'
GROUP BY
    relations.id,
    relations.tags->'ref:INSEE'
"""

sql11 = """
CREATE TEMP TABLE commune_dump AS
SELECT
    id,
    ref,
    (ST_Dump(polygon)).geom AS polygon
FROM
    commune
"""

sql12 = """
CREATE INDEX commune_dump_polygon_idx ON commune_dump USING gist(polygon)
"""

sql13 = """
CREATE INDEX commune_dump_ref_idx ON commune_dump(ref)
"""

sql20 = """
CREATE TEMP TABLE geodesic_hull AS
SELECT
    relations.id,
    ST_ConvexHull(ST_Collect(nodes.geom)) AS hull,
    substring(relations.tags->'ref', 1, 5) AS ref
FROM
    relations
    JOIN relation_members ON
        relation_members.relation_id = relations.id AND
        relation_members.member_type = 'N'
    JOIN nodes ON
        nodes.id = relation_members.member_id
WHERE
    relations.tags?'type' AND
    relations.tags->'type' = 'site' AND
    relations.tags?'site' AND
    relations.tags->'site' = 'geodesic' AND
    relations.tags?'ref' AND
    length(relations.tags->'ref') >= 5
GROUP BY
    relations.id,
    substring(relations.tags->'ref', 1, 5)
"""

sql21 = """
CREATE INDEX geodesic_hull_ref ON geodesic_hull(ref);
"""

sql22 = """
SELECT
    geodesic_hull.id,
    commune.id,
    ST_AsText(ST_Centroid(geodesic_hull.hull))
FROM
    geodesic_hull
    JOIN commune_dump AS commune ON
        geodesic_hull.ref = commune.ref
WHERE
    ST_IsValid(geodesic_hull.hull) AND
    ST_IsValid(commune.polygon)
GROUP BY
    commune.id,
    geodesic_hull.hull,
    geodesic_hull.id
HAVING
    NOT BOOL_OR(ST_Intersects(geodesic_hull.hull, commune.polygon))
"""

sql40 = """
SELECT
    c1.id,
    c2.id,
    ST_AsText(ST_Centroid(ST_Intersection(c1.polygon, c2.polygon)))
FROM
    commune_dump AS c1
    JOIN commune_dump AS c2 ON
        c1.id < c2.id AND
        c1.polygon && c2.polygon AND
        ST_Overlaps(c1.polygon, c2.polygon)
WHERE
    ST_IsValid(c1.polygon) AND
    ST_IsValid(c2.polygon)
"""

sql50 = """
CREATE TEMP TABLE boundary AS
SELECT
    id,
    linestring
FROM
    {0}ways AS ways
WHERE
    tags != ''::hstore AND
    tags?'boundary' AND
    tags->'boundary' = 'administrative' AND
    nodes[1] != nodes[array_length(nodes, 1)]
"""

sql51 = """
SELECT
    ways.id,
    ST_AsText(way_locate(ways.linestring))
FROM
    boundary AS ways
    LEFT JOIN relation_members ON
        relation_members.member_type = 'W' AND
        relation_members.member_id = ways.id
WHERE
    relation_members.member_id IS NULL
"""

sql52 = """
SELECT
    ways.id,
    ST_AsText(way_locate(ways.linestring))
FROM
    boundary AS ways
    JOIN relation_members ON
        relation_members.member_type = 'W' AND
        relation_members.member_id = ways.id
    JOIN relations ON
        relation_members.relation_id = relations.id
GROUP BY
    ways.id,
    ways.linestring
HAVING
    NOT BOOL_OR(relations.tags?'boundary')
"""

class Analyser_Osmosis_Boundary_Administrative(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.FR = config.options and ("country" in config.options and config.options["country"].startswith("FR") or "test" in config.options)
        if self.FR:
            self.classs[100] = self.def_class(item = 6070, level = 3, tags = ['boundary', 'geom', 'fix:chair'],
                title = T_('Survey point out of boundary'),
                trap = T_(
'''The geodesic markers should not be moved. These are reference points.
Some geodesic markers are really out of boundary.'''))
        self.classs[2] = self.def_class(item = 6060, level = 1, tags = ['boundary', 'geom', 'fix:chair'],
            title = T_('Boundary intersection'),
            detail = T_(
'''An area is marked as belonging to several city at once.'''),
            fix = T_(
'''Check how this area should be owned.'''))
        self.classs_change[3] = self.def_class(item = 6060, level = 2, tags = ['boundary', 'geom', 'fix:chair'],
            title = T_('Lone boundary fragment'),
            detail = T_(
'''Unconnected boundary fragment, a way with a boundary tag not part of a
boundary relation.'''),
            fix = T_(
'''Delete the way, remove boundary tag or add to a relation.'''))

        self.callback20 = lambda res: {"class":100, "data":[self.relation_full, self.relation_full, self.positionAsText]}
        self.callback40 = lambda res: {"class":2, "subclass": stablehash64(res[2]), "data":[self.relation_full, self.relation_full, self.positionAsText]}
        self.callback50 = lambda res: {"class":3, "data":[self.way_full, self.positionAsText]}

    def analyser_osmosis_common(self):
        admin_level = self.config.options and self.config.options.get("boundary_detail_level", 8) or 8
        self.run(sql10.format(admin_level))
        self.run(sql11)
        self.run(sql12)
        self.run(sql13)
        if self.FR:
            self.run(sql20)
            self.run(sql21)
            self.run(sql22, self.callback20)
        self.run(sql40, self.callback40)

    def analyser_osmosis_full(self):
        self.run(sql50.format(""))
        self.run(sql51, self.callback50)
        self.run(sql52, self.callback50)

    def analyser_osmosis_diff(self):
        self.run(sql50.format("touched_"))
        self.run(sql51, self.callback50)
        self.run(sql52, self.callback50)

###########################################################################

from .Analyser_Osmosis import TestAnalyserOsmosis

class Test(TestAnalyserOsmosis):
    @classmethod
    def setup_class(cls):
        from modules import config
        TestAnalyserOsmosis.setup_class()
        # TODO: generate a .osm file that triggers errors
        cls.analyser_conf = cls.load_osm("tests/saint_barthelemy.osm.bz2",
                                         config.dir_tmp + "/tests/osmosis_boundary_administrative.test.xml")

    def test(self):
        with Analyser_Osmosis_Boundary_Administrative(self.analyser_conf, self.logger) as a:
            a.analyser()

        self.root_err = self.load_errors()
        self.check_num_err(0)
