import mne
from mne.time_frequency import csd_morlet
from mne.beamformer import make_dics,apply_dics_csd
import numpy as np

root_dir = "../proc/"
runs = ["1","2","3"]
trig_inds = [["143","128","129","130"],["131","132","133","134"]]
sides = ["links","rechts"]
subjects_dir = "/home/jeff/freesurfer/subjects/"
subjects_dir = "../subjects/"
label_names = ["lateraloccipital","lingual", "pericalcarine", "cuneus",
               "superiorparietal","fusiform","inferiorparietal","precuneus"]
fmin=7
fmax=13
frequencies = np.linspace(fmin, fmax, fmax-fmin+1)

typ="aic"

if typ=="a":
    subjs = ["VP2","VP3","VP4","VP5","VP7"] # not enough trials in VP1, VP6
else:
    subjs = ["VP1","VP2","VP3","VP4","VP5","VP6","VP7"]

#subjs = ["VP7"]
#subjs = ["VP1"]
#runs = ["1"]
#sides = ["links"]

#all_labels = mne.read_labels_from_annot("fsaverage",subjects_dir=subjects_dir)
#for h in ["lh","rh"]:
#    labels = []
#    hemi_names = ["{}-{}".format(l,h) for l in label_names]
#    [labels.append(l) for l in all_labels if l.name in hemi_names]
#    grand_label = labels.pop()
#    for l in labels:
#        grand_label += l


for sub in subjs:
    stc_runs = []
    for run in runs:
        epo_name = "{a}{b}_{c}_{d}-epo.fif".format(a=root_dir,b=sub,c=run,d=typ)        
        fwd_name = "{a}{b}_{c}_{d}-fwd.fif".format(a=root_dir,b=sub,c=run,d=typ)
        epo = mne.read_epochs(epo_name)
        epo = mne.epochs.combine_event_ids(epo,trig_inds[0],{"links":1})
        epo = mne.epochs.combine_event_ids(epo,trig_inds[1],{"rechts":2})
        epo.equalize_event_counts(sides)
        fwd = mne.read_forward_solution(fwd_name)
        for side in sides:
            e = epo[side]
            csd = csd_morlet(e, tmin=0.8, tmax=1.8,
                           frequencies=frequencies)
            
            filters = make_dics(e.info, fwd, csd)
            stc = apply_dics_csd(csd,filters)

            stc[0].save("{a}stcs/{b}_{c}_{d}_{e}".format(
                    a=root_dir,b=sub,c=run,d=side,e=typ))