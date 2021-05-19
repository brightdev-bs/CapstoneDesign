# Implementation of pairs.txt from lfw dataset
# Section f: http://vis-www.cs.umass.edu/lfw/lfw.pdf
# More succint, less explicit: http://vis-www.cs.umass.edu/lfw/README.txt
import time
import glob
import io
import os
import random
import argparse
from argparse import ArgumentParser, Namespace
from typing import List, Optional, Set, Tuple, cast
import numpy as np
from facenet_sandberg.utils import transform_to_lfw_format

import mxnet as mx
from mxnet import ndarray as nd
import pickle
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'eval'))
import lfw

Mismatch = Tuple[str, int, str, int]
Match = Tuple[str, int, int]
CommandLineArgs = Namespace


def write_pairs_to_file(fname: str,
                        match_folds: List[List[Match]],
                        mismatch_folds: List[List[Mismatch]],
                        num_folds: int,
                        num_matches_mismatches: int) -> None:
    metadata = '{}\t{}\n'.format(num_folds, num_matches_mismatches)
    with io.open(fname,
                 'w',
                 io.DEFAULT_BUFFER_SIZE,
                 encoding='utf-8') as fpairs:
        fpairs.write(metadata)
        for match_fold, mismatch_fold in zip(match_folds, mismatch_folds):
            """
            for match in match_fold:
                line = '{}\t{}\t{}\n'.format(match[0], match[1], match[2])
                fpairs.write(line)
            """
            
            for mismatch in mismatch_fold:
                line = '{}\t{}\t{}\t{}\n'.format(
                    mismatch[0], mismatch[1], mismatch[2], mismatch[3])
                fpairs.write(line)
        fpairs.flush()


def _split_people_into_folds(image_dir: str,
                             num_folds: int) -> List[List[str]]:
    names = [d for d in os.listdir(image_dir)
             if os.path.isdir(os.path.join(image_dir, d))]
    random.shuffle(names)
    return [list(arr) for arr in np.array_split(names, num_folds)]


def _make_matches(image_dir: str,
                  people: List[str],
                  total_matches: int) -> List[Match]:
    matches = cast(Set[Match], set())
    curr_matches = 0
    while curr_matches < total_matches:
        person = random.choice(people)
        images = _clean_images(image_dir, person)
        if len(images) > 1:
            img1, img2 = sorted(
                [images.index(random.choice(images)) + 1,
                 images.index(random.choice(images)) + 1])
            match = (person, img1, img2)
            if (img1 != img2) and (match not in matches):
                matches.add(match)
                curr_matches += 1
    return sorted(list(matches), key=lambda x: x[0].lower())


def _make_mismatches(image_dir: str,
                     people: List[str],
                     total_matches: int) -> List[Mismatch]:
    mismatches = cast(Set[Mismatch], set())
    curr_matches = 0
    while curr_matches < total_matches:
        person1 = random.choice(people)
        person2 = random.choice(people)
        if person1 != person2:
            person1_images = _clean_images(image_dir, person1)
            person2_images = _clean_images(image_dir, person2)
            if person1_images and person2_images:
                img1 = person1_images.index(random.choice(person1_images)) + 1
                img2 = person2_images.index(random.choice(person2_images)) + 1
                if person1.lower() > person2.lower():
                    person1, img1, person2, img2 = person2, img2, person1, img1
                mismatch = (person1, img1, person2, img2)
                if mismatch not in mismatches:
                    mismatches.add(mismatch)
                    curr_matches += 1
    return sorted(list(mismatches), key=lambda x: x[0].lower())


def _clean_images(base: str, folder: str):
    images = os.listdir(os.path.join(base, folder))
    images = [image for image in images if image.endswith(
        ".jpg") or image.endswith(".png") or image.endswith(".jpeg")]
    return images


def generate_pairs(
        image_dir: str,
        num_folds: int,
        num_matches_mismatches: int,
        write_to_file: bool=False,
        pairs_file_name: str="") -> None:
    transform_to_lfw_format(image_dir)
    people_folds = _split_people_into_folds(image_dir, num_folds)
    matches = []
    mismatches = []
    for fold in people_folds:
        #matches는 필요 없음.
        matches.append(_make_matches(image_dir,
                                     fold,
                                     num_matches_mismatches))
        mismatches.append(_make_mismatches(image_dir,
                                           fold,
                                           num_matches_mismatches))
    if write_to_file:
        write_pairs_to_file(pairs_file_name,
                            matches,
                            mismatches,
                            num_folds,
                            num_matches_mismatches)
    return matches, mismatches


def _cli() -> None:
    args = _parse_arguments()
    generate_pairs(
        args.image_dir,
        args.num_folds,
        args.num_matches_mismatches,
        True,
        args.pairs_file_name)


def lfw_to_pack():
    # general
    args = _parse_arguments()
    lfw_dir = args.data_dir
    image_size = [int(x) for x in args.image_size.split(',')]
    lfw_pairs = lfw.read_pairs(os.path.join(lfw_dir, 'pairs.txt'))
    lfw_paths, issame_list = lfw.get_paths(lfw_dir, lfw_pairs)
    lfw_bins = []
    # lfw_data = nd.empty((len(lfw_paths), 3, image_size[0], image_size[1]))
    i = 0
    for path in lfw_paths:
        with open(path, 'rb') as fin:
            _bin = fin.read()
            lfw_bins.append(_bin)
            # img = mx.image.imdecode(_bin)
            # img = nd.transpose(img, axes=(2, 0, 1))
            # lfw_data[i][:] = img
            i += 1
            if i % 1000 == 0:
                print('loading lfw', i)

    with open(args.output, 'wb') as f:
        pickle.dump((lfw_bins, issame_list), f, protocol=pickle.HIGHEST_PROTOCOL)


def _parse_arguments() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument('--image_dir',
                        type=str,
                        required=True,
                        help='Path to the image directory.')
    parser.add_argument('--pairs_file_name',
                        type=str,
                        required=True,
                        help='Filename of pairs.txt')
    parser.add_argument('--num_folds',
                        type=int,
                        required=True,
                        help='Number of folds for k-fold cross validation.')
    parser.add_argument('--num_matches_mismatches',
                        type=int,
                        required=True,
                        help='Number of matches/mismatches per fold.')
    parser.add_argument('--data-dir', default='data', help='')                   #서버에서 여기 경로 바꾸기!
    parser.add_argument('--image-size', type=str, default='112,112', help='')
    parser.add_argument('--output', default='data/lfw.bin', help='path to save.')  #서버에서 여기 경로 바꾸기!
    return parser.parse_args()


if __name__ == '__main__':
    start = time.time() 
    _cli()
    lfw_to_pack()
    print("걸린 시간 : ", time.time() - start)
