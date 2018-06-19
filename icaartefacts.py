import mne
import numpy as np
from mne.preprocessing.ica import corrmap
from scipy.stats import skew
import matplotlib.pyplot as plt


root_dir = "../proc/"
subjs = ["VP1","VP2","VP3","VP4","VP5","VP6","VP7"]
#subjs = ["VP2","VP3"]
runs = ["1","2","3"]
art = 0

icas = []
epos = []
id_list = []
bad_chans = []
for sub in subjs:
    f = "{a}{b}-ica.fif".format(a=root_dir,b=sub)
    icas.append(mne.preprocessing.read_ica(f))
    f = "{a}{b}-epo.fif".format(a=root_dir,b=sub)
    epos.append(mne.read_epochs(f))
    bad_chans.append(epos[-1].info["bads"])
    epos[-1].interpolate_bads()
    id_list.append("{b}".format(b=sub))
        
eog_template = (0,31)
ekg_template = (9,0)

corrmap(icas,template=eog_template,show=False,label="eog", 
            threshold=0.85, ch_type='mag',plot=False)

sources = []
for idx,ica in enumerate(icas):
    source = ica.get_sources(inst=epos[idx])
    eog_comps = ica.labels_["eog"]
    comp_names = [source.ch_names[x] for x in eog_comps]
    if comp_names:
        sources.append(source.pick_channels(comp_names))
    else:
        sources.append(None)

if art:

    # mark the interpolated channels as bad again
    for epo_idx,epo in enumerate(epos):
        epo.info["bads"] = bad_chans[epo_idx] 
    
    for source_idx,source in enumerate(sources):
        if source is not None:
            sub_idx = 1
            data = source.get_data()
            goods = []
            for e_idx in range(data.shape[0]):
                std = np.std(data[e_idx,0,:])
                if std < 0.9:
                    goods.append(e_idx)
            new_epo = epos[source_idx][goods]
    #       viz
            fig = plt.figure()
            for e_idx in range(data.shape[0]):
                plt.subplot(13,18,sub_idx)
                std = np.std(data[e_idx,0,:])
                color = "blue" if std<0.9 else "red"
                plt.plot(data[e_idx,0,:],color=color)
                plt.ylim((-10,10))
                plt.text(400,7,str(std)[:4])
                sub_idx += 1
        else:
            new_epo = epos[source_idx].copy()
        new_epo.save("{a}{b}_a-epo.fif".format(a=root_dir,b=id_list[source_idx]))

else:        
    #remove components
    for i_idx,i in enumerate(icas):
        exclude = i.labels_["eog"].copy()
        i.apply(epos[i_idx], exclude=exclude)
        epo.info["bads"] = bad_chans[i_idx] # mark the interpolated channels as bad again
        epos[i_idx].save("{a}{b}_aic-epo.fif".format(a=root_dir,b=id_list[i_idx]))