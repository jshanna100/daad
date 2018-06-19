import mne

root_dir = "../proc/"
subjs = ["VP1","VP2","VP3","VP4","VP5","VP6","VP7"]
runs = ["1","2","3"]

#subjs = ["VP1"]
#runs = ["1"]

for sub in subjs:
    f = "{a}{b}-epo.fif".format(a=root_dir,b=sub)
    epo = mne.read_epochs(f).interpolate_bads()
    ica = mne.preprocessing.ICA(n_components=64)
    ica.fit(epo)
    ica.save("{a}{b}-ica.fif".format(a=root_dir,b=sub))
        