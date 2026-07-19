import cocotb, logging, random
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge
from cocotb.types import LogicArray

class hanoi_test:
  def __init__(self, disk_num):
    self.disk_num = disk_num
    self.tower = [[], [], []]
    self.spare = 0
    self.source = 1
    self.dest = 2
    self.magnet = False
    self.crane_pos = 0
    self.crane_head = 0
    self.input_num = 0

  def test_gen(self):
    gen_tower = [0,1,2]
    self.source = gen_tower.pop(random.randint(0,2))
    self.dest = gen_tower.pop(random.randint(0,1))
    self.spare = gen_tower.pop()
    for i in reversed(range(self.disk_num)):
      self.tower[self.source].append(i)

  def magnet_ope(self):
    self.magnet = not self.magnet
    if self.magnet:
      assert len(self.tower[self.crane_pos]) != 0, f"{self.crane_pos}のタワーにはディスクがありません"
      self.crane_head = self.tower[self.crane_pos].pop()
    else:
      if len(self.tower[self.crane_pos]) > 0:
        assert self.tower[self.crane_pos][-1] > self.crane_head, f"{self.tower[self.crane_pos][-1]}の上に{self.crane_head}を乗せる事は出来ません"
      self.tower[self.crane_pos].append(self.crane_head)

  def crane_ope(self, num):
    self.crane_pos = num
  
  def clear_check(self):
    return len(self.tower[self.dest]) > (self.disk_num - 1)
  
  def start_input(self):
    result = None
    match self.input_num:
      case 0:
        result = self.disk_num - 1
      case 1:
        result = self.source
      case 2:
        result = self.dest
      case 3:
        result = self.spare
    self.input_num += 1
    assert result is not None, "これ以上の入力を要求することは出来ません"
    return result
  
  def show_tower(self):
    return self.tower

@cocotb.test()
async def Symphony_test(dut):
  logger = logging.getLogger("cocotb.Symphony_test")
  hanoi_case = hanoi_test(4)
  hanoi_case.test_gen()
  dut.clk.value = 0
  dut.io_input.value = hanoi_case.start_input()
  await Timer(1, unit="ns")
  dut.clk.value = 1
  await Timer(1, unit="ns")
  dut.clk.value = 0
  await Timer(1, unit="ns")
  dut.start_flag.value = 1
  for i in range(10000):
    dut.clk.value = 0
    await Timer(1, unit="ns")
    dut.clk.value = 1
    await Timer(1, unit="ns")
    if i % 4 == 2  and dut.input_flag.value:
      dut.io_input.value = hanoi_case.start_input()
    elif i % 4 == 0:
      dut.io_input.value = 0
    if i % 4 == 2  and dut.output_flag.value:
      out = dut.io_output.value
      match out:
        case 5:
          hanoi_case.magnet_ope()
          logger.info(hanoi_case.show_tower())
        case _:
          hanoi_case.crane_ope(out)
      if hanoi_case.clear_check():
        break