# Pathway Studios http://pathway.studio - @pathwaymc on Twitter
# Copyright (C) 2017  Pathway Studios

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from pymclevel import TAG_Compound, TAG_Int, TAG_Short, TAG_Byte, TAG_String, TAG_Float, TAG_List, TileEntity, id_definitions, leveldb, leveldbpocket
from collections import Counter
import string
import os.path
import json
import urllib2
import math

displayName = "Bedrock - can_place_on_Blocks"
VERSION = 1.0

if os.path.isfile('pe-item-associations.json'): 
	idMappings = json.load(open('pe-item-associations.json'))
	associations = 1

req = urllib2.Request('http://pathway.studio/resources/pe-item-associations.json')
url=urllib2		

try:
	response = urllib2.urlopen(req)
	idMappingsRemote = json.loads(response.read())

except url.URLError as e:
	print "Error getting associations file: " +str(e.reason)
	
inputs = (
	("Generate chest of blocks from selection with can_place_on tag", "label"),
	("Pick a can_place_on block:", "blocktype")
)

newIdMappings = dict((v,k) for k,v in idMappings["items"].iteritems())


def perform(level, box, options):
	canPlaceOn = options["Pick a can_place_on block:"].ID
	canPlaceOn = newIdMappings[str(canPlaceOn)]
	blockData = []
	blocks = []
	for (x, y, z) in box.positions:
		block = level.blockAt(x,y,z)
		data = level.blockDataAt(x,y,z)
		if (block != 0):
			if (block == 54):
				chest=x,y,z
				cx=x
				cy=y
				cz=z
			else:
				bdata = block,data
				blockData.append(bdata)	
				if (bdata) not in blocks:
					blocks.append(bdata)
	bcounts = Counter(blockData)
	newte = createChest(blocks,bcounts,canPlaceOn,chest,level)
	print(newte)
	rmChest = level.tileEntityAt(cx, cy, cz)
	chunk = level.getChunk(cx/16,cz/16)
	chunk.TileEntities.remove(rmChest)
	chunk.TileEntities.append(newte)
	chunk.dirty = True
def createChest(blockData,count,canPlaceOn,chest,level):
	newte = TileEntity.Create("Chest")
	slot = 0
	for i in blockData:		
		if count[i] > 64:
			icount = 1
			iterCount = math.ceil(count[i]/64.0)
			rcount = count[i] % 64				
			while icount <= iterCount:
				if icount == iterCount:
					item= TAG_Compound()
					item["CanPlaceOn"] = TAG_List()
					item["id"] = TAG_Short(i[0])
					item["Damage"] = TAG_Short(i[1])
					item["Count"] = TAG_Byte(rcount)					
					item["Slot"] = TAG_Byte(int(slot))
					item["CanPlaceOn"] = [TAG_String(canPlaceOn)]
					newte["Items"].append(item)
					slot += 1
				else:
					item= TAG_Compound()
					item["CanPlaceOn"] = TAG_List()
					item["id"] = TAG_Short(i[0])
					item["Damage"] = TAG_Short(i[1])
					item["Damage"] = TAG_Short(i[1])
					item["Count"] = TAG_Byte(64)					
					item["Slot"] = TAG_Byte(int(slot))
					item["CanPlaceOn"] = [TAG_String(canPlaceOn)]
					newte["Items"].append(item)
					slot += 1
				icount += 1
		else:
			item= TAG_Compound()
			item["CanPlaceOn"] = TAG_List()
			item["id"] = TAG_Short(i[0])
			item["Damage"] = TAG_Short(i[1])
			item["Count"] = TAG_Byte(count[i])
			item["Slot"] = TAG_Byte(int(slot))
			item["CanPlaceOn"] = [TAG_String(canPlaceOn)]
			newte["Items"].append(item)
			slot += 1		
		
	print(chest)
	newte['x'] = TAG_Int(chest[0])
	newte['y'] = TAG_Int(chest[1])
	newte['z'] = TAG_Int(chest[2])
	return newte
	
	