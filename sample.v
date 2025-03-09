module Sample_Circuit (
    input wire A,
    input wire B,
    input wire C,
    output wire Y
);
    wire n1, n2, n3;

    and (n1, A, B);     // AND Gate
    or  (n2, B, C);     // OR Gate
    xor (n3, n1, n2);   // XOR Gate

    assign Y = ~n3;     // NOT Gate (Inversion)
endmodule
