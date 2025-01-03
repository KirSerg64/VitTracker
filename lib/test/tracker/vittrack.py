# from lib.test.tracker.basetracker import BaseTracker
# import torch
# from lib.train.data.processing_utils import sample_target
# # for debug
# import cv2
# import os
# import lib.models.vt.levit_utils as utils
# from lib.utils.merge import merge_template_search
# # from lib.models.vittrack import build_vittrack_baseline
# from lib.models.vittrack import build_vittrack
# from lib.test.tracker.data_utils import Preprocessor
# from lib.utils.box_ops import clip_box


# class VitTrack(BaseTracker):
#     def __init__(self, params, dataset_name):
#         super(VitTrack, self).__init__(params)
#         network = build_vittrack(params.cfg)
#         network.load_state_dict(torch.load(self.params.checkpoint, map_location='cpu')['net'], strict=True)
#         self.cfg = params.cfg
#         if "LeViT" in self.cfg.MODEL.BACKBONE.TYPE:
#             # merge conv+bn to one operator
#             utils.replace_batchnorm(network.backbone.body)
#         self.network = network.cuda()
#         # self.network = network
#         self.network.eval()
#         self.preprocessor = Preprocessor()
#         self.state = None
#         # for debug
#         # self.debug = False
#         self.debug = params.debug
#         self.frame_id = 0
#         if self.debug == 2:
#             save_dir = "/home/cx/cx1/MSRA/CLOUD/MyExperiments/PlayGround/vis_results"
#             self.save_dir = os.path.join(save_dir, params.yaml_name)
#             if not os.path.exists(self.save_dir):
#                 os.makedirs(self.save_dir)
#         # for save boxes from all queries
#         self.save_all_boxes = params.save_all_boxes
#         self.z_dict1 = {}

#     def initialize(self, image, info: dict):
#         # forward the template once
#         # info['init_bbox']: list [x0,y0,w,h] example: [367.0, 101.0, 41.0, 16.0]
#         if self.debug == 2:
#             self.save_path = os.path.join(self.save_dir, info['seq_name'])
#             if not os.path.exists(self.save_path):
#                 os.makedirs(self.save_path)
#         if self.cfg.DATA.TEMPLATE.PREPROCESS == 'rect':
#             import cv2
#             x1, y1, w, h = info['init_bbox']
#             cv2.rectangle(image, (int(x1), int(y1)), (int(x1 + w), int(y1 + h)), color=(0, 0, 255), thickness=3)
#             # cv2.imshow('img', image)
#             # cv2.waitKey(0)
#             # cv2.destroyAllWindows()
#         z_patch_arr, resize_factor, z_amask_arr = sample_target(image, info['init_bbox'], self.params.template_factor,
#                                                     output_sz=self.params.template_size)
#         # cv2.imshow('img', z_patch_arr)
#         # cv2.waitKey(0)
#         # cv2.destroyAllWindows()
#         self.z_patch_arr = z_patch_arr
#         template = self.preprocessor.process(z_patch_arr, z_amask_arr)
#         with torch.no_grad():
#             self.z_dict1 = template
#         # save states
#         self.init_bbox = info['init_bbox']
#         self.state = info['init_bbox']
#         self.frame_id = 0
#         if self.save_all_boxes:
#             '''save all predicted boxes'''
#             all_boxes_save = info['init_bbox'] * self.cfg.MODEL.NUM_OBJECT_QUERIES
#             return {"all_boxes": all_boxes_save}

#     def track(self, image, info: dict = None):
#         H, W, _ = image.shape
#         self.frame_id += 1
#         x_patch_arr, resize_factor, x_amask_arr = sample_target(image, self.state, self.params.search_factor,
#                                                                 output_sz=self.params.search_size)  # (x1, y1, w, h)
#         search = self.preprocessor.process(x_patch_arr, x_amask_arr)
#         with torch.no_grad():
#             x_dict = search
#             out_dict, _ = self.network.forward(
#                 z=self.z_dict1.tensors, x=x_dict.tensors, template_anno=torch.tensor(self.init_bbox).view(-1, 4).cuda())

#         pred_boxes = out_dict['pred_boxes'].view(-1, 4)
#         # Baseline: Take the mean of all pred boxes as the final result
#         pred_box = (pred_boxes.mean(dim=0) * self.params.search_size / resize_factor).tolist()  # (cx, cy, w, h) [0,1]
#         # get the final box result
#         self.state = clip_box(self.map_box_back(pred_box, resize_factor), H, W, margin=10)
#         # self.state: list [x0,y0,w,h,] example: [365.4537048339844, 102.24719142913818, 47.13159942626953, 15.523386001586914]

#         # for debug
#         if self.debug == 2:
#             x1, y1, w, h = self.state
#             image_BGR = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
#             cv2.rectangle(image_BGR, (int(x1),int(y1)), (int(x1+w),int(y1+h)), color=(0,0,255), thickness=2)
#             save_path = os.path.join(self.save_path, "%04d.jpg" % self.frame_id)
#             cv2.imwrite(save_path, image_BGR)
#         elif self.debug == 1:
#             x1, y1, w, h = self.state
#             image_BGR = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
#             cv2.rectangle(image_BGR, (int(x1),int(y1)), (int(x1+w),int(y1+h)), color=(0,0,255), thickness=2)
#             cv2.imshow('vis', image_BGR)
#             cv2.waitKey(1)
#             # if cv2.waitKey() & 0xFF == ord('q'):
#             #     pass
#         if self.save_all_boxes:
#             '''save all predictions'''
#             all_boxes = self.map_box_back_batch(pred_boxes * self.params.search_size / resize_factor, resize_factor)
#             all_boxes_save = all_boxes.view(-1).tolist()  # (4N, )
#             return {"target_bbox": self.state,
#                     "all_boxes": all_boxes_save}
#         else:
#             return {"target_bbox": self.state}

#     def map_box_back(self, pred_box: list, resize_factor: float):
#         cx_prev, cy_prev = self.state[0] + 0.5 * self.state[2], self.state[1] + 0.5 * self.state[3]
#         cx, cy, w, h = pred_box
#         half_side = 0.5 * self.params.search_size / resize_factor
#         cx_real = cx + (cx_prev - half_side)
#         cy_real = cy + (cy_prev - half_side)
#         return [cx_real - 0.5 * w, cy_real - 0.5 * h, w, h]

#     def map_box_back_batch(self, pred_box: torch.Tensor, resize_factor: float):
#         cx_prev, cy_prev = self.state[0] + 0.5 * self.state[2], self.state[1] + 0.5 * self.state[3]
#         cx, cy, w, h = pred_box.unbind(-1) # (N,4) --> (N,)
#         half_side = 0.5 * self.params.search_size / resize_factor
#         cx_real = cx + (cx_prev - half_side)
#         cy_real = cy + (cy_prev - half_side)
#         return torch.stack([cx_real - 0.5 * w, cy_real - 0.5 * h, w, h], dim=-1)


# def get_tracker_class():
#     return VitTrack
