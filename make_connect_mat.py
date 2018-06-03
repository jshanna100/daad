import mne
import scipy.sparse

def con_mat_build(mat):
    mat_size = mat.shape[0]
    new_mat_size = mat.shape[0]*6
    new_mat = scipy.sparse.dok_matrix((new_mat_size,new_mat_size))
    
    for i_idx in range(0,new_mat_size,mat_size):
        new_mat[i_idx:i_idx+mat_size,i_idx:i_idx+mat_size] = mat
    for i_idx in range(mat_size,new_mat_size,mat_size):
        new_mat[i_idx-mat_size:i_idx,i_idx:i_idx+mat_size] = mat
        
    return new_mat
    

proc_dir = "../proc/"

filename = "fsaverage-src.fif"

src_l = mne.read_source_spaces(proc_dir+filename)
#src_r = src_l.copy()
#src_l.remove(src_l[1])
#src_r.remove(src_r[0])

cnx_l = mne.spatial_src_connectivity(src_l)
#cnx_r = mne.spatial_src_connectivity(src_r)

#del src_l, src_r

#f_cnx_l = con_mat_build(cnx_l)
scipy.sparse.save_npz("cnx_lh.npz",scipy.sparse.coo_matrix(cnx_l))
#scipy.sparse.save_npz("f_cnx_lh.npz",scipy.sparse.coo_matrix(f_cnx_l))
#del f_cnx_l
#f_cnx_r = con_mat_build(cnx_r)
#scipy.sparse.save_npz("cnx_rh.npz",scipy.sparse.coo_matrix(cnx_r))
#scipy.sparse.save_npz("f_cnx_rh.npz",scipy.sparse.coo_matrix(f_cnx_r))
#del f_cnx_r



