import sys

from server.server import Server


def main():
    i = int(sys.argv[1])
    Server(i)


if __name__ == "__main__":
    main()