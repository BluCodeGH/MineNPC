from random import randint
try:
  import pyperclip
  pyp = True
except ImportError:
  pyp = False
  print("Copy paste not supported, reverting to text-based output.")

class Speaker:
  def setup(self): #Setup the scoreboard objectives, etc.
    self.comm = "summon falling_block ~ ~1.5 ~ {Block:stone,Time:1,Passengers:[{id:falling_block,Block:redstone_block,Time:1,Passengers:[{id:falling_block,Block:activator_rail,Time:1},{id:commandblock_minecart,Command:gamerule commandBlockOutput false},"
    self.comm += "{id:commandblock_minecart,Command:scoreboard objectives add rightClick stat.talkedToVillager},"
    self.comm += "{id:commandblock_minecart,Command:scoreboard objectives add speech dummy},"
    self.comm += "{id:commandblock_minecart,Command:scoreboard objectives add speechMax dummy},"
    self.comm += "{id:commandblock_minecart,Command:scoreboard objectives add qs dummy},"
    self.comm += "{id:commandblock_minecart,Command:scoreboard objectives add awayTime dummy},"
    self.comm += "{id:commandblock_minecart,Command:scoreboard teams add NPC},"
    self.comm += "{id:commandblock_minecart,Command:scoreboard teams option NPC collisionRule never},"
    self.comm += "{id:commandblock_minecart,Command:setblock ~ ~-3 ~-1 minecraft:repeating_command_block 2 replace {auto:1b,Command:/execute @e[tag=talks,score_speech_min=1] ~ ~ ~ execute @r[r=7] ~ ~ ~ /scoreboard players add @e[tag=talks,score_speech_min=1,r=7] speech 1}},"
    self.comm += "{id:commandblock_minecart,Command:setblock ~ ~-3 ~-2 minecraft:chain_command_block 2 replace {auto:1b,Command:execute @e[tag=talks,score_speech_min=1] ~ ~ ~ scoreboard players add @e[tag=talks,r=0,score_speech_min=1] awayTime 1}},"
    self.comm += "{id:commandblock_minecart,Command:setblock ~ ~-3 ~-3 minecraft:chain_command_block 2 replace {auto:1b,Command:/execute @a ~ ~ ~ execute @e[tag=talks,r=9] ~ ~ ~ scoreboard players set @e[tag=talks,r=0] awayTime 0}},"
    self.comm += "{id:commandblock_minecart,Command:setblock ~ ~-3 ~-4 minecraft:chain_command_block 2 replace {auto:1b,Command:/execute @e[tag=talks,score_awayTime_min=300] ~ ~ ~ scoreboard players operation @e[tag=talks,r=0] speech = @e[tag=talks,r=0] speechMax}},"
    self.comm += "{id:commandblock_minecart,Command:setblock ~ ~-3 ~-5 minecraft:chain_command_block 2 replace {auto:1b,Command:/execute @e[tag=talks,score_awayTime_min=300] ~ ~ ~ scoreboard players set @e[tag=talks,r=0] awayTime 0}},"
    self.comm += "{id:commandblock_minecart,Command:setblock ~ ~-3 ~-6 minecraft:chain_command_block 2 replace {auto:1b,Command:/execute @a[score_rightClick_min=1] ~ ~ ~ /scoreboard players set @e[r=4,score_speech=0] speech 1}},"
    self.comm += "{id:commandblock_minecart,Command:setblock ~ ~-3 ~-7 minecraft:chain_command_block 2 replace {auto:1b,Command:/scoreboard players set @a[score_rightClick_min=1] rightClick 0}},"
    self.comm += "{id:commandblock_minecart,Command:setblock ~ ~-3 ~-8 minecraft:chain_command_block 2 replace {auto:1b,Command:/effect @e[tag=talks] minecraft:slowness 10 225 true}},"
    self.comm += "{id:commandblock_minecart,Command:setblock ~ ~-3 ~-9 minecraft:chain_command_block 2 replace {auto:1b,Command:/execute @e[tag=talks] ~ ~ ~ execute @r[r=7] ~ ~ ~ /scoreboard players add @e[tag=talks,r=7] speech 0}},"
    self.comm += "{id:commandblock_minecart,Command:setblock ~ ~-3 ~-10 minecraft:chain_command_block 2 replace {auto:1b,Command:/scoreboard players add @a qs 0}},"
    self.comm += '{id:commandblock_minecart,Command:setblock ~ ~-2 ~-1 minecraft:standing_sign 8 replace {Text1:"{\\\\"text\\\\":\\\\"MineNPC Main\\\\",\\\\"bold\\\\":true,\\\\"clickEvent\\\\":{\\\\"action\\\\":\\\\"run_command\\\\",\\\\"value\\\\":\\\\"fill ~ ~ ~ ~ ~-1 ~-9 air\\\\"}}",Text2:"{\\\\"text\\\\":\\\\"By BluCode\\\\",\\\\"color\\\\":\\\\"blue\\\\",\\\\"clickEvent\\\\":{\\\\"action\\\\":\\\\"run_command\\\\",\\\\"value\\\\":\\\\"fill ~ ~ ~ ~ ~-1 ~-9 air\\\\"}}",Text3:"{\\\\"text\\\\":\\\\"Right-Click to\\\\",\\\\"color\\\\":\\\\"red\\\\",\\\\"clickEvent\\\\":{\\\\"action\\\\":\\\\"run_command\\\\",\\\\"value\\\\":\\\\"fill ~ ~ ~ ~ ~-1 ~-9 air\\\\"}}",Text4:"{\\\\"text\\\\":\\\\"Remove\\\\",\\\\"color\\\\":\\\\"red\\\\",\\\\"clickEvent\\\\":{\\\\"action\\\\":\\\\"run_command\\\\",\\\\"value\\\\":\\\\"fill ~ ~ ~ ~ ~-1 ~-9 air\\\\"}}"}},'
    self.comm += '{id:commandblock_minecart,Command:tellraw @a ["",{"text":"Successfully setup speech for all NPCs in this world.","color":"blue"}]},'
    self.comm += "{id:commandblock_minecart,Command:setblock ~ ~1 ~ command_block 0 0 {auto:1,Command:fill ~ ~-4 ~ ~ ~ ~ air}},{id:commandblock_minecart,Command:kill @e[type=commandblock_minecart,r=1]}]}]}"
    return self.comm

  def speak(self, file):
    lines, already = self.getData(file) #Get the needed data from the tab to the left.
    self.comm = ""
    if already: #Gen 1 cmd at same place as before, if possible.
      self.comm += "execute @e[name=" + self.name +",tag=mark] ~ ~-1 ~ "
    self.framework() #Add the base 1 cmd framework.

    self.duration = 1 #setup vars
    self.tick = 1
    old_dur = -1
    z = 0
    branches = []
    toReset = []
    nextRepeat = False
    notAuto = False

    for line in lines: #main loop
      line = line.lstrip()

      line, old_dur, nextRepeat, notAuto, dv, block, auto = self.checks(line, old_dur, z, nextRepeat, notAuto) #check for block, data value and auto

      if line[0] != "/": #plain text
        length, line = line.split(" ", 1)
        self.comm += self.base(1, z, block, dv, auto) + 'tellraw @a[r=7] ["",{"text":"[' + self.name + '] ' + self.all(line) + '","color":"green"}]}},'
        self.tick += int(float(length) * 20)

      else:
        if line == "/end": #stop speaking by setting the speak score past the last line's score
          self.comm += self.base(0, z, block, dv, auto) + "scoreboard players set " + self.base(2) + " speech |f}}," #|f is the final self.tick + 1

        elif line[:4] == "/qs ": #verify the player(s) have talked to the right people already.
          _, num, newName = line.split(" ", 2)
          self.comm += self.base(1, z, block, dv, auto) + "testfor @a[score_qs=" + str(int(num) - 1) + "]}},"
          z += 1
          self.comm += self.base(1, z, " chain_command_block", " 10 ", auto) + 'tellraw @a[r=7] ["",{"text":"[' + self.name + '] You should probably go talk to ' + newName + ' first.","color":"green"}]}},'
          z += 1
          self.comm += self.base(0, z, " chain_command_block", " 10 ", auto) + "scoreboard players set @e[tag=talks,name=" + self.name + "] speech |f}}," #|f is the final self.tick + 1

        elif line[:4] == "/qss": #set everyone's qs score.
          _, num = line.split()
          less = str(int(num) - 1)
          self.comm += self.base(1, z, block, dv, auto) + 'scoreboard players set @a[score_qs=' + less + ',score_qs_min=' + less + '] qs ' + num + '}},'

        elif line[:7] == "/branch": #give the player a choice.
          data = line.split(" | ")
          before = data[0][8:]
          data = data[1:]
          branches.append([self.tick, 1, len(data), 0, []]) #[the tick for each new branch to begin at, the # of branches that are done, total # of branches to setup, the max duration, list of z values of blockdata cmds to be updated]
          options = ',{"text":"'
          for i, option in enumerate(data):
            extra = ""
            if i + 1 == len(data):
              extra += "?"
            #json magyk. |num1num2 will be the inverse of the z difference between the marker and the place to setblock the redstone block.
            options += '[' + option + ']' + extra + ' ","color":"red","bold":true,"clickEvent":{"action":"run_command","value":"/execute @e[tag=mark,name=' + self.name + '] ~ ~ ~ setblock ~ ~-1 ~-|' + str(len(branches)) + str(i) + ' redstone_block"}},{"text":"'
          options = options[:-10].replace("|" + str(len(branches)) + "0", str(z + 2)) #first location to set redstone block

          self.tick -= 1
          self.comm += self.base(1, z, block, dv, auto) + 'tellraw @a[r=7] ["",{"text":"[' + self.name + '] ' + before + ' ","color":"green"}' + options + ']}},' #main tellraw command
          z += 1
          self.comm += self.base(0, z, " chain_command_block", dv, auto) + "scoreboard players set " + self.base(2) + " speech |f}}," #|f is the final self.tick + 1. This prevents speech until the player has chosen an option.
          self.tick += 1
          z += 1

          self.comm += "{id:commandblock_minecart,Command:setblock ~ ~-2 ~-" + str(z) + " command_block 2 replace {Command:scoreboard players set @e[tag=talks,name=" + self.name + "] speech " + str(self.tick) + "}}," #these activate when the player chooses. reset speech score.
          self.comm += "{id:commandblock_minecart,Command:setblock ~ ~-2 ~-" + str(z + 1) + " chain_command_block 2 replace {auto:1b,Command:blockdata ~ ~-1 ~-|a" + str(len(branches)) + "0 {auto:1b}}}," #blockdata the repeat cmd that activates after the branch to auto
          branches[-1][4].append(z + 1) #add the previous cmd's z to the list

          nextRepeat = True #make the next command a needs redstone repeat, as it will be the first command in the branch.
          notAuto = True

        elif line[:5] == "/next": #move to the next option in the branch or end the branch.
          if branches[-1][1] < branches[-1][2]: #the number of branches done < the total to do.
            if block == " repeating_command_block": #make sure repeats aren't auto
              auto = "0"
            else:
              auto = "1"

            self.comm += self.base(0, z, block, dv, auto) + "scoreboard players set " + self.base(2) + " speech |t" + str(len(branches)) + "}}," #|tnum1 is the tick the longest branch ends at. finish off the previous branch.
            z += 1

            if block == " repeating_command_block": #make space so two repeats aren't powered with 1 redstone block.
              z += 1

            self.comm = self.comm.replace("|" + str(len(branches)) + str(branches[-1][1]), str(z)) #next redstone block location

            self.comm += "{id:commandblock_minecart,Command:setblock ~ ~-2 ~-" + str(z) + " command_block 2 replace {Command:scoreboard players set @e[tag=talks,name=" + self.name + "] speech " + str(branches[-1][0]) + "}}," #set the speak score
            self.comm += "{id:commandblock_minecart,Command:setblock ~ ~-2 ~-" + str(z + 1) + " chain_command_block 2 replace {auto:1b,Command:blockdata ~ ~-1 ~-|a" + str(len(branches)) + str(branches[-1][1]) + " {auto:1b}}}," #blockdata the repeat
            branches[-1][4].append(z + 1) #add the previous cmd's z to the list

            if self.tick > branches[-1][3]: #update the longest duration if needed
              branches[-1][3] = self.tick

            self.tick = branches[-1][0] #set the tick back to the beginning to reset
            branches[-1][1] += 1 #update setup count

          else: #time to finish the branch
            self.comm += self.base(0, z, block, dv, "1") + "scoreboard players set " + self.base(2) + " speech |t" + str(len(branches)) + "}}," #|tnum1 is the tick the longest branch ends at. finish off the previous branch.

            for i, z2 in enumerate(branches[-1][4]): #update the auto blockdatas
              diff = z + 1 - z2
              self.comm = self.comm.replace("|a" + str(len(branches)) + str(i), str(diff))
            toReset.append(z + 1) #make sure to disable the next block on a reset

            if self.tick < branches[-1][3]: #set self.tick to the longest duration
              self.tick = branches[-1][3]

            self.comm = self.comm.replace("|t" + str(len(branches)), str(self.tick)) #update the |tnums
            self.tick += 1
            branches = branches[:-1] #remove this from branches

          notAuto = True #setup vars
          nextRepeat = True

        elif line[:5] == "/move": #move the entity
          _, direction, blocks, time = line.split()
          time = int(float(time) * 20)
          blocks = int(blocks)
          speed = blocks / time
          if direction == "n":
            direction = " ~ ~ ~-" + str(speed)
          elif direction == "s":
            direction = " ~ ~ ~" + str(speed)
          elif direction == "e":
            direction = " ~" + str(speed) + " ~ ~"
          elif direction == "w":
            direction = " ~-" + str(speed) + " ~ ~"
          else:
            raise ValueError
          selector = '@e[name=' + self.name + ',score_speech_min=' + str(self.tick) + ',score_speech=' + str(self.tick + time) + ']'
          self.comm += self.base(0, z, block, dv, auto) + 'execute ' + selector + " ~ ~ ~ execute @r[r=7] ~ ~ ~ tp " + selector + direction + '}},'

        elif line[:5] == "/wait": #wait
          _, time = line.split()
          self.tick += int(float(time) * 20)
          z -= 1

        else:
          self.comm += self.base(1, z, block, dv, auto) + line + "}}," #run general command
      z += 1

    for i, z2 in enumerate(toReset): #reset the branch-end repeats to not auto
      if i == 0:
        block = " repeating_command_block"
      else:
        block = " chain_command_block"
      self.comm += self.base(0, z, block, " 2 ", "1") + "execute @e[name=" + self.name + ",score_speech_min=" + str(self.tick + 400) + ',score_speech=' + str(self.tick + 400) +'] ~ ~ ~ execute @e[name=' + self.name + ',tag=mark] ~ ~ ~ /blockdata ~ ~-1 ~-' + str(z2) + ' {auto:0b}}},'
      z += 1

    #remove redstone blocks
    self.comm += "{id:commandblock_minecart,Command:setblock ~ ~-3 ~-" + str(z) + " chain_command_block 2 replace {auto:1b,Command:execute @e[name=" +self.name + ",score_speech_min=" + str(self.tick + 400) + ',score_speech=' + str(self.tick + 400) +'] ~ ~ ~ execute @e[tag=mark,name=' +self.name + '] ~ ~ ~ fill ~ ~-1 ~-1 ~ ~-1 ~-|l air 0 replace redstone_block}},'
    z += 1
    #reset speech score
    self.comm += "{id:commandblock_minecart,Command:setblock ~ ~-3 ~-" + str(z) + " chain_command_block 2 replace {auto:1b,Command:execute @e[name=" +self.name + ",score_speech_min=" + str(self.tick + 400) + ',score_speech=' + str(self.tick + 400) +'] ~ ~ ~ scoreboard players set @e[name=' +self.name + ',r=0] speech 0}},'
    #update length and finish tick
    self.comm = self.comm.replace("|l", str(z+1)).replace("|f", str(self.tick))
    #add old tag to old villager and mark
    self.comm += '{id:commandblock_minecart,Command:scoreboard players tag @e[tag=talks,name=' + self.name + '] add old},'
    self.comm += '{id:commandblock_minecart,Command:scoreboard players tag @e[tag=mark,name=' + self.name + '] add old},'
    #summon new villager and mark
    self.comm += '{id:commandblock_minecart,Command:summon villager ~ ~ ~ {CustomName:"' + self.name + '",CustomNameVisible:1,Tags:["talks"],Offers:{Recipes:[]},Profession:' + str(randint(0,4)) + ',Invulnerable:1,PersistenceRequired:1,Silent:1}},'
    self.comm += '{id:commandblock_minecart,Command:summon armor_stand ~ ~-2 ~ {CustomName:"'+ self.name + '",CustomNameVisible:0,Tags:["mark"],Marker:1b,NoGravity:1b,Invisible:1,Invulnerable:1,PersistenceRequired:1}},'
    #setup new villager and kill old
    self.comm += '{id:commandblock_minecart,Command:scoreboard players set @e[tag=talks,tag=!old,name=' + self.name + '] speechMax ' + str(self.tick + 400) + "},"
    self.comm += '{id:commandblock_minecart,Command:scoreboard teams join NPC @e[tag=talks,tag=!old,name=' + self.name + ']},'
    self.comm += '{id:commandblock_minecart,Command:tp @e[tag=talks,tag=!old,name=' + self.name + '] @e[tag=old,tag=talks,rm=1,name=' + self.name + ']},'
    self.comm += '{id:commandblock_minecart,Command:kill @e[tag=old,name=' + self.name + ']},'
    #success tellraw, sign and cleanup
    self.comm += '{id:commandblock_minecart,Command:setblock ~ ~-2 ~-1 minecraft:air 0 replace},'
    self.comm += '{id:commandblock_minecart,Command:setblock ~ ~-2 ~-1 minecraft:standing_sign 8 replace {Text1:"{\\\\"text\\\\":\\\\"MineNPC NPC\\\\",\\\\"bold\\\\":true,\\\\"clickEvent\\\\":{\\\\"action\\\\":\\\\"run_command\\\\",\\\\"value\\\\":\\\\"kill @e[name=' + self.name + ']\\\\"}}",Text2:"{\\\\"text\\\\":\\\\"' + self.name + '\\\\",\\\\"color\\\\":\\\\"blue\\\\",\\\\"clickEvent\\\\":{\\\\"action\\\\":\\\\"run_command\\\\",\\\\"value\\\\":\\\\"kill @e[name=' + self.name + ']\\\\"}}",Text3:"{\\\\"text\\\\":\\\\"Right-Click then\\\\",\\\\"color\\\\":\\\\"red\\\\",\\\\"clickEvent\\\\":{\\\\"action\\\\":\\\\"run_command\\\\",\\\\"value\\\\":\\\\"kill @e[name=' + self.name + ']\\\\"}}",Text4:"{\\\\"text\\\\":\\\\"Break to Remove.\\\\",\\\\"color\\\\":\\\\"red\\\\",\\\\"clickEvent\\\\":{\\\\"action\\\\":\\\\"run_command\\\\",\\\\"value\\\\":\\\\"kill @e[name=' + self.name + ']\\\\"}}"}},'
    self.comm += '{id:commandblock_minecart,Command:tellraw @a ["",{"text":"Successfully implemented speech for ' + self.name + '.","color":"blue"}]},'
    self.comm += "{id:commandblock_minecart,Command:setblock ~ ~1 ~ command_block 0 0 {auto:1,Command:fill ~ ~-3 ~ ~ ~ ~ air}},{id:commandblock_minecart,Command:kill @e[type=commandblock_minecart,r=1]}]}]}"
    return self.comm

  def framework(self):
    self.comm += "summon falling_block ~ ~1.5 ~ {Block:stone,Time:1,Passengers:[{id:falling_block,Block:redstone_block,Time:1,Passengers:[{id:falling_block,Block:activator_rail,Time:1},{id:commandblock_minecart,Command:gamerule commandBlockOutput false},"
    self.comm += "{id:commandblock_minecart,Command:fill ~ ~-3 ~ ~ ~-2 ~-|l air 0 replace repeating_command_block},"
    self.comm += "{id:commandblock_minecart,Command:fill ~ ~-3 ~ ~ ~-2 ~-|l air 0 replace chain_command_block},"
    self.comm += "{id:commandblock_minecart,Command:fill ~ ~-3 ~ ~ ~-2 ~-|l air 0 replace command_block},"

  def getData(self, filename):
    with open(filename, "r") as f:
      text = f.read()
    lines = text.split("\n")
    self.name = lines[0]
    if len(self.name.split()) > 1:
      if self.name.split()[-1] == "e":
        already = True
      self.name = self.name.split(" ", 1)[0]
    else:
      already = False
      with open(filename, "w") as f:
        name = self.name + " e"
        body = "\n".join(lines[1:])
        f.write(name + "\n" + body)
    lines = lines[1:]
    return lines, already

  def checks(self, line, old_dur, z, nextRepeat, notAuto):
    if line[0] == ".": #check if should be a conditional cmd block
      dv = " 10 "
      line = line[1:]
      if old_dur == -1:
        old_dur = self.tick
    else:
      dv = " 2 "
      if old_dur != -1:
        self.tick = old_dur
        old_dur = -1

    if z == 0 or nextRepeat: #check if should be a repeat cmd block
      block = " repeating_command_block"
      nextRepeat = False
    else:
      block = " chain_command_block"

    if notAuto: #check if should be an auto cmd block
      auto = "0"
      notAuto = False
    else:
      auto = "1"

    return line, old_dur, nextRepeat, notAuto, dv, block, auto

  def base(self, t, a=None, b=None, c=None, d=None): #0 for run command, 1 for execute at tag=talks with duration, 2 for reference
    if t == 0:
      return "{id:commandblock_minecart,Command:setblock ~ ~-3 ~-" + str(a) + b + c + "replace {auto:" + d + "b,Command:"
    elif t == 1:
      return "{id:commandblock_minecart,Command:setblock ~ ~-3 ~-" + str(a) + b + c + "replace {auto:" + d + "b,Command:execute @e[name=" + self.name + ",score_speech_min=" + str(self.tick) + ",score_speech=" + str(self.tick) + "] ~ ~ ~ "
    elif t == 2:
      return "@e[name=" + self.name + ",score_speech_min=" + str(self.tick) + ",score_speech=" + str(self.tick) + "]"
    else:
      raise NotImplementedError

  def all(self, s):
    return s.replace("@a", '","color":"green"},{"selector":"@a","color":"green"},{"text":"')

if __name__ == '__main__':
  print("Welcome to MineNPC, a program written with care by BluCode.")
  speaker = Speaker()
  fname = input("Please enter the path to the speech data file, or '\\setup' to \ngenerate a required install for every world: ")
  if fname != "\\setup":
    res = speaker.speak(fname)
  else:
    res = speaker.setup()
  if pyp:
    pyperclip.copy(res)
    print("Copied command to clipboard. Press CTRL+V in a command block to paste it.")
  else:
    print("\n\n" + res)
  input("\n\nPress enter to quit.")
