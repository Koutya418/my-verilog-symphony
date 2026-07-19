module register_file_module #(
  parameter data_width = 32,
  parameter addr_width = 16
)(
  input wire clk,
  input wire s_flag,
  input wire arg_a_flag,
  input wire [3:0] arg_a_addr,
  output reg [31:0] arg_a_port = 32'h0,
  input wire arg_b_flag,
  input wire [3:0] arg_b_addr,
  output reg [31:0] arg_b_port = 32'h0,
  input wire store_flag,
  input wire [3:0] store_addr,
  input wire [31:0] store_value,
  output reg [31:0] spdebug_port = 32'h0,
  output reg [31:0] flags_debug_port = 32'h0
);

integer i;
reg [data_width-1:0] register_array [addr_width-1:0];

initial begin
    for (i = 0; i < addr_width; i = i + 1) begin
        register_array[i] = 32'h0;
    end
end

always @(negedge clk) begin
  if (arg_a_flag && (arg_a_addr != 4'h0)) begin
    arg_a_port <= register_array[arg_a_addr];
  end else begin
    arg_a_port <= 32'h0;
  end
  if (arg_b_flag && (arg_b_addr != 4'h0)) begin
    arg_b_port <= register_array[arg_b_addr];
  end else begin
    arg_b_port <= 32'h0;
  end
end

always @(posedge s_flag) begin
  if (store_flag) begin
    register_array[store_addr] <= store_value;
  end
end

always @(*) begin
 spdebug_port <= register_array[14];
 flags_debug_port <= register_array[15];
end

endmodule