import mne

root_dir = "../proc/"
subjs = ["VP1","VP2","VP3","VP4","VP5","VP6","VP7"]
runs = ["1","2","3"]

# make the annotations
filelist = []
for sub in subjs:
    for run in runs:
        filelist.append("{d}{s}_{r}-epo.fif".format(d=root_dir,s=sub,r=run))
class Cycler():
    
    def __init__(self,filelist):
        self.filelist = filelist
        
    def go(self):
        fn = self.filelist.pop()
        self.raw = mne.read_epochs(fn)
        self.raw.plot(n_channels=250,scalings=dict(mag=3e-11),decim=5)
        
    def save(self):
        if self.raw.annotations is not None:
            self.raw.annotations.save("{d}{s}_{r}-annot.fif".format(
                    d=root_dir,s=sub,r=run))
        else:
            print("No annotations to save.")

cyc = Cycler(filelist)
# harvest the annotations
#for sub in subjs:
#    for run in runs:
#        f = "{a}{b}_{c}-raw.fif".format(a=root_dir,b=sub,c=run)
#        raw = mne.io.Raw(f)
#        if raw.annotations is not None:
#            raw.annotations.save("{a}{b}_{c}-annot.fif".format(a=root_dir,b=sub,c=run))