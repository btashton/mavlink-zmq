import zmq

from argparse import ArgumentParser
from pymavlink import mavutil

def main():
    parser = ArgumentParser()
    parser.add_argument("--device", help="MAVLink device to add to zmq", required=True)
    parser.add_argument("--zmq", help="zmq url", required=True)

    args = parser.parse_args()

    try:
        msrc = mavutil.mavlink_connection(args.device, planner_format=False,
                                  notimestamps=True, robust_parsing=True)
    except Exception, e:
        print 'Could not connect to mavlink device at %s' % args.device
        print e
        return False
    
    context = zmq.Context()
    zmq_socket = context.socket(zmq.PUB)
    try:
        zmq_socket.connect(args.zmq)
    
    except Exception, e:
        print 'Failed to establish connection with zmq gateway'
        print e

    #send messages from mavlink connection to zmq gateway
    try:
        while True:
            mav_msg = msrc.recv_match()
            if mav_msg is not None:
                topic = mav_msg.get_type()
                print topic
                zmq_socket.send(topic,zmq.SNDMORE)
                zmq_socket.send_pyobj(mav_msg)
    except Exception, e:
        print 'Bridge failed'
        print e

    zmq_socket.close()
    context.term()

if __name__ == "__main__":
    main()
