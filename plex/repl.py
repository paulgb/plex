from .service import Service
from json import loads, dumps


def repl():
    s = Service()

    while True:
        message_json = input()
        message = loads(message_json)

        for m in s.send_message(message):
            print(dumps(m))


if __name__ == '__main__':
    repl()
