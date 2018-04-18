# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

# NOTE: This file was altered from the original classify_image.py Tensorflow Imagenet Tutorial

import logging
import re
from pathlib import Path

import tensorflow as tf

logger = logging.getLogger(__name__)

AGENT_DIRECTORY = Path(__file__).parent


class NodeLookup(object):
    """Converts integer node ID's to human readable labels."""

    def __init__(self, label_lookup_path=None, uid_lookup_path=None):

        model_directory = AGENT_DIRECTORY.joinpath('model_data')

        label_lookup_path = str(model_directory.joinpath('imagenet_2012_challenge_label_map_proto.pbtxt'))
        if not tf.gfile.Exists(label_lookup_path):
            tf.logging.fatal('Missing Label file %s', label_lookup_path)

        uid_lookup_path = str(model_directory.joinpath('imagenet_synset_to_human_label_map.txt'))
        if not tf.gfile.Exists(uid_lookup_path):
            tf.logging.fatal('Missing UID Lookup file %s', uid_lookup_path)

        # Loads mapping from string UID to human-readable string
        proto_as_ascii_lines = tf.gfile.GFile(uid_lookup_path).readlines()
        uid_to_human = {}
        p = re.compile(r'[n\d]*[ \S,]*')
        for line in proto_as_ascii_lines:
            parsed_items = p.findall(line)
            uid = parsed_items[0]
            human_string = parsed_items[2]
            uid_to_human[uid] = human_string

        # Loads mapping from string UID to integer node ID.
        node_id_to_uid = {}
        proto_as_ascii = tf.gfile.GFile(label_lookup_path).readlines()
        target_class = ''
        for line in proto_as_ascii:
            if line.startswith('  target_class:'):
                target_class = int(line.split(': ')[1])
            if line.startswith('  target_class_string:'):
                target_class_string = line.split(': ')[1]
                node_id_to_uid[target_class] = target_class_string[1:-2]

        # Loads the final mapping of integer node ID to human-readable string
        self.node_id_to_name = {}
        for key, val in node_id_to_uid.items():
            if val not in uid_to_human:
                tf.logging.fatal('Failed to locate: %s', val)
            name = uid_to_human[val]
            self.node_id_to_name[key] = name

    def id_to_string(self, node_id):
        if node_id not in self.node_id_to_name:
            return ''
        return self.node_id_to_name[node_id]
