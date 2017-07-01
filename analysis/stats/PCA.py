"""
EEG is a multi-dimensional data with dimensions being either time points or electrodes.
PCA is a statistical method for the reduction of dimensions.
This implementation assumes each electrode is a variable (a dimension) and time points are observations.
The analysis can be run at once using function pca or step-by-step dependent on the GUI implementation.
The implementation is based on Cohen(2014) Analyzing Neural Time Series Data - Theory and Practice and sklearn docs.
"""
import numpy as np
from sklearn.decomposition import PCA
from numbers import Number
from analysis.Reportable import Reportable


class PrinComp(Reportable):

    def return_as_node(self):
        pass

    @staticmethod
    def _extract_data(imported_data, signals=None):
        """
        This function extracts data needed for analysis from the raw data imported.
        :param imported_data: data imported via GUI (or ImportedData method)
        :param signals: electrodes chosen for analysis; the default is None, in which case all electrodes are analyzed;
        list string values corresponding to header names in the data
        :type imported_data: dict
        :type signals: list of strings
        :return: array with data from each electrode in columns
        :rtype: Numpy array of shape (number of time points, number of electrodes)
        
        TODO: Labels for electrodes are stored by not used.
        """

        data_array = []
        # data_array_labels = []
        if signals is None:
            for label in imported_data['signal'].keys():
                data_array.append(imported_data['signal'][label][1])  # store only signal values without time markers
                # data_array_labels.append(label)
        elif signals is not None:
            for label in signals:
                if label not in imported_data['signal'].keys():
                    raise ValueError("Signal " + label + " is not available in the data.")
                else:
                    data_array.append(imported_data['signal'][label][1])
                    # data_array_labels.append(label)
        data_array = np.transpose(np.array(data_array))
        return data_array

    @staticmethod
    def _run_decomposition(preprocessed_data):
        """
        Function fits input data to PCA model.
        :param preprocessed_data: data array with electrode signals in columns
        :type preprocessed_data: Numpy array of shape (number of time points, number of electrodes)
        :return: PCA model fitted to input data
        :rtype: sklearn.decomposition.PCA object
        """
        pca = PCA()
        pca.fit(preprocessed_data)
        return pca

    @staticmethod
    def _select_components(pca_model, threshold_num=None, threshold_var=None):
        """
        Function selects the number of components to retain. Given that components are sorted by explained variance
        and there is no viable reason to skip components with larger explained variance, first n components are always
        retained. Function does not modify the model or data. 
        If threshold_num is too large it is truncated to the number of components.
        If neither of the thresholds is specified, the threshold is calculated as 1/number of electrodes following 
        the approach in Cohen(2014). If two threshold are specified, exception is raised.
        :param pca_model: PCA model fitted to data
        :param threshold_num: number of components to retain
        :param threshold_var: cumulative explained variance ratio required (must be between 0 and 1)
        :type pca_model: sklearn.decomposition.PCA object fitted to data
        :type threshold_num: int
        :type threshold_var: float
        :return: number of components to retain
        :rtype: int
        """
        num_components = pca_model.components_.shape[0]
        if threshold_num and threshold_var:
            raise ValueError("Only one threshold value is expected.")
        if threshold_num is not None:
            if threshold_num < 1 or not isinstance(threshold_num, int):
                raise ValueError("Threshold number of components must be an integer >= 1.")
            else:
                cutoff = min(threshold_num, num_components)
        elif threshold_var is not None:
            if threshold_var <= 0 or threshold_var > 1 or not isinstance(threshold_var, Number):
                raise ValueError("Variance threshold must be between 0 and 1.")
            else:
                cum_vars = np.cumsum(pca_model.explained_variance_ratio_)
                cutoff = np.argmax(cum_vars > threshold_var) + 1
        elif threshold_num is None and threshold_var is None:
            threshold_auto = 1/num_components
            cutoff = len([var for var in pca_model.explained_variance_ratio_ if var >= threshold_auto])
        return cutoff

    @staticmethod
    def _run_analysis(preprocessed_data, n_components):
        """
        Function initializes and fits a PCA model for a given number of components.
        :param preprocessed_data: data array with electrode signals in columns
        :param n_components: number of components to retain
        :type preprocessed_data: Numpy array of shape (number of time points, number of electrodes)
        :type n_components: int
        :return: dictionary with components' loadings, transformed (rotated and reduced) data and ratio of variance
        explained by each components
        :rtype: dict
        """
        pca = PCA(n_components)
        pca.fit(preprocessed_data)
        output = {'loadings': pca.components_,
                  'transformed_data': pca.transform(preprocessed_data),
                  'explained_var': pca.explained_variance_ratio_}
        return output

    @staticmethod
    def pca(data, signals=None, threshold_num=None, threshold_var=None):
        """
        Function runs a complete PCA.
        :param data: data imported via ImportedData method
        :param signals: electrodes chosen for analysis; the default is None, in which case all electrodes are analyzed
        :param threshold_num: number of components to retain
        :param threshold_var: cumulative explained variance ratio required (must be between 0 and 1)
        :type data: dict
        :type signals: list with string values corresponding to header names in the data
        :type threshold_num: int
        :type threshold_var: float
        :return: dictionary with components' loadings, transformed (rotated and reduced) data and ratio of variance
        explained by each components
        :rtype: dict
        """
        preprocessed = PrinComp._extract_data(data, signals)
        decomposition = PrinComp._run_decomposition(preprocessed)
        n_components = PrinComp._select_components(decomposition, threshold_num, threshold_var)
        pca = PrinComp._run_analysis(preprocessed, n_components)
        return pca
