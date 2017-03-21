from boards.memory_board import MemoryBoard
from states.candidate import Candidate
from states.follower import Follower
from states.leader import Leader
from servers.server import Server


def main():
    board = MemoryBoard()
    state = Follower()
    oserver = Server(0, state, [], board, [])

    board = MemoryBoard()
    state = Candidate()
    server = Server(1, state, [], board, [oserver])

    oserver._neighbors.append(server)


if __name__ == "__main__":
    main()