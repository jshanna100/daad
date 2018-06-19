import mne

root_dir = "../proc/"
subjs = ["VP1","VP2","VP3","VP4","VP5","VP6","VP7"]
runs = ["1","2","3"]
subjects_dir = "/home/jeff/freesurfer/subjects"
subject = "fsaverage"

typ = "a"



#subjs = ["VP1"]
#runs = ["1"]

for sub in subjs:
    src = mne.read_source_spaces(root_dir+"fsaverage_{}-src.fif".format(sub.lower()))
    conductivity = (0.3,)  # for single layer
    model = mne.make_bem_model(subject='fsaverage_{}'.format(sub.lower()), ico=4,
                           conductivity=conductivity,
                           subjects_dir=subjects_dir)
    bem = mne.make_bem_solution(model)
    f = "{a}{b}_{d}-epo.fif".format(a=root_dir,b=sub,d=typ)
    t = "{a}fsaverage_{b}-trans.fif".format(a=root_dir,b=sub.lower())
    fwd = mne.make_forward_solution(f, trans=t, src=src, bem=bem,
                            meg=True, eeg=False, mindist=5.0, n_jobs=4)
    mne.write_forward_solution(
            "{a}{b}_{d}-fwd.fif".format(a=root_dir,b=sub,d=typ),
            fwd,overwrite=True)