"""
Test script runs analysis.stats.PCA analysis on various basic test cases.
"""
import analysis.stats.PCA as PCA
from input_interface.ImportedData import ImportedData

# import data
data = ImportedData('test\\sample.edf').data

# initialize PrinComp object
p = PCA.PrinComp()

# test case 1, correct data, correct threshold, threshold_num
pca1 = p.pca(data=data, signals=['EEG A1', 'EEG A2', 'EEG C3', 'EEG C4', 'EEG CZ'], threshold_num=4)
print(pca1)

# test case 2, correct data, correct threshold, threshold_var
pca2 = p.pca(data=data, signals=['EEG A1', 'EEG A2', 'EEG C3', 'EEG C4', 'EEG CZ'], threshold_var=0.90)
print(pca2)

# test case 3, correct data, no threshold
pca3 = p.pca(data=data, signals=['EEG A1', 'EEG A2', 'EEG C3', 'EEG C4', 'EEG CZ'])
print(pca3)

# test case 4, incorrect data
try:
    pca4 = p.pca(data=data, signals=['EEG A1', 'EEG A2', 'EEG C3', 'EEG C4', 'Test'])
except ValueError as e:
    print(e)

# test case 5, incorrect threshold
try:
    pca5 = p.pca(data=data, signals=['EEG A1', 'EEG A2', 'EEG C3', 'EEG C4', 'EEG CZ'], threshold_var=1.5)
except ValueError as e:
    print(e)

# test case 6, incorrect threshold
try:
    pca6 = p.pca(data=data, signals=['EEG A1', 'EEG A2', 'EEG C3', 'EEG C4', 'EEG CZ'], threshold_num=-17)
except ValueError as e:
    print(e)

# test case 7, incorrect threshold
try:
    pca7 = p.pca(data=data, signals=['EEG A1', 'EEG A2', 'EEG C3', 'EEG C4'], threshold_var=0.5, threshold_num=3)
except ValueError as e:
    print(e)
