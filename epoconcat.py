import mne

root_dir = "../proc/"
subjs = ["VP1","VP2","VP3","VP4","VP5","VP6","VP7"]
runs = ["1","2","3"]

#subjs = ["VP1"]
#runs = ["1"]

for sub in subjs:
    epo_list = []
    for run in runs:
        f = "{a}{b}_{c}-epo.fif".format(a=root_dir,b=sub,c=run)
        epo_list.append(mne.read_epochs(f))
    e = mne.concatenate_epochs(epo_list)
    e.save("{a}{b}-epo.fif".format(a=root_dir,b=sub))