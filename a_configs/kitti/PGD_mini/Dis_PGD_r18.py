_base_ = ['./kitti-mono3d.py']
model = dict(
    type='DIS_PGD',
    tea_pretrained="/workspace/mmdetection3d-master/work_dirs/pgd_101_2/epoch_48.pth",
    # todo student model
    backbone=dict(
        type='ResNet',
        depth=18,
        num_stages=4,
        out_indices=(0, 1, 2, 3),
        frozen_stages=0,
        norm_cfg=dict(type='BN', requires_grad=True),
        norm_eval=True,
        style='pytorch',
        init_cfg=dict(
            type='Pretrained',
            checkpoint='/home/pretrained model/resnet18-5c106cde.pth')
        ),
    neck=dict(
        type='FPN',
        in_channels=[64, 128, 256, 512],
        out_channels=256,
        start_level=0,
        add_extra_convs='on_output',
        num_outs=4,
        relu_before_extra_convs=True),
    bbox_head=dict(
        type='PGDHeadDIS',
        num_classes=3,
        in_channels=256,
        stacked_convs=2,
        feat_channels=256,
        bbox_code_size=7,
        use_onlyreg_proj=True,
        use_direction_classifier=True,
        diff_rad_by_sin=True,
        pred_attrs=False,
        pred_velo=False,
        pred_bbox2d=True,
        pred_keypoints=True,
        dir_offset=0.7854,  # pi/4
        strides=[4, 8, 16, 32],
        regress_ranges=((-1, 64), (64, 128), (128, 256), (256, 1e8)),
        group_reg_dims=(2, 1, 3, 1, 16, 4),  # offset, depth, size, rot, kpts, bbox2d
        cls_branch=(256,),
        reg_branch=(
            (256, ),  # offset
            (256, ),  # depth
            (256, ),  # size
            (256, ),  # rot
            (256, ),  # kpts
            (256, )  # bbox2d
        ),
        centerness_branch=(256,),
        dir_branch=(256,),
        attr_branch=(256,),
        norm_on_bbox=True,
        centerness_on_reg=True,
        center_sampling=True,
        conv_bias=True,
        dcn_on_last_conv=True,
        use_depth_classifier=True,
        depth_branch=(256,),
        depth_range=(0, 70),
        depth_unit=10,
        division='uniform',
        depth_bins=8,
        loss_cls=dict(
            type='FocalLoss',
            use_sigmoid=True,
            gamma=2.0,
            alpha=0.25,
            loss_weight=1.0),
        weight_dim=1,
        loss_bbox=dict(type='SmoothL1Loss', beta=1.0 / 9.0, loss_weight=1.0),
        loss_dir=dict(
            type='CrossEntropyLoss', use_sigmoid=False, loss_weight=1.0),
        loss_attr=dict(
            type='CrossEntropyLoss', use_sigmoid=False, loss_weight=1.0),
        loss_centerness=dict(
            type='CrossEntropyLoss', use_sigmoid=True, loss_weight=1.0),
        loss_depth=dict(
            type='UncertainSmoothL1Loss', alpha=1.0, beta=3.0,
            loss_weight=1.0),
        bbox_coder=dict(
            type='PGDBBoxCoder',
            base_depths=((28.01, 16.32),),
            base_dims=((0.8, 1.73, 0.6), (1.76, 1.73, 0.6), (3.9, 1.56, 1.6)),
            code_size=7)),
    # todo teacher model
    tea_model=dict(type='FCOSMono3D',
    backbone=dict(
        type='ResNet',
        depth=101,
        num_stages=4,
        out_indices=(0, 1, 2, 3),
        frozen_stages=0,
        norm_cfg=dict(type='BN', requires_grad=True),
        norm_eval=True,
        style='pytorch',
        init_cfg=dict(
            type='Pretrained',
            checkpoint='/home/pretrained model/resnet101_caffe-3ad79236.pth')
        ),
    neck=dict(
        type='FPN',
        in_channels=[256, 512, 1024, 2048],
        out_channels=256,
        start_level=0,
        add_extra_convs='on_output',
        num_outs=4,
        relu_before_extra_convs=True),
    bbox_head=dict(
        type='PGDHeadDIS',
        num_classes=3,
        in_channels=256,
        stacked_convs=2,
        feat_channels=256,
        bbox_code_size=7,
        use_onlyreg_proj=True,
        use_direction_classifier=True,
        diff_rad_by_sin=True,
        pred_attrs=False,
        pred_velo=False,
        pred_bbox2d=True,
        pred_keypoints=True,
        dir_offset=0.7854,  # pi/4
        strides=[4, 8, 16, 32],
        regress_ranges=((-1, 64), (64, 128), (128, 256), (256, 1e8)),
        group_reg_dims=(2, 1, 3, 1, 16, 4),  # offset, depth, size, rot, kpts, bbox2d
        cls_branch=(256,),
        reg_branch=(
            (256, ),  # offset
            (256, ),  # depth
            (256, ),  # size
            (256, ),  # rot
            (256, ),  # kpts
            (256, )  # bbox2d
        ),
        centerness_branch=(256,),
        dir_branch=(256,),
        attr_branch=(256,),
        loss_cls=dict(
            type='FocalLoss',
            use_sigmoid=True,
            gamma=2.0,
            alpha=0.25,
            loss_weight=1.0),
        weight_dim=1,
        loss_bbox=dict(type='SmoothL1Loss', beta=1.0 / 9.0, loss_weight=1.0),
        loss_dir=dict(
            type='CrossEntropyLoss', use_sigmoid=False, loss_weight=1.0),
        loss_attr=dict(
            type='CrossEntropyLoss', use_sigmoid=False, loss_weight=1.0),
        loss_centerness=dict(
            type='CrossEntropyLoss', use_sigmoid=True, loss_weight=1.0),
        loss_depth=dict(
            type='UncertainSmoothL1Loss', alpha=1.0, beta=3.0,
            loss_weight=1.0),
        norm_on_bbox=True,
        centerness_on_reg=True,
        center_sampling=True,
        conv_bias=True,
        dcn_on_last_conv=True,
        use_depth_classifier=True,
        depth_branch=(256,),
        depth_range=(0, 70),
        depth_unit=10,
        division='uniform',
        depth_bins=8,
        bbox_coder=dict(
            type='PGDBBoxCoder',
            base_depths=((28.01, 16.32),),
            base_dims=((0.8, 1.73, 0.6), (1.76, 1.73, 0.6), (3.9, 1.56, 1.6)),
            code_size=7))),
    # todo train_test_cfg
    train_cfg=dict(
        allowed_border=0,
        code_weight=[
        1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2,
        0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 1.0, 1.0, 1.0, 1.0],
        pos_weight=-1,
        debug=False),
    test_cfg=dict(
        use_rotate_nms=True,
        nms_across_levels=False,
        nms_pre=100,
        nms_thr=0.8,
        score_thr=0.001,
        min_bbox_size=0,
        max_per_img=20))

class_names = ['Pedestrian', 'Cyclist', 'Car']
img_norm_cfg = dict(
    mean=[103.530, 116.280, 123.675], std=[1.0, 1.0, 1.0], to_rgb=False)
train_pipeline = [
    dict(type='LoadImageFromFileMono3D'),
    dict(
        type='LoadAnnotations3D',
        with_bbox=True,
        with_label=True,
        with_attr_label=False,
        with_bbox_3d=True,
        with_label_3d=True,
        with_bbox_depth=True),
    dict(type='Resize', img_scale=(1242, 375), keep_ratio=True),
    dict(type='RandomFlip3D', flip_ratio_bev_horizontal=0.5),
    dict(type='Normalize', **img_norm_cfg),
    dict(type='Pad', size_divisor=32),
    dict(type='DefaultFormatBundle3D', class_names=class_names),
    dict(
        type='Collect3D',
        keys=[
            'img', 'gt_bboxes', 'gt_labels', 'gt_bboxes_3d', 'gt_labels_3d',
            'centers2d', 'depths'
        ]),
]
test_pipeline = [
    dict(type='LoadImageFromFileMono3D'),
    dict(
        type='MultiScaleFlipAug',
        scale_factor=1.0,
        flip=False,
        transforms=[
            dict(type='RandomFlip3D'),
            dict(type='Normalize', **img_norm_cfg),
            dict(type='Pad', size_divisor=32),
            dict(
                type='DefaultFormatBundle3D',
                class_names=class_names,
                with_label=False),
            dict(type='Collect3D', keys=['img']),
        ])
]
data = dict(
    samples_per_gpu=9,
    workers_per_gpu=3,
    train=dict(pipeline=train_pipeline),
    val=dict(pipeline=test_pipeline),
    test=dict(pipeline=test_pipeline))
# optimizer
optimizer = dict(
    lr=0.001, paramwise_cfg=dict(bias_lr_mult=2., bias_decay_mult=0.))
optimizer_config = dict(
    _delete_=True, grad_clip=dict(max_norm=35, norm_type=2))
# learning policy
lr_config = dict(
    policy='step',
    warmup='linear',
    warmup_iters=500,
    warmup_ratio=1.0 / 3,
    step=[32, 44])
total_epochs = 48
runner = dict(type='EpochBasedRunner', max_epochs=48)
evaluation = dict(interval=2)
checkpoint_config = dict(interval=8)

