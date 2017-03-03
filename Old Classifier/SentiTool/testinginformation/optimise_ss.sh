#!/bin/bash

echo "Optimizing SentiStrength EmotionLookupTable.txt"
java -jar /home/jake/Development/Undergrad_Research/SentiTool/lib/SentiStrengthCom.jar sentidata /home/jake/Development/Undergrad_Research/SentiTool/data/ minimprovement 1 input /home/jake/Development/Undergrad_Research/SentiTool/indiv_results.csv  optimise /home/jake/Development/Undergrad_Research/SentiTool/data/EmotionLookupTable.txt input /home/jake/Development/Undergrad_Research/SentiTool/indiv_results.csv
sleep 3 
echo "Optimization finished:  Compare with backup for final results."
