# -*- coding: utf-8 -*-
#
# Modified by Peize Sun, Rufeng Zhang
# Contact: {sunpeize, cxrfzhang}@foxmail.com
#
# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from detectron2.config import CfgNode as CN


def add_custom_config(cfg, model_name):
    if model_name == "fsdet":
        return add_fsdet_config(cfg)
    elif model_name == "gdl":
        return add_gdl_config(cfg)
    elif model_name == "sparsercnn":
        return add_sparsercnn_config(cfg)
    elif model_name == "fsce":
        return add_fsce_config(cfg)

def add_fsdet_config(cfg):
    return cfg

def add_fsce_config(cfg):
    cfg.MODEL.PROPOSAL_GENERATOR.NAME = "RPN_FSCE"
    
    cfg.MODEL.ROI_BOX_HEAD.CONTRASTIVE_BRANCH = CN()
    cfg.MODEL.ROI_BOX_HEAD.CONTRASTIVE_BRANCH.MLP_FEATURE_DIM = 128
    cfg.MODEL.ROI_BOX_HEAD.CONTRASTIVE_BRANCH.TEMPERATURE = 0.1
    cfg.MODEL.ROI_BOX_HEAD.CONTRASTIVE_BRANCH.LOSS_WEIGHT = 1.0
    cfg.MODEL.ROI_BOX_HEAD.BOX_REG_WEIGHT = 1.0
    cfg.MODEL.ROI_BOX_HEAD.BOX_CLS_WEIGHT = 1.0
    cfg.MODEL.ROI_BOX_HEAD.CONTRASTIVE_BRANCH.DECAY = CN({"ENABLED": False})
    cfg.MODEL.ROI_BOX_HEAD.CONTRASTIVE_BRANCH.DECAY.STEPS = [8000, 16000]
    cfg.MODEL.ROI_BOX_HEAD.CONTRASTIVE_BRANCH.DECAY.RATE = 0.2
    cfg.MODEL.ROI_BOX_HEAD.CONTRASTIVE_BRANCH.IOU_THRESHOLD = 0.5
    cfg.MODEL.ROI_BOX_HEAD.CONTRASTIVE_BRANCH.LOSS_VERSION = 'V1'
    cfg.MODEL.ROI_BOX_HEAD.CONTRASTIVE_BRANCH.REWEIGHT_FUNC = 'none'
    cfg.MODEL.ROI_BOX_HEAD.CONTRASTIVE_BRANCH.HEAD_ONLY = False

    return cfg

def add_gdl_config(cfg):
    """
    Add config for GDL. 
    """

    cfg.MODEL.ROI_HEADS.NAME = "Res5ROIHeads"
    cfg.MODEL.ROI_HEADS.FREEZE_FEAT = False
    cfg.MODEL.ROI_HEADS.ENABLE_DECOUPLE = False
    cfg.MODEL.ROI_HEADS.BACKWARD_SCALE = 1.0
    cfg.MODEL.ROI_HEADS.OUTPUT_LAYER = "FastRCNNOutputLayers"
    cfg.MODEL.ROI_HEADS.CLS_DROPOUT = False
    cfg.MODEL.ROI_HEADS.DROPOUT_RATIO = 0.8
    cfg.MODEL.ROI_BOX_HEAD.POOLER_RESOLUTION = 7
    
    cfg.TEST.PCB_ENABLE = False
    cfg.TEST.PCB_MODELTYPE = 'resnet'             # res-like
    cfg.TEST.PCB_MODELPATH = ""
    cfg.TEST.PCB_ALPHA = 0.50
    cfg.TEST.PCB_UPPER = 1.0
    cfg.TEST.PCB_LOWER = 0.05 
    cfg.SOLVER.WEIGHT_DECAY = 5e-5

    cfg.MODEL.PROPOSAL_GENERATOR.FREEZE = False
    cfg.MODEL.PROPOSAL_GENERATOR.ENABLE_DECOUPLE = False
    cfg.MODEL.PROPOSAL_GENERATOR.BACKWARD_SCALE=1.0

    cfg.MODEL.BACKBONE.FREEZE_AT = 3
    return cfg

def add_sparsercnn_config(cfg):
    """
    Add config for SparseRCNN.
    """
    cfg.MODEL.SparseRCNN = CN()
    cfg.MODEL.SparseRCNN.NUM_CLASSES = 80
    cfg.MODEL.SparseRCNN.NUM_PROPOSALS = 300

    # RCNN Head.
    cfg.MODEL.SparseRCNN.NHEADS = 8
    cfg.MODEL.SparseRCNN.DROPOUT = 0.0
    cfg.MODEL.SparseRCNN.DIM_FEEDFORWARD = 2048
    cfg.MODEL.SparseRCNN.ACTIVATION = 'relu'
    cfg.MODEL.SparseRCNN.HIDDEN_DIM = 256
    cfg.MODEL.SparseRCNN.NUM_CLS = 1
    cfg.MODEL.SparseRCNN.NUM_REG = 3
    cfg.MODEL.SparseRCNN.NUM_HEADS = 6

    # Dynamic Conv.
    cfg.MODEL.SparseRCNN.NUM_DYNAMIC = 2
    cfg.MODEL.SparseRCNN.DIM_DYNAMIC = 64

    # Loss.
    cfg.MODEL.SparseRCNN.CLASS_WEIGHT = 2.0
    cfg.MODEL.SparseRCNN.GIOU_WEIGHT = 2.0
    cfg.MODEL.SparseRCNN.L1_WEIGHT = 5.0
    cfg.MODEL.SparseRCNN.DEEP_SUPERVISION = True
    cfg.MODEL.SparseRCNN.NO_OBJECT_WEIGHT = 0.1

    # Focal Loss.
    cfg.MODEL.SparseRCNN.USE_FOCAL = True
    cfg.MODEL.SparseRCNN.ALPHA = 0.25
    cfg.MODEL.SparseRCNN.GAMMA = 2.0
    cfg.MODEL.SparseRCNN.PRIOR_PROB = 0.01

    # Optimizer.
    cfg.SOLVER.OPTIMIZER = "ADAMW"
    cfg.SOLVER.BACKBONE_MULTIPLIER = 1.0
    return cfg