# 1-GML Parsing (GML reduction and Buffer creation):

### Workflow:

1. Download ITN maps from [https://digimap.edina.ac.uk/roam/download/os](https://digimap.edina.ac.uk/roam/download/os)
    - (optional) Download topography maps (separate folder)
2. Place the downloaded files (itn.gml and itnpaths.gml) in the same folder as the python scripts
3. Run itnparsing.py to consolidate the gml files and generate output files (itnout.gml and itnpathsout.gml)
4. Run buffer.py to generate the buffer around the roads and paths (as shapefiles, exported in &#39;Output&#39; folder)
5. Import consolidated ITN GML files (or topography maps) and Buffer shapefiles to QGIS using the &quot;add vector layer&quot; function

Notes:

Required python libraries: shapely, osgeo

Use topography maps to visualise the bridge and overlay it with flight paths etc. since they consist of polygons and offer better visualisation of the area

ITN maps are used to create buffers around roads and footpaths since they consist of polylines and not polygons

The exported shapefiles (.SHP) from buffer.py script that describe the buffer around roads and footpaths do not have embedded information about their coordinate system the same way GML files do. Upon importing the shapefile to QGIS, a dialog box will pop up asking you to define the coordinate system of the shapefile; select EPSG:27700 (British national grid – Ordnance survey)

### Files:

### GML Parsing:

The two scripts described below aim to remove any unnecessary information from the ITN and topography maps to reduce the filesize and make it more manageable

#### ITN Parsing(itnparsing.py)

This python script removes all unnecessary information from the GML files for the Integrated Transport Network (ITN) maps. It requires two inputs: itn.gml which contains major roads, and itnpaths.gml that contains footpaths. The outputs are itnout.gml and itnpathsout.gml respectively.

#### Topography maps parsing (topoparse.py)

Topography maps offer a better visualisation of the area using polygons instead of polylines that ITN uses. The topoparse.py script offers the same functionality as the itnparsing.py script. The difference is that it takes as input a topography map (topo.gml) and outputs a consolidated version of the topo map(outputtopo.gml)

##### Create buffer around roads and paths (buffer.py)

This script only works with ITN maps. NOT WITH TOPOGRAPHY MAPS

This is the script responsible for creating a buffer around roads and paths extracted from itnout.gml and itnpathsout.gml (that were generated using itnparsing.py). Besides the ITN files, this script requires a template GML file (polytemplate.gml) and a folder (gmllayers) to output the files to.

The outputs are two shapefiles (.shp): one for the buffer around the roads and paths, and one for the free space. The outputs can be found in the output folder.



# 2-Waypoint conversion (Mission planner to QGIS)

### Workflow:

1. Export waypoints from MissionPlanner as .txt file (wp.txt)
2. Run Matlab script waypoints.m to sort and create a text file (wpout.txt) with the correct waypoints format
3. Run python script wp.py to generate a GML file (path.gml) from the matlab output
4. Import path.gml in QGIS and overlay it on topography maps

### Files:

##### Waypoints.m

Simple matlab script that takes as input the exported waypoints from mission planner as &#39;wp.txt&#39; and exports a modified text file (wpout.txt) with the correct format required by the GML files. It removes all other unused information

#### Wp.py

Python script that takes as input the exported matlab text file (wpout.txt) along with a GML template file (template.gml) and exports a GML file with the waypoints (path.gml). This can then be imported in QGIS and overlaid on topography maps.

# 3-KML Conversion (From mission planner log files to QGIS-readable GML format)

### Workflow:

1. Export mission planner log files as KMZ (zipped KML file)
2. Extract KMZ file (using 7zip) and retain KML file. Rename to log.kml
3. Run kmlconv.py to generate the output GML file (convertedpath.gml)
4. Import convertedpath.gml in QGIS along with Topography map (see section 1 – GML parsing)

### Files:

#### Kmlconv.py

This python script takes as input the log.kml file as extracted from the .kmz file (which can be exported from mission planner). The script also takes as input a template GML file (wptemplate.gml). It then extracts the long and lat coordinates from the KML file (gx:tour-\&gt; gx:Playlist-\&gt;gx:Flyto-\&gt;Camera) and writes them to a new GML file (convertedpath.gml). The output GML file can now be imported in QGIS and overlaid on topography maps.

A second python script kmlconv2.py is also present. It follows the same process as kmlconv.py, however it extracts the lat and long coordinates from a different element in the KML log file
(Folder-\&gt;Placemark-\&gt;Model-\&gt;Location). Both scripts should produce the same coordinates; if one doesn&#39;t work (due to lack of information in the gx:tour element for example) try the other script.
