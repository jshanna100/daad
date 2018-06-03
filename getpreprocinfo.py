import mne
from ANOAR import BadChannelFind

root_dir = "d:/nadia_daad/"
subjs = ["VP1","VP2","VP3","VP4","VP5","VP6","VP7"]
runs = ["1","2","3"]

config_file = "config"
headshape_file = "hs_file"
raw_file = ["c,rfhp0.1Hz","e,rfhp1.0Hz,COH","e,rfhp1.0Hz,COH1"]
raw_file = ["c,rfhp0.1Hz"]

bad_list = []
hps = []
for sub in subjs:
    for run in runs:
        for r in raw_file:
            rawdir = "{a}raw/{b}/Run{c}/".format(a=root_dir,b=sub,c=run)
            raw = mne.io.read_raw_bti(rawdir+r,config_fname=rawdir+config_file,
                                       head_shape_fname=rawdir+headshape_file,preload=True)
            hps.append(raw.info["dev_head_t"]["trans"][:3,3]*1000)
hps_arr = np.array(hps)
hps_avg = np.mean(hps_arr,0)

