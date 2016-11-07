#!/bin/bash

pwd
echo "Getting Term Weights..."
cd ../lib/
java -jar SentiStrengthCom.jar sentidata /home/jacob/Development/Undergrad_Research/SentiTool/data/ input /home/jacob/Development/Undergrad_Research/SentiTool/indiv_results.csv termWeights
sleep 3
echo "Term weights collected from results"
