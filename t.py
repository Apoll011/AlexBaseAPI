from features.intent_recognition.padaos import IntentContainer
from features.intent_recognition import train

train("pt-pt")

container = IntentContainer()

container.add_intent('system@activate', ['(ative|iniciar|ativar|ligue) (o|a) modo {do}'])
container.add_intent('goodbye', ['See you!', 'Goodbye!'])
container.add_intent('search', ['Search for {query} (using|on) {engine}.'])

print(container.calc_intent('Iniciar o modo Voo'))
print(container.calc_intent('Search for cats on CatTube.'))

container.remove_intent('goodbye')