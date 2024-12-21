from lib.test.evaluation.environment import EnvSettings

def local_env_settings():
    settings = EnvSettings()

    # Set your local paths here.

    settings.davis_dir = ''
    settings.got10k_lmdb_path = '/src/vitTracker/data/got10k_lmdb'
    settings.got10k_path = '/src/vitTracker/data/got10k'
    settings.got_packed_results_path = ''
    settings.got_reports_path = ''
    settings.itb_path = '/src/vitTracker/data/itb'
    settings.lasot_extension_subset_path_path = '/src/vitTracker/data/lasot_extension_subset'
    settings.lasot_lmdb_path = '/src/vitTracker/data/lasot_lmdb'
    settings.lasot_path = '/src/vitTracker/data/lasot'
    settings.network_path = '/src/vitTracker/output/test/networks'    # Where tracking networks are stored.
    settings.nfs_path = '/src/vitTracker/data/nfs'
    settings.otb_path = '/src/vitTracker/data/otb'
    settings.prj_dir = '/src/vitTracker'
    settings.result_plot_path = '/src/vitTracker/output/test/result_plots'
    settings.results_path = '/src/vitTracker/output/test/tracking_results'    # Where to store tracking results
    settings.save_dir = '/src/vitTracker/output'
    settings.segmentation_path = '/src/vitTracker/output/test/segmentation_results'
    settings.tc128_path = '/src/vitTracker/data/TC128'
    settings.tn_packed_results_path = ''
    settings.tnl2k_path = '/src/vitTracker/data/tnl2k'
    settings.tpl_path = ''
    settings.trackingnet_path = '/src/vitTracker/data/trackingnet'
    settings.uav_path = '/src/vitTracker/data/uav'
    settings.vot18_path = '/src/vitTracker/data/vot2018'
    settings.vot22_path = '/src/vitTracker/data/vot2022'
    settings.vot_path = '/src/vitTracker/data/VOT2019'
    settings.youtubevos_dir = ''

    return settings

