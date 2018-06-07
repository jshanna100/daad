import mne
#subjects_dir = "/home/jeff/freesurfer/subjects"
subjects_dir = "../subjects"
proc_dir = "../proc/"
subject = "fsaverage"



src = mne.setup_source_space(subject, spacing='oct6',
                             subjects_dir=subjects_dir, add_dist=False)
src.save(proc_dir+"fsaverage-src.fif")



