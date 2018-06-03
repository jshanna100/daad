import mne

root_dir = "d:/nadia_daad/proc/"
subjs = ["VP1","VP2","VP3","VP4","VP5","VP6","VP7"]
runs = ["1","2","3"]

for sub in subjs:
    for run in runs:
        f = "{a}{b}_{c}-raw.fif".format(a=root_dir,b=sub,c=run)
        raw = mne.io.Raw(f)
        if raw.annotations is not None:
            raw.annotations.save("{a}{b}_{c}-annot.fif".format(a=root_dir,b=sub,c=run))