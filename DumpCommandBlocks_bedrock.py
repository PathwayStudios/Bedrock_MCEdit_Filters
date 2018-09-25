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
# TexelElf: http://elemanser.com/filters.html


from pymclevel import TAG_Byte, TAG_Int, TAG_Compound, TAG_String
import mcplatform

sorts = {"Y, X, Z":(1,0,2), "Y, Z, X":(1,2,0),"X, Y, Z":(0,1,2), "Z, Y, X":(2,1,0), "X, Z, Y":(0,2,1), "Z, X, Y":(2,0,1)}

inputs = (
	("Operation:",("Dump Command Blocks","Import Command Block Dump")),
	("Sort command blocks by:",tuple(sorted(sorts.keys()))),
	("Clear and prevent output tracking on import:",True),
	("Reset Success Count on import:",True),
	("Dump only commands containing: (\"None\" to dump all)",("string","value=None")),
	("File path:",("string","value=None")),
	)

displayName = "Bedrock - Dump Command Blocks"

def indent(ct):
	return "".join(["\t" for i in xrange(ct)])

def strexplode(command):
	coms = []
	if not command:
		return coms
	i = 0
	line = ""
	inquote = 0
	for c in xrange(len(command)):
		if command[c] == "{":
			if inquote:
				line += command[c]
			else:
				if line:
					coms.append(indent(i)+line+"\n")
					line = ""
				coms.append(indent(i)+"{\n")
				i += 1
		elif command[c] == "}":
			if inquote:
				line += command[c]
			else:
				if line:
					coms.append(indent(i)+line+"\n")
					line = ""
				i -= 1
				line += command[c]
		elif command[c] == "[":
			if inquote:
				line += command[c]
			else:
				if line:
					coms.append(indent(i)+line+"\n")
					line = ""
				coms.append(indent(i)+"[\n")
				i += 1
		elif command[c] == "]":
			if inquote:
				line += command[c]
			else:
				if line:
					coms.append(indent(i)+line+"\n")
					line = ""
				i -= 1
				line += command[c]
		elif command[c] == '\"':
			if command[c-1] != "\\":
				inquote ^= 1
			line += command[c]
		elif command[c] == ",":
			if inquote:
				line += command[c]
			else:
				coms.append(indent(i)+line+",\n")
				line = ""
		else:
			line += command[c]
	else:
		if line:
			coms.append(indent(i)+line+"\n")
	return coms

def strcollapse(lines):
	commands = []
	command = ""
	id = ""
	comfound = False
	for l in lines:
		if not l:
			continue
		if l[0] == ";":
			continue
		if l[0] == "#":
			if id:
				commands.append((id,command.decode("unicode-escape")))
			id = l[1:].rstrip().decode("unicode-escape")
			command = ""
			comfound = True
		else:
			if comfound:
				comfound = False
				command += l.lstrip().rstrip() + " "
			else:
				command += l.lstrip().rstrip()
	else:
		commands.append((id,command.decode("unicode-escape")))
	
		
	return commands

def perform(level, box, options):
	op = options["Operation:"]
	cleartrack = options["Clear and prevent output tracking on import:"]
	reset = options["Reset Success Count on import:"]
	filterstr = options["Dump only commands containing: (\"None\" to dump all)"]
	filepath = options["File path:"]
	order = sorts[options["Sort command blocks by:"]]
	if op == "Dump Command Blocks":
		if filterstr == "None":
			filtercoms = False
		else:
			filtercoms = True
		commands = []
		for (chunk, _, _) in level.getChunkSlices(box):
			for e in chunk.TileEntities:
				x = e["x"].value
				y = e["y"].value
				z = e["z"].value
				if (x,y,z) in box:
					if "CommandBlock" in e["id"].value:
						if "CustomName" in e:
							name = e["CustomName"].value.encode("unicode-escape")
						else:
							name = "@"
						type = level.blockAt(x,y,z)
						direction = level.blockDataAt(x,y,z)
						if "powered" in e:
							powered = e["powered"].value
						else:
							powered = 0
						if "auto" in e:
							auto = e["auto"].value
						else:
							auto = 0
						if "conditionMet" in e:
							conditionMet = e["conditionMet"].value
						else:
							conditionMet = 0
						if filtercoms:
							if e["Command"].value.find(filterstr) != -1:
								commands.append(((x,y,z),type,direction,powered,auto,conditionMet,name,e["Command"].value.encode("unicode-escape")))
						else:
							commands.append(((x,y,z),type,direction,powered,auto,conditionMet,name,e["Command"].value.encode("unicode-escape")))
		if not commands:
			raise Exception("ERROR: No command blocks exist within the selection!")
		commands.sort(key=lambda s: (s[0][order[0]], s[0][order[1]], s[0][order[2]]))
		outputlines = []
		for (coords,type, direction, powered, auto, conditionMet, comname, command) in commands:
			outputlines.append(u"#%d,%d,%d|%d|%d|%d|%d|%d:%s\n" % (coords[0],coords[1],coords[2],type,direction,powered,auto,conditionMet,comname))
			if "{" in command:
				mdatapos = command.find("{")
				outputlines.append(command[:mdatapos]+"\n")
				outputlines+=strexplode(command[mdatapos:])
			else:
				outputlines.append(str(command)+"\n")
			outputlines.append("\n")

		if filepath == "None":
			text_file = mcplatform.askSaveFile(mcplatform.lastSchematicsDir or mcplatform.schematicsDir, "Save Dumped Text File...", "", "Text File\0*.txt\0\0", ".txt")
			if text_file == None:
				print "ERROR: No filename provided!"
				return
		else:
			text_file = filepath
		file = open(text_file,"w")
		file.writelines(outputlines)
		file.close()
	else:
		if filepath == "None":
			text_file = mcplatform.askOpenFile(title="Select a Dumped Text File...", schematics=False)
			if text_file == None:
				print "ERROR: No filename provided!"
				return
		else:
			text_file = filepath
		file = open(text_file, 'rb')
		filearray = file.readlines()
		file.close()
		blocks = strcollapse(filearray)
		for idstr, command in blocks:
			precoordstr, name = idstr.split(":",1)
			if "|" in precoordstr:
				coordstr, bdata = precoordstr.split("|",1)
			else:
				coordstr = precoordstr
				bdata = None
			cx, cy, cz = coordstr.split(",")
			if bdata:
				parts = bdata.split("|")
				if len(parts) != 5:
					type = 137
					direction = 0
					powered = 0
					auto = 0
					conditionMet = 0
				else:
					type = int(parts[0])
					direction = int(parts[1])
					powered = int(parts[2])
					auto = int(parts[3])
					conditionMet = int(parts[4])
			else:
				type = 137
				direction = 0
				powered = 0
				auto = 0
				conditionMet = 0
			cx = int(cx)
			cy = int(cy)
			cz = int(cz)
			level.setBlockAt(cx, cy, cz, type)
			level.setBlockDataAt(cx, cy, cz, direction)
			chunk = level.getChunk(cx>>4, cz>>4)
			ent = level.tileEntityAt(cx,cy,cz)
			if ent != None:
				if cleartrack:
					ent["TrackOutput"] = TAG_Byte(0)
					if "LastOutput" in ent:
						del ent["LastOutput"]
				if reset:
					ent["SuccessCount"] = TAG_Int(0)
				ent["powered"] = TAG_Byte(powered)
				ent["auto"] = TAG_Byte(auto)
				ent["conditionMet"] = TAG_Byte(conditionMet)
				ent["CustomName"] = TAG_String(name)
				ent["Command"] = TAG_String(command)
				chunk.dirty = True
			else:
				cmd = TAG_Compound()
				cmd["id"] = TAG_String("CommandBlock")
				cmd["x"] = TAG_Int(cx)
				cmd["y"] = TAG_Int(cy)
				cmd["z"] = TAG_Int(cz)
				if cleartrack:
					cmd["TrackOutput"] = TAG_Byte(0)
				cmd["powered"] = TAG_Byte(powered)
				cmd["auto"] = TAG_Byte(auto)
				cmd["conditionMet"] = TAG_Byte(conditionMet)
				cmd["CustomName"] = TAG_String(name)
				cmd["Command"] = TAG_String(command)
				try:
					chunk.TileEntities.remove(cmd)
				except ValueError:
					print ("missing command block at "+str(cx)+","+str(cy)+","+str(cz))
				chunk.TileEntities.append(cmd)
				chunk.dirty = True
