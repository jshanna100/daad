import mne

root_dir = "../proc/stcs/"
runs = ["1","2","3"]
sides = ["links","rechts"]
hemis = ["lh","rh"]
subjects_dir = "../subjects/"

sub = "VP1"
hemis = ["lh"]
#runs = ["1"]
freq = 8

fig_idx = 0
for run in runs:
    for hemi in hemis:
        filename = "{a}{b}_{c}_{d}-{e}.stc".format(a=root_dir,b=sub,c=run,d=side,e=hemi)
        stc = mne.read_source_estimate(filename)
        freq_num = len(stc.times)
        for freq_idx in range(freq_num):
            message = 'DICS source power at {:1.1f} Hz'.format(stc.times[freq_idx]*1e3)
            brain = stc.plot(surface='inflated', hemi=hemi, subjects_dir=subjects_dir,
                     time_label=message, initial_time=stc.times[freq_idx], 
                     figure=fig_idx, subject="fsaverage")
            brain.show_view('lateral')
            fig_idx += 1
        