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
    integer i;  // Loop variable

    initial begin
        $dumpfile("testbench.vcd");  // Dumps waveform data for GTKWave
        $dumpvars(0, testbench); 

        $display("🚀 Running Testbench with 60+ test cases...\n");

        // Apply 60+ test cases dynamically
        for (i = 0; i < 60; i = i + 1) begin
            A = $random;  // Generate random test values
            B = $random;
            C = $random;
            D = $random;
            #10;  // Delay of 10 time units
            $display("Test %0d | A: %h B: %h C: %h D: %h | Out: %h", i+1, A, B, C, D, out_signal);
        end

        $display("\n✅ Test completed with 60+ test cases.");
        $finish; // End simulation
    end

endmodule
