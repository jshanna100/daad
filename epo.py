import mne
import numpy as np
from os import listdir

root_dir = "../proc/"
filelist = listdir(root_dir)
subjs = ["VP1","VP2","VP3","VP4","VP5","VP6","VP7"]
runs = ["1","2","3"]

#subjs = ["VP1"]
#runs = ["1"]

for sub in subjs:
    for run in runs:
        f = "{a}{b}_{c}-raw.fif".format(a=root_dir,b=sub,c=run)
        a = "{b}_{c}-annot.fif".format(b=sub,c=run)
        raw = mne.io.Raw(f)
        if a in filelist:
            annot = mne.read_annotations(root_dir+a)
            raw.annotations = annot
        trigs = mne.find_events(raw,stim_channel="STI 014")
        resps = mne.find_events(raw,stim_channel="STI 013")
    
        new_trigs = []    
        i_idx = 0
        bufferwert = (-9999,0)
        while i_idx < len(trigs):
            neuwert = trigs[i_idx,2] - 4095 if trigs[i_idx,2]>4000 else trigs[i_idx,2]
            if neuwert > 127:
                bufferwert = (trigs[i_idx,0],neuwert)
                i_idx += 1
                continue
            else:
                if trigs[i_idx,0]-bufferwert[0] > 1100:
                    i_idx += 1
                    continue
                else:
                    new_trigs.append([trigs[i_idx,0],0,bufferwert[1]])
                    i_idx += 1
#        new_trigs = np.array(new_trigs,dtype=np.int64)
            
        epo = mne.Epochs(raw,new_trigs,tmin=-1,tmax=2,baseline=(None,0))
        epo.load_data()
        epo.resample(200)
        epo = epo.interpolate_bads()
        epo.save("{a}{b}_{c}-epo.fif".format(a=root_dir,b=sub,c=run))
    
    
