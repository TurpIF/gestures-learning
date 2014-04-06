import pymouse
import time
import sys
from sklearn.neighbors import KNeighborsClassifier as Learner

class Move(object):
    """
    Basic structure representing a move.

    Arguments:
    name  -- String : Name of the move
    descr -- [(Integer, Integer)] : Temporal list of (dx, dy) representing the
    movement.
    """
    def __init__(self, name, descr):
        assert len(descr) >= 1
        super(Move, self).__init__()
        self.name = name
        self.descr = descr

    def __str__(self):
        """
        String representation of the move.

        Returns:
        String representation
        """
        pos_str = map(lambda p: '%d %d' % p, self.descr)
        return '%s %s' % (self.name, ' '.join(pos_str))

    @classmethod
    def from_string(cls, string):
        """
        Construct a *Move* from a string.

        Arguments:
        string -- Input string to transfom into Move

        Returns:
        The constructed move

        Raises:
        ValueError : When the string format is not good
        """
        words = string.split(' ')
        if len(words) < 3:
            raise ValueError('A move have to contain a minimum of a name and one position.')
        if len(words) % 2 != 1:
            raise ValueError('Expected one more integer')

        name = words[0]
        try:
            ints = map(int, words[1:])
        except ValueError as e:
            raise e
        couples = zip(ints[::2], ints[1::2])
        return cls(name, couples)

    def save(self, file=sys.stdout):
        """
        Write the moves into the file *file*

        Arguments:
        file    -- File : File to write in

        Raises:
        IOError : When it's impossible to write into the file
        """
        try:
            file.write(str(self))
        except IOError:
            raise

def acquire_move(size, time_sleep=0.005):
    """
    Get a mouse move with a size of *size* points.

    Arguments:
    size       -- Integer : The number of position taken for the move
    time_sleep -- Real : Time to sleep between taking the positions (default
    0.005)

    Returns:
    [Real] : A list of size *size* containing the moves (dx, dy).
    """
    mouse = pymouse.PyMouse()
    o = mouse.position()
    move = []
    for _ in xrange(size):
        pos = mouse.position()
        dx = pos[0] - o[0]
        dy = pos[1] - o[1]
        move.append((dx, dy))
        time.sleep(time_sleep)
    return move

def wait_mouse_move(static_threashold=20):
    """
    Wait and block until the mouse move by *static_threashold*.

    Arguments:
    static_threashold -- Real : Distance the mouse has to move (default 20)
    """
    mouse = pymouse.PyMouse()
    o = mouse.position()
    static_threashold = 20
    while abs(mouse.position()[0] - o[0]) + abs(mouse.position()[1] - o[1]) \
            < static_threashold:
        time.sleep(0.01)

if __name__ == '__main__':
    cont = True
    moves = []

    print 'Move name ?',
    name = raw_input()

    while cont:
        print 'Waiting the beginning of the move...'
        wait_mouse_move()
        print 'Recording the move...'
        move = Move('LEFT', acquire_move(100))
        print 'Keep it ? (y/n)',
        if raw_input() == 'y':
            moves.append(move)
            print 'Continue ? (y/n)',
            cont = raw_input() == 'y'

    if moves:
        print 'Save moves into ? [%s]' % (name.lower() + '.mv'),
