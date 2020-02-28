# Copyright 2017 Neural Networks and Deep Learning lab, MIPT
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

import re
import pickle
from string import punctuation
from typing import List, Tuple

from deeppavlov.core.common.registry import register
from deeppavlov.core.models.component import Component
from deeppavlov.core.models.serializable import Serializable


@register('template_matcher')
class TemplateMatcher(Component, Serializable):
    def __init__(self, load_path: str, templates_filename: str = None, *args, **kwargs) -> None:
        super().__init__(save_path=None, load_path=load_path)
        self._templates_filename = templates_filename
        self.load()

    def load(self) -> None:
        if self._templates_filename is not None:
            with open(self.load_path.parent / self._templates_filename, 'rb') as t:
                self.templates = pickle.load(t)

    def save(self) -> None:
        raise NotImplementedError

    def __call__(self, question: str, *args, **kwargs) -> Tuple[str, str]:
        entities = []
        relations = []
        min_length = 100
        for template in self.templates:
            template_regexp = template.replace("xxx", "([a-z\d\s\.]+)")
            fnd = re.findall(template_regexp, question)
            if fnd is not None:
                entities_cand = fnd[0]
                cur_len = sum([len(entity) for entity in entities_cand])
                if cur_len < min_length:
                    entities = entities_cand
                    relations = self.templates[template]

        return entities, relations

