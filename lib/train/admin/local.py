class EnvironmentSettings:
    def __init__(self):
        self.workspace_dir = '/src/vitTracker'    # Base directory for saving network checkpoints.
        self.tensorboard_dir = '/src/vitTracker/tensorboard'    # Directory for tensorboard files.
        self.pretrained_networks = '/src/vitTracker/pretrained_networks'
        self.lasot_dir = '/src/vitTracker/data/lasot'
        self.got10k_dir = '/src/vitTracker/data/got10k/train'
        self.got10k_val_dir = '/src/vitTracker/data/got10k/val'
        self.lasot_lmdb_dir = '/src/vitTracker/data/lasot_lmdb'
        self.got10k_lmdb_dir = '/src/vitTracker/data/got10k_lmdb'
        self.trackingnet_dir = '/src/vitTracker/data/trackingnet'
        self.trackingnet_lmdb_dir = '/src/vitTracker/data/trackingnet_lmdb'
        self.coco_dir = '/src/vitTracker/data/coco'
        self.coco_lmdb_dir = '/src/vitTracker/data/coco_lmdb'
        self.lvis_dir = ''
        self.sbd_dir = ''
        self.imagenet_dir = '/src/vitTracker/data/vid'
        self.imagenet_lmdb_dir = '/src/vitTracker/data/vid_lmdb'
        self.imagenetdet_dir = ''
        self.ecssd_dir = ''
        self.hkuis_dir = ''
        self.msra10k_dir = ''
        self.davis_dir = ''
        self.youtubevos_dir = ''
