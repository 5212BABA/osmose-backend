#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re # noqa

from plugins.Plugin import with_options # noqa
from plugins.PluginMapCSS import PluginMapCSS


class TagFix_MultipleTag2(PluginMapCSS):



    def init(self, logger):
        super().init(logger)
        tags = capture_tags = {} # noqa
        self.errors[20800] = self.def_class(item = 2080, level = 1, tags = mapcss.list_('tag') + mapcss.list_('tag', 'highway', 'roundabout', 'fix:chair'), title = mapcss.tr('Tag highway missing on junction'), trap = mapcss.tr('Check if it is really a highway and it is not already mapped.'), detail = mapcss.tr('The way has a tag `junction=*` but without `highway=*`.'))
        self.errors[20801] = self.def_class(item = 2080, level = 1, tags = mapcss.list_('tag') + mapcss.list_('tag', 'highway', 'fix:chair'), title = mapcss.tr('Tag highway missing on oneway'), trap = mapcss.tr('Check if it is really a highway and it is not already mapped.'), detail = mapcss.tr('The way has a tag `oneway=*` but without `highway=*`.'))
        self.errors[20802] = self.def_class(item = 2080, level = 2, tags = mapcss.list_('tag') + mapcss.list_('highway'), title = mapcss.tr('Missing tag ref for emergency access point'))
        self.errors[21102] = self.def_class(item = 2110, level = 2, tags = mapcss.list_('tag') + mapcss.list_('tag'), title = mapcss.tr('Missing relation type'), detail = mapcss.tr('The relation is missing a `type` tag to define what it represents.'))
        self.errors[30320] = self.def_class(item = 3032, level = 1, tags = mapcss.list_('tag') + mapcss.list_('fix:chair', 'highway', 'tag'), title = mapcss.tr('Watch multiple tags'))
        self.errors[30322] = self.def_class(item = 3032, level = 3, tags = mapcss.list_('tag'), title = mapcss.tr('{0} together with {1}, usually {1} is located underneath the {2}. Tag the {3} as a separate object.', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{0.value}'), mapcss._tag_uncapture(capture_tags, '{1.key}')))
        self.errors[30327] = self.def_class(item = 3032, level = 2, tags = mapcss.list_('tag') + mapcss.list_('tag', 'fix:chair'), title = mapcss.tr('Waterway with `level`'), trap = mapcss.tr('Remove `level` and check if `layer` is needed instead.'), detail = mapcss.tr('The tag `level` should be used for buildings, shops, amenities, etc.'))
        self.errors[32301] = self.def_class(item = 3230, level = 2, tags = mapcss.list_('tag') + mapcss.list_('fix:chair'), title = mapcss.tr('Probably only for bottles, not any type of glass'), detail = mapcss.tr('Most street-side glass containers only accept soda-lime glass (e.g. bottles and jars), but not glasses for high temperatures or window glass.'), resource = 'https://wiki.openstreetmap.org/wiki/Tag:amenity=recycling')
        self.errors[32302] = self.def_class(item = 3230, level = 2, tags = mapcss.list_('tag') + mapcss.list_('fix:chair'), title = mapcss.tr('Suspicious name for a container'))
        self.errors[40106] = self.def_class(item = 4010, level = 3, tags = mapcss.list_('tag') + mapcss.list_('tag', 'tree', 'fix:chair', 'deprecated'), title = mapcss.tr('Deprecated tag'))
        self.errors[40201] = self.def_class(item = 4020, level = 1, tags = mapcss.list_('tag') + mapcss.list_('fix:chair', 'highway', 'roundabout'), title = mapcss.tr('Roundabout as area'))
        self.errors[71301] = self.def_class(item = 7130, level = 3, tags = mapcss.list_('tag') + mapcss.list_('tag', 'highway', 'maxheight', 'fix:survey'), title = mapcss.tr('Missing maxheight tag'), detail = mapcss.tr('Missing `maxheight=*` or `maxheight:physical=*` for a tunnel or a way under a bridge.'))
        self.errors[303211] = self.def_class(item = 3032, level = 3, tags = mapcss.list_('tag') + mapcss.list_('tag'), title = mapcss.tr('suspicious tag combination'))

        self.re_2ae49e65 = re.compile(r'^(motorway_link|trunk_link|primary|primary_link|secondary|secondary_link)$')


    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[building=roof][amenity][amenity!=shelter][parking!=rooftop]
        if ('amenity' in keys and 'building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'roof')) and (mapcss._tag_capture(capture_tags, 1, tags, 'amenity')) and (mapcss._tag_capture(capture_tags, 2, tags, 'amenity') != mapcss._value_const_capture(capture_tags, 2, 'shelter', 'shelter')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking') != mapcss._value_const_capture(capture_tags, 3, 'rooftop', 'rooftop')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"3032/30322/3"
                # throwWarning:tr("{0} together with {1}, usually {1} is located underneath the {2}. Tag the {3} as a separate object.","{0.tag}","{1.tag}","{0.value}","{1.key}")
                err.append({'class': 30322, 'subclass': 0, 'text': mapcss.tr('{0} together with {1}, usually {1} is located underneath the {2}. Tag the {3} as a separate object.', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{0.value}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # *[highway=emergency_access_point][!ref]
        if ('highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'emergency_access_point')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'ref')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("highway")
                # -osmoseItemClassLevel:"2080/20802:1/2"
                # throwWarning:tr("Missing tag ref for emergency access point")
                err.append({'class': 20802, 'subclass': 1, 'text': mapcss.tr('Missing tag ref for emergency access point')})

        # *[amenity=recycling][recycling_type!=centre][recycling:glass=yes][outside("CZ")]
        if ('amenity' in keys and 'recycling:glass' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'recycling')) and (mapcss._tag_capture(capture_tags, 1, tags, 'recycling_type') != mapcss._value_const_capture(capture_tags, 1, 'centre', 'centre')) and (mapcss._tag_capture(capture_tags, 2, tags, 'recycling:glass') == mapcss._value_capture(capture_tags, 2, 'yes')) and (mapcss.outside(self.father.config.options, 'CZ')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("fix:chair")
                # -osmoseDetail:tr("Most street-side glass containers only accept soda-lime glass (e.g. bottles and jars), but not glasses for high temperatures or window glass.")
                # -osmoseItemClassLevel:"3230/32301/2"
                # -osmoseResource:"https://wiki.openstreetmap.org/wiki/Tag:amenity=recycling"
                # throwWarning:tr("Probably only for bottles, not any type of glass")
                # fixRemove:"recycling:glass"
                # fixAdd:"recycling:glass_bottles=yes"
                # -osmoseAssertNoMatchWithContext:list("node amenity=recycling recycling_type=container recycling:glass=yes","inside=CZ")
                # -osmoseAssertMatchWithContext:list("node amenity=recycling recycling_type=container recycling:glass=yes","inside=FR")
                err.append({'class': 32301, 'subclass': 0, 'text': mapcss.tr('Probably only for bottles, not any type of glass'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['recycling:glass_bottles','yes']]),
                    '-': ([
                    'recycling:glass'])
                }})

        # *[amenity=recycling][recycling_type!=centre][name]
        if ('amenity' in keys and 'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'recycling')) and (mapcss._tag_capture(capture_tags, 1, tags, 'recycling_type') != mapcss._value_const_capture(capture_tags, 1, 'centre', 'centre')) and (mapcss._tag_capture(capture_tags, 2, tags, 'name')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("fix:chair")
                # -osmoseItemClassLevel:"3230/32302/2"
                # throwWarning:tr("Suspicious name for a container")
                # assertMatch:"node amenity=recycling recycling_type=container name=\"My nice awesome container\""
                err.append({'class': 32302, 'subclass': 0, 'text': mapcss.tr('Suspicious name for a container')})

        # node[natural=tree][type][type!=palm]
        if ('natural' in keys and 'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'natural') == mapcss._value_capture(capture_tags, 0, 'tree')) and (mapcss._tag_capture(capture_tags, 1, tags, 'type')) and (mapcss._tag_capture(capture_tags, 2, tags, 'type') != mapcss._value_const_capture(capture_tags, 2, 'palm', 'palm')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Deprecated tag")
                # -osmoseTags:list("tag","tree","fix:chair","deprecated")
                # -osmoseItemClassLevel:"4010/40106/3"
                # throwWarning:tr("The tag `{0}` is deprecated in favour of {1}","{1.key}","`leaf_type`")
                err.append({'class': 40106, 'subclass': 0, 'text': mapcss.tr('The tag `{0}` is deprecated in favour of {1}', mapcss._tag_uncapture(capture_tags, '{1.key}'), '`leaf_type`')})

        # node[tunnel][!highway][!area:highway][!railway][!waterway][!piste:type][type!=tunnel][public_transport!=platform][route!=ferry][man_made!=pipeline][man_made!=goods_conveyor][man_made!=wildlife_crossing][man_made!=tunnel][power!=cable]
        if ('tunnel' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tunnel')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'area:highway')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'railway')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'waterway')) and (not mapcss._tag_capture(capture_tags, 5, tags, 'piste:type')) and (mapcss._tag_capture(capture_tags, 6, tags, 'type') != mapcss._value_const_capture(capture_tags, 6, 'tunnel', 'tunnel')) and (mapcss._tag_capture(capture_tags, 7, tags, 'public_transport') != mapcss._value_const_capture(capture_tags, 7, 'platform', 'platform')) and (mapcss._tag_capture(capture_tags, 8, tags, 'route') != mapcss._value_const_capture(capture_tags, 8, 'ferry', 'ferry')) and (mapcss._tag_capture(capture_tags, 9, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 9, 'pipeline', 'pipeline')) and (mapcss._tag_capture(capture_tags, 10, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 10, 'goods_conveyor', 'goods_conveyor')) and (mapcss._tag_capture(capture_tags, 11, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 11, 'wildlife_crossing', 'wildlife_crossing')) and (mapcss._tag_capture(capture_tags, 12, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 12, 'tunnel', 'tunnel')) and (mapcss._tag_capture(capture_tags, 13, tags, 'power') != mapcss._value_const_capture(capture_tags, 13, 'cable', 'cable')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # -osmoseTags:list("tag")
                # -osmoseItemClassLevel:"3032/303211/3"
                # throwWarning:tr("{0} on suspicious object","{0.key}")
                err.append({'class': 303211, 'subclass': 0, 'text': mapcss.tr('{0} on suspicious object', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[building=roof][amenity][amenity!=shelter][parking!=rooftop]
        if ('amenity' in keys and 'building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'roof')) and (mapcss._tag_capture(capture_tags, 1, tags, 'amenity')) and (mapcss._tag_capture(capture_tags, 2, tags, 'amenity') != mapcss._value_const_capture(capture_tags, 2, 'shelter', 'shelter')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking') != mapcss._value_const_capture(capture_tags, 3, 'rooftop', 'rooftop')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"3032/30322/3"
                # throwWarning:tr("{0} together with {1}, usually {1} is located underneath the {2}. Tag the {3} as a separate object.","{0.tag}","{1.tag}","{0.value}","{1.key}")
                # assertMatch:"way building=roof amenity=fuel"
                # assertNoMatch:"way building=roof amenity=parking parking=rooftop"
                err.append({'class': 30322, 'subclass': 0, 'text': mapcss.tr('{0} together with {1}, usually {1} is located underneath the {2}. Tag the {3} as a separate object.', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{0.value}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # *[highway=emergency_access_point][!ref]
        if ('highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'emergency_access_point')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'ref')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("highway")
                # -osmoseItemClassLevel:"2080/20802:1/2"
                # throwWarning:tr("Missing tag ref for emergency access point")
                err.append({'class': 20802, 'subclass': 1, 'text': mapcss.tr('Missing tag ref for emergency access point')})

        # *[amenity=recycling][recycling_type!=centre][recycling:glass=yes][outside("CZ")]
        if ('amenity' in keys and 'recycling:glass' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'recycling')) and (mapcss._tag_capture(capture_tags, 1, tags, 'recycling_type') != mapcss._value_const_capture(capture_tags, 1, 'centre', 'centre')) and (mapcss._tag_capture(capture_tags, 2, tags, 'recycling:glass') == mapcss._value_capture(capture_tags, 2, 'yes')) and (mapcss.outside(self.father.config.options, 'CZ')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("fix:chair")
                # -osmoseDetail:tr("Most street-side glass containers only accept soda-lime glass (e.g. bottles and jars), but not glasses for high temperatures or window glass.")
                # -osmoseItemClassLevel:"3230/32301/2"
                # -osmoseResource:"https://wiki.openstreetmap.org/wiki/Tag:amenity=recycling"
                # throwWarning:tr("Probably only for bottles, not any type of glass")
                # fixRemove:"recycling:glass"
                # fixAdd:"recycling:glass_bottles=yes"
                err.append({'class': 32301, 'subclass': 0, 'text': mapcss.tr('Probably only for bottles, not any type of glass'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['recycling:glass_bottles','yes']]),
                    '-': ([
                    'recycling:glass'])
                }})

        # *[amenity=recycling][recycling_type!=centre][name]
        if ('amenity' in keys and 'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'recycling')) and (mapcss._tag_capture(capture_tags, 1, tags, 'recycling_type') != mapcss._value_const_capture(capture_tags, 1, 'centre', 'centre')) and (mapcss._tag_capture(capture_tags, 2, tags, 'name')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("fix:chair")
                # -osmoseItemClassLevel:"3230/32302/2"
                # throwWarning:tr("Suspicious name for a container")
                err.append({'class': 32302, 'subclass': 0, 'text': mapcss.tr('Suspicious name for a container')})

        # way[highway][fee][!amenity][!leisure]
        if ('fee' in keys and 'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'fee')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'amenity')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'leisure')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Watch multiple tags")
                # -osmoseTags:list("fix:chair","highway","tag")
                # -osmoseItemClassLevel:"3032/30320:1000/1"
                # throwWarning:tr("Use tag \"toll\" instead of \"fee\"")
                # fixChangeKey:"fee=>toll"
                # assertMatch:"way highway=primary fee=yes"
                # assertNoMatch:"way highway=service fee=yes amenity=weighbridge"
                err.append({'class': 30320, 'subclass': 1000, 'text': mapcss.tr('Use tag "toll" instead of "fee"'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['toll', mapcss.tag(tags, 'fee')]]),
                    '-': ([
                    'fee'])
                }})

        # way[highway][junction=roundabout][area][area!=no]
        if ('area' in keys and 'highway' in keys and 'junction' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'junction') == mapcss._value_capture(capture_tags, 1, 'roundabout')) and (mapcss._tag_capture(capture_tags, 2, tags, 'area')) and (mapcss._tag_capture(capture_tags, 3, tags, 'area') != mapcss._value_const_capture(capture_tags, 3, 'no', 'no')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("fix:chair","highway","roundabout")
                # -osmoseItemClassLevel:"4020/40201:0/1"
                # throwWarning:tr("Roundabout as area")
                # fixRemove:"area"
                # assertMatch:"way area=yes highway=secondary junction=roundabout"
                err.append({'class': 40201, 'subclass': 0, 'text': mapcss.tr('Roundabout as area'), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'area'])
                }})

        # way[junction][junction!=yes][!highway][!area:highway]
        if ('junction' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'junction')) and (mapcss._tag_capture(capture_tags, 1, tags, 'junction') != mapcss._value_const_capture(capture_tags, 1, 'yes', 'yes')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'area:highway')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("tag","highway","roundabout","fix:chair")
                # -osmoseTrap:tr("Check if it is really a highway and it is not already mapped.")
                # -osmoseDetail:tr("The way has a tag `junction=*` but without `highway=*`.")
                # -osmoseItemClassLevel:"2080/20800:0/1"
                # throwWarning:tr("Tag highway missing on junction")
                # assertNoMatch:"way junction=roundabout highway=service"
                # assertMatch:"way junction=roundabout waterway=river"
                # assertNoMatch:"way junction=yes"
                err.append({'class': 20800, 'subclass': 0, 'text': mapcss.tr('Tag highway missing on junction')})

        # way[oneway][!highway][!railway][!aerialway][!waterway][!aeroway][!piste:type]
        if ('oneway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'oneway')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'railway')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'aerialway')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'waterway')) and (not mapcss._tag_capture(capture_tags, 5, tags, 'aeroway')) and (not mapcss._tag_capture(capture_tags, 6, tags, 'piste:type')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("tag","highway","fix:chair")
                # -osmoseTrap:tr("Check if it is really a highway and it is not already mapped.")
                # -osmoseDetail:tr("The way has a tag `oneway=*` but without `highway=*`.")
                # -osmoseItemClassLevel:"2080/20801:0/1"
                # throwWarning:tr("Tag highway missing on oneway")
                # assertNoMatch:"way highway=x cycleway=opposite oneway=yes"
                # assertMatch:"way oneway=yes building=yes"
                err.append({'class': 20801, 'subclass': 0, 'text': mapcss.tr('Tag highway missing on oneway')})

        # way[waterway][level]
        if ('level' in keys and 'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'waterway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'level')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("tag","fix:chair")
                # -osmoseTrap:tr("Remove `level` and check if `layer` is needed instead.")
                # -osmoseDetail:tr("The tag `level` should be used for buildings, shops, amenities, etc.")
                # -osmoseItemClassLevel:"3032/30327:0/2"
                # throwWarning:tr("Waterway with `level`")
                # fixChangeKey:"level=>layer"
                # assertMatch:"way waterway=stream level=-1"
                err.append({'class': 30327, 'subclass': 0, 'text': mapcss.tr('Waterway with `level`'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['layer', mapcss.tag(tags, 'level')]]),
                    '-': ([
                    'level'])
                }})

        # way[tunnel][highway=~/^(motorway_link|trunk_link|primary|primary_link|secondary|secondary_link)$/][!maxheight][!maxheight:physical][tunnel!=no]
        # way[covered][highway=~/^(motorway_link|trunk_link|primary|primary_link|secondary|secondary_link)$/][!maxheight][!maxheight:physical][covered!=no]
        if ('covered' in keys and 'highway' in keys) or ('highway' in keys and 'tunnel' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tunnel')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_2ae49e65), mapcss._tag_capture(capture_tags, 1, tags, 'highway'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'maxheight')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'maxheight:physical')) and (mapcss._tag_capture(capture_tags, 4, tags, 'tunnel') != mapcss._value_const_capture(capture_tags, 4, 'no', 'no')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'covered')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_2ae49e65), mapcss._tag_capture(capture_tags, 1, tags, 'highway'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'maxheight')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'maxheight:physical')) and (mapcss._tag_capture(capture_tags, 4, tags, 'covered') != mapcss._value_const_capture(capture_tags, 4, 'no', 'no')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("tag","highway","maxheight","fix:survey")
                # -osmoseDetail:tr("Missing `maxheight=*` or `maxheight:physical=*` for a tunnel or a way under a bridge.")
                # -osmoseItemClassLevel:"7130/71301:0/3"
                # throwWarning:tr("Missing maxheight tag")
                # assertNoMatch:"way highway=primary covered=no"
                # assertMatch:"way highway=primary covered=yes"
                # assertNoMatch:"way highway=primary tunnel=yes maxheight=2.4"
                # assertMatch:"way highway=primary tunnel=yes"
                err.append({'class': 71301, 'subclass': 0, 'text': mapcss.tr('Missing maxheight tag')})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[building=roof][amenity][amenity!=shelter][parking!=rooftop]
        if ('amenity' in keys and 'building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'roof')) and (mapcss._tag_capture(capture_tags, 1, tags, 'amenity')) and (mapcss._tag_capture(capture_tags, 2, tags, 'amenity') != mapcss._value_const_capture(capture_tags, 2, 'shelter', 'shelter')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking') != mapcss._value_const_capture(capture_tags, 3, 'rooftop', 'rooftop')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"3032/30322/3"
                # throwWarning:tr("{0} together with {1}, usually {1} is located underneath the {2}. Tag the {3} as a separate object.","{0.tag}","{1.tag}","{0.value}","{1.key}")
                err.append({'class': 30322, 'subclass': 0, 'text': mapcss.tr('{0} together with {1}, usually {1} is located underneath the {2}. Tag the {3} as a separate object.', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{0.value}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # *[highway=emergency_access_point][!ref]
        if ('highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'emergency_access_point')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'ref')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("highway")
                # -osmoseItemClassLevel:"2080/20802:1/2"
                # throwWarning:tr("Missing tag ref for emergency access point")
                err.append({'class': 20802, 'subclass': 1, 'text': mapcss.tr('Missing tag ref for emergency access point')})

        # *[amenity=recycling][recycling_type!=centre][recycling:glass=yes][outside("CZ")]
        if ('amenity' in keys and 'recycling:glass' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'recycling')) and (mapcss._tag_capture(capture_tags, 1, tags, 'recycling_type') != mapcss._value_const_capture(capture_tags, 1, 'centre', 'centre')) and (mapcss._tag_capture(capture_tags, 2, tags, 'recycling:glass') == mapcss._value_capture(capture_tags, 2, 'yes')) and (mapcss.outside(self.father.config.options, 'CZ')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("fix:chair")
                # -osmoseDetail:tr("Most street-side glass containers only accept soda-lime glass (e.g. bottles and jars), but not glasses for high temperatures or window glass.")
                # -osmoseItemClassLevel:"3230/32301/2"
                # -osmoseResource:"https://wiki.openstreetmap.org/wiki/Tag:amenity=recycling"
                # throwWarning:tr("Probably only for bottles, not any type of glass")
                # fixRemove:"recycling:glass"
                # fixAdd:"recycling:glass_bottles=yes"
                err.append({'class': 32301, 'subclass': 0, 'text': mapcss.tr('Probably only for bottles, not any type of glass'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['recycling:glass_bottles','yes']]),
                    '-': ([
                    'recycling:glass'])
                }})

        # *[amenity=recycling][recycling_type!=centre][name]
        if ('amenity' in keys and 'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'recycling')) and (mapcss._tag_capture(capture_tags, 1, tags, 'recycling_type') != mapcss._value_const_capture(capture_tags, 1, 'centre', 'centre')) and (mapcss._tag_capture(capture_tags, 2, tags, 'name')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("fix:chair")
                # -osmoseItemClassLevel:"3230/32302/2"
                # throwWarning:tr("Suspicious name for a container")
                err.append({'class': 32302, 'subclass': 0, 'text': mapcss.tr('Suspicious name for a container')})

        # relation[!type]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not mapcss._tag_capture(capture_tags, 0, tags, 'type')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("tag")
                # -osmoseDetail:tr("The relation is missing a `type` tag to define what it represents.")
                # -osmoseItemClassLevel:"2110/21102/2"
                # throwWarning:tr("Missing relation type")
                # assertMatch:"relation"
                err.append({'class': 21102, 'subclass': 0, 'text': mapcss.tr('Missing relation type')})

        return err


from plugins.PluginMapCSS import TestPluginMapcss


class Test(TestPluginMapcss):
    def test(self):
        n = TagFix_MultipleTag2(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        with with_options(n, {'country': 'CZ'}):
            self.check_not_err(n.node(data, {'amenity': 'recycling', 'recycling:glass': 'yes', 'recycling_type': 'container'}), expected={'class': 32301, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_err(n.node(data, {'amenity': 'recycling', 'recycling:glass': 'yes', 'recycling_type': 'container'}), expected={'class': 32301, 'subclass': 0})
        self.check_err(n.node(data, {'amenity': 'recycling', 'name': 'My nice awesome container', 'recycling_type': 'container'}), expected={'class': 32302, 'subclass': 0})
        self.check_err(n.way(data, {'amenity': 'fuel', 'building': 'roof'}, [0]), expected={'class': 30322, 'subclass': 0})
        self.check_not_err(n.way(data, {'amenity': 'parking', 'building': 'roof', 'parking': 'rooftop'}, [0]), expected={'class': 30322, 'subclass': 0})
        self.check_err(n.way(data, {'fee': 'yes', 'highway': 'primary'}, [0]), expected={'class': 30320, 'subclass': 1000})
        self.check_not_err(n.way(data, {'amenity': 'weighbridge', 'fee': 'yes', 'highway': 'service'}, [0]), expected={'class': 30320, 'subclass': 1000})
        self.check_err(n.way(data, {'area': 'yes', 'highway': 'secondary', 'junction': 'roundabout'}, [0]), expected={'class': 40201, 'subclass': 0})
        self.check_not_err(n.way(data, {'highway': 'service', 'junction': 'roundabout'}, [0]), expected={'class': 20800, 'subclass': 0})
        self.check_err(n.way(data, {'junction': 'roundabout', 'waterway': 'river'}, [0]), expected={'class': 20800, 'subclass': 0})
        self.check_not_err(n.way(data, {'junction': 'yes'}, [0]), expected={'class': 20800, 'subclass': 0})
        self.check_not_err(n.way(data, {'cycleway': 'opposite', 'highway': 'x', 'oneway': 'yes'}, [0]), expected={'class': 20801, 'subclass': 0})
        self.check_err(n.way(data, {'building': 'yes', 'oneway': 'yes'}, [0]), expected={'class': 20801, 'subclass': 0})
        self.check_err(n.way(data, {'level': '-1', 'waterway': 'stream'}, [0]), expected={'class': 30327, 'subclass': 0})
        self.check_not_err(n.way(data, {'covered': 'no', 'highway': 'primary'}, [0]), expected={'class': 71301, 'subclass': 0})
        self.check_err(n.way(data, {'covered': 'yes', 'highway': 'primary'}, [0]), expected={'class': 71301, 'subclass': 0})
        self.check_not_err(n.way(data, {'highway': 'primary', 'maxheight': '2.4', 'tunnel': 'yes'}, [0]), expected={'class': 71301, 'subclass': 0})
        self.check_err(n.way(data, {'highway': 'primary', 'tunnel': 'yes'}, [0]), expected={'class': 71301, 'subclass': 0})
        self.check_err(n.relation(data, {}, []), expected={'class': 21102, 'subclass': 0})
