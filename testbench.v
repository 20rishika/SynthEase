`timescale 1ns / 1ps

module testbench;

    // Declare test signals
    reg [15:0] A, B, C, D;
    wire out_signal;

    // Instantiate the design under test (DUT)
    combinational_circuit uut (
        .A(A),
        .B(B),
        .C(C),
        .D(D),
        .out_signal(out_signal)
    );

    // Test Stimulus
    initial begin
        $dumpfile("testbench.vcd");  // Dumps waveform data for GTKWave
        $dumpvars(0, testbench); 

        // Apply test cases
        A = 16'h000F; B = 16'h00F0; C = 16'h0F00; D = 16'hF000; #10;
        A = 16'hAAAA; B = 16'h5555; C = 16'hFFFF; D = 16'h0000; #10;
        A = 16'h1234; B = 16'h5678; C = 16'h9ABC; D = 16'hDEF0; #10;

        $display("Test completed.");
        $finish; // End simulation
    end

endmodule
