module decoder_module (
  input wire clk,
  input wire [31:0] inst,
  output wire [1:0] mode,
  output wire imm_flag,
  output wire [3:0] opecode,
  output wire [3:0] dest_addr,
  output wire [3:0] arg_a_addr,
  output wire [3:0] arg_b_addr,
  output wire [15:0] imm_value
);

assign mode = inst[30:29];
assign imm_flag = inst[28];
assign opecode = inst[27:24];
assign dest_addr = inst[23:20];
assign arg_a_addr = inst[19:16];
assign arg_b_addr = inst[11:8];
assign imm_value = inst[15:0];

endmodule