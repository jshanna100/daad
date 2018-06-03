import mne
import pickle
import scipy.sparse
from scipy.stats import ttest_rel, t

def mass_t(A,B):
    t_val,p_val = ttest_rel(A,B)
    return t_val

proc_dir = "../proc/stcs/"
sub = "VP1"
side="lh"
threshold = 0.95

filename = proc_dir+sub+"_"+side
with open(filename,"rb") as file:
    stcs = pickle.load(file)

connect = scipy.sparse.load_npz("cnx_"+side+".npz")

threshold = t.interval(threshold,stcs[0].shape[0])[1]
t_obs, clusters, cluster_pv, H0 = clu = mne.stats.spatio_temporal_cluster_test(
        stcs,connectivity=connect,stat_fun=mass_t,threshold=threshold,n_jobs=4)



