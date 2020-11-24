# hrv_cutter
Cuts intervals from RR/IBI-sequences to prepare for hrv-analysis

Executable in your prefered python environment

This piece of code is helpful for:
- preparing .hrm-files for analysis in other software that requires .txt-input (e.g. helpf ul for batch processing in ARTiiFACT: http://artiifact.de/) 
- cutting custom-selected intervals (e.g., 5-minute intervals) from a whole file by specifying a clock time (helpful incase you wrote a protocol of the recording and want to select certain periods)

Using hrv_cutter:
1) select your working directories for file upload and save in the "Program" menu
2) upload your .hrm-file via "HRdata" and "Load data"
3) "Select interval" by specifying your desired time frame and confirm by clicking "OK"
4) "Cut & save interval" by assigning a name to the file that you later want to analyze
5) repeat steps 3 and 4 as often as you like in this file, or restart from step 2 uploading another file
