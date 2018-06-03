import mne
from mne.stats import spatio_temporal_cluster_test
from scipy.stats import ttest_rel, t
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

def mass_t(A,B):
    t_val,p_val = ttest_rel(A,B)
    return t_val

root_dir = "d:/nadia_daad/proc/"
subjs = ["VP1","VP2","VP3","VP4","VP5","VP6","VP7"]
runs = ["1","2","3"]

freqs = np.array(range(8,13))
n_cycles = freqs / 2.
trig_inds = [["143","128","129","130"],["131","132","133","134"]]
sides = ["links","rechts"]
p_accept = 0.05
threshold = 0.95

subjs = ["VP1"]

epos = []
for sub in subjs:
    sub_epos = []
    for run_idx,run in enumerate(runs):
        f = "{a}{b}_{c}-ica-epo.fif".format(a=root_dir,b=sub,c=run)
        epo = mne.read_epochs(f)
        epo = mne.epochs.combine_event_ids(epo,trig_inds[0],{"links":1})
        epo = mne.epochs.combine_event_ids(epo,trig_inds[1],{"rechts":2})
        if run_idx == 0:
            dev_head_t = epo.info["dev_head_t"]
        else:
            epo.info["dev_head_t"] = dev_head_t
        sub_epos.append(epo)
    epo = mne.concatenate_epochs(sub_epos)
    epo.equalize_event_counts(sides)
    connectivity, ch_names = mne.channels.find_ch_connectivity(
            epo.info, ch_type='mag')
    X = [np.zeros((0,len(epo.times),
                   len(mne.pick_types(epo.info,"mag")))) for s in sides]
    data = []
    for s_idx,s in enumerate(sides):
        power = mne.time_frequency.tfr_morlet(
                epo[s], freqs=freqs, n_cycles=n_cycles,return_itc=False,average=False)       
        power.apply_baseline((None,0))
        # find maximal frequency
#        temp_mean = np.mean(np.mean(power.data,axis=0),axis=0)
#        time_inds = epo.time_as_index((0.2,2.27))
#        temp_sums = np.sum(temp_mean[:,time_inds[0]:time_inds[1]],axis=1)
#        highest_freq = np.argsort(temp_sums)[-1]
#        data.append(np.transpose(power.data[:,:,highest_freq,:],(0,2,1)))
        
        # use mean frequency
        data.append(np.transpose(np.mean(power.data,axis=2),(0,2,1)))

    threshold = t.interval(threshold,data[0].shape[0])[1]
    T_obs, clusters, p_values, _ = spatio_temporal_cluster_test(
            data, threshold=threshold, n_permutations=300, stat_fun=mass_t,
            connectivity=connectivity, n_jobs=1)
    
    good_cluster_inds = np.where(p_values < p_accept)[0]
    
    # visualise
    
    colors = {"links":"crimson","rechts":"steelblue"}
    evo = epo.average()
    pos = mne.find_layout(evo.info).pos
    evokeds = {"links":mne.EvokedArray(np.mean(data[0],axis=0).T,evo.info,tmin=-1,comment="links"),
               "rechts":mne.EvokedArray(np.mean(data[1],axis=0).T,evo.info,tmin=-1,comment="rechts")}
    
    for i_clu, clu_idx in enumerate(good_cluster_inds):
        # unpack cluster information, get unique indices
        time_inds, space_inds = np.squeeze(clusters[clu_idx])
        ch_inds = np.unique(space_inds)
        time_inds = np.unique(time_inds)
    
        # get topography for F stat
        f_map = T_obs[time_inds, ...].mean(axis=0)
    
        # get signals at the sensors contributing to the cluster
        sig_times = evo.times[time_inds]
    
        # create spatial mask
        mask = np.zeros((f_map.shape[0], 1), dtype=bool)
        mask[ch_inds, :] = True
    
        # initialize figure
        fig, ax_topo = plt.subplots(1, 1, figsize=(10, 3))
        fig.suptitle(sub)
    
        # plot average test statistic and mark significant sensors
        image, _ = mne.viz.plot_topomap(f_map, pos, mask=mask, axes=ax_topo, cmap='Reds',
                                vmin=np.min, vmax=np.max, show=False)
    
        # create additional axes (for ERF and colorbar)
        divider = make_axes_locatable(ax_topo)
    
        # add axes for colorbar
        ax_colorbar = divider.append_axes('right', size='5%', pad=0.05)
        plt.colorbar(image, cax=ax_colorbar)
        ax_topo.set_xlabel(
            'Averaged t-map ({:0.3f} - {:0.3f} s)'.format(*sig_times[[0, -1]]))
    
        # add new axis for time courses and plot time courses
        ax_signals = divider.append_axes('right', size='300%', pad=1.2)
        title = 'Cluster #{0}, {1} sensor'.format(i_clu + 1, len(ch_inds))
        if len(ch_inds) > 1:
            title += "s (mean)"
        mne.viz.plot_compare_evokeds(evokeds, title=title, picks=ch_inds, axes=ax_signals,
                             colors=colors, show=False, split_legend=True, truncate_yaxis='max_ticks')
    
        # plot temporal cluster extent
        ymin, ymax = ax_signals.get_ylim()
        ax_signals.fill_betweenx((ymin, ymax), sig_times[0], sig_times[-1],
                                 color='orange', alpha=0.3)
    
        # clean up viz
        mne.viz.tight_layout(fig=fig)
        fig.subplots_adjust(bottom=.05)
        plt.show()