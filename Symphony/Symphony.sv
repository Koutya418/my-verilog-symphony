`include "./component/alu/alu.sv"
`include "./component/ram/ram.sv"
`include "./component/ram/pram.sv"
`include "./component/cond/cond.sv"
`include "./component/ram/register_file.sv"
`include "./component/counter/counter.sv"
`include "./component/decoder/decoder.sv"

module Symphony(
  input wire clk,
  input wire start_flag,
  input wire [31:0] io_input,
  output reg input_flag,
  output reg [31:0] io_output,
  output reg output_flag
);

wire s_flag;
wire [31:0] inst_bus;
wire [31:0] inst_addr;
wire [3:0] opecode;
wire [1:0] mode;
wire [3:0] arg_a_addr;
wire [3:0] arg_b_addr;
wire [3:0] dest_addr;
wire imm_flag;
wire [15:0] imm_value;
wire [31:0] alu_out;
wire cond_out;
wire [31:0] load8_out;
wire [31:0] load16_out;
wire [31:0] load32_out;
wire [31:0] pload_out;
wire [31:0] arg_a_port;
wire [31:0] arg_b_port;
reg store_flag = 'h0;
reg [31:0] arg_a_bus = 32'h0;
reg [31:0] arg_b_bus = 32'h0;
reg dest_flag = 'h0;
reg [31:0] dest_bus = 32'h0;
reg [31:0] ram_out = 32'h0;
reg [31:0] i_o_out = 32'h0;
reg [31:0] return_bus = 32'h0;
reg jmp_flag = 'h0;

wire [31:0] spdebug_wire;
wire [31:0] spdebug_value;
wire [31:0] flags_value;

reg all_true = 'h1;

counter_module counter(
  .clk(clk && start_flag),
  .w_f(jmp_flag),
  .w_v(return_bus),
  .count(inst_addr),
  .s_flag(s_flag)
);

ram_module ram(
  .clk(clk),
  .s_flag(s_flag),
  .inst_flag(all_true),
  .load8_flag(all_true),
  .load16_flag(all_true),
  .load32_flag(all_true),
  .store8_flag((opecode == 4'h4) && (mode == 2'h3)),
  .store16_flag((opecode == 4'h5) && (mode == 2'h3)),
  .store32_flag((opecode == 4'h6) && (mode == 2'h3)),
  .inst_addr(inst_addr),
  .load8_addr(arg_b_bus),
  .load16_addr(arg_b_bus),
  .load32_addr(arg_b_bus),
  .store8_addr(arg_b_bus),
  .store16_addr(arg_b_bus),
  .store32_addr(arg_b_bus),
  .store8_value(arg_a_bus),
  .store16_value(arg_a_bus),
  .store32_value(arg_a_bus),
  .inst_port(inst_bus),
  .load8_port(load8_out),
  .load16_port(load16_out),
  .load32_port(load32_out),
  .spdebug_addr(spdebug_wire),
  .spdebug_value(spdebug_value)
);

pram_module pram(
  .clk(clk),
  .s_flag(s_flag),
  .load_flag(all_true),
  .store_flag((opecode == 4'h7) && (mode == 2'h3)),
  .load_addr(arg_b_bus),
  .store_addr(arg_b_bus),
  .store_value(arg_a_bus),
  .load_port(pload_out)
);

decoder_module decoder(
  .clk(clk),
  .inst(inst_bus),
  .mode(mode),
  .imm_flag(imm_flag),
  .opecode(opecode),
  .dest_addr(dest_addr),
  .arg_a_addr(arg_a_addr),
  .arg_b_addr(arg_b_addr),
  .imm_value(imm_value)
);

register_file_module register_file(
  .clk(clk),
  .s_flag(s_flag),
  .arg_a_flag(all_true),
  .arg_a_addr(arg_a_addr),
  .arg_a_port(arg_a_port),
  .arg_b_flag(all_true),
  .arg_b_addr(arg_b_addr),
  .arg_b_port(arg_b_port),
  .store_flag(dest_flag),
  .store_addr(dest_addr),
  .store_value(return_bus),
  .spdebug_port(spdebug_wire),
  .flags_debug_port(flags_value)
);

alu_module alu(
  .opecode(opecode),
  .arg_a(arg_a_bus),
  .arg_b(arg_b_bus),
  .out(alu_out)
);

cond_module cond(
  .flags(arg_a_bus),
  .condition(opecode),
  .result(cond_out)
);

always @(*) begin
  arg_a_bus <= arg_a_port;
  if (imm_flag) begin
    arg_b_bus[15:0] <= imm_value;
    arg_b_bus[31:16] <= 16'h0;
  end else begin
    arg_b_bus <= arg_b_port;
  end

  case (mode)
    2'h0: begin
      return_bus <= i_o_out;
      ram_out <= 32'h0;
      jmp_flag <= 'h0;
      case (opecode)
        4'h1: begin
          dest_flag <= 'h1;
          input_flag <= 'h1;
          output_flag <= 'h0;
          i_o_out <= io_input;
          io_output <= 32'h0;
        end
        4'h2: begin
          dest_flag <= 'h0;
          input_flag <= 'h0;
          output_flag <= 'h1;
          io_output <= arg_b_bus;
          i_o_out <= 32'h0;
        end
        4'h7: begin
          dest_flag <= 'h1;
          input_flag <= 'h0;
          output_flag <= 'h0;
          i_o_out <= inst_addr;
        end
        default: begin
          dest_flag <= 'h0;
          input_flag <= 'h0;
          output_flag <= 'h0;
          i_o_out <= 32'h0;
        end
      endcase
    end
    2'h1: begin
      return_bus <= alu_out;
      dest_flag <= 'h1;
      input_flag <= 'h0;
      output_flag <= 'h0;
      io_output <= 32'h0;
      ram_out <= 32'h0;
      jmp_flag <= 'h0;
    end
    2'h2: begin
      return_bus <= arg_b_bus;
      jmp_flag <= cond_out;
      dest_flag <= 'h0;
      input_flag <= 'h0;
      output_flag <= 'h0;
      io_output <= 32'h0;
      ram_out <= 32'h0;
    end
    2'h3: begin
      input_flag <= 'h0;
      output_flag <= 'h0;
      io_output <= 32'h0;
      jmp_flag <= 'h0;
        case (opecode)
          4'h0: ram_out <= load8_out;
          4'h1: ram_out <= load16_out;
          4'h2: ram_out <= load32_out;
          4'h3: ram_out <= pload_out;
          default: ram_out <= 32'h0;
        endcase
        case (opecode)
          4'h0: dest_flag <= 'h1;
          4'h1: dest_flag <= 'h1;
          4'h2: dest_flag <= 'h1;
          4'h3: dest_flag <= 'h1;
          4'h4: dest_flag <= 'h0;
          4'h5: dest_flag <= 'h0;
          4'h6: dest_flag <= 'h0;
          4'h7: dest_flag <= 'h0;
          default: dest_flag <= 'h0;
        endcase
        return_bus <= ram_out;
      end
    default: begin
      return_bus <= 32'h0;
      ram_out <= 32'h0;
      jmp_flag <= 'h0;
      dest_flag <= 'h0;
      input_flag <= 'h0;
      output_flag <= 'h0;
      i_o_out <= 32'h0;
      io_output <= 32'h0;
    end
  endcase
end

endmodule