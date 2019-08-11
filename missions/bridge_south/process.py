import processing

out_path = "./Documents/maps/outputs/"

############# V1 used 'processing' approach ################################

def get_relevant_hazards():
  # expand the specified flight_area region
  processing.runalg('qgis:fixeddistancebuffer', "flight_area", 50.0, 12, False,out_path+"flight_buffer.shp")
  iface.addVectorLayer(out_path+"flight_buffer.shp","Flight Buffer","ogr")

  # extract everything from the hazards layer "all_hazards" that overlaps with the expanded flight area
  processing.runalg("qgis:clip","all_hazards","Flight Buffer",out_path+"relevant_hazards.shp")
  iface.addVectorLayer(out_path+"relevant_hazards.shp","Relevant Hazards","ogr")

def find_all_hazard_buffers():
  # add a buffer to all the hazards identified above
  processing.runalg('qgis:fixeddistancebuffer', "Relevant Hazards", 50.0, 12, False,out_path+"hazard_buffers.shp")
  iface.addVectorLayer(out_path+"hazard_buffers.shp","Hazard Buffers","ogr")

def make_buffer_layer(layer_name):
  new_layer_name = layer_name + ' Buffer'
  layer_file_name = out_path + new_layer_name.replace(' ','_') + '.shp'
  processing.runalg('qgis:fixeddistancebuffer', layer_name, 50.0, 12, True,layer_file_name)
  iface.addVectorLayer(layer_file_name,new_layer_name,"ogr")  

def get_safe_region():
  # the safe region is that set of locations outside all the hazards but still inside the flight area
  # if it comes up empty, need to expand the flight area
  processing.runalg("qgis:difference","flight_area","Hazard Buffers",out_path+"safe_regions.shp")
  sfr_lyr = iface.addVectorLayer(out_path+"safe_regions.shp","Safe Regions","ogr")

def get_safti_point():
  # grab the waypoints as a list, assuming that the first of them is the "home" location
  wp_lyr = QgsMapLayerRegistry.instance().mapLayersByName("waypoints")[0]
  wp_list=[]
  for f in wp_lyr.getFeatures():
    wp_list.append(f)
  home_point = wp_list[0].geometry().asPoint()
  # also grab the safety regions as a list
  sfr_lyr = QgsMapLayerRegistry.instance().mapLayersByName("Safe Regions")[0]
  sfr_list=[]
  for f in sfr_lyr.getFeatures():
    sfr_list.append(f)
  # get closest point in safety region to home waypoint
  (safti_point,b,c,d,dist_sqrd) = sfr_list[0].geometry().closestVertex(home_point)
  return(safti_point,home_point)

def get_no_fly_zones():
  # assumes that the marshalled bits of the 'relevant_hazards' layer have been removed
  processing.runalg('qgis:fixeddistancebuffer', "Relevant Hazards", 50.0, 12, True,out_path+"no_fly_zones.shp")
  iface.addVectorLayer(out_path+"no_fly_zones.shp","No Fly Zones","ogr")  

def get_hazards_by_map():
  # expand the specified flight_area region
  processing.runalg('qgis:fixeddistancebuffer', "flight_area", 50.0, 12, False,out_path+"flight_buffer.shp")
  iface.addVectorLayer(out_path+"flight_buffer.shp","Flight Buffer","ogr")

  # extract everything from the hazards layer "all_hazards" that overlaps with the expanded flight area
  processing.runalg("qgis:clip","all_hazards","Flight Buffer",out_path+"relevant_hazards.shp")
  iface.addVectorLayer(out_path+"relevant_hazards.shp","Relevant Hazards","ogr")

############ EXPERIMENTS ######################

def add_stuff_example():
  # Specify the geometry type
  layer = QgsVectorLayer('LineString?crs=epsg:27700', 'FlightPath' , 'memory')
 
  # Set the provider to&nbsp;accept the data source
  prov = layer.dataProvider()
  #point1 = QgsPoint(100,100)
  #point2 = QgsPoint(200,200)
  (point1,point2)=get_safti_point()
 
  # Add a new feature and assign the geometry
  feat = QgsFeature()
  feat.setGeometry(QgsGeometry.fromPolyline([point1, point2]))
  prov.addFeatures([feat])
 
  # Update extent of the layer
  layer.updateExtents()
 
  # Add the layer to the Layers panel
  QgsMapLayerRegistry.instance().addMapLayers([layer])

################################################

def safe_get_layer_by_name(layer_name):
  layer_list = QgsMapLayerRegistry.instance().mapLayersByName(layer_name)
  num_layers = len(layer_list)
  assert(num_layers==1)
  return(layer_list[0])

def list_all_features(layer):
  return([f for f in layer.getFeatures()])

def show_layer(layer_in):
  QgsMapLayerRegistry.instance().addMapLayers([layer_in])

def make_buffer_layer(layer_in):
  # start a new Polygon layer
  layer = QgsVectorLayer('Polygon?crs=epsg:27700', 'Flight Area Buffer' , 'memory')
 
  # Set the provider to&nbsp;accept the data source
  prov = layer.dataProvider()
 
  for f_in in layer_in.getFeatures():
    # Add a new feature and assign the geometry
    feat = QgsFeature()    
    feat.setGeometry(f_in.geometry().buffer(50.0,12))
    prov.addFeatures([feat])
 
  # Update extent of the layer
  layer.updateExtents()
  return(layer)

def extract_relevant_hazards():
  # extract everything from the hazards layer "all_hazards" that overlaps with the expanded flight area
  processing.runalg("qgis:clip","all_hazards","Flight Area Buffer",out_path+"relevant_hazards.shp")
  iface.addVectorLayer(out_path+"relevant_hazards.shp","Relevant Hazards","ogr")

def make_hazard_map():
  # get to the point where the user sorts the hazards into controlled and uncontrolled
  flight_area_layer = safe_get_layer_by_name('Flight Area')
  flight_buffer_layer = make_buffer_layer(flight_area_layer)

def add_safti_marker():
  # Specify the geometry type
  layer = QgsVectorLayer('Point?crs=epsg:27700', 'SAFTI' , 'memory')
 
  # Set the provider to accept the data source
  prov = layer.dataProvider()
  (point,point2)=get_safti_point()
 
  # Add a new feature and assign the geometry
  feat = QgsFeature()
  feat.setGeometry(QgsGeometry.fromPoint(point))
  prov.addFeatures([feat])
 
  # Update extent of the layer
  layer.updateExtents()
 
  # Add the layer to the Layers panel
  QgsMapLayerRegistry.instance().addMapLayers([layer])

def add_approach_markers():
  wpfs = list_all_features(safe_get_layer_by_name('waypoints'))
  sffs = list_all_features(safe_get_layer_by_name('safti'))
  gm_safti = sffs[0].geometry()
  gm_wp1 = wpfs[0].geometry()
  dist_safti_wp1 = gm_safti.distance(gm_wp1)

  # Specify the geometry type
  layer = QgsVectorLayer('Point?crs=epsg:27700', 'Approach' , 'memory')
  prov = layer.dataProvider()
  
  # 20m waypoint
  r = 20.0
  if dist_safti_wp1>r:
    nx = gm_wp1.asPoint()[0] + (r/dist_safti_wp1)*(gm_safti.asPoint()[0]-gm_wp1.asPoint()[0])
    ny = gm_wp1.asPoint()[1] + (r/dist_safti_wp1)*(gm_safti.asPoint()[1]-gm_wp1.asPoint()[1])
    # Add a new feature and assign the geometry
    feat = QgsFeature()
    feat.setGeometry(QgsGeometry.fromPoint(QgsPoint(nx,ny)))
    prov.addFeatures([feat])

  # 20m waypoint
  r = 10.0
  if dist_safti_wp1>r:
    nx = gm_wp1.asPoint()[0] + (r/dist_safti_wp1)*(gm_safti.asPoint()[0]-gm_wp1.asPoint()[0])
    ny = gm_wp1.asPoint()[1] + (r/dist_safti_wp1)*(gm_safti.asPoint()[1]-gm_wp1.asPoint()[1])
    # Add a new feature and assign the geometry
    feat = QgsFeature()
    feat.setGeometry(QgsGeometry.fromPoint(QgsPoint(nx,ny)))
    prov.addFeatures([feat])

  # Update extent of the layer
  layer.updateExtents()
 
  # Add the layer to the Layers panel
  QgsMapLayerRegistry.instance().addMapLayers([layer])

def compile_flight_path():
  hmfs = list_all_features(safe_get_layer_by_name('home'))
  apfs = list_all_features(safe_get_layer_by_name('Approach'))
  wpfs = list_all_features(safe_get_layer_by_name('waypoints'))
  sffs = list_all_features(safe_get_layer_by_name('safti'))
  flfs = hmfs+sffs+apfs+wpfs+sffs+hmfs # round trip
  fl_polyline = [f.geometry().asPoint() for f in flfs]

  # Specify the geometry type
  layer = QgsVectorLayer('LineString?crs=epsg:27700', 'Flight' , 'memory')
 
  # Set the provider to&nbsp;accept the data source
  prov = layer.dataProvider()
 
  # Add a new feature and assign the geometry
  feat = QgsFeature()
  feat.setGeometry(QgsGeometry.fromPolyline(fl_polyline))
  prov.addFeatures([feat])
 
  # Update extent of the layer
  layer.updateExtents()
 
  # Add the layer to the Layers panel
  QgsMapLayerRegistry.instance().addMapLayers([layer])

def get_all_points():
  hmfs = list_all_features(safe_get_layer_by_name('home'))
  apfs = list_all_features(safe_get_layer_by_name('Approach'))
  wpfs = list_all_features(safe_get_layer_by_name('waypoints'))
  sffs = list_all_features(safe_get_layer_by_name('safti'))
  flfs = hmfs+sffs+apfs+wpfs # all of them
  fl_polyline = [f.geometry().asPoint() for f in flfs]

  # Specify the geometry type
  layer = QgsVectorLayer('Point?crs=epsg:27700', 'All Points' , 'memory')
  prov = layer.dataProvider()
  
  for p in fl_polyline:
    # Add a new feature and assign the geometry
    feat = QgsFeature()
    feat.setGeometry(QgsGeometry.fromPoint(p))
    prov.addFeatures([feat])

  # Update extent of the layer
  layer.updateExtents()
 
  # Add the layer to the Layers panel
  QgsMapLayerRegistry.instance().addMapLayers([layer])


  # Specify the geometry type
  layer = QgsVectorLayer('LineString?crs=epsg:27700', 'Flight' , 'memory')
 
  # Set the provider to&nbsp;accept the data source
  prov = layer.dataProvider()
 
  # Add a new feature and assign the geometry
  feat = QgsFeature()
  feat.setGeometry(QgsGeometry.fromPolyline(fl_polyline))
  prov.addFeatures([feat])
 
  # Update extent of the layer
  layer.updateExtents()
 
  # Add the layer to the Layers panel
  QgsMapLayerRegistry.instance().addMapLayers([layer])

# call relevant parts of the process
#get_relevant_hazards()
#find_all_hazards_buffers()
#get_safe_region()
#get_safti_point()
#get_no_fly_zones()
#make_buffer_layer('Towpath Hazards')
#make_buffer_layer('Bridge Hazards')
#add_stuff_example()
#add_safti_marker()
#compile_flight_path()
