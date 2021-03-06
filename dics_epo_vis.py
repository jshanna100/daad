import mne

sub = "VP4"
typ = "a"
sides = ["links","rechts"]
runs = ["1","2","3"]
proc_dir = "../proc/stcs/"
subjects_dir = "/home/jeff/freesurfer/subjects"
subject = "fsaverage"

side_list = []
for side in sides:
    stc_list = []
    for run in runs:
        stc_list.append(mne.read_source_estimate("{a}{b}_{c}_{d}_{e}-lh.stc".format(
                a=proc_dir,b=sub,c=run,d=side,e=typ)))
    stc = stc_list[0]
    for s in stc_list[1:]:
        stc += s
    stc /= len(stc_list)
    side_list.append(stc)
subtract_last = side_list[0] - side_list[1]

#side_list[0].plot(subjects_dir=subjects_dir,subject=subject,hemi="both",colormap="mne",time_viewer=True)
#side_list[1].plot(subjects_dir=subjects_dir,subject=subject,hemi="both",colormap="mne",time_viewer=True)
subtract_last.plot(subjects_dir=subjects_dir,subject=subject,hemi="both",colormap="mne",time_viewer=True)


#for sub in ["VP3","VP3","VP4","VP5","VP6","VP7"]:
#    side_list = []
#    for side in sides:
#        stc_list = []
#        for run in runs:
#            stc_list.append(mne.read_source_estimate("{a}{b}_{c}_{d}_{e}-lh.stc".format(
#                    a=proc_dir,b=sub,c=run,d=side)))
#        stc = stc_list[0]
#        for s in stc_list[1:]:
#            stc += s
#        stc /= len(stc_list)
#        side_list.append(stc)
#    subtract = (side_list[0] - side_list[1])
#    subtract_last += subtract
#subtract_last /= 7
#subtract_last.plot(subjects_dir=subjects_dir,subject=subject,hemi="both",colormap="mne",time_viewer=True)
    