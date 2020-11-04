# encoding: utf-8

import gvsig
import sys

from gvsig import uselib
uselib.use_plugin("org.gvsig.topology.app.mainplugin")

from org.gvsig.fmap.geom import Geometry
from org.gvsig.tools.util import ListBuilder
from org.gvsig.topology.lib.api import TopologyLocator
from org.gvsig.topology.lib.spi import AbstractTopologyRuleFactory, RuleResourceLoaderUtils
 

from java.io import File
from java.lang import IllegalStateException

from containsOnePointPolygonRule import ContainsOnePointPolygonRule


class ContainsOnePointPolygonRuleFactory(AbstractTopologyRuleFactory):
      
    def __init__(self):
        AbstractTopologyRuleFactory.__init__(
            self,
            "ContainsOnePointPolygon",
            "Contains One Point Polygon Rule GSoC2020",
            "The rule evaluates all the polygons. If each polygon has only one point inside, the rule returns True. The point has to fall within the polygon's area, not on the boundary or out of it. The evaluated polygons without points make the rule False too. The red polygons does the rule false. In 2DM, 3D and 3DM formats, the Z coordinate or M coordinate are ignored.\n \n NOTE 1: If the Tolerance equals zero, the rule does as above. If the tolerance is greater than zero, the scrip does a polygon buffer with tolerance value. If the point are inside of new dataset 1 polygon, the rule return True. \n \n NOTE 2: For Multipolygons, only one of their geometries can have one point inside, the rule returns True. For Multipoints, if only one of these geometries are inside of polygon's area, the rule returns True.",
            ListBuilder().add(Geometry.TYPES.POLYGON).add(Geometry.TYPES.MULTIPOLYGON).asList(),
            ListBuilder().add(Geometry.TYPES.POINT).add(Geometry.TYPES.MULTIPOINT).asList()
        )

        pathName = gvsig.getResource(__file__,'ContainsOnePointPolygon.json')
        url = File(pathName).toURL()
        gvsig.logger(str(url))
        json = RuleResourceLoaderUtils.getRule(url)
        self.load_from_resource(url, json)
    
    def createRule(self, plan, dataSet1, dataSet2, tolerance):
      #store1=dataSet1.getFeatureStore()
      #store2=dataSet2.getFeatureStore()
      
      #if store1.getSRSDefaultGeometry()!=store2.getSRSDefaultGeometry():
        #raise IllegalStateException("Can't execute rule. The two datasets cant have a different projection.")
  
      rule = ContainsOnePointPolygonRule(plan, self, tolerance, dataSet1, dataSet2)
      return rule

def selfRegister():
    try:
        manager = TopologyLocator.getTopologyManager()
        manager.addRuleFactories(ContainsOnePointPolygonRuleFactory())
    except:
        ex = sys.exc_info()[1]
        gvsig.logger("Can't register rule. Class Name: " + ex.__class__.__name__ + ". Exception: " + str(ex), gvsig.LOGGER_ERROR)

def main(*args):
    pass