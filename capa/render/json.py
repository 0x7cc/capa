# Copyright (C) 2023 Mandiant, Inc. All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
# You may obtain a copy of the License at: [package root]/LICENSE.txt
# Unless required by applicable law or agreed to in writing, software distributed under the License
#  is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.
import capa.render.result_document as rd
from capa.rules import RuleSet
from capa.engine import MatchResults


def render(meta, rules: RuleSet, capabilities: MatchResults) -> str:
    return rd.ResultDocument.from_capa(meta, rules, capabilities).model_dump_json(exclude_none=True)
