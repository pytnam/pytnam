"""
Test script runs analysis.stats.PCA analysis on various basic test cases.
"""
import analysis.stats.ICA as ICA
from input_interface.ImportedData import ImportedData

# import data
data = ImportedData('test\\sample.edf').data

# initialize ICA object
i = ICA.ICA()

# preprocess data and run decomposition
preprocessed = i.extract_data(data, ['EEG A1', 'EEG A2', 'EEG C3', 'EEG C4', 'EEG CZ'])
ica = i.run_decomposition(preprocessed)

# test case 1, correct components, retain, not retain_all
output1 = i.select_components(preprocessed, ica, [1, 2, 4])
print(output1)

# test case 2, incorrect components, retain, not retain_all
try:
    output2 = i.select_components(preprocessed, ica, [1, 2, 4, 18])
except ValueError as e:
    print(e)

# test case 3, correct components, not retain, not retain_all
output3 = i.select_components(preprocessed, ica, [1, 2], retain=False)
print(output3)

# test case 4, correct components, retain, retain_all
output4 = i.select_components(preprocessed, ica, [1, 2], retain=False, retain_all=True)
print(output4)



