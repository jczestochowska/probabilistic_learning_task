CycleNo = 10; % it is equivalent to 30 trials, because single cycle contains random sequence of 3 trials
MinimumBlocks = 3;
MaximumBlocks = 3;
    


filename = input('Podaj nazwê pliku z raportem (bez rozszerzenia): ','s');

runtest(filename, CycleNo, MinimumBlocks, MaximumBlocks);