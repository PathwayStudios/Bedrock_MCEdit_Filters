# Modified and updated for Bedrock
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

#todo
# - adding wool support (for marking default loot table type)
# - deal with double chests

from pymclevel import TAG_Compound, TAG_Int, TAG_Short, TAG_Byte, TAG_String, TAG_Float, TAG_List, TAG_Long, TileEntity, id_definitions, leveldb, leveldbpocket
import string
import random
import time

displayName = "Bedrock - Dungeon Tools"
VERSION = 1.0

defaultLootTables = {
	"Abandoned Mineshaft": "loot_tables/chests/abandoned_mineshaft",
	"Desert Pyramid": "loot_tables/chests/desert_pyramid",
	"Dispenser Trap": "loot_tables/chests/dispenser_trap",
	"End City Treasure": "loot_tables/chests/end_city_treasure",
	"Igloo Chest": "loot_tables/chests/igloo_chest",
	"Jungle Temple": "loot_tables/chests/jungle_temple",
	"Monster Room": "loot_tables/chests/monster_room",
	"Nether Bridge": "loot_tables/chests/nether_bridge",
	"Simple Dungeon": "loot_tables/chests/simple_dungeon",
	"Spawn Bonus Chest": "loot_tables/chests/spawn_bonus_chest",
	"Stronghold Corridor": "loot_tables/chests/stronghold_corridor",
	"Stronghold Crossing": "loot_tables/chests/stronghold_crossing",
	"Stronghold Library": "loot_tables/chests/stronghold_library",
	"Village Blacksmith": "loot_tables/chests/village_blacksmith",
	"Village Two Room House": "loot_tables/chests/village_two_room_house",
	"Woodland Mansion": "loot_tables/chests/woodland_mansion"
	}
	
defaultLootTablesKeys = ()
for key in defaultLootTables.keys():
	defaultLootTablesKeys = defaultLootTablesKeys + (key,)
	

inputs = [(("Chests", "title"),
		("Default Loot Table", defaultLootTablesKeys),
		("Custom Loot Table", ("string", "width=250")),
		("Default loot table used if left blank", "label"),
		("Loot Table Seed", ("string", "width=250")),
		("Random loot table seed used if left blank", "label"),
		("Only apply to empty chests", True),	),
	
		(("Spawners", "title"),
		("COMING SOON!", "label"))]
		

def perform(level, box, options):
	start = time.time()
	print(start)
	if options["Custom Loot Table"] == '':
		lootTable = defaultLootTables[options["Default Loot Table"]]+".json"
	else:
		lootTable = options["Custom Loot Table"]
		
	if (options["Loot Table Seed"] == 0) or (options["Loot Table Seed"] == ''):
		lootSeed = 0
	else:
		lootSeed = options["Loot Table Seed"]
		
	applyBlank = options["Only apply to empty chests"]
	
	checkChests=[]
	tcount=0
	ecount=0
	icount=0
	for (chunk, slices, point) in level.getChunkSlices(box):
		for t in chunk.TileEntities:				
			cx = t["x"].value
			cy = t["y"].value
			cz = t["z"].value	
			id = t["id"].value	
			if ((cx,cy,cz) in box) and (id == "Chest") and (cx,cy,cz) not in checkChests:
				tcount += 1
				checkChests.append((cx,cy,cz))
				if (applyBlank == True):
					if ("LootTable" in t) and (t["LootTable"] != ""):
						print("Chest @ "+str(cx) + ", " + str(cy) + ", " + str(cz) +" has loot table")
						icount += 1
					else:
						if len(t["Items"]) == 0:
							newte = createChest(lootTable,lootSeed,cx,cy,cz)
							chunk.TileEntities.remove(t)
							chunk.TileEntities.append(newte)
							ecount += 1
							print("Chest @ "+str(cx) + ", " + str(cy) + ", " + str(cz) +" set with "+ lootTable)
							chunk.dirty = True
						else:
							print("Chest @ "+str(cx) + ", " + str(cy) + ", " + str(cz) +" has items")
							icount += 1
				else:
					newte = createChest(lootTable,lootSeed,cx,cy,cz)
					chunk.TileEntities.remove(t)
					chunk.TileEntities.append(newte)
					ecount += 1
					print("Chest @ "+str(cx) + ", " + str(cy) + ", " + str(cz) +" set with "+ lootTable)
					chunk.dirty = True
		
	end = time.time()
	finalTime = end - start
	print("This operation took " + str(end) +" on " + str(tcount) +" chests")
	print("There were " + str(ecount) + " chests updated and " + str(icount) + " ignored")
	
	
def createChest(lootTable, lootSeed, cx, cy, cz):
	if (lootSeed == 0):
		lootSeed = random.getrandbits(32)
	newte = TileEntity.Create("Chest")
	newte["Items"] = TAG_List()
	newte["LootTable"] = TAG_String(lootTable)
	newte["LootTableSeed"] = TAG_Long(lootSeed)
	newte["x"] = TAG_Int(cx)
	newte["y"] = TAG_Int(cy)
	newte["z"] = TAG_Int(cz)
	return newte