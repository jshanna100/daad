import mne
subjects_dir = "/home/jeff/freesurfer/subjects"
#subjects_dir = "../subjects"
proc_dir = "../proc/"
subject = "fsaverage"
subjs = ["vp1","vp2","vp3","vp4","vp5","vp6","vp7"]

for sub in subjs:
    src = mne.setup_source_space("{a}_{b}".format(a=subject,b=sub), 
                                 spacing='oct6',subjects_dir=subjects_dir,
                                 add_dist=False)
    src.save("{a}{b}_{c}-src.fif".format(a=proc_dir,b=subject,c=sub),overwrite=True)



