import os, sys
this_dir = os.path.dirname(os.path.realpath(__name__))
sys.path.insert(0, os.path.join(this_dir, 'libs', 'leap'))

import Leap
import time
import sys

class FingerPoint(object):
    """
    All usefull information about a finger.

    Arguments:
    position  -- (Real, Real, Real) : Position of the finger
    velocity  -- (Real, Real, Real) : Velocity of the finger
    direction -- (Real, Real, Real) : Direction vector of the finger
    """
    def __init__(self, position, velocity, direction):
        super(FingerPoint, self).__init__()
        self.position = position
        self.velocity = velocity
        self.direction = direction

    def __str__(self):
        """
        String representation of the point.

        Returns:
        String representation
        """
        info = list(self.position)
        info += list(self.velocity)
        info += list(self.direction)
        return '%f %f %f %f %f %f %f %f %f' % tuple(info)

    @classmethod
    def from_words(cls, words):
        """
        Construct a *FingerPoint* from a list of words *words*. Consum the read
        words from the list.

        Arguments:
        words -- List of words to read in

        Returns:
        Constructed *FingerPoint*

        Raises:
        ValueError : if there is not enough words to read or if read words are
        not real number.
        """
        if len(words) < 9:
            raise ValueError('Not enough words to read a FingerPoint.')

        X = [words.pop(0) for _ in xrange(9)]
        try:
            X = map(float, X)
        except ValueError as e:
            raise e

        position = X[0], X[1], X[2]
        velocity = X[3], X[4], X[5]
        direction = X[6], X[7], X[8]
        return cls(position, velocity, direction)

class FingerMove(object):
    """
    Basic structure representing a move of a finger.

    Arguments:
    name -- String : Name of the move
    data -- [FingerPoint] : Temporal list of finger points
    """
    def __init__(self, name, data):
        assert len(data) >= 1
        super(FingerMove, self).__init__()
        self.name = name
        self.data = data

    def __str__(self):
        """
        String representation of the move.

        Returns:
        String representation
        """
        pos_str = map(str, self.data)
        return '%s %s' % (self.name, ' '.join(pos_str))

    @classmethod
    def from_string(cls, string):
        """
        Construct a *FingerMove* from a string.

        Arguments:
        string -- Input string to transfom into Move

        Returns:
        The constructed move

        Raises:
        ValueError : When the string format is not good
        """
        words = string.split(' ')
        if len(words) < 2:
            raise ValueError('A move have to contain a minimum of a name.')

        name = words.pop(0)
        data = []
        while words:
            try:
                data.append(FingerPoint.from_words(words))
            except ValueError as e:
                raise e

        return cls(name, data)

    def save(self, file=sys.stdout):
        """
        Write the moves into the file *file*

        Arguments:
        file    -- File : File to write in

        Raises:
        IOError : When it's impossible to write into the file
        """
        try:
            file.write(str(self) + '\n')
        except IOError:
            raise

def acquire_move(ctrl, size, time_sleep=0.005):
    """
    Get a mouse move with a size of *size* points.

    Arguments:
    ctrl       -- Leap.Controller : Controller to use
    size       -- Integer : The number of position taken for the move
    time_sleep -- Real : Time to sleep between taking the positions (default
    0.005)

    Returns:
    [Real] : A list of size *size* containing the moves (dx, dy).

    Raises:
    RuntimeError : When there is a problem during the acquisition (more than
    one hand or finger or the finger disappear, ...)
    """
    while len(ctrl.frame().hands) != 1 and len(ctrl.frame().hands[0].fingers) != 1:
        time.sleep(0.001)

    frame = ctrl.frame()
    id_hand = frame.hands[0].id
    id_finger = frame.hands[0].fingers[0].id

    finger = frame.hands[0].fingers[0]
    o_pos = finger.tip_position.x, finger.tip_position.y, finger.tip_position.z
    # o_vel = finger.tip_velocity.x, finger.tip_velocity.y, finger.tip_velocity.z
    # o_dir = finger.direction.x, finger.direction.y, finger.direction.z
    move = []
    for _ in xrange(size):
        frame = ctrl.frame()
        if len(frame.hands) != 1:
            raise RuntimeError('Data acquisition stop by hands.')
        if frame.hands[0].id != id_hand:
            raise RuntimeError('Data acquisition stop by hand\'s id.')
        if len(frame.hands[0].fingers) != 1:
            raise RuntimeError('Data acquisition stop by fingers.')
        if frame.hands[0].fingers[0].id != id_finger:
            raise RuntimeError('Data acquisition stop by finger\'s id.')

        finger = frame.hands[0].fingers[0]
        f_pos = finger.tip_position.x, finger.tip_position.y, finger.tip_position.z
        f_vel = finger.tip_velocity.x, finger.tip_velocity.y, finger.tip_velocity.z
        f_dir = finger.direction.x, finger.direction.y, finger.direction.z
        f_dpos = map(lambda x: x[0] - x[1], zip(f_pos, o_pos))
        point = FingerPoint(f_dpos, f_vel, f_dir)
        move.append(point)
        time.sleep(time_sleep)
    return move

def wait_move(ctrl, static_threashold=10):
    """
    Wait and block until there is only one hand and one finger and the finger
    move by *static_threashold* distance.

    Arguments:
    ctrl              -- Leap.Controller : Controller to use
    static_threashold -- Real : Distance the finger has to move (default 20)
    """
    origin = None
    while True:
        time.sleep(0.01)
        frame = ctrl.frame()
        if len(frame.hands) != 1:
            origin = None
            continue
        if len(frame.hands[0].fingers) != 1:
            origin = None
            continue
        if origin is None:
            origin = frame.hands[0].fingers[0].tip_position
            continue
        p = frame.hands[0].fingers[0].tip_position
        if abs(p.x - origin.x) + abs(p.y - origin.y) >= static_threashold:
            break

if __name__ == '__main__':
    ctrl = Leap.Controller()
    while not ctrl.is_connected:
        time.sleep(0.001)

    cont = True
    moves = []

    print 'Move name ?',
    name = raw_input()

    while cont:
        print 'Waiting the beginning of the move...'
        wait_move(ctrl)
        print 'Recording the move...'
        try:
            move = FingerMove(name, acquire_move(ctrl, 100))
        except RuntimeError as e:
            print e.message
        else:
            print 'Keep it ? (y/n)',
            if raw_input() == 'y':
                moves.append(move)
                print 'Continue ? (y/n)',
                cont = raw_input() == 'y'

    if moves:
        _f_name = name.lower() + '.mv'
        print 'Save moves into ? [%s]' % _f_name,
        f_name = raw_input()
        if not f_name:
            f_name = _f_name

        print 'Saving into %s...' % f_name,
        with open(f_name, 'w+') as f:
            for m in moves:
                m.save(f)
        print 'OK'
