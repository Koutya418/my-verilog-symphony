module ram_module #(
  parameter data_width = 8,
  parameter addr_width = 1024
)(
  input wire clk,
  input wire s_flag,
  input wire inst_flag,
  input wire load8_flag,
  input wire load16_flag,
  input wire load32_flag,
  input wire store8_flag,
  input wire store16_flag,
  input wire store32_flag,
  input wire [31:0] inst_addr,
  input wire [31:0] load8_addr,
  input wire [31:0] load16_addr,
  input wire [31:0] load32_addr,
  input wire [31:0] store8_addr,
  input wire [31:0] store16_addr,
  input wire [31:0] store32_addr,
  input wire [31:0] store8_value,
  input wire [31:0] store16_value,
  input wire [31:0] store32_value,
  input wire [31:0] spdebug_addr,
  output reg [31:0] spdebug_value,
  output reg [31:0] inst_port = 32'h0,
  output reg [31:0] load8_port = 32'h0,
  output reg [31:0] load16_port = 32'h0,
  output reg [31:0] load32_port = 32'h0
);

reg [$clog2(addr_width) - 1:0] inst_mask_addr = 'h0;
reg [$clog2(addr_width) - 1:0] load8_mask_addr = 'h0;
reg [$clog2(addr_width) - 1:0] load16_mask_addr = 'h0;
reg [$clog2(addr_width) - 1:0] load32_mask_addr = 'h0;
reg [$clog2(addr_width) - 1:0] store8_mask_addr = 'h0;
reg [$clog2(addr_width) - 1:0] store16_mask_addr = 'h0;
reg [$clog2(addr_width) - 1:0] store32_mask_addr = 'h0;

reg [data_width - 1:0] ram_block [addr_width - 1:0];

reg [$clog2(addr_width) - 1:0] sp_mask_addr = 'h0;

integer i;

initial begin
  for (i = 0; i < addr_width; i = i + 1) begin
      ram_block[i] = 8'h0;
  end
  $readmemh("program.hex", ram_block);
end

always @(*) begin
  sp_mask_addr <= spdebug_addr & (addr_width - 1);
  spdebug_value[7:0] <= ram_block[sp_mask_addr + 3];
  spdebug_value[15:8] <= ram_block[sp_mask_addr + 2];
  spdebug_value[23:16] <= ram_block[sp_mask_addr + 1];
  spdebug_value[31:24] <= ram_block[sp_mask_addr];
  inst_mask_addr <= inst_addr & (addr_width - 1);
  load8_mask_addr <= load8_addr & (addr_width - 1);
  load16_mask_addr <= load16_addr & (addr_width - 1);
  load32_mask_addr <= load32_addr & (addr_width - 1);
  store8_mask_addr <= store8_addr & (addr_width - 1);
  store16_mask_addr <= store16_addr & (addr_width - 1);
  store32_mask_addr <= store32_addr & (addr_width - 1);
end

always @(negedge clk) begin
  if (inst_flag) begin
    inst_port[7:0] <= ram_block[inst_mask_addr + 3];
    inst_port[15:8] <= ram_block[inst_mask_addr + 2];
    inst_port[23:16] <= ram_block[inst_mask_addr + 1];
    inst_port[31:24] <= ram_block[inst_mask_addr];
  end else begin
    inst_port <= 32'h0;
  end
  if (load8_flag) begin
    load8_port[7:0] <= ram_block[load8_mask_addr];
    load8_port[15:8] <= 8'h0;
    load8_port[23:16] <= 8'h0;
    load8_port[31:24] <= 8'h0;
  end else begin
    load8_port <= 32'h0;
  end
  if (load16_flag) begin
    load16_port[7:0] <= ram_block[load16_mask_addr + 1];
    load16_port[15:8] <= ram_block[load16_mask_addr];
    load16_port[23:16] <= 8'h0;
    load16_port[31:24] <= 8'h0;
  end else begin
    load16_port <= 32'h0;
  end
  if (load32_flag) begin
    load32_port[7:0] <= ram_block[load32_mask_addr + 3];
    load32_port[15:8] <= ram_block[load32_mask_addr + 2];
    load32_port[23:16] <= ram_block[load32_mask_addr + 1];
    load32_port[31:24] <= ram_block[load32_mask_addr];
  end else begin
    load32_port <= 32'h0;
  end
end

always @(posedge s_flag) begin
  if (store8_flag) begin
    ram_block[store8_mask_addr] <= store8_value[7:0];
  end
  if (store16_flag) begin
    ram_block[store16_mask_addr + 1] <= store16_value[7:0];
    ram_block[store16_mask_addr] <= store16_value[15:8];
  end
  if (store32_flag) begin
    ram_block[store32_mask_addr + 3] <= store32_value[7:0];
    ram_block[store32_mask_addr + 2] <= store32_value[15:8];
    ram_block[store32_mask_addr + 1] <= store32_value[23:16];
    ram_block[store32_mask_addr] <= store32_value[31:24];
  end
end
endmodule