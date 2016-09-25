from map import map
from ai import ai

def main():
    AI = ai(map(10))
    while True:
        AI.loop()
main()
