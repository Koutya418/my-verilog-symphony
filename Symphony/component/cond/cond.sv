module cond_module(
  input wire [31:0] flags,
  input wire [3:0] condition,
  output reg result = 'h0
);

reg flag = 'h0;

always @(*) begin
  if (flags[2:0] & condition[2:0] != 0) begin
    flag <= 'h1;
  end else begin
    flag <= 'h0;
  end
  result <= condition[3] ^ flag;
end
endmodule