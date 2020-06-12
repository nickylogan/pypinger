import argparse
import datetime as dt

import matplotlib as mpl
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from pythonping import ping

# disables default toolbar
# comment out this line if you wanna show them.
mpl.rcParams['toolbar'] = 'None'


class Pinger:
    TIMEOUT = 2000  # default timeout (in ms)

    def __init__(self, host: str, timeout: int = TIMEOUT):
        self.host = host
        self.timeout = timeout

    def call(self) -> float:
        try:
            resp = ping(self.host, count=1, timeout=self.timeout/1000)
            rtt = resp.rtt_avg_ms
        except Exception as e:
            rtt = self.timeout

        return rtt


class PingPlotter:
    LIMIT = 1000  # default limit of data points to display
    INTERVAL = 500  # default interval between pings (in ms)

    def __init__(self, pinger: Pinger, limit: int = LIMIT, interval: int = INTERVAL):
        self.pinger = pinger
        self.limit = limit
        self.interval = interval

        # Initialize data points
        self.timestamps = []
        self.rtts = []

        # init plot
        self.fig, self.ax = plt.subplots()

    def __update_data(self):
        rtt = self.pinger.call()

        self.timestamps.append(dt.datetime.now())
        self.timestamps = self.timestamps[-self.limit:]
        self.rtts.append(rtt)
        self.rtts = self.rtts[-self.limit:]

    def __render_frame(self, i: int):
        self.__update_data()

        self.ax.clear()
        self.ax.grid(True)
        self.ax.plot_date(self.timestamps, self.rtts, 'b-')

        host = self.pinger.host
        plt.title('Latency over time to {}'.format(host))
        plt.ylabel('Round-trip time (ms)')

    def start(self):
        # assign to variable to avoid garbage collection.
        a = animation.FuncAnimation(
            fig=self.fig,
            func=self.__render_frame,
            interval=self.interval,
        )

        plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Plots a real-time graph of ping latency.")
    parser.add_argument('-H', '--host', dest='host',
                        default='8.8.8.8', type=str, help='the host to ping')
    parser.add_argument('-i', '--interval', dest='interval', default=PingPlotter.INTERVAL,
                        type=int, help='the interval (in ms) between consecutive ping calls')
    parser.add_argument('-l', '--limit', dest='limit', default=PingPlotter.LIMIT,
                        type=int, help='max number of data points to display')
    parser.add_argument('-t', '--timeout', dest='timeout',
                        default=Pinger.TIMEOUT, type=int, help='max ping timeout (in ms)')
    args = parser.parse_args()

    pinger = Pinger(args.host, timeout=args.timeout)
    plotter = PingPlotter(pinger, limit=args.limit, interval=args.interval)
    plotter.start()