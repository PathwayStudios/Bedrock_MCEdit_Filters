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

# ORIGINAL VERISION BY:
# Feel free to modify and use this filter however you wish. If you do,
# please give credit to SethBling.
# http://youtube.com/SethBling

from pymclevel import TAG_Compound, TAG_Int, TAG_Short, TAG_Byte, TAG_String, TAG_Float, TAG_List
import string


VERSION = 1.0

Professions = {
	"Farmer (brown - 0)": 0,
	"Fisherman (brown - 0)": 1,
	"Shepherd (brown - 0)": 2,
	"Fletcher (brown - 0)": 3,
	"Librarian (white - 1)": 4,
	"Cartographer (white - 1)": 5,
	"Cleric (purple - 2)": 6,
	"Armorer (black apron - 3)": 7,
	"Weapon Smith (black apron - 3)": 8,
	"Tool Smith (black apron - 3)": 9,
	"Butcher (white apron - 4)": 10,
	"Leather Worker (white apron - 4)": 11,
	"Detect Wool":12
	}

professionsLookup = {
	0:"farmer",
	1:"fisherman",
	2:"shepherd",
	3:"fletcher",
	4:"librarian",
	5:"cartographer",
	6:"cleric",
	7:"armorer",
	8:"weaponsmith",
	9:"toolsmith",
	10:"butcher",
	11:"leatherworker",
	12:"detect"
	}

variantLookup = {
	0:0,
	1:0,
	2:0,
	3:0,
	4:1,
	5:1,
	6:2,
	7:3,
	8:3,
	9:3,
	10:4,
	11:4,
	12:5
}
	
ProfessionKeys = ()
for key in Professions.keys():
	ProfessionKeys = ProfessionKeys + (key,)
	

inputs = [(("Trade", "title"),
		("Custom Name", ("string", "width=250")),
		("Custom Name Visible", False),	
		("Custom Component Groups", ("string", "width=250")),
		("Reward XP", 1),	
		("Profession", ProfessionKeys),
		("Stop Trade Upgrade", True),
		("Max Health", True),		
		("Unlimited Trades", True),),
	
		(("Help", "title"),
		("How to setup chest:\n"
		"	Top Row: Buy A\n"
		"	Middle Row: Buy B (optional)\n"
		"	Bottom Row: Sell\n"
		"*Each column is a different trade*\n\n"
		"In order to use Detect Wool, you must place a wool block over the chest\n"
		"Below are the assignments:\n"
		"	White -> Farmer\n"
		"	Orange -> Fisherman\n"
		"	Magenta -> Shepherd\n"
		"	Light Blue -> Fletcher\n" 
		"	Yellow -> Librarian\n"
		"	Lime -> Cartographer\n"
		"	Pink -> Cleric\n"
		"	Gray -> Armorer\n"
		"	Light Gray -> Weapon Smith\n"
		"	Cyan -> Tool Smith\n"
		"	Purple -> Butcher\n"
		"	Blue -> Leather Worker\n"
		, "label"))]

displayName = "Bedrock - Create Shops"


def perform(level, box, options):
	rewardXP = options["Reward XP"]
	stopTrade = options["Stop Trade Upgrade"]
	unlimited = options["Unlimited Trades"]
	maxHealth = options["Max Health"]	
	customName = options["Custom Name"]
	customNameVisible = options["Custom Name Visible"]
	componentGroups = options["Custom Component Groups"]
	
	for (x, y, z) in box.positions:
		if level.blockAt(x, y, z) == 54:
			dontConvert = 1
			if Professions[options["Profession"]] == 12:
				if level.blockAt(x, y+1, z) == 35:					
					bdata = level.blockDataAt(x,y+1,z)
					if bdata < 12:
						variant = int(variantLookup[bdata])
						professionGUI = professionsLookup[bdata]
						dontConvert = 0
					level.setBlockAt(x, y+1, z, 0)
				else:
					dontConvert = 1						
			else:
				variant = int(variantLookup[Professions[options["Profession"]]])
				professionGUI = professionsLookup[Professions[options["Profession"]]]
				dontConvert = 0
			if dontConvert == 0:
				createShop(level, x, y, z, stopTrade, variant, unlimited, customName, customNameVisible, maxHealth, professionGUI, rewardXP, componentGroups)
			else:
				print("what?")
def createShop(level, x, y, z, stopTrade, variant, unlimited, customName, customNameVisible, maxHealth, professionGUI, rewardXP, componentGroups):
	chest = level.tileEntityAt(x, y, z)
	if chest == None:
		return

	priceList = {}
	priceListB = {}
	saleList = {}

	for item in chest["Items"]:
		slot = item["Slot"].value
		if slot >= 0 and slot <= 8:
			priceList[slot] = item
			del priceList[slot]["Slot"]
			priceList[slot]["id"] = TAG_Short(int(priceList[slot]["id"].value))
		elif slot >= 9 and slot <= 17:
			priceListB[slot-9] = item
			del priceListB[slot-9]["Slot"]
			priceListB[slot-9]["id"] = TAG_Short(int(priceListB[slot-9]["id"].value))			
		elif slot >= 18 and slot <= 26:
			saleList[slot-18] = item
			del saleList[slot-18]["Slot"]
			saleList[slot-18]["id"] = TAG_Short(int(saleList[slot-18]["id"].value))				

	villager = TAG_Compound()
	villager["OnGround"] = TAG_Byte(1)	
	villager["Air"] = TAG_Short(300)
	villager["Armor"] = TAG_List()
	for i in range(3):
		armorData = TAG_Compound()
		armorData["Count"] = TAG_Byte(0)
		armorData["Damage"] = TAG_Short(0)
		armorData["id"] = TAG_Short(0)
		villager["Armor"].append(armorData)	
	villager["AttackTime"] = TAG_Short(0)
	villager["BodyRot"] = TAG_Float(-132.68496704101562)
	villager["ChestItems"] = TAG_List()
	for i in range(7):
		chestData = TAG_Compound()
		chestData["Count"] = TAG_Byte(0)
		chestData["Damage"] = TAG_Short(0)
		chestData["id"] = TAG_Short(0)
		villager["ChestItems"].append(chestData)	
	villager["Chested"] = TAG_Byte(0)
	villager["Color"] = TAG_Byte(0)
	villager["DeathTime"] = TAG_Short(0)
	villager["FallDistance"] = TAG_Float(0.0)
	villager["Fire"] = TAG_Short(0)
	villager["HurtTime"] = TAG_Short(0)
	villager["Invulnerable"] = TAG_Byte(0)
	villager["Variant"] = TAG_Int(variant)
	villager["Riches"] = TAG_Int(0)
	villager["Persistent"] = TAG_Byte(1)
	villager["id"] = TAG_String("Villager")
	villager["CustomName"] = TAG_String(customName)
	villager["Pos"] = TAG_List()
	villager["Pos"].append(TAG_Float(x + 0.5))
	villager["Pos"].append(TAG_Float(y))
	villager["Pos"].append(TAG_Float(z + 0.5))
	villager["definitions"] = TAG_List()
	villager["definitions"].append(TAG_String(u'+minecraft:villager'))
	villager["definitions"].append(TAG_String("+" + professionGUI))	

	villager["Rotation"] = TAG_List()
	villager["Rotation"].append(TAG_Float(0))
	villager["Rotation"].append(TAG_Float(0))
	
	if customNameVisible:
		villager["CustomName"] = TAG_String(customName)
		villager["CustomNameVisible"] = TAG_Byte(1)
	else:
		villager["CustomName"] = TAG_String(customName)
		villager["CustomNameVisible"] = TAG_Byte(0)

	if maxHealth:
		attributes = TAG_Compound()
		attributes["Name"] = TAG_String(u'minecraft:health')
		attributes["Base"] = TAG_Float(1024.0)
		attributes["Current"] = TAG_Float(1024.0)
		attributes["Max"] = TAG_Float(1024.0)
		villager["Attributes"] = TAG_List()
		villager["Attributes"].append(attributes)
	else:
		attributes = TAG_Compound()
		attributes["Name"] = TAG_String(u'minecraft:health')
		attributes["Base"] = TAG_Float(20.0)
		attributes["Current"] = TAG_Float(20.0)
		attributes["Max"] = TAG_Float(20.0)
		villager["Attributes"] = TAG_List()
		villager["Attributes"].append(attributes)

	villager["Offers"] = TAG_Compound()
	villager["Offers"]["Recipes"] = TAG_List()
	for i in range(9):
		if (i in priceList or i in priceListB) and i in saleList:
			offer = TAG_Compound()
			if unlimited:
				offer["uses"] = TAG_Int(-2000000000)
				offer["maxUses"] = TAG_Int(2000000000)
			else:
				offer["uses"] = TAG_Int(0)
				offer["maxUses"] = TAG_Int(1)
			offer["rewardExp"] = TAG_Byte(rewardXP)
			if i in priceList:
				offer["buyA"] = priceList[i]
			if i in priceListB:
				if i in priceList:
					offer["buyB"] = priceListB[i]
				else:
					offer["buyA"] = priceListB[i]
			
			offer["sell"] = saleList[i]
			villager["Offers"]["Recipes"].append(offer)

	if stopTrade:
		villager["TradeTier"] = TAG_Int(-2000000000)
	
	if componentGroups:
		componentGroups = string.split(componentGroups,",")
		for i in componentGroups:
			villager["definitions"].append(TAG_String("+" + i))	
			
			

	level.setBlockAt(x, y, z, 0)
	
	chunk = level.getChunk(x / 16, z / 16)
	chunk.Entities.append(villager)
	chunk.TileEntities.remove(chest)
	chunk.dirty = True
