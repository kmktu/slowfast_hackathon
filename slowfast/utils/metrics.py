#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved.

"""Functions for computing metrics."""

import torch
ori_labels = {
    0:"smoking",
    1:"fishing",
    2:"trash_dump",
    3:"wall_over",
    4:"damage_to_facilities",
    5:"banner_action",
    6:"fliers_action",
    7:"tent_setup",
    8:"sit_down_bench",
    9:"sit_down_floor",
    10:"moving",
    11:"stand"
}

def topks_correct(preds, labels, ks, log_txt):
    """
    Given the predictions, labels, and a list of top-k values, compute the
    number of correct predictions for each top-k value.

    Args:
        preds (array): array of predictions. Dimension is batchsize
            N x ClassNum.
        labels (array): array of labels. Dimension is batchsize N.
        ks (list): list of top-k values. For example, ks = [1, 5] correspods
            to top-1 and top-5.

    Returns:
        topks_correct (list): list of numbers, where the `i`-th entry
            corresponds to the number of top-`ks[i]` correct predictions.
    """
    assert preds.size(0) == labels.size(
        0
    ), "Batch dim of predictions and labels must match"

    # Find the top max_k predictions for each sample
    _top_max_k_vals, top_max_k_inds = torch.topk(
        preds, max(ks), dim=1, largest=True, sorted=True
    )
    # i = 0
    # i2 = 0
    log_txt.write("============================================================")
    log_txt.write(" Mini Batch Top5 Preds ")
    log_txt.write("============================================================\n")
    batch_top_1 = 0
    batch_top_5 = 0

    for label_i in range(len(labels)):
        log_txt.write("Ground_truth_class_name : " + str(ori_labels[labels[label_i].item()]) +
                      ", Ground_truth_class_num : " + str(labels[label_i].item()) + "\n")
        for val_i in range(len(_top_max_k_vals[label_i])):
            log_txt.write("batch_num : " + str(label_i) + ", top5_preds_" + str(val_i) + " : " + str(_top_max_k_vals[label_i][val_i].item())
                          + ", top5_labels_" + str(val_i) + " : " + str(ori_labels[top_max_k_inds[label_i][val_i].item()])
                          + ", Class_num : " + str(top_max_k_inds[label_i][val_i].item()) + "\n")

        log_txt.write("\n")

    # log_txt.write("============================================================")
    # log_txt.write(" Batch Top1 Top5 Err ")
    # log_txt.write("============================================================\n")
    # log_txt.write("Top1_ERR : " + str(100.0 - (batch_top_1 / len(labels))) +
    #               ", Top5_ERR : " + str(100.0 - (batch_top_5 / len(labels))) + "\n")

        #     for val in range(len(_top_max_k_vals[label_i])):
        #         log_txt.write("batch_num : " + str(i) + " top5_preds_ " + str(i2) + " : " + str(val.item()) +
        #                       " top5_labels_ " + str(i2) + " : " + str(ori_labels[top_max_k_inds[i][i2].item()]) + "\n")
        #         i2 += 1
        # log_txt.write("====================================================================================")
        # i2 = 0
        # i += 1

    # (batch_size, max_k) -> (max_k, batch_size).
    top_max_k_inds = top_max_k_inds.t()
    # log_txt.write("top_max_k_inds_down : " + str(top_max_k_inds))
    # for val in _top_max_k_vals:
    #     log_txt.write("val : " + str(val) + "\n")
        # for items in val:
        #     log_txt.write("values : " + str(items.item()) + "\n")

    # log_txt.write("top_max_k_inds : " + str(top_max_k_inds) + "\n")
    # (batch_size, ) -> (max_k, batch_size).
    rep_max_k_labels = labels.view(1, -1).expand_as(top_max_k_inds)
    # log_txt.write("rep_max_k_labels : " + str(rep_max_k_labels) + "\n")
    # (i, j) = 1 if top i-th prediction for the j-th sample is correct.
    top_max_k_correct = top_max_k_inds.eq(rep_max_k_labels)
    # log_txt.write("top_max_k_correct : " + str(top_max_k_correct) + "\n")
    # Compute the number of topk correct predictions for each k.
    topks_correct = [top_max_k_correct[:k, :].float().sum() for k in ks]
    # log_txt.write("topks_correct : " + str(topks_correct) + "\n")

    return topks_correct


def topk_errors(preds, labels, ks):
    """
    Computes the top-k error for each k.
    Args:
        preds (array): array of predictions. Dimension is N.
        labels (array): array of labels. Dimension is N.
        ks (list): list of ks to calculate the top accuracies.
    """
    num_topks_correct = topks_correct(preds, labels, ks)
    return [(1.0 - x / preds.size(0)) * 100.0 for x in num_topks_correct]


def topk_accuracies(preds, labels, ks):
    """
    Computes the top-k accuracy for each k.
    Args:
        preds (array): array of predictions. Dimension is N.
        labels (array): array of labels. Dimension is N.
        ks (list): list of ks to calculate the top accuracies.
    """
    num_topks_correct = topks_correct(preds, labels, ks)
    return [(x / preds.size(0)) * 100.0 for x in num_topks_correct]
