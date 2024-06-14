import os
import io
import json
import typing
import socket
from pathlib import Path
import lingua_franca

from features.intent_recognition.intent_fsticuffs.ini_jsgf import Expression, Word, parse_ini, split_rules
from features.intent_recognition.intent_fsticuffs.jsgf import walk_expression
from features.intent_recognition.intent_fsticuffs.jsgf_graph import graph_to_json, sentences_to_graph
from features.intent_recognition.intent_fsticuffs.number_utils import number_range_transform, number_transform
from features.intent_recognition.intent_fsticuffs.slots import add_slot_replacements
from features.intent_recognition.intent_fsticuffs import IntentRecognizer, IntentRequest, IntentResult

class Train:
    """Train intent recognizer with fsticuffs"""

    def define_slots(self, slots:dict):
        """# Slots 
        Are the `$something` in the sentence.ini input an Dictionary `{"$slotname": lambda *x: list, ...}`"""
        self.slots = slots

    def train_intent(self, lang="pt"):
        if True:
            # Automatic casing applied to all words (keep, lower, upper)
            casing = "lower"
            number_language = lang
            replace_numbers = True
            
            input_file = Path(f"features/intent_recognition/intents/sentences/sentence_{lang}.ini")

            output_graph_path = Path(f"features/intent_recognition/intents/graphs/graph_{lang}.json")

            lingua_franca.load_language(number_language)

            with open(input_file, "r", encoding="utf-8") as sentences_file:
                ini_text = sentences_file.read()
            
            intents = parse_ini(ini_text)
            print(len(intents))
            sentences, replacements = split_rules(intents)

            # Transform words
            word_transform: typing.Optional[typing.Callable[[str], str]] = None

            if casing == "lower":
                word_transform = str.lower
            elif casing == "upper":
                word_transform = str.upper

            word_visitor: typing.Optional[
                typing.Callable[[Expression], typing.Union[bool, Expression]]
            ] = None

            if word_transform:
                # Apply transformation to words

                def transform_visitor(word: Expression):
                    if isinstance(word, Word):
                        assert word_transform
                        new_text = word_transform(word.text)

                        # Preserve case by using original text as substition
                        if (word.substitution is None) and (new_text != word.text):
                            word.substitution = word.text

                        word.text = new_text

                    return word

                word_visitor = transform_visitor

            # Apply case/number transforms
            if word_visitor or replace_numbers:
                for intent_sentences in sentences.values():
                    for sentence in intent_sentences:
                        if replace_numbers:
                            # Replace number ranges with slot references
                            # type: ignore
                            walk_expression(sentence, number_range_transform, replacements)

                        if word_visitor:
                            # Do case transformation
                            # type: ignore
                            walk_expression(sentence, word_visitor, replacements)

            # Load slot values
            add_slot_replacements(
                replacements,
                intents,
                slot_generators=self.slots,
                slot_visitor=word_visitor,
            )

            if replace_numbers:
                # Do single number transformations
                for intent_sentences in sentences.values():
                    for sentence in intent_sentences:
                        walk_expression(
                            sentence,
                            number_transform,
                            replacements,
                        )

            # Convert to directed graph
            graph = sentences_to_graph(sentences, replacements=replacements)

            # Write JSON graph
            new_json = graph_to_json(graph)
            with open(output_graph_path, "w", encoding="utf-8") as graph_file:
                json.dump(new_json, graph_file)


def train(lang):
    def number_range(*args):
        if len(args) == 3:
            start, stop, step = map(int, args)
        elif len(args) == 2:
            start, stop = map(int, args)
            step = 1
        else:
            raise ValueError(f"Invalid number range args {args}")

        for num in range(start, stop + 1, step):
            yield str(num)

    T = Train()
    T.define_slots({"$number": number_range, "$day": lambda *x: ["Segunda", "Terca" "Quarta", "Quinta", "Sesta"]})
    return T.train_intent(lang)

def recog(lang, text):
    Recognizer = IntentRecognizer()

    graph_path = f"graph_{lang}.json"
    with open(graph_path, "r", encoding="utf-8") as graph_file:
        Recognizer.start(graph_file)
        result = Recognizer.recognize(IntentRequest(text=text.lower()))
        Recognizer.stop()
    return result

