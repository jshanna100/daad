import mne
import pickle
import numpy as np

sub = "VP1"
proc_dir = "../proc/stcs/"
subjects_dir="../subjects"

filename = proc_dir+sub+"_clust"
with open(filename,"rb") as file:
    clu = pickle.load(file)
    vertices = [np.arange(4098),np.arange(4098)]
    res = mne.stats.summarize_clusters_stc(
           clu, p_thresh=0.05, tstep=1, tmin=0, subject='fsaverage', vertices=vertices)
    res.plot(subjects_dir=subjects_dir,hemi="both",colormap="mne",time_viewer=True)