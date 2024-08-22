# ironhack_data_science_final
Parkinson's Disease Prediction from Keystroke Data

### Credits to source dataset creators: https://physionet.org/content/tappy/1.0.0/

### Introduction

The general idea is to build a model capable of predicting Parkinson's Disease of an individual, based on their keystroke data

### Dataset (

The original dataset "Archived-Data" contains around 400 files. Each file corresponds to an individual persons keystroke data and has the following columns: 

UserKey: 10 character code for that user
Date: YYMMDD
Timestamp: HH:MM:SS.SSS
Hand: L or R key pressed
Hold time: Time between press and release for current key mmmm.m milliseconds
Direction: Previous to current LL, LR, RL, RR (and S for a space key)
Latency time: Time between pressing the previous key and pressing current key. Milliseconds
Flight time: Time between release of previous key and press of current key. Milliseconds

Additionally, in a separate file "Archived-Users", there is personal information about date of Birth, Tremor, Gender etc... of each patient

### Data Cleaning and processing

To generate features that will be used to build a model, the Jupyter Notebook called "code" must be run. It requires the existence of unzipped Archived-Data and Archived-Users. Replace "physionetdotorg/files/tappy/1/extracted/TappyData/" with the path to the required unzipped files and "physionetdotorg/files/tappy/1/processed_test_spark.csv" with the directory of the output file

This output file will contain a CSV with 40 columns (features) that will be used to train model

### Model Training

The second part of the project requires the output of the first. But it will be already included. Its the "processed_17082024.txt". Change the input file directory in line:

data = pd.read_csv("physionetdotorg/files/tappy/1/processed_17082024.csv") 

and run the jupyter notebook

### Generate Own tappy data

Unfortunately, it seems that Tappy program is not maintined anymore. A python script was made to imitate the program and it generates the file with exactly the same format as needed. Open tappytest4.py script, change the output file directory in line 

        self.log_file = 'MAKSYM0000_2008.txt'  # File to write output to

and launch the script. The script will register everything you write and output in in a file. Process the file exactly the same as the files of the original data (with code in notebook code.ipynb).

