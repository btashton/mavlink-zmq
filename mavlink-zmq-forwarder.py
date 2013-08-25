import zmq

from argparse import ArgumentParser

def main():
    parser = ArgumentParser()
    parser.add_argument("--subport", help="zmq subscriber port", type=int, default=5559)
    parser.add_argument("--pubport", help="zmq publisher port", type=int, default=5560)
    args = parser.parse_args()

    try:
        context = zmq.Context(1)
        mavlink_out = context.socket(zmq.SUB)
        mavlink_out.bind("tcp://*:%s" % args.subport)

        mavlink_out.setsockopt(zmq.SUBSCRIBE, "")

        mavlink_in = context.socket(zmq.PUB)
        mavlink_in.bind("tcp://*:%s" % args.pubport)

        zmq.device(zmq.FORWARDER, mavlink_out, mavlink_in)

    except Exception, e:
        print e
        print "zmq forwarder going offline"

    mavlink_out.close()
    mavlink_in.close()
    context.term()

if __name__== "__main__":
    main()
