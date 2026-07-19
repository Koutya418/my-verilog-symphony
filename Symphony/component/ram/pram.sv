module pram_module #(
  parameter data_width = 8,
  parameter addr_width = 1024
)(
  input wire clk,
  input wire s_flag,
  input wire load_flag,
  input wire store_flag,
  input wire [31:0] load_addr,
  input wire [31:0] store_addr,
  input wire [31:0] store_value,
  output reg [31:0] load_port = 32'h0
);

integer i;
reg [$clog2(addr_width) - 1:0] load_mask_addr = 'h0;
reg [$clog2(addr_width) - 1:0] store_mask_addr = 'h0;
reg [data_width-1:0] ram_block [addr_width-1:0];

initial begin
  for (i = 0; i < addr_width; i = i + 1) begin
      ram_block[i] = 8'h0;
  end
end

always @(*) begin
  load_mask_addr <= load_addr & (addr_width - 1);
  store_mask_addr <= store_addr & (addr_width - 1);
end

always @(negedge clk) begin
  if (load_flag) begin
    load_port[7:0] <= ram_block[load_mask_addr + 3];
    load_port[15:8] <= ram_block[load_mask_addr + 2];
    load_port[23:16] <= ram_block[load_mask_addr + 1];
    load_port[31:24] <= ram_block[load_mask_addr];
  end else begin
    load_port <= 32'h0;
  end
end

always @(posedge s_flag) begin
  if (store_flag) begin
    ram_block[store_mask_addr + 3] <= store_value[7:0];
    ram_block[store_mask_addr + 2] <= store_value[15:8];
    ram_block[store_mask_addr + 1] <= store_value[23:16];
    ram_block[store_mask_addr] <= store_value[31:24];
  end
end
endmodule