from lxml import etree
from lxml.etree import fromstring
from pykml import parser
from os import path
import math
import utm
import re
from tkinter import filedialog

def line2PointDist(linePt1x, linePt1y, linePt2x, linePt2y, outsidePtx, outsidePty):
    numerator = (linePt2y - linePt1y)*outsidePtx - (linePt2x - linePt1x)*outsidePty + linePt2x*linePt1y - linePt2y*linePt1x
    denominator = math.sqrt((linePt2y - linePt1y)**2 + (linePt2x - linePt1x)**2)
    return abs(numerator)/denominator

#user specifies path
filename = filedialog.askopenfilename()
shortFileName = re.search('/[^/]*\.kml', filename)
thing = shortFileName.group(0)
thing = thing.replace("/", "")
thing = thing.replace(".kml", "")
with open(filename) as f:
    doc = parser.parse(f)

kmlstring = str(etree.tostring(doc))
coords = re.findall('<coordinates>-?[0-9][0-9]\.[0-9]*,-?[0-9][0-9]\.[0-9]*', kmlstring)
for x in range(0, len(coords)):
    coords[x] = coords[x].replace("<coordinates>", "")
    coords[x] = coords[x].split(",")

#input overlap % and height, this will calculate v_max  and d_int and print those out?
alpha = float(input("Desired overlap as a decimal\n"))
h = float(input("Desired height\n"))
#v_max in km/h
v_max = (18.0/5.0)*(h/0.0088)*0.0087552*(1.0-alpha)/2.0
#d_int in meters
d_int = (h/0.0088)*0.0131328*(1.0-alpha)
print("V_max:  " + str(v_max) + " km/h")
print("d_int:  " + str(d_int) + " m")

c1Lat = float(coords[0][1])
c1Lon = float(coords[0][0])
c2Lat = float(coords[1][1])
c2Lon = float(coords[1][0])
c3Lat = float(coords[2][1])
c3Lon = float(coords[2][0])
c4Lat = float(coords[3][1])
c4Lon = float(coords[3][0])

utm1 = utm.from_latlon(c1Lat, c1Lon)
utm2 = utm.from_latlon(c2Lat, c2Lon)
utm3 = utm.from_latlon(c3Lat, c3Lon)
utm4 = utm.from_latlon(c4Lat, c4Lon)

utm1Easting = utm1[0]
utm1Northing = utm1[1]
utm2Easting = utm2[0]
utm2Northing = utm2[1]
utm3Easting = utm3[0]
utm3Northing = utm3[1]
utm4Easting = utm4[0]
utm4Northing = utm4[1]

#find number of passes and change in easting and northing between passes
dist1 = line2PointDist(utm1Easting, utm1Northing, utm2Easting, utm2Northing, utm3Easting, utm3Northing)
dist2 = line2PointDist(utm1Easting, utm1Northing, utm2Easting, utm2Northing, utm4Easting, utm4Northing)
if dist1 > dist2:
    passes = int(math.ceil(dist1/d_int))
else:
    passes = int(math.ceil(dist2/d_int))
dEasting_1 = (utm4Easting - utm1Easting)/passes
dNorthing_1 = (utm4Northing - utm1Northing)/passes
dEasting_2 = (utm3Easting - utm2Easting)/passes
dNorthing_2 = (utm3Northing - utm2Northing)/passes

waypoints = []

switch = True
#go until hit last waypoint
for x in range(0, passes +1):
    if switch:
        waypoints.append([utm1Easting +(x)*dEasting_1, utm1Northing + (x)*dNorthing_1])
        waypoints.append([utm2Easting +(x)*dEasting_2, utm2Northing + (x)*dNorthing_2])
    else:
        waypoints.append([utm2Easting +(x)*dEasting_2, utm2Northing + (x)*dNorthing_2])
        waypoints.append([utm1Easting +(x)*dEasting_1, utm1Northing + (x)*dNorthing_1])
    switch = not switch

#make KML
earth = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
<Document>
	<name>{0}</name>
	<open>1</open>
	<Schema name="Parallelogram Test" id="S_Parallelogram_Test_SDD">
		<SimpleField type="string" name="Point"><displayName>&lt;b&gt;Point&lt;/b&gt;</displayName>
</SimpleField>
		<SimpleField type="double" name="Lat"><displayName>&lt;b&gt;Lat&lt;/b&gt;</displayName>
</SimpleField>
		<SimpleField type="double" name="Long"><displayName>&lt;b&gt;Long&lt;/b&gt;</displayName>
</SimpleField>
	</Schema>
	<Style id="normPointStyle">
		<IconStyle>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href>
			</Icon>
		</IconStyle>
		<BalloonStyle>
			<text><![CDATA[<table border="0">
  <tr><td><b>Point</b></td><td>$[Parallelogram Test/Point]</td></tr>
  <tr><td><b>Lat</b></td><td>$[Parallelogram Test/Lat]</td></tr>
  <tr><td><b>Long</b></td><td>$[Parallelogram Test/Long]</td></tr>
</table>
]]></text>
		</BalloonStyle>
	</Style>
	<StyleMap id="pointStyleMap">
		<Pair>
			<key>normal</key>
			<styleUrl>#normPointStyle</styleUrl>
		</Pair>
		<Pair>
			<key>highlight</key>
			<styleUrl>#hlightPointStyle</styleUrl>
		</Pair>
	</StyleMap>
	<Style id="hlightPointStyle">
		<IconStyle>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle_highlight.png</href>
			</Icon>
		</IconStyle>
		<BalloonStyle>
			<text><![CDATA[<table border="0">
  <tr><td><b>Point</b></td><td>$[Parallelogram Test/Point]</td></tr>
  <tr><td><b>Lat</b></td><td>$[Parallelogram Test/Lat]</td></tr>
  <tr><td><b>Long</b></td><td>$[Parallelogram Test/Long]</td></tr>
</table>
]]></text>
		</BalloonStyle>
	</Style>
	<Folder id="layer 0">
		<name>{0}</name>
		<open>1</open>
		"""
ender = """</Folder>
</Document>
</kml>
"""

for x in range(0, len(waypoints)):
    z = x + 3
    if(z%2 == 1):
        ptName = "P" + str(int(math.floor(z/2))) +"-1"
    else:
        ptName = "P" + str(int(math.floor(z/2)-1)) +"-2"
    tup = utm.to_latlon(waypoints[x][0], waypoints[x][1], utm1[2], utm1[3])
    repeat = """<Placemark>
        <name>{}</name>
        <styleUrl>#pointStyleMap</styleUrl>
        <Style id="inline">
            <IconStyle>
                <color>fff0f0f0</color>
                <colorMode>normal</colorMode>
            </IconStyle>
            <LineStyle>
                <color>fff0f0f0</color>
                <colorMode>normal</colorMode>
            </LineStyle>
            <PolyStyle>
                <color>fff0f0f0</color>
                <colorMode>normal</colorMode>
            </PolyStyle>
        </Style>
        <ExtendedData>
            <SchemaData schemaUrl="#S_PUMapMaker_SDD">
                <SimpleData name="Point">{}</SimpleData>
                <SimpleData name="Lat">{}</SimpleData>
                <SimpleData name="Long">{}</SimpleData>
            </SchemaData>
        </ExtendedData>
        <Point>
            <coordinates>{},{},0</coordinates>
        </Point>
    </Placemark>\n""".format(ptName, ptName, tup[0], tup[1], tup[1], tup[0])
    earth = earth + repeat
earth = earth + ender
xml = earth.format(thing).encode('utf-8')
parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
h = fromstring(xml, parser=parser)
filename = filename.replace('.kml', '_MM.kml')
outfile = open(filename,'wb')
outfile.write(etree.tostring(h, pretty_print=True))
