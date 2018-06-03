import mne
from mne.stats import spatio_temporal_cluster_test
import numpy as np

root_dir = "d:/nadia_daad/proc/"
subjs = ["VP1","VP2","VP3","VP4","VP5","VP6","VP7"]
sides = ["links","rechts"]
p_accept = 0.5

filename = "{a}VP1_1-epo.fif".format(a=root_dir)
epo = mne.read_epochs(filename)
connectivity, ch_names = mne.channels.find_ch_connectivity(
        epo.info, ch_type='mag')

filename = "{a}VP1_links-tfr.h5".format(a=root_dir)
tfr = mne.time_frequency.read_tfrs(filename)[0]
X = [np.zeros((0,len(tfr.times),len(tfr.ch_names))) for s in sides]
for sub in subjs:
    tfr = []
    for s_idx,s in enumerate(sides):
        filename = "{a}{b}_{c}-tfr.h5".format(a=root_dir,b=sub,c=s)
        tfr = mne.time_frequency.read_tfrs(filename)[0]
        data = np.expand_dims(np.mean(tfr.data[:,8:11,:],axis=1).T, 0)
        X[s_idx] = np.concatenate((X[s_idx],data))
        
T_obs, clusters, p_values, _ = spatio_temporal_cluster_test(
        X, n_permutations=1000,connectivity=connectivity)  
good_cluster_inds = np.where(p_values < p_accept)[0]
