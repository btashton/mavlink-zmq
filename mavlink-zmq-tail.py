import zmq

from argparse import ArgumentParser

def main():
    parser = ArgumentParser(description="Subscribe and display messages from zmq publisher")
    parser.add_argument("--zmq", help="zmq url", default="tcp://localhost:5560")
    parser.add_argument("--topics", help="zmq topic prefixes to subscribe to", default=[""], nargs='*')
    
    args = parser.parse_args()

    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    print "Collecting mavlink messages..."

    socket.connect(args.zmq)
    for topic in args.topics:
        socket.setsockopt(zmq.SUBSCRIBE, topic)
    while True:
        topic = socket.recv()
        messagedata = socket.recv_pyobj()
        print topic, messagedata

if __name__ == "__main__":
    main()
