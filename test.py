from kit import IntentKit

ik = IntentKit()

ik.reuse("pt")
ik.reuse("en")

while True:
    t = input("Your sentence: ")
    print(ik.parse(t))