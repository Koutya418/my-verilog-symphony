module counter_module (
  input wire clk,
  input wire w_f,
  input wire [31:0] w_v,
  output reg [31:0] count = 32'h0,
  output reg s_flag = 'h0
);

reg [1:0] c = 2'h0;

always @(posedge clk) begin
  c <= c + 1;
  if (w_f && (c == 2'h1)) begin
    count <= w_v;
  end else if(c == 2'h1) begin
    count <= count + 32'h4;
  end
  if (c == 2'h0) begin
    s_flag <= 'h1;
  end else begin
    s_flag <= 'h0;
  end
end

endmodule

module counter_varclock_module (
  input wire clk,
  input wire w_f,
  input wire [31:0] w_v,
  output reg [31:0] count = 32'h0
);

reg [1:0] c = 2'h0;

always @(posedge clk) begin
  c <= c + 2'h1;
  if (w_f && (c == 2'h0)) begin
    count <= w_v;
  end else if(c == 2'h0) begin
    count <= count + 32'h4;
  end
end

endmodule