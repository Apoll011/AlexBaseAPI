import sys

from kit import IntentKit

intentKit = IntentKit()
intentKit.train(sys.argv[1] if len(sys.argv) > 1 else "en")