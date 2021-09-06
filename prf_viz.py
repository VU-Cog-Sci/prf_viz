import os
import h5py
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import nilearn as nl
import nilearn.surface as surface
import cortex as cx

# from prfpy.rf import *
# from prfpy.timecourse import *
# from prfpy.stimulus import PRFStimulus2D
# from prfpy.model import Iso2DGaussianModel
from prfpy.rf import gauss2D_iso_cart

hemis = ['L', 'R']
prf_par_names = ['x', 'y', 'size', 'beta', 'baseline', 'rsq']

subject = 'hcp_999999'
data_dir = '/Users/knapen/projects/prf_viz/data'
tc_gii_filename = 'tfMRI_{run_name}_7T_AP_Atlas_1.6mm_MSMAll_hp2000_clean.dtseries_sg_psc_{hemi}.gii'
prf_gii_filename = 'V12_retmap_results_polar_bar_iterative.scalar.{hemi}.gii'
design_matrix_filename = '7T_{run_name}_small.hdf5'

run_name = 'RETBAR1'
flatmap_height = 2048

vf_extent = [-10, 10]
nr_vf_pix = 100
prf_space_x, prf_space_y = np.meshgrid(np.linspace(vf_extent[0], vf_extent[1], nr_vf_pix, endpoint=True),
                                       np.linspace(vf_extent[0], vf_extent[1], nr_vf_pix, endpoint=True))

###################################################################################################
###################################################################################################
#######
# load data
#######
###################################################################################################
###################################################################################################

tc_data = np.vstack([surface.load_surf_data(os.path.join(data_dir, tc_gii_filename.format(
    run_name=run_name, hemi=hemi))) for hemi in hemis])

prf_pars = np.vstack([surface.load_surf_data(os.path.join(
    data_dir, prf_gii_filename.format(hemi=hemi))) for hemi in hemis])
prf_pars_df = pd.DataFrame(prf_pars, columns=prf_par_names)

with h5py.File(os.path.join(data_dir, design_matrix_filename.format(run_name=run_name)), 'r') as f:
    design_matrix = np.array(f.get('stim'))

###################################################################################################
###################################################################################################
#######
# create pycortex flatmap info
#######
###################################################################################################
###################################################################################################


angs_n = ((np.pi+np.angle(prf_pars_df['y'] +
                          prf_pars_df['x']*1j)) % (2*np.pi))/(2*np.pi)
rsq_mask = np.array(prf_pars_df['rsq'])
prf_size = np.array(prf_pars_df['size'])

polar_v = cx.Vertex2D(dim1=angs_n, dim2=rsq_mask, subject=subject,
                      cmap='Retinotopy_HSV_alpha', vmin=0, vmax=1.0, vmin2=0.15, vmax2=0.99)
size_v = cx.Vertex2D(dim1=prf_size, dim2=rsq_mask, subject=subject,
                     cmap='hot_alpha', vmin=0, vmax=7.0, vmin2=0.15, vmax2=0.99)

# cx.quickshow(polar_v, with_rois=True, with_curvature=True)
# cx.quickshow(size_v, with_rois=True, with_curvature=True)

###################################################################################################
###################################################################################################
#######
# create figure layout etc.
#######
###################################################################################################
###################################################################################################

full_fig = plt.figure(constrained_layout=True)
gs = full_fig.add_gridspec(3, 3)
flatmap_ax = full_fig.add_subplot(gs[:2, :])
timecourse_ax = full_fig.add_subplot(gs[2, :2])
prf_ax = full_fig.add_subplot(gs[2, 2])

flatmap_ax.set_title('flatmap')
timecourse_ax.set_title('timecourse')
prf_ax.set_title('prf')

###################################################################################################
###################################################################################################
#######
# redraw per-vertex data
#######
###################################################################################################
###################################################################################################


def redraw_vertex_plots(vertex):
    timecourse_ax.plot(tc_data[vertex])
    prf = gauss2D_iso_cart(prf_space_x,
                           prf_space_y,
                           prf_pars_df.iloc[vertex]['x'],
                           prf_pars_df.iloc[vertex]['y'],
                           prf_pars_df.iloc[vertex]['size'])
    prf_ax.imshow(prf, extent=vf_extent+vf_extent)

###################################################################################################
###################################################################################################
#######
# create pycortex vars
#######
###################################################################################################
###################################################################################################


mask, extents = cx.quickflat.utils.get_flatmask(subject, height=flatmap_height)
vc = cx.quickflat.utils._make_vertex_cache(subject, height=flatmap_height)

mask_index = np.zeros(mask.shape)
mask_index[mask] = np.arange(mask.sum())


def onclick(event):
    clicked_vertex = vc[int(mask_index[int(event.xdata), int(event.ydata)])]
    redraw_vertex_plots(clicked_vertex)


cx.quickshow(polar_v, with_rois=False, with_curvature=True, fig=flatmap_ax)

flatmap_ax.canvas.mpl_connect('button_press_event', onclick)
plt.show()
