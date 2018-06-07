import mne
import numpy as np
from os import listdir
import pickle

root_dir = "../proc/stcs/"
subjs = ["VP1","VP2","VP3","VP4","VP5","VP6","VP7"]
sides = ["links","rechts"]
runs = ["1","2","3"]
freqs = ["8","9","10","11","12","13"]

#subjs = ["VP1"]

filelist = listdir(root_dir)

for sub in subjs:
    print("Subject: {a}".format(a=sub))
    X = []
    for side_idx,side in enumerate(sides):
        X_temp = []
        for run in runs:                
            epo_num = 0
            filename = "{a}_{b}_{c}_{e}-lh.stc".format(
                    a=sub,b=run,c=side,e=epo_num)
            while filename in filelist:
                temp = []
                filename = "{a}_{b}_{c}_{e}-lh.stc".format(
                        a=sub,b=run,c=side,e=epo_num)
                stc = mne.read_source_estimate(root_dir+filename)
                temp.append(np.swapaxes(stc.data,0,1))
                temp = np.array(temp)
                temp = np.swapaxes(temp,0,1)
                temp = np.reshape(temp,(temp.shape[0],-1))
                X_temp.append(temp)
                epo_num += 1
                filename = "{a}_{b}_{c}_{e}-lh.stc".format(
                        a=sub,b=run,c=side,e=epo_num)
        X.append(np.array(X_temp))
    with open(root_dir+"{a}".format(a=sub),"wb")as f:
        pickle.dump(X,f)