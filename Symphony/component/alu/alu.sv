module alu_module (
  input wire [3:0] opecode,
  input wire [31:0] arg_a,
  input wire [31:0] arg_b,
  output reg [31:0] out = 32'h0
);

reg [31:0] cmp_out = 32'h0;

always @(*) begin
  case (opecode)
    4'h0: out <= ~(arg_a & arg_b);
    4'h1: out <= arg_a | arg_b;
    4'h2: out <= arg_a & arg_b;
    4'h3: out <= ~(arg_a | arg_b);
    4'h4: out <= arg_a + arg_b;
    4'h5: out <= arg_a - arg_b;
    4'h6: out <= arg_a ^ arg_b;
    4'h7: out <= arg_a << arg_b;
    4'h8: out <= arg_a >> arg_b;
    4'h9: out <= arg_a >>> arg_b;
    4'ha: begin
      cmp_out[0] <= $unsigned(arg_a) == $unsigned(arg_b);
      cmp_out[1] <= $unsigned(arg_a) < $unsigned(arg_b);
      cmp_out[2] <= $signed(arg_a) < $signed(arg_b);
      cmp_out[31:3] <= 'h0;
      out <= cmp_out;
    end
    default: out <= 32'h0;
  endcase
end
endmodule