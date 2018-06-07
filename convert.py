import mne
from anoar import BadChannelFind

root_dir = "../"
subjs = ["VP1","VP2","VP3","VP4","VP5","VP6","VP7"]
runs = ["1","2","3"]

config_file = "config"
headshape_file = "hs_file"
raw_file = "c,rfhp0.1Hz"

#subjs = ["VP1"]
#runs = ["1"]

for sub in subjs:
    for run in runs:
        rawdir = "{a}raw/{b}/Run{c}/".format(a=root_dir,b=sub,c=run)
        raw = mne.io.read_raw_bti(rawdir+raw_file,config_fname=rawdir+config_file,
                                   head_shape_fname=rawdir+headshape_file,preload=True)
        picks = mne.pick_types(raw.info,meg=False,ref_meg=True,misc=True)
        temp = [raw.info["ch_names"][x] for x in picks]
        raw.drop_channels(temp)

        filt = raw.filter(h_freq=20,l_freq=1,n_jobs=1)
        filt = filt.notch_filter([50])
        picks = mne.pick_types(raw.info,meg=True)
        bcf = BadChannelFind(picks,thresh=0.6,twin_len=3)
        bad_chans = bcf.recommend(filt)
        filt.info['bads'] = bad_chans
        
#        raw_sss = mne.preprocessing.maxwell_filter(
#                filt,destination=(0.0032,-0.03037,0.069718),ignore_ref=True)
        filt.save("{a}proc/{b}_{c}-raw.fif".format(a=root_dir,b=sub,c=run),
                  overwrite=True)