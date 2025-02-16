import "DPI-C" function shortint add_dpi(
  input shortint a,
  input shortint b
);

// Simple counter, only takes the clock as input.
module counter (
    input clk,
    output [15:0] counter
);

  assign counter = cnt;
  reg [15:0] cnt = 0;

  always @(posedge clk) cnt <= cnt + 1;

endmodule

// Simple combinatorial circuit, adds two inputs.
module immediate_plus (
    input  [15:0] a,
    input  [15:0] b,
    output [15:0] out
);

  assign out = a + b;

endmodule

// Simple combinatorial circuit, subtracts two inputs.
module immediate_minus (
    input  [15:0] a,
    input  [15:0] b,
    output [15:0] out
);

  assign out = a - b;

endmodule


// Add inputs using a DPI-C function.
module dpi_plus (
    input  [15:0] a,
    input  [15:0] b,
    output [15:0] out
);

  assign out = add_dpi(a, b);

endmodule

// Add inputs at the next clock cycle.
module clocked_plus (
    input clk,
    input [15:0] a,
    input [15:0] b,
    output [15:0] out
);

  assign out = sum;
  reg [15:0] sum = 0;

  always @(posedge clk) sum <= a + b;

endmodule

// Simple MUX.
module mux_module (
    input [15:0] a,
    input [15:0] b,
    input sel,
    output [15:0] out
);

  assign out = sel ? a : b;

endmodule


// Top module
module top (
    input clk,
    input [15:0] a,
    input [15:0] b,
    input [1:0] sel,
    output [15:0] counter,
    output [15:0] immediate_plus,
    output [15:0] immediate_minus,
    output [15:0] clocked_plus,
    output [15:0] dpi_plus,
    output [15:0] selected
);

  counter cnt (
      clk,
      counter
  );
  immediate_plus ip (
      a,
      b,
      immediate_plus
  );
  immediate_minus im (
      a,
      b,
      immediate_minus
  );
  dpi_plus dp (
      a,
      b,
      dpi_plus
  );

  clocked_plus cp (
      clk,
      a,
      b,
      clocked_plus
  );

  mux_module mux (
      a,
      b,
      sel[0],
      selected
  );

endmodule
