import mne
import numpy as np
from mne.preprocessing.ica import corrmap
from scipy.stats import skew
import matplotlib.pyplot as plt


root_dir = "../proc/"
subjs = ["VP1","VP2","VP3","VP4","VP5","VP6","VP7"]
#subjs = ["VP2","VP3"]
runs = ["1","2","3"]

icas = []
epos = []
id_list = []
for sub in subjs:
    for run in runs:
        f = "{a}{b}_{c}-ica.fif".format(a=root_dir,b=sub,c=run)
        icas.append(mne.preprocessing.read_ica(f))
        f = "{a}{b}_{c}-epo.fif".format(a=root_dir,b=sub,c=run)
        epos.append(mne.read_epochs(f).interpolate_bads())
        id_list.append("{b}_{c}".format(b=sub,c=run))
        
eog_template = (9,2)
ekg_template = (9,0)

corrmap(icas, template=eog_template, show=False,label="eog", 
            threshold=0.9, ch_type='mag',plot=False)

sources = []
for idx,ica in enumerate(icas):
    source = ica.get_sources(inst=epos[idx])
#    source.picks = np.array(range(ica.n_components))
    eog_comps = ica.labels_["eog"]
    comp_names = [source.ch_names[x] for x in eog_comps]
    sources.append(source.pick_channels(comp_names))
#    if comp_names:
#        sources.append(source.pick_channels(comp_names))
#    else:
#        sources.append(None)

#epos = []
#for sub in subjs:
#    for run in runs:
#        epos.append(mne.read_epochs(f)) # now reload the epos without interpolated channels
#
#for source_idx,source in enumerate(sources):
#    if source is not None:
#        sub_idx = 1
#        data = source.get_data()
#        goods = []
#        for e_idx in range(data.shape[0]):
#            std = np.std(data[e_idx,0,:])
#            if std < 0.8:
#                goods.append(e_idx)
#        new_epo = epos[source_idx][goods]
##       viz
##       fig = plt.figure()
##       plt.subplot(8,10,sub_idx)
##       color = "blue" if std<0.8 else "red"
##       plt.plot(data[e_idx,0,:],color=color)
##       plt.ylim((-10,10))
##       plt.text(400,7,str(std)[:4])
##       sub_idx += 1
#    else:
#        new_epo = epos[source_idx].copy()
#    new_epo.save("{a}{b}_a-epo.fif".format(a=root_dir,b=id_list[source_idx]))

        

#fig_template, fig_detected = corrmap(icas, template=ekg_template, show=False,
#                                     label="ekg", threshold=0.7, ch_type='mag',
#                                     plot=False)




# remove components
#for i_idx,i in enumerate(icas):
#    exclude = i.labels_["eog"].copy()
#    exclude.extend(i.labels_["ekg"].copy())
#    i.apply(epos[i_idx], exclude=exclude)
#    epos[i_idx].save(epos[i_idx].filename[:-7]+"ica-epo.fif")
    
# use components to make artificial EOG, EKG channels

        
    
