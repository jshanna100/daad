import mne
from mne.time_frequency import tfr_morlet
import numpy as np

root_dir = "../proc/"
runs = ["1","2","3"]
trig_inds = [["143","128","129","130"],["131","132","133","134"]]
sides = ["links","rechts"]

fmin=7
fmax=13
freqs = np.linspace(fmin, fmax, fmax-fmin+1)
cycles = freqs/2.

typ="aic"

#if typ=="a":
#    subjs = ["VP2","VP3","VP4","VP5","VP7"] # not enough trials in VP1, VP6
#else:
#    subjs = ["VP1","VP2","VP3","VP4","VP5","VP6","VP7"]

subjs = ["VP1","VP2","VP3","VP4","VP5","VP6","VP7"]
pows = [[],[]]
itcs = [[],[]]
evos = [[],[]]
for sub in subjs:
    epo_name = "{a}{b}_{d}-epo.fif".format(a=root_dir,b=sub,d=typ)        
    epo = mne.read_epochs(epo_name)
    epo = mne.epochs.combine_event_ids(epo,trig_inds[0],{"links":1})
    epo = mne.epochs.combine_event_ids(epo,trig_inds[1],{"rechts":2})
    epo.equalize_event_counts(sides)
    temp = []
    for side_idx,side in enumerate(sides):
        power, itc = tfr_morlet(epo[side], freqs=freqs, n_cycles=cycles, use_fft=True,
                    return_itc=True, decim=3, n_jobs=4)
        pows[side_idx].append(power)
        itcs[side_idx].append(itc)
        evos[side_idx].append(epo[side].average())

grand_pow,grand_itc,grand_evo = [],[],[]
for p in pows:
    grand_pow.append(mne.grand_average(p))
for i in itcs:
    grand_itc.append(mne.grand_average(i))
for e in evos:
    grand_evo.append(mne.grand_average(e).filter(h_freq=10,l_freq=None))
pow_sub = grand_pow[0]-grand_pow[1]


        