import mne
import numpy as np

root_dir = "d:/nadia_daad/proc/"
subjs = ["VP1","VP2","VP3","VP4","VP5","VP6","VP7"]
runs = ["1","2","3"]

freqs = np.array(range(1,20))
n_cycles = freqs / 2.
trig_inds = [["143","128","129","130"],["131","132","133","134"]]
sides = ["links","rechts"]

#subjs = ["VP5"]
#runs = ["2"]

epos = []
for sub in subjs:
    sub_epos = [[],[]]
    for run in runs:
        f = "{a}{b}_{c}-ica-epo.fif".format(a=root_dir,b=sub,c=run)
        epo = mne.read_epochs(f)
        epo = mne.epochs.combine_event_ids(epo,trig_inds[0],{"links":1})
        epo = mne.epochs.combine_event_ids(epo,trig_inds[1],{"rechts":2})
        epo.equalize_event_counts(sides)
        for s_idx,s in enumerate(sides):
            power = mne.time_frequency.tfr_morlet(
                    epo[s], freqs=freqs, n_cycles=n_cycles, use_fft=True,return_itc=False, decim=3, n_jobs=1)
            power.apply_baseline((None,0))
            sub_epos[s_idx].append(power)
    for s_idx,s in enumerate(sides):
        mne.grand_average(sub_epos[s_idx]).save(
                "{a}{b}_{c}-tfr.h5".format(a=root_dir,b=sub,c=s),overwrite=True)

