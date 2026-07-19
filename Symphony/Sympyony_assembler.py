import os, re
cwd = os.getcwd()
program_path = "/Symphony/program.txt"
real_instruction_path = "/Symphony/real_instruction.txt"
hex_path = "/Symphony/program.hex"

instruction_list = {
  "nop":{
    "mode": 0,
    "opecode": 0,
    "arg_a": [],
    "arg_b": [],
    "dest": [],
  },
  "in":{
    "mode": 0,
    "opecode": 1,
    "arg_a": [],
    "arg_b": [],
    "dest": ["reg"],
  },
  "out":{
    "mode": 0,
    "opecode": 2,
    "arg_a": [],
    "arg_b": ["reg", "imm", "label"],
    "dest": [],
  },
  "keyboard":{
    "mode": 0,
    "opecode": 3,
    "arg_a": [],
    "arg_b": [],
    "dest": ["reg"],
  },
  "screen":{
    "mode": 0,
    "opecode": 4,
    "arg_a": ["reg"],
    "arg_b": ["reg", "imm", "label"],
    "dest": [],
  },
  "time_0":{
    "mode": 0,
    "opecode": 5,
    "arg_a": [],
    "arg_b": [],
    "dest": ["reg"],
  },
  "time_1":{
    "mode": 0,
    "opecode": 6,
    "arg_a": [],
    "arg_b": [],
    "dest": ["reg"],
  },
  "counter":{
    "mode": 0,
    "opecode": 7,
    "arg_a": [],
    "arg_b": [],
    "dest": ["reg"],
  },
  "nand":{
    "mode": 1,
    "opecode": 0,
    "arg_a": ["reg"],
    "arg_b": ["reg", "imm", "label"],
    "dest": ["reg"],
  },
  "or":{
    "mode": 1,
    "opecode": 1,
    "arg_a": ["reg"],
    "arg_b": ["reg", "imm", "label"],
    "dest": ["reg"],
  },
  "and":{
    "mode": 1,
    "opecode": 2,
    "arg_a": ["reg"],
    "arg_b": ["reg", "imm", "label"],
    "dest": ["reg"],
  },
  "nor":{
    "mode": 1,
    "opecode": 3,
    "arg_a": ["reg"],
    "arg_b": ["reg", "imm", "label"],
    "dest": ["reg"],
  },
  "add":{
    "mode": 1,
    "opecode": 4,
    "arg_a": ["reg"],
    "arg_b": ["reg", "imm", "label"],
    "dest": ["reg"],
  },
  "sub":{
    "mode": 1,
    "opecode": 5,
    "arg_a": ["reg"],
    "arg_b": ["reg", "imm", "label"],
    "dest": ["reg"],
  },
  "xor":{
    "mode": 1,
    "opecode": 6,
    "arg_a": ["reg"],
    "arg_b": ["reg", "imm", "label"],
    "dest": ["reg"],
  },
  "lsl":{
    "mode": 1,
    "opecode": 7,
    "arg_a": ["reg"],
    "arg_b": ["reg", "imm", "label"],
    "dest": ["reg"],
  },
  "lsr":{
    "mode": 1,
    "opecode": 8,
    "arg_a": ["reg"],
    "arg_b": ["reg", "imm", "label"],
    "dest": ["reg"],
  },
  "asr":{
    "mode": 1,
    "opecode": 9,
    "arg_a": ["reg"],
    "arg_b": ["reg", "imm", "label"],
    "dest": ["reg"],
  },
  "cmp":{
    "mode": 1,
    "opecode": 10,
    "arg_a": ["reg"],
    "arg_b": ["reg", "imm", "label"],
    "dest": ["flags"],
  },
  "je":{
    "mode": 2,
    "opecode": 1,
    "arg_a": ["flags"],
    "arg_b": ["imm", "label"],
    "dest": [],
  },
  "jb":{
    "mode": 2,
    "opecode": 2,
    "arg_a": ["flags"],
    "arg_b": ["imm", "label"],
    "dest": [],
  },
  "jbe":{
    "mode": 2,
    "opecode": 3,
    "arg_a": ["flags"],
    "arg_b": ["imm", "label"],
    "dest": [],
  },
  "jl":{
    "mode": 2,
    "opecode": 4,
    "arg_a": ["flags"],
    "arg_b": ["imm", "label"],
    "dest": [],
  },
  "jle":{
    "mode": 2,
    "opecode": 5,
    "arg_a": ["flags"],
    "arg_b": ["imm", "label"],
    "dest": [],
  },
  "jmp":{
    "mode": 2,
    "opecode": 8,
    "arg_a": ["flags"],
    "arg_b": ["reg", "imm", "label"],
    "dest": [],
  },
  "jne":{
    "mode": 2,
    "opecode": 9,
    "arg_a": ["flags"],
    "arg_b": ["imm", "label"],
    "dest": [],
  },
  "jae":{
    "mode": 2,
    "opecode": 10,
    "arg_a": ["flags"],
    "arg_b": ["imm", "label"],
    "dest": [],
  },
  "ja":{
    "mode": 2,
    "opecode": 11,
    "arg_a": ["flags"],
    "arg_b": ["imm", "label"],
    "dest": [],
  },
  "jge":{
    "mode": 2,
    "opecode": 12,
    "arg_a": ["flags"],
    "arg_b": ["imm", "label"],
    "dest": [],
  },
  "jg":{
    "mode": 2,
    "opecode": 13,
    "arg_a": ["flags"],
    "arg_b": ["imm", "label"],
    "dest": [],
  },
  "load_8":{
    "mode": 3,
    "opecode": 0,
    "arg_a": [],
    "arg_b": ["reg", "imm"],
    "dest": ["reg"],
  },
  "load_16":{
    "mode": 3,
    "opecode": 1,
    "arg_a": [],
    "arg_b": ["reg", "imm"],
    "dest": ["reg"],
  },
  "load_32":{
    "mode": 3,
    "opecode": 2,
    "arg_a": [],
    "arg_b": ["reg", "imm"],
    "dest": ["reg"],
  },
  "pload":{
    "mode": 3,
    "opecode": 3,
    "arg_a": [],
    "arg_b": ["reg", "imm"],
    "dest": ["reg"],
  },
  "store_8":{
    "mode": 3,
    "opecode": 4,
    "arg_a": ["reg"],
    "arg_b": ["reg", "imm"],
    "dest": [],
  },
  "store_16":{
    "mode": 3,
    "opecode": 5,
    "arg_a": ["reg"],
    "arg_b": ["reg", "imm"],
    "dest": [],
  },
  "store_32":{
    "mode": 3,
    "opecode": 6,
    "arg_a": ["reg"],
    "arg_b": ["reg", "imm"],
    "dest": [],
  },
  "pstore":{
    "mode": 3,
    "opecode": 7,
    "arg_a": ["reg"],
    "arg_b": ["reg", "imm"],
    "dest": [],
  },
}

mnemonic_list = {
  "nop":{
    "mode": 0,
    "opecode": 0,
    "macro":False,
    "operands": [],
  },
  "in":{
    "mode": 0,
    "opecode": 1,
    "macro":False,
    "operands": ["dest"],
  },
  "out":{
    "mode": 0,
    "opecode": 2,
    "macro":False,
    "operands": ["arg_b"],
  },
  "keyboard":{
    "mode": 0,
    "opecode": 3,
    "macro":False,
    "operands": ["dest"],
  },
  "screen":{
    "mode": 0,
    "opecode": 4,
    "macro":False,
    "operands": ["arg_a", "arg_b"],
  },
  "time_0":{
    "mode": 0,
    "opecode": 5,
    "macro":False,
    "operands": ["dest"],
  },
  "time_1":{
    "mode": 0,
    "opecode": 6,
    "macro":False,
    "operands": ["dest"],
  },
  "counter":{
    "mode": 0,
    "opecode": 7,
    "macro":False,
    "operands": ["dest"],
  },
  "nand":{
    "mode": 1,
    "opecode": 0,
    "macro":False,
    "operands": ["dest", "arg_a", "arg_b"],
  },
  "or":{
    "mode": 1,
    "opecode": 1,
    "macro":False,
    "operands": ["dest", "arg_a", "arg_b"],
  },
  "and":{
    "mode": 1,
    "opecode": 2,
    "macro":False,
    "operands": ["dest", "arg_a", "arg_b"],
  },
  "nor":{
    "mode": 1,
    "opecode": 3,
    "macro":False,
    "operands": ["dest", "arg_a", "arg_b"],
  },
  "add":{
    "mode": 1,
    "opecode": 4,
    "macro":False,
    "operands": ["dest", "arg_a", "arg_b"],
  },
  "sub":{
    "mode": 1,
    "opecode": 5,
    "macro":False,
    "operands": ["dest", "arg_a", "arg_b"],
  },
  "xor":{
    "mode": 1,
    "opecode": 6,
    "macro":False,
    "operands": ["dest", "arg_a", "arg_b"],
  },
  "lsl":{
    "mode": 1,
    "opecode": 7,
    "macro":False,
    "operands": ["dest", "arg_a", "arg_b"],
  },
  "lsr":{
    "mode": 1,
    "opecode": 8,
    "macro":False,
    "operands": ["dest", "arg_a", "arg_b"],
  },
  "asr":{
    "mode": 1,
    "opecode": 9,
    "macro":False,
    "operands": ["dest", "arg_a", "arg_b"],
  },
  "cmp":{
    "mode": 1,
    "opecode": 10,
    "macro":False,
    "operands": ["arg_a", "arg_b"],
  },
  "je":{
    "mode": 2,
    "opecode": 1,
    "macro":False,
    "operands": ["arg_b"],
  },
  "jb":{
    "mode": 2,
    "opecode": 2,
    "macro":False,
    "operands": ["arg_b"],
  },
  "jbe":{
    "mode": 2,
    "opecode": 3,
    "macro":False,
    "operands": ["arg_b"],
  },
  "jl":{
    "mode": 2,
    "opecode": 4,
    "macro":False,
    "operands": ["arg_b"],
  },
  "jle":{
    "mode": 2,
    "opecode": 5,
    "macro":False,
    "operands": ["arg_b"],
  },
  "jmp":{
    "mode": 2,
    "opecode": 8,
    "macro":False,
    "operands": ["arg_b"],
  },
  "jne":{
    "mode": 2,
    "opecode": 9,
    "macro":False,
    "operands": ["arg_b"],
  },
  "jae":{
    "mode": 2,
    "opecode": 10,
    "macro":False,
    "operands": ["arg_b"],
  },
  "ja":{
    "mode": 2,
    "opecode": 11,
    "macro":False,
    "operands": ["arg_b"],
  },
  "jge":{
    "mode": 2,
    "opecode": 12,
    "macro":False,
    "operands": ["arg_b"],
  },
  "jg":{
    "mode": 2,
    "opecode": 13,
    "macro":False,
    "operands": ["arg_b"],
  },
  "load_8":{
    "mode": 3,
    "opecode": 0,
    "macro":False,
    "operands": ["dest", "arg_b"],
  },
  "load_16":{
    "mode": 3,
    "opecode": 1,
    "macro":False,
    "operands": ["dest", "arg_b"],
  },
  "load_32":{
    "mode": 3,
    "opecode": 2,
    "macro":False,
    "operands": ["dest", "arg_b"],
  },
  "pload":{
    "mode": 3,
    "opecode": 3,
    "macro":False,
    "operands": ["dest", "arg_b"],
  },
  "store_8":{
    "mode": 3,
    "opecode": 4,
    "macro":False,
    "operands": ["arg_b", "arg_a"],
  },
  "store_16":{
    "mode": 3,
    "opecode": 5,
    "macro":False,
    "operands": ["arg_b", "arg_a"],
  },
  "store_32":{
    "mode": 3,
    "opecode": 6,
    "macro":False,
    "operands": ["arg_b", "arg_a"],
  },
  "pstore":{
    "mode": 3,
    "opecode": 7,
    "macro":False,
    "operands": ["arg_b", "arg_a"],
  },
  "mov":{
    "macro":True,
    "operands": ["dest", "arg_b"],
    "operations": [
      {
        "operation": "or",
        "operand": ["dest", "zr", "arg_b"],
      },
    ]
  },
  "neg":{
    "macro":True,
    "operands": ["dest", "arg_b"],
    "operations": [
      {
        "operation": "sub",
        "operand": ["dest", "zr", "arg_b"],
      },
    ]
  },
  "not":{
    "macro":True,
    "operands": ["dest", "arg_b"],
    "operations": [
      {
        "operation": "nor",
        "operand": ["dest", "zr", "arg_b"],
      },
    ]
  },
  "push":{
    "macro":True,
    "operands": ["arg_a"],
    "operations": [
      {
        "operation": "sub",
        "operand": ["sp", "sp", "4"],
      },
      {
        "operation": "store_32",
        "operand": ["[sp]", "arg_a"],
      },
    ]
  },
  "pop":{
    "macro":True,
    "operands": ["dest"],
    "operations": [
      {
        "operation": "load_32",
        "operand": ["dest", "[sp]"]
      },
      {
        "operation": "add",
        "operand": ["sp", "sp", "4"],
      },
    ]
  },
  "call":{
    "macro":True,
    "operands": ["arg_b"],
    "operations": [
      {
        "operation": "counter",
        "operand": ["flags"],
      },
      {
        "operation": "add",
        "operand": ["flags", "flags", "20"],
      },
      {
        "operation": "push",
        "operand": ["flags"]
      },
      {
        "operation": "jmp",
        "operand": ["arg_b"],
      },
    ]
  },
  "ret":{
    "macro":True,
    "operands": [],
    "operations": [
      {
        "operation": "pop",
        "operand": ["flags"],
      },
      {
        "operation": "jmp",
        "operand": ["flags"],
      },
    ]
  },
}

reg_list = {
  "zr": 0,
  "r1": 1,
  "r2": 2,
  "r3": 3,
  "r4": 4,
  "r5": 5,
  "r6": 6,
  "r7": 7,
  "r8": 8,
  "r9": 9,
  "r10": 10,
  "r11": 11,
  "r12": 12,
  "r13": 13,
  "sp": 14,
  "flags": 15,
}

def word_type_check(word):
  result = None
  if type(word) == int:
    result = "number"
  elif word.isdigit():
    result = "number"
  elif word in mnemonic_list:
    result = "mnemonic"
  elif re.sub(r'\[|\]', '',word) in reg_list:
    result = "register"
  elif word[-1] == ":":
    result = "jmp_label"
  else:
    result = "label"
  return result

def mnemonic_decoder(line):
  result = []
  mnemonic = line[0]
  mnemonic_data = mnemonic_list.get(mnemonic)
  if not mnemonic_data.get("macro"):
    result.append(line)
  else:
    args = []
    if len(line) > 1:
      args += line[1:]
    arg_dict = {}
    operands = mnemonic_data.get("operands")
    operations = mnemonic_data.get("operations")
    for i, operand in enumerate(operands): #arg_a, arg_b, destをキーにオペランドの辞書を作っておく
      arg_dict[operand] = args[i]
    for operation in operations:
      inst = []
      inst.append(operation.get("operation"))
      for operand in operation.get("operand"):
        if operand in arg_dict: #辞書に登録されている場合に値を使う事で、元の命令のオペランドを置き換え後の命令のオペランドに渡す
          inst.append(arg_dict.get(operand))
        else:
          inst.append(operand)
      result += mnemonic_decoder(inst) #置き換え後の命令も実命令になるまで再帰を行う
  return result

def instruction_decoder(line):
  result = "0"
  mnemonic = line[0]
  mnemonic_data = mnemonic_list.get(mnemonic)
  mnemonic_arg_list = mnemonic_data.get("operands")
  arg_table = {}
  for i, arg in enumerate(mnemonic_arg_list):
    arg_type = []
    arg_value = ""
    match word_type_check(line[1 + i]):
      case "number":
        arg_type = "imm"
      case "register":
        arg_type = "reg"
      case _:
        pass
    if arg_type == "reg":
      arg_table[arg] = {"value":re.sub(r'\[|\]', '', line[1 + i]), "type":arg_type}
    else:
      arg_table[arg] = {"value":line[1 + i], "type":arg_type}
  inst_data = instruction_list.get(mnemonic)
  result += '{:02b}'.format(inst_data.get("mode"))
  dest_value, _ = register_decoder("dest", arg_table, inst_data)
  arg_a_value, _ = register_decoder("arg_a", arg_table, inst_data)
  arg_b_value, imm_flag = register_decoder("arg_b", arg_table, inst_data)
  dest_bin = '{:04b}'.format(dest_value)
  arg_a_bin = '{:04b}'.format(arg_a_value)
  arg_b_bin = '{:016b}'.format(arg_b_value) if imm_flag else '0000{:04b}00000000'.format(arg_b_value)
  imm_flag = str(int(imm_flag))
  result += imm_flag
  result += '{:04b}'.format(inst_data.get("opecode"))
  result += dest_bin + arg_a_bin + arg_b_bin
  return result

def register_decoder(arg_key, arg_table, inst_data):
  value = 0
  imm_flag = False
  inst_type_list = inst_data.get(arg_key)
  if set(inst_type_list) & set(list(reg_list.keys())):
    value = reg_list.get(list(set(inst_type_list) & set(list(reg_list.keys())))[0])
  else:
    if arg_key in arg_table:
      arg_type = arg_table.get(arg_key).get("type")
      if arg_type in inst_type_list:
        match arg_type:
          case "imm":
            imm_flag = True
            value = int(arg_table.get(arg_key).get("value"))
          case "reg":
            value = reg_list.get(arg_table.get(arg_key).get("value"))
  return value, imm_flag


inst_list = []
label_list = {}
label_use_list = {}
hex_inst_list = []
bin_inst_list = []
real_inst_list = []
with open(cwd + program_path, encoding="utf-8") as f:
  lines = []
  for line in f.readlines():
    if line.rstrip():
      lines.append(line.rstrip().replace(',', '').split(" "))
  for line in lines: #全ての命令を実命令に置き換え、ラベルのリストも作っておく。
    for word in line:
      match word_type_check(word):
        case "number":
          pass
        case "mnemonic":
          inst_list += mnemonic_decoder(line)
        case "register":
          pass
        case "jmp_label":
          label_list[word[:-1]] = len(inst_list)
        case "label":
          pass
        case _:
          pass
  
  for i, inst in enumerate(inst_list): #ラベルが使用されている行のリストの作成
    label = ""
    label = list(inst & label_list.keys())[0] if len(list(inst & label_list.keys())) > 0 else ""
    if label:
      if label in label_use_list:
        label_use_list.get(label).append(i)
      else:
        label_use_list[label] = [i]

  for inst in inst_list:
    real_inst_list.append(' '.join(inst))

  with open(cwd + real_instruction_path, encoding="utf-8", mode='w') as m:
    m.write('\n'.join(real_inst_list))

  for label, addr_list in label_use_list.items(): #ラベルのリテラルへの置き換え
    for addr in addr_list:
      inst_list[addr][inst_list[addr].index(label)] = label_list.get(label) * 4

  for inst in inst_list:
    bin_inst_list.append(instruction_decoder(inst))

  for inst in bin_inst_list:
    hex_inst = ""
    for i in range(8):
      hex_inst += '{:0x}'.format(int(inst[i * 4:i * 4 + 4], 2))
    hex_inst_list.append(hex_inst[0:2])
    hex_inst_list.append(hex_inst[2:4])
    hex_inst_list.append(hex_inst[4:6])
    hex_inst_list.append(hex_inst[6:8])

  with open(cwd + hex_path, encoding="utf-8", mode='w') as h:
    h.write('\n'.join(hex_inst_list))