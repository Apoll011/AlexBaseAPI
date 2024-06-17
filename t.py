from adapt.intent import IntentBuilder
from adapt.engine import IntentDeterminationEngine
from adapt.context import ContextManager

class IntentClassifier:
    def __init__(self) -> None:
        self.engine = IntentDeterminationEngine()
        self.context_manager = ContextManager()

    def registerIntent(self, intent: IntentBuilder):
        self.engine.register_intent_parser(intent)

    def registerIntents(self, intents: list[IntentBuilder]):
        for i in intents:
            self.engine.register_intent_parser(i)
    
    def registerEntitys(self, name, listSentences: list):
        for s in listSentences:
            self.engine.register_entity(s, name)
    
    def registerEntity(self, name, string):
        self.engine.register_entity(string, name)
    
    def classify(self, text):
        intent = next(self.engine.determine_intent(text, include_tags=True, context_manager=self.context_manager))

        for tag in intent['__tags__']:
            context_entity = tag.get('entities')[0]
            self.context_manager.inject_context(context_entity)
        
        return intent

ic = IntentClassifier()

intent1 = IntentBuilder("TimeQueryIntent")\
            .require("TimeQuery")\
            .optionally("Location")\
            .build()

intent2 = IntentBuilder("WeatherQueryIntent")\
            .require("WeatherKeyword")\
            .optionally("Location")\
            .build()

system_activate = IntentBuilder("system@activate")\
            .require("ActivateKeyword")\
            .require("AlexMode")\
            .build()

system_deactive = IntentBuilder("system@desactivate")\
            .require("DeactiveKeyword")\
            .require("AlexMode")\
            .build()

what_calendar= IntentBuilder("what@calendar")\
            .require("TimeQuery")\
            .require("Activity")\
            .optionally("Calendar")\
            .build()

ic.registerIntents([intent1, intent2, system_activate, system_deactive])


ic.registerEntitys("TimeQuery", ["qual é o tempo", "quantas horas"])
ic.registerEntitys("Location", ["Mindelo", "Salamasa", "São Vicente", "Praia","Porto Novo"])
ic.registerEntitys("WeatherKeyword", ["clima", "condição climatica"])
ic.registerEntitys("AlexMode", ["não perturbe", "silêncio", "poupança de bateria"])
ic.registerEntitys("ActivateKeyword", ["ative","inicie","iniciar","ativar","ligue"])
ic.registerEntitys("DeactiveKeyword", ["desative","desligue","desligar","desativar"])
ic.registerEntity("Calendar", "Calendario")
ic.registerEntitys("Activity", ["reunião","aula","trabalho", "escola"])

while True:
    utterance = input("Frase: ")
    print(ic.classify(utterance))