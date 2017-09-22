# Fix Villager Variants for Bedrock
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

from pymclevel import TAG_Compound, TAG_Int, TAG_Short, TAG_Byte, TAG_String, TAG_Float, TAG_List
import string, csv

displayName = "Bedrock - Fix Villager Variants"
VERSION = 1.0

inputs =(("Fix Villager Variants for Bedrock", "label"),
		("Component Group Mappings CSV", "label"),
		("(componentGroup:variant)",("string", "width=350"))
		)
def perform(level, box, options):
	cgCSV = options["(componentGroup:variant)"]
	allowedCG = string.split(cgCSV,",")
	mapping = []
	for item in allowedCG:
		items = string.split(item,":")
		mapping.append(items)
	print(mapping)
	for (chunk, slices, point) in level.getChunkSlices(box):
		for e in chunk.Entities:
				x = e["Pos"][0].value
				y = e["Pos"][1].value
				z = e["Pos"][2].value
				id = e["id"].value
				if ((x,y,z) in box) and (id == "Villager"):
					for definitions in e["definitions"]:
						for componentGroupMap in mapping:
							componentGroup = componentGroupMap[0]
							variant = componentGroupMap[1]
							if definitions.value.replace("+","").lower() == componentGroup.lower():
								print("allowedCG")
								chunk.Entities.remove(e)
								villager = e
								villager["Variant"] = TAG_Int(int(variant))
								chunk.Entities.append(villager)
								chunk.dirty = True
								

