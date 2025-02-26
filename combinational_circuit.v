module combinational_circuit (
    input wire [15:0] A, B, C, D,
    output wire out_signal
);

    wire [15:0] n1, n2, n3, n4, n5, n6, n7, n8, n9, n10;
    wire [15:0] n11, n12, n13, n14, n15, n16, n17, n18, n19, n20;

    Logic_Block1 U1 (.x(A[0]), .y(B[0]), .z(n1[0]), .w(n2[0]));
    Logic_Block2 U6 (.p(C[0]), .q(D[0]), .r(n11[0]), .s(n12[0]));

    and (n21[0], n1[0], n11[0]); 
    or  (n22[0], n2[0], n12[0]); 
    xor (n23[0], n21[0], n22[0]); 

    assign out_signal = ~n23[0]; 

endmodule

module Logic_Block1 (input wire x, y, output wire z, w);
    and (z, x, y);
    or  (w, x, y);
endmodule

module Logic_Block2 (input wire p, q, output wire r, s);
    xor (r, p, q);
    nand (s, p, q);
endmodule
