"""Helper for evaluation on the Labeled Faces in the Wild dataset 
"""

# MIT License
#
# Copyright (c) 2016 David Sandberg
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import argparse
import sys
import numpy as np
from scipy import misc
from sklearn.model_selection import KFold
from scipy import interpolate
import sklearn
import cv2
import math
import datetime
import pickle
from sklearn.decomposition import PCA
import mxnet as mx
from mxnet import ndarray as nd
from PIL import Image
import matplotlib.pyplot as plt
import requests as req
import time
import face_recognition

class LFold:
    def __init__(self, n_splits=2, shuffle=False):
        self.n_splits = n_splits
        if self.n_splits > 1:
            self.k_fold = KFold(n_splits=n_splits, shuffle=shuffle)

    def split(self, indices):
        if self.n_splits > 1:
            return self.k_fold.split(indices)
        else:
            return [(indices, indices)]

def calculate_roc(thresholds,
                  embeddings1,
                  embeddings2,
                  actual_issame,
                  nrof_folds=10,
                  pca=0):
    assert (embeddings1.shape[0] == embeddings2.shape[0])
    assert (embeddings1.shape[1] == embeddings2.shape[1])
    nrof_pairs = min(len(actual_issame), embeddings1.shape[0])
    nrof_thresholds = len(thresholds)
    #print(nrof_thresholds)    ----------------------------------> 400출력
    k_fold = LFold(n_splits=nrof_folds, shuffle=False)
    tprs = np.zeros((nrof_folds, nrof_thresholds))
    fprs = np.zeros((nrof_folds, nrof_thresholds))
    accuracy = np.zeros((nrof_folds))
    indices = np.arange(nrof_pairs)

    if pca == 0:
        diff = np.subtract(embeddings1, embeddings2)
        dist = np.sum(np.square(diff), 1)

    for fold_idx, (train_set, test_set) in enumerate(k_fold.split(indices)):
        if pca > 0:
            print('doing pca on', fold_idx)
            embed1_train = embeddings1[train_set]
            embed2_train = embeddings2[train_set]
            _embed_train = np.concatenate((embed1_train, embed2_train), axis=0)
            #print(_embed_train.shape)
            pca_model = PCA(n_components=pca)
            pca_model.fit(_embed_train)
            embed1 = pca_model.transform(embeddings1)
            embed2 = pca_model.transform(embeddings2)
            embed1 = sklearn.preprocessing.normalize(embed1)
            embed2 = sklearn.preprocessing.normalize(embed2)
            #print(embed1.shape, embed2.shape)
            diff = np.subtract(embed1, embed2)
            dist = np.sum(np.square(diff), 1)

        '''
        # Find the best threshold for the fold
        acc_train = np.zeros((nrof_thresholds))
        for threshold_idx, threshold in enumerate(thresholds):
            _, _, acc_train[threshold_idx] = calculate_accuracy(
                threshold, dist[train_set], actual_issame[train_set])
        best_threshold_index = np.argmax(acc_train)

        for threshold_idx, threshold in enumerate(thresholds):

            tprs[fold_idx,
                 threshold_idx], fprs[fold_idx,
                                      threshold_idx], _ = calculate_accuracy(
                                          threshold, dist[test_set],
                                          actual_issame[test_set])
        '''
        _, _, accuracy[fold_idx] = calculate_accuracy(
            thresholds[120], dist[test_set],
            actual_issame[test_set])

    tpr = np.mean(tprs, 0)
    fpr = np.mean(fprs, 0)
    return tpr, fpr, accuracy


def calculate_accuracy(threshold, dist, actual_issame):
    # print("dist : {} threshold : {} ".format(dist, threshold))
    tr_idx = []
    predict_issame = np.less(dist, threshold)
    
    # print("*********** cal_acc")
    # print(predict_issame)
    
    
    
    for i in range(0, len(predict_issame)):
        if predict_issame[i] == True:
            # print(namePath[i])
            # print(dist[i])
            pass
    for real_idx, real_val in enumerate(predict_issame):
        if(real_val == True):
            tr_idx.append(real_idx)



    header = {'cookie': 'JSESSIONID=' + args.sessionid}
    print("sessionid: ",args.sessionid)

    result_dict ={}
    for data in tr_idx:
        hash = namePath[data].split(".")[1].split("/")[-1]
        result_dict[(hash, compare[data])] = dist[data]


    result_dict = sorted(result_dict.items(), key=lambda x:x[1])

    for img, dist in result_dict:
        precision = dist
        hash = img[0]
        if precision <= 0.9:
            precision = "높음"
        elif precision <=1.0:
            precision ="중간"
        else:
            precision = "낮음"

        files = {'face': img[1]}
        try:
            # local test
            # result = req.post('http://localhost:8080/api/detection/result', files=files,     data={'hash': hash, 'precision': precision}, headers=header)

            # aws server
            result = req.post('http://ec2-13-209-242-131.ap-northeast-2.compute.amazonaws.com:8080/api/detection/result', files=files, data={'hash': hash, 'precision': precision}, headers=header)
            # print(result)

        except Exception as E:
            print("Encode 전송 에러")
            print(E)


    tp = np.sum(np.logical_and(predict_issame, actual_issame)) #true pair
    fp = np.sum(np.logical_and(predict_issame, np.logical_not(actual_issame)))
    tn = np.sum(
        np.logical_and(np.logical_not(predict_issame),
                       np.logical_not(actual_issame)))
    fn = np.sum(np.logical_and(np.logical_not(predict_issame), actual_issame))

    tpr = 0 if (tp + fn == 0) else float(tp) / float(tp + fn)
    fpr = 0 if (fp + tn == 0) else float(fp) / float(fp + tn)
    acc = float(tp + tn) / dist.size
    return tpr, fpr, acc


def calculate_val(thresholds,
                  embeddings1,
                  embeddings2,
                  actual_issame,
                  far_target,
                  nrof_folds=10):
    assert (embeddings1.shape[0] == embeddings2.shape[0])
    assert (embeddings1.shape[1] == embeddings2.shape[1])
    nrof_pairs = min(len(actual_issame), embeddings1.shape[0])
    nrof_thresholds = len(thresholds)
    k_fold = LFold(n_splits=nrof_folds, shuffle=False)

    val = np.zeros(nrof_folds)
    far = np.zeros(nrof_folds)

    diff = np.subtract(embeddings1, embeddings2) 
    dist = np.sum(np.square(diff), 1)
    indices = np.arange(nrof_pairs)

    for fold_idx, (train_set, test_set) in enumerate(k_fold.split(indices)):
        # Find the threshold that gives FAR = far_target
        far_train = np.zeros(nrof_thresholds)
        for threshold_idx, threshold in enumerate(thresholds):
            _, far_train[threshold_idx] = calculate_val_far(
                threshold, dist[train_set], actual_issame[train_set])
            if np.max(far_train) >= far_target:
                f = interpolate.interp1d(far_train, thresholds, kind='slinear')
                threshold = f(far_target)
            else:
                threshold = 0.0

        val[fold_idx], far[fold_idx] = calculate_val_far(
            threshold, dist[test_set], actual_issame[test_set])

    val_mean = np.mean(val)
    far_mean = np.mean(far)
    #print(far_mean)  ------------> 0.0
    val_std = np.std(val)
    return val_mean, val_std, far_mean



def calculate_val_far(threshold, dist, actual_issame):
    predict_issame = np.less(dist, threshold)
    true_accept = np.sum(np.logical_and(predict_issame, actual_issame))
    false_accept = np.sum(
        np.logical_and(predict_issame, np.logical_not(actual_issame)))
    n_same = np.sum(actual_issame)
    n_diff = np.sum(np.logical_not(actual_issame))
    if(n_same == 0): 
        return 0, 0
    
    val = float(true_accept) / float(n_same)
    far = float(false_accept) / float(n_diff)
    print("far %s" % (far))
    return val, far   # var -> 0으로 수정함


def evaluate(embeddings, actual_issame, nrof_folds=10, pca=0):
    # Calculate evaluation metrics
    thresholds = np.arange(0, 4, 0.01)
    embeddings1 = embeddings[0::2]
    embeddings2 = embeddings[1::2]
    tpr, fpr, accuracy = calculate_roc(thresholds,
                                       embeddings1,
                                       embeddings2,
                                       np.asarray(actual_issame),
                                       nrof_folds=nrof_folds,
                                       pca=pca)
    '''
    thresholds = np.arange(0, 4, 0.001)
    val, val_std, far = calculate_val(thresholds,
                                      embeddings1,
                                      embeddings2,
                                      np.asarray(actual_issame),
                                      1e-3,
                                      nrof_folds=nrof_folds)
    '''
    return tpr, fpr, accuracy #, val, val_std, far

bins = []
compare = []

namePath = []

def load_bin(image_size):
    #try:
    #    with open(path, 'rb') as f:
    #        bins1, issame_list1 = pickle.load(f)  #py2
    #except UnicodeDecodeError as e:
    #    with open(path, 'rb') as f:
    #        bins1, issame_list1 = pickle.load(f, encoding='bytes')  #py3
    
    ### 추가코드 #######################
    print("----------")
    target_image_path = './data/target/'+args.filename #웹 클라이언트에서 받을 이미지
    crawling_folder = './data/crawling/' # 크롤링 저장소 경로
    
    issame_list  = []

    #print("load folder : "+ str(os.listdir(crawling_folder)))
    
    # loading_img = cv2.imread(target_image_path)
    
    temp_face_location = face_recognition.load_image_file(target_image_path)
    temp_encoding = face_recognition.face_encodings(temp_face_location)
    
    cnt = len(temp_encoding)
    if cnt == 0:
       print("N/F")
       os.remove(target_image_path)
       sys.exit(0)
    elif cnt == 1:
        for (top, right, bottom, left) in face_recognition.face_locations(temp_face_location):
                face_img = temp_face_location[top:bottom, left:right]  
                
                pil_img = Image.fromarray(face_img)

                head, ext = target_image_path.split(".")[1:]
                head = "./"+head + "." + ext
                
                pil_img.save(head)
                with open(head, 'rb') as fp:
                    target_image = fp.read()
    else:
        target =0
        target_face = [0,0,0,0]
        for (top, right, bottom, left) in face_recognition.face_locations(temp_face_location):
            face_img = temp_face_location[top:bottom, left:right]
            curr =abs(left -right) + abs(top - bottom)
            if( curr> target):
                target = curr
                target_face[0] = top
                target_face[1] = right
                target_face[2] = bottom
                target_face[3] = left

        face_img = temp_face_location[target_face[0]:target_face[2], target_face[3]:target_face[1]]
        pil_img = Image.fromarray(face_img)

        head, ext = target_image_path.split(".")[1:]
        head = "./" + head + "." + ext
        pil_img.save(head)
        with open(head, 'rb') as fp:
            target_image = fp.read()

    os.remove(target_image_path)

    for i in os.listdir(crawling_folder):
        try:
            path = os.path.join(crawling_folder, i)
            Image.open(path)
        except IOError as E:
            print(E)
            continue  


        with open(path, 'rb') as fp:
            if(path.split(".")[-1] == "gif"): #gif 인식 불가
                print(path.split(".")[-1])
                continue
            
            bins.append(target_image)
            data = fp.read()
            bins.append(data)
            compare.append(data)
            namePath.append(path)

        issame_list.append(False)
    

    ### 추가코드 #######################
    data_list = []
    for flip in [0, 1]:
        data = nd.empty(
            (len(issame_list) * 2, 3, image_size[0], image_size[1]))
        data_list.append(data)
    for i in range(len(issame_list) * 2):
        _bin = bins[i]
        img = mx.image.imdecode(_bin)
        if img.shape[1] != image_size[0] or img.shape[0] != image_size[1]:
            img = mx.image.imresize(img, image_size[0], image_size[1])
        img = nd.transpose(img, axes=(2, 0, 1))
        for flip in [0, 1]:
            if flip == 1:
                img = mx.ndarray.flip(data=img, axis=2)
            data_list[flip][i][:] = img
        if i % 1000 == 0:
            print('loading bin', i)

    print(data_list[0].shape) 
    return (data_list, issame_list)


def test(data_set,
         mx_model,
         batch_size,
         nfolds=10,
         data_extra=None,
         label_shape=None):
    print('testing verification..')
    data_list = data_set[0]
    issame_list = data_set[1]
    model = mx_model
    embeddings_list = []
    if data_extra is not None:
        _data_extra = nd.array(data_extra)
    time_consumed = 0.0
    if label_shape is None:
        _label = nd.ones((batch_size, ))
    else:
        _label = nd.ones(label_shape)
    for i in range(len(data_list)):
        data = data_list[i]
        embeddings = None
        ba = 0
        while ba < data.shape[0]:
            bb = min(ba + batch_size, data.shape[0])
            count = bb - ba
            _data = nd.slice_axis(data, axis=0, begin=bb - batch_size, end=bb)
            #print(_data.shape, _label.shape)
            time0 = datetime.datetime.now()
            if data_extra is None:
                db = mx.io.DataBatch(data=(_data, ), label=(_label, ))
            else:
                db = mx.io.DataBatch(data=(_data, _data_extra),
                                     label=(_label, ))
            model.forward(db, is_train=False)
            net_out = model.get_outputs()
            #_arg, _aux = model.get_params()
            #__arg = {}
            #for k,v in _arg.iteritems():
            #  __arg[k] = v.as_in_context(_ctx)
            #_arg = __arg
            #_arg["data"] = _data.as_in_context(_ctx)
            #_arg["softmax_label"] = _label.as_in_context(_ctx)
            #for k,v in _arg.iteritems():
            #  print(k,v.context)
            #exe = sym.bind(_ctx, _arg ,args_grad=None, grad_req="null", aux_states=_aux)
            #exe.forward(is_train=False)
            #net_out = exe.outputs
            _embeddings = net_out[0].asnumpy()
            time_now = datetime.datetime.now()
            diff = time_now - time0
            time_consumed += diff.total_seconds()
            #print(_embeddings.shape) 
            if embeddings is None:
                embeddings = np.zeros((data.shape[0], _embeddings.shape[1]))
            embeddings[ba:bb, :] = _embeddings[(batch_size - count):, :]
            ba = bb
        embeddings_list.append(embeddings)

    _xnorm = 0.0
    _xnorm_cnt = 0
    for embed in embeddings_list:
        for i in range(embed.shape[0]):
            _em = embed[i]
            _norm = np.linalg.norm(_em)
            #print(_em.shape, _norm)
            _xnorm += _norm
            _xnorm_cnt += 1
    _xnorm /= _xnorm_cnt

    embeddings = embeddings_list[0].copy()
    embeddings = sklearn.preprocessing.normalize(embeddings)
    acc1 = 0.0
    std1 = 0.0
    #_, _, accuracy, val, val_std, far = evaluate(embeddings, issame_list, nrof_folds=10)
    #acc1, std1 = np.mean(accuracy), np.std(accuracy)

    #print('Validation rate: %2.5f+-%2.5f @ FAR=%2.5f' % (val, val_std, far))
    #embeddings = np.concatenate(embeddings_list, axis=1)
    embeddings = embeddings_list[0] + embeddings_list[1]
    embeddings = sklearn.preprocessing.normalize(embeddings)
    print(embeddings.shape)
    print('infer time', time_consumed)
    _, _, accuracy = evaluate(embeddings,
                            issame_list,
                            nrof_folds=nfolds)
    acc2, std2 = np.mean(accuracy), np.std(accuracy)
    return acc1, std1, acc2, std2, _xnorm, embeddings_list # far = acc2였음


def test_badcase(data_set,
                 mx_model,
                 batch_size,
                 name='',
                 data_extra=None,
                 label_shape=None):
    print('testing verification badcase..')
    data_list = data_set[0]
    issame_list = data_set[1]
    model = mx_model
    embeddings_list = []
    if data_extra is not None:
        _data_extra = nd.array(data_extra)
    time_consumed = 0.0
    if label_shape is None:
        _label = nd.ones((batch_size, ))
    else:
        _label = nd.ones(label_shape)
    for i in range(len(data_list)):
        data = data_list[i]
        embeddings = None
        ba = 0
        while ba < data.shape[0]:
            bb = min(ba + batch_size, data.shape[0])
            count = bb - ba
            _data = nd.slice_axis(data, axis=0, begin=bb - batch_size, end=bb)
            #print(_data.shape, _label.shape)
            time0 = datetime.datetime.now()
            if data_extra is None:
                db = mx.io.DataBatch(data=(_data, ), label=(_label, ))
            else:
                db = mx.io.DataBatch(data=(_data, _data_extra),
                                     label=(_label, ))
            model.forward(db, is_train=False)
            net_out = model.get_outputs()
            _embeddings = net_out[0].asnumpy()
            time_now = datetime.datetime.now()
            diff = time_now - time0
            time_consumed += diff.total_seconds()
            if embeddings is None:
                embeddings = np.zeros((data.shape[0], _embeddings.shape[1]))
            embeddings[ba:bb, :] = _embeddings[(batch_size - count):, :]
            ba = bb
        embeddings_list.append(embeddings)
    embeddings = embeddings_list[0] + embeddings_list[1]
    embeddings = sklearn.preprocessing.normalize(embeddings)
    thresholds = np.arange(0, 4, 0.01)
    actual_issame = np.asarray(issame_list)
    nrof_folds = 10
    embeddings1 = embeddings[0::2]
    embeddings2 = embeddings[1::2]
    assert (embeddings1.shape[0] == embeddings2.shape[0])
    assert (embeddings1.shape[1] == embeddings2.shape[1])
    nrof_pairs = min(len(actual_issame), embeddings1.shape[0])
    nrof_thresholds = len(thresholds)
    k_fold = LFold(n_splits=nrof_folds, shuffle=False)

    tprs = np.zeros((nrof_folds, nrof_thresholds))
    fprs = np.zeros((nrof_folds, nrof_thresholds))
    accuracy = np.zeros((nrof_folds))
    indices = np.arange(nrof_pairs)

    diff = np.subtract(embeddings1, embeddings2)
    dist = np.sum(np.square(diff), 1)
    data = data_list[0]

    pouts = []
    nouts = []

    for fold_idx, (train_set, test_set) in enumerate(k_fold.split(indices)):

        # Find the best threshold for the fold
        acc_train = np.zeros((nrof_thresholds))
        #print(train_set)
        #print(train_set.__class__)
        for threshold_idx, threshold in enumerate(thresholds):
            p2 = dist[train_set]
            p3 = actual_issame[train_set]
            _, _, acc_train[threshold_idx] = calculate_accuracy(
                threshold, p2, p3)
        best_threshold_index = np.argmax(acc_train)
        for threshold_idx, threshold in enumerate(thresholds):
            tprs[fold_idx,
                 threshold_idx], fprs[fold_idx,
                                      threshold_idx], _ = calculate_accuracy(
                                          threshold, dist[test_set],
                                          actual_issame[test_set])
        _, _, accuracy[fold_idx] = calculate_accuracy(
            thresholds[best_threshold_index], dist[test_set],
            actual_issame[test_set])
        best_threshold = thresholds[best_threshold_index]
        for iid in test_set:
            ida = iid * 2
            idb = ida + 1
            asame = actual_issame[iid]
            _dist = dist[iid]
            violate = _dist - best_threshold
            if not asame:
                violate *= -1.0
            if violate > 0.0:
                imga = data[ida].asnumpy().transpose(
                    (1, 2, 0))[..., ::-1]  #to bgr
                imgb = data[idb].asnumpy().transpose((1, 2, 0))[..., ::-1]
                #print(imga.shape, imgb.shape, violate, asame, _dist)
                if asame:
                    pouts.append((imga, imgb, _dist, best_threshold, ida))
                else:
                    nouts.append((imga, imgb, _dist, best_threshold, ida))

    tpr = np.mean(tprs, 0)
    fpr = np.mean(fprs, 0)
    acc = np.mean(accuracy)
    pouts = sorted(pouts, key=lambda x: x[2], reverse=True)
    nouts = sorted(nouts, key=lambda x: x[2], reverse=False)
    print(len(pouts), len(nouts))
    print('acc', acc)
    gap = 10
    image_shape = (112, 224, 3)
    out_dir = "./badcases"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    if len(nouts) > 0:
        threshold = nouts[0][3]
    else:
        threshold = pouts[-1][3]

    for item in [(pouts, 'positive(false_negative).png'),
                 (nouts, 'negative(false_positive).png')]:
        cols = 4
        rows = 8000
        outs = item[0]
        if len(outs) == 0:
            continue
        #if len(outs)==9:
        #  cols = 3
        #  rows = 3

        _rows = int(math.ceil(len(outs) / cols))
        rows = min(rows, _rows)
        hack = {}

        if name.startswith('cfp') and item[1].startswith('pos'):
            hack = {
                0: 'manual/238_13.jpg.jpg',
                6: 'manual/088_14.jpg.jpg',
                10: 'manual/470_14.jpg.jpg',
                25: 'manual/238_13.jpg.jpg',
                28: 'manual/143_11.jpg.jpg'
            }

        filename = item[1]
        if len(name) > 0:
            filename = name + "_" + filename
        filename = os.path.join(out_dir, filename)
        img = np.zeros((image_shape[0] * rows + 20, image_shape[1] * cols +
                        (cols - 1) * gap, 3),
                       dtype=np.uint8)
        img[:, :, :] = 255
        text_color = (0, 0, 153)
        text_color = (255, 178, 102)
        text_color = (153, 255, 51)
        for outi, out in enumerate(outs):
            row = outi // cols
            col = outi % cols
            if row == rows:
                break
            imga = out[0].copy()
            imgb = out[1].copy()
            if outi in hack:
                idx = out[4]
                print('noise idx', idx)
                aa = hack[outi]
                imgb = cv2.imread(aa)
                #if aa==1:
                #  imgb = cv2.transpose(imgb)
                #  imgb = cv2.flip(imgb, 1)
                #elif aa==3:
                #  imgb = cv2.transpose(imgb)
                #  imgb = cv2.flip(imgb, 0)
                #else:
                #  for ii in range(2):
                #    imgb = cv2.transpose(imgb)
                #    imgb = cv2.flip(imgb, 1)
            dist = out[2]
            _img = np.concatenate((imga, imgb), axis=1)
            k = "%.3f" % dist
            #print(k)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(_img, k, (80, image_shape[0] // 2 + 7), font, 0.6,
                        text_color, 2)
            #_filename = filename+"_%d.png"%outi
            #cv2.imwrite(_filename, _img)
            img[row * image_shape[0]:(row + 1) * image_shape[0],
                (col * image_shape[1] +
                 gap * col):((col + 1) * image_shape[1] + gap * col), :] = _img
        #threshold = outs[0][3]
        font = cv2.FONT_HERSHEY_SIMPLEX
        k = "threshold: %.3f" % threshold
        cv2.putText(img, k, (img.shape[1] // 2 - 70, img.shape[0] - 5), font,
                    0.6, text_color, 2)
        cv2.imwrite(filename, img)


def dumpR(data_set,
          mx_model,
          batch_size,
          name='',
          data_extra=None,
          label_shape=None):
    print('dump verification embedding..')
    data_list = data_set[0]
    issame_list = data_set[1]
    model = mx_model
    embeddings_list = []
    if data_extra is not None:
        _data_extra = nd.array(data_extra)
    time_consumed = 0.0
    if label_shape is None:
        _label = nd.ones((batch_size, ))
    else:
        _label = nd.ones(label_shape)
    for i in range(len(data_list)):
        data = data_list[i]
        embeddings = None
        ba = 0
        while ba < data.shape[0]:
            bb = min(ba + batch_size, data.shape[0])
            count = bb - ba
            _data = nd.slice_axis(data, axis=0, begin=bb - batch_size, end=bb)
            #print(_data.shape, _label.shape)
            time0 = datetime.datetime.now()
            if data_extra is None:
                db = mx.io.DataBatch(data=(_data, ), label=(_label, ))
            else:
                db = mx.io.DataBatch(data=(_data, _data_extra),
                                     label=(_label, ))
            model.forward(db, is_train=False)
            net_out = model.get_outputs()
            _embeddings = net_out[0].asnumpy()
            time_now = datetime.datetime.now()
            diff = time_now - time0
            time_consumed += diff.total_seconds()
            if embeddings is None:
                embeddings = np.zeros((data.shape[0], _embeddings.shape[1]))
            embeddings[ba:bb, :] = _embeddings[(batch_size - count):, :]
            ba = bb
        embeddings_list.append(embeddings)
    embeddings = embeddings_list[0] + embeddings_list[1]
    embeddings = sklearn.preprocessing.normalize(embeddings)
    actual_issame = np.asarray(issame_list)
    outname = os.path.join('temp.bin')
    with open(outname, 'wb') as f:
        pickle.dump((embeddings, issame_list),
                    f,
                    protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    testf = open("./asd.txt", "a")
    testf.write("asdaadsfasdfasdf")

    parser = argparse.ArgumentParser(description='do verification')
    # general
    parser.add_argument('--data-dir', default='data', help='')
    parser.add_argument('--model',
                        default='./models/model/model,0',
                        help='path to load model.')
    parser.add_argument('--target',
                        default='lfw,cfp_ff,cfp_fp,agedb_30',
                        help='test targets.')
    parser.add_argument('--gpu', default=0, type=int, help='gpu id')
    parser.add_argument('--batch-size', default=24, type=int, help='')
    parser.add_argument('--max', default='', type=str, help='')
    parser.add_argument('--mode', default=0, type=int, help='')
    parser.add_argument('--nfolds', default=10, type=int, help='')
    parser.add_argument('--sessionid', type=str)
    parser.add_argument('--filename', type=str)
    args = parser.parse_args()
    #sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
    #import face_image
    #prop = face_image.load_property(args.data_dir)
    #image_size = prop.image_size
    image_size = [112, 112]
    print('image_size', image_size)
    ctx = mx.gpu(args.gpu)
    nets = []
    vec = args.model.split(',')
    prefix = args.model.split(',')[0]
    epochs = []
    if len(vec) == 1:
        pdir = os.path.dirname(prefix)
        for fname in os.listdir(pdir):
            if not fname.endswith('.params'):
                continue
            _file = os.path.join(pdir, fname)
            if _file.startswith(prefix):
                epoch = int(fname.split('.')[0].split('-')[1])
                epochs.append(epoch)
        epochs = sorted(epochs, reverse=True)
        if len(args.max) > 0:
            _max = [int(x) for x in args.max.split(',')]
            assert len(_max) == 2
            if len(epochs) > _max[1]:
                epochs = epochs[_max[0]:_max[1]]

    else:
        epochs = [int(x) for x in vec[1].split('|')]
    print('model number', len(epochs))
    time0 = datetime.datetime.now()
    for epoch in epochs:
        print('loading', prefix, epoch)
        sym, arg_params, aux_params = mx.model.load_checkpoint(prefix, epoch)
        #arg_params, aux_params = ch_dev(arg_params, aux_params, ctx)
        all_layers = sym.get_internals()
        sym = all_layers['fc1_output']
        model = mx.mod.Module(symbol=sym, context=ctx, label_names=None)
        #model.bind(data_shapes=[('data', (args.batch_size, 3, image_size[0], image_size[1]))], label_shapes=[('softmax_label', (args.batch_size,))])
        model.bind(data_shapes=[('data', (args.batch_size, 3, image_size[0],
                                          image_size[1]))])
        model.set_params(arg_params, aux_params)
        nets.append(model)
    time_now = datetime.datetime.now()
    diff = time_now - time0
    print('model loading time', diff.total_seconds())

    ver_list = []
    ver_name_list = []
    ver_name_list.append('lfw')
    data_set = load_bin(image_size)
    ver_list.append(data_set)

    
    if args.mode == 0:
        for i in range(len(ver_list)):
            results = []
            for model in nets:
                acc1, std1, acc2, std2, xnorm, embeddings_list = test(
                    ver_list[i], model, args.batch_size, args.nfolds)
                print('[%s]XNorm: %f' % (ver_name_list[i], xnorm))
                #print('[%s]Accuracy: %1.5f+-%1.5f' %
                #     (ver_name_list[i], acc1, std1))
                print('[%s]Accuracy-Flip: %1.5f+-%1.5f' %
                      (ver_name_list[i], acc2, std2))
                results.append(acc2)
            print('Max of [%s] is %1.5f' % (ver_name_list[i], np.max(results)))

    elif args.mode == 1:
        model = nets[0]
        test_badcase(ver_list[0], model, args.batch_size, args.target)
    else:
        model = nets[0]
        dumpR(ver_list[0], model, args.batch_size, args.target)


