import threading
import signal
import sys

int_args = ["id", "is_proxy", 'retry']

def parse_argv():
    ret_dict = {}
    for arg in sys.argv:
        pos = arg.find('=')
        if pos < 0:
            continue
        ret_dict[arg[:pos]] = arg[pos+1:]
    for int_key in int_args:
        if int_key in ret_dict:
            val = ret_dict[int_key]
            try:
                ret_dict[int_key] = int(val)
            except:
                ret_dict.pop(int_key)
    return ret_dict


def run(Client):
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print "Usage: python %s is_proxy=0 retry=2 [id]" % sys.argv[0]
        return
    client = Client()
    t = threading.Thread(target = client.start, kwargs=parse_argv())
    t.start()
    signal.signal(signal.SIGINT, client.shutdown)
    signal.signal(signal.SIGTERM, client.shutdown)
    signal.pause()
    t.join()

if __name__ == "__main__":
    print parse_argv()
