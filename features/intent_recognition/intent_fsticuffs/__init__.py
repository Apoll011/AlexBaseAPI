# Copyright 2022 Michael Hansen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#

import json
import typing
import networkx as nx
from dataclasses import dataclass, field
from .fsticuffs import recognize
from .jsgf_graph import json_to_graph

@dataclass
class IntentEntity:
    """Entity from intent recognition"""

    name: str
    """Name of entity"""

    value: typing.Any
    """Value of entitiy"""


@dataclass
class IntentRequest:
    """Request for intent recognition"""

    text: str
    """Text to recognize intent from"""


@dataclass
class IntentResult:
    """Result of intent recognition"""

    intent_name: str
    """Name of recognized intent"""

    confidence: float
    """The confidence"""

    text: str
    """The text"""

    raw_text: str
    """The raw text"""

    entities: typing.List[IntentEntity] = field(default_factory=list)
    """Recognized named entities"""



class IntentRecognizer:
    """Recognize intents using fsticuffs"""

    def __init__(self):
        self.graph: typing.Optional[nx.DiGraph] = None



    def recognize(self, request: IntentRequest) -> typing.Optional[dict]:
        """Recognize an intent"""
        assert self.graph is not None

        results = recognize(request.text, self.graph)
        if results:
            result = results[0]
            if result.intent is not None:
                return {
                    "intent_name":result.intent.name,
                    "confidence":result.intent.confidence,
                    "text":result.text,
                    "raw_text":result.raw_text,
                    "entities": [
                        {"name": e.entity, "value": e.value}
                        for e in result.entities
                    ],
                    "recognized_seconds":result.recognize_seconds
                    }

        return None

    def start(self, graph_file):
        graph_dict = json.load(graph_file)
        self.graph = json_to_graph(graph_dict)

    def stop(self):
        self.graph = None
