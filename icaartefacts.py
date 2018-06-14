import mne
from mne.preprocessing.ica import corrmap

root_dir = "../proc/"
subjs = ["VP1","VP2","VP3","VP4","VP5","VP6","VP7"]
runs = ["1","2","3"]

icas = []
epos = []
for sub in subjs:
    for run in runs:
        f = "{a}{b}_{c}-ica.fif".format(a=root_dir,b=sub,c=run)
        icas.append(mne.preprocessing.read_ica(f))
        f = "{a}{b}_{c}-epo.fif".format(a=root_dir,b=sub,c=run)
        epos.append(mne.read_epochs(f).interpolate_bads())
        
eog_template = (9,2)
ekg_template = (9,0)

corrmap(icas, template=eog_template, show=False,label="eog", 
            threshold=0.9, ch_type='mag',plot=False)

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

        
    
