import sys, getopt
import itertools
import re

def main(argv):
   top_level = ''
   module = ''
   mod_begin_index = ''
   top_mod_indicies = []
   all_mod_ports = []
   missing_ports = []
   write_ports = []
   port_found = 0
   NUM_OF_SLOTS = 0

   #Read arguments from python run
   try:
      opts, args = getopt.getopt(argv,"ht:m:e:",["ifile1=","ifile2=","ifile3="])
   except getopt.GetoptError:
      print ('top_level_adjust.py -t <top_level> -m <module> -e <extension>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('top_level_adjust.py -t <top_level> -m <module> -e <extension>')
         sys.exit()
      elif opt in ("-t", "--ifile1"):
         top_level = arg
      elif opt in ("-m", "--ifile2"):
         module = arg
      elif opt in ("-e", "--ifile3"):
         ext = arg

   fp_top = open(top_level)
   fp_mod = open(module)
   fp_top_modified = open("design_mod.v", 'w+')
   fp_store_mods = open("reconfig_mods.txt",'w+')
   
   #Read the entirety of the top level design and top module designs
   top_list = fp_top.readlines()
   mod_list = fp_mod.readlines()

   #Find the top module name
   for line in mod_list:
      stripped_line = line.strip(' \n\r')
      if "module" in line and ext == 'v':
         mod_name = line.split(' ')[1].replace('_top','')
         #It is known that the top design contains system
         if("system_" not in mod_name):
            mod_name = "system_" + mod_name
         #Need to remove module count from name 
         if "top" not in line and any(i.isdigit() for i in mod_name[-4:]):
            #DEBUG: Tracks the module name 
            #print(mod_name)
            mod_name = mod_name[:-4]
         mod_begin_index = mod_list.index(line)
         #DEBUG - Determine start index for module definition
         #print(mod_begin_index)
      elif ("ENTITY" in line) and (ext == 'vhd'):
         mod_name = line.split(' ')[1].replace('_top','')
         #Remove the last 4 characters since there are multiple modules
         mod_name = mod_name[:-4]
         mod_begin_index = mod_list.index(line)

      #Need to handle case where PORT is not defined same line as a port
      if ext == 'vhd' and "PORT" in line and ";" not in line:
         mod_begin_index += 1

      if ");" in line and ext == 'v':
         mod_end_index = mod_list.index(line)
         if mod_begin_index != '':
            break
      elif (");" == stripped_line) and ext == 'vhd':
         mod_end_index = mod_list.index(line)
         if mod_begin_index != '':
            break
   #Keep an eye on this
   #Might need to remove '-1' or place constraints depeneding on type of file
   #Or make mod_begin 2 instead of 1
   mod_len = mod_end_index - mod_begin_index - 1

   #DEBUG - Determine Module Length
   #print(mod_len)

   #Find the top module name in the top level design
   for line in top_list:
        if mod_name in line.split(' ')[0]:
            test_line = line.split(' ')[0]
            if len(mod_name) >= (len(test_line) - 4):
                #DEBUG - Determine the names of the module instantiations in top level design
                #print(test_line)
                #print(mod_name)
                fp_store_mods.write(line.split(' ')[1])
                top_mod_indicies.append(top_list.index(line))
                NUM_OF_SLOTS = NUM_OF_SLOTS + 1
   #DEBUG - Determine the Module base name
   #print(mod_name)
   #print(top_mod_indicies)
   #print(NUM_OF_SLOTS)
   #print(top_mod_indicies)
   #DEBUG
   #i = 0

   #Find the missing ports in the top level design
   for line in itertools.islice(mod_list,mod_begin_index + 1,mod_end_index):
      if ext == 'v':
         temp_line = line[:-1].replace(",",'').strip(' ')
      else:
         temp_line = line.strip(' ').split(' ')[0]
      #DEBUG
      #if i == 0:
         #print(temp_line.strip(' '))
      for line2 in itertools.islice(top_list,top_mod_indicies[0] + 1, top_mod_indicies[0] + mod_len + 1):
         #DEBUG
         #if i == 0:
         #   print(line2)
         if temp_line in line2:
            port_found = 1
            break
         #Mod length is max length, should quite if module is shorter than max length
         if ");" in line2:
            break;
      #DEBUG
      #i += 1
      if port_found == 0:
         missing_ports.append(temp_line)
      port_found = 0
      all_mod_ports.append(temp_line)

   it = iter(top_list)
   port_found = 0
   printed_ports = 0
   mod_count = 0
   mod_insts = []

   #DEBUG
   print(missing_ports)

   for line in it:
      # Get all the ports available in the top level design for the RM
      # Write everything else in top level design to new file
      if mod_name in line.split(' ')[0]:
         test_line = line.split(' ')[0]
         if len(mod_name) >= (len(test_line) - 4):
            print(line)
            mod_insts.append(line.split(' ', 1)[0])
            fp_top_modified.write(line)
            fp_top_modified.write("(")
            top_mod_ports = next(it).strip('\n')
            top_mod_ports = top_mod_ports.replace("(", '', 1)
            #DEBUG
            #print(top_mod_ports)
            while top_mod_ports[-2:] != ");":
               write_ports.append(top_mod_ports)
               top_mod_ports = next(it).strip('\n')
            write_ports.append(top_mod_ports[:-2] + ',')
            #Put ports in the correct order and add missing ports
            for mod_ports in all_mod_ports:
               for ports in write_ports:
                  if mod_ports in ports:
                     #Check if this is the last port
                     if mod_ports == all_mod_ports[-1]:
                        ports = ports.replace(',', '')
                     fp_top_modified.write(ports + '\n')
                     port_found = 1
                     break
               if port_found == 0:
                  if mod_ports != all_mod_ports[-1]:
                     fp_top_modified.write('        .' + mod_ports + '(' + mod_ports + str(mod_count) + '),\n')
                  else:
                     fp_top_modified.write('        .' + mod_ports + '(' + mod_ports + str(mod_count) + ')\n')
               else:
                  port_found = 0
            del write_ports[:]
            fp_top_modified.write(');\n')
            mod_count += 1
         else:
            fp_top_modified.write(line)
      else:
         if 'wire' in line and not printed_ports:
            for x in range(0,NUM_OF_SLOTS):
               for missing in missing_ports:
                  fp_top_modified.write('  wire ' + missing + str(x) + ';\n')
               fp_top_modified.write('\n')
            printed_ports = 1
         fp_top_modified.write(line)
   
   it = iter(mod_list)
   fp_top_modified.write('\n')
   parameters = []
   in_outputs = []
   count_ports = 0

   #Add black box definitions to the end of the modified file
   if ext == 'v':
      mod_ports = next(it).strip(';\n')
      while count_ports != mod_len:
         if 'parameter' in mod_ports:
            while 'parameter' in mod_ports:
               parameters.append(mod_ports.split(' ',1)[1])
               mod_ports = next(it).strip(';\n')
         if 'output' in mod_ports or 'input' in mod_ports:
            while 'input' in mod_ports or 'output' in mod_ports:
               in_outputs.append(mod_ports.replace("wire", ''))
               count_ports += 1
               mod_ports = next(it).strip(';\n')
         mod_ports = next(it).strip(';\n')
   else:
      while "PORT" not in mod_ports:
         mod_ports = next(it)
      mod_ports = next(it)
      while "END" not in mod_ports:
         port_size = ""
         #Need to add port size to black box definition
         #Remove all non_numeric values
         if "VECTOR" in mod_ports:
            port_size = re.sub("[^0-9]","",mod_ports)
            port_size = "[" + port_size[:-1] + ":" + port_size[len(port_size) - 1] + "] "
         if "IN" in mod_ports:
            mod_ports = mod_ports.strip(' ').split(' ')[0]
            in_outputs.append("input " + port_size + mod_ports)
         elif "OUT" in mod_ports:
            mod_ports = mod_ports.strip(' ').split(' ')[0]
            in_outputs.append("output " + port_size + mod_ports)
         mod_ports = next(it)

   for mod in mod_insts:
      fp_top_modified.write('module ' + mod + '\n')
      if parameters:
         fp_top_modified.write('   #(parameter\n')
         for x in range(0, len(parameters)):
            if x == len(parameters) - 1:
               fp_top_modified.write('      ' + parameters[x] + '\n')
            else:
               fp_top_modified.write('      ' + parameters[x] + ',\n')
         fp_top_modified.write('      )(\n')
      else:
         fp_top_modified.write('       (\n')

      if in_outputs:
         for x in range(0, len(in_outputs)):
            if x == len(in_outputs) - 1:
               fp_top_modified.write('           ' + in_outputs[x] + '\n')
            else:
               fp_top_modified.write('           ' + in_outputs[x] + ',\n')
      fp_top_modified.write(');\n')
      fp_top_modified.write('endmodule\n')

if __name__ == "__main__":
   main(sys.argv[1:])
