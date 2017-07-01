"""
ICA is a statistical method for blind source separation.
This method can be used to decompose the signal into independent components for analysis and data filtering.
This implementation uses FastICA algorithm implemented in sklearn package.
Unlike in PCA, components are not sorted in any particular order and are manually removed.
The analysis is run step-by-step.
The implementation is based on sklearn docs.
"""
import numpy as np
from sklearn.decomposition import FastICA
from analysis.Reportable import Reportable


class ICA(Reportable):

    def return_as_node(self):
        pass

    @staticmethod
    def extract_data(imported_data, signals=None):
        """
        This function extracts data needed for analysis from the raw data imported.
        :param imported_data: data imported via GUI (or ImportedData method)
        :param signals: electrodes chosen for analysis; the default is None, in which case all electrodes are analyzed
        :type imported_data: dict
        :type signals: list with string values corresponding to header names in the data
        :return: array with data from each electrode in columns
        :rtype: Numpy array of shape (number of time points, number of electrodes)

        TODO: Labels for electrodes are stored by not used.
        """
        data_array = []
        # data_array_labels = []
        if signals is None:
            for label in imported_data['signal'].keys():
                data_array.append(imported_data['signal'][label][1])
                # data_array_labels.append(label)
        elif signals is not None:
            for label in signals:
                if label not in imported_data['signal'].keys():
                    raise IndexError("Signal " + label + " is not available in the data.")
                else:
                    data_array.append(imported_data['signal'][label][1])
                    # data_array_labels.append(label)
        data_array = np.transpose(np.array(data_array))
        return data_array

    @staticmethod
    def run_decomposition(preprocessed_data):
        """
        Function fits input data to FastICA model.
        :param preprocessed_data: data array with electrode signals in columns
        :type preprocessed_data: Numpy array of shape (number of time points, number of electrodes)
        :return: FastICA model fitted to input data
        :rtype: sklearn.decomposition.FastICA object
        """
        ica = FastICA()
        ica.fit(preprocessed_data)
        return ica

    @staticmethod
    def select_components(preprocessed_data, ica_model, components, retain=True, retain_all=False):
        """
        Function selects components from the model and transformes and filters data. Returns componenents coefficients
         and transformed and filtered data.
        :param preprocessed_data: data array with electrode signals in columns
        :param ica_model: FastICA model fitted to data
        :param components: list of numeric indices of components; incorrect type or value raises ValueError
        :param retain: if True, components listed in components variable are kept; if False all but listed components
        are retained
        :param retain_all: if True, all components are kept; overrides components argument
        :type preprocessed_data: Numpy array of shape (number of time points, number of electrodes)
        :type ica_model: sklearn.decomposition.FastICA object
        :type components: list of integers
        :type retain: bool
        :type retain_all: bool
        :return: selected components' coefficients and filtered transformed data
        :rtype: dict
        """
        all_components = ica_model.components_
        n_components = all_components.shape[0]
        if retain_all:
            components_to_retain = list(range(n_components))
        else:
            for comp in components:
                if not isinstance(comp, int):
                    raise ValueError("Components must be expressed as indices.")
                if comp < 0 or comp > n_components:
                    raise ValueError("Index " + str(comp) + " does not match any component.")
            if retain:
                components_to_retain = [ind-1 for ind in components]
            else:
                components_to_retain = [ind for ind in range(n_components) if ind+1 not in components]
        selected_components = all_components[components_to_retain, :]
        transformed_data = ica_model.transform(preprocessed_data)[:, components_to_retain]
        output = {'components': selected_components, 'transformed_data': transformed_data}
        return output