import argparse
import datetime as dt

import matplotlib as mpl
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.figure import Axes
from matplotlib.ticker import MaxNLocator
from pythonping import ping

# disables default toolbar. Uncomment this line if you wanna show them.
mpl.rcParams['toolbar'] = 'None'


class Pinger:
    """A class for pinging hosts"""

    TIMEOUT = 2000  # default timeout (in ms)

    def __init__(self, host: str, timeout: int = TIMEOUT):
        """Creates a new Pinger

        Arguments:
            host {str} -- the host to ping
            timeout {int} -- the timeout (in ms)
        """
        self.host = host
        self.timeout = timeout

    def call(self) -> float:
        """Invokes a ping command

        Returns:
            float -- the round trip time (in ms)
        """
        try:
            resp = ping(self.host, count=1, timeout=self.timeout/1000)
            rtt = resp.rtt_avg_ms
        except Exception as e:
            rtt = Pinger.TIMEOUT

        return rtt


class PingPlotter:
    """A class for plotting pings"""

    LIMIT = 1000  # default limit of data points to display
    INTERVAL = 500  # default interval between pings (in ms)

    def __init__(self, pinger: Pinger, limit: int = LIMIT, interval: int = INTERVAL):
        """Creates a new PingPlotter

        Arguments:
            pinger {Pinger} -- a Pinger instance to invoke a ping request.

        Keyword Arguments:
            limit {int} -- maximum number of data points to display (default: {LIMIT})
            interval {int} -- time interval (in ms) between consecutive ping calls  (default: {INTERVAL})
        """
        self.pinger = pinger
        self.limit = limit
        self.interval = interval

        # Initialize data points
        self.timestamps = []
        self.rtts = []

    def start(self):
        """Starts the plotter to show pings"""

        fig = plt.figure()
        ax = fig.add_subplot()

        def __render_frame(i: int):
            """Renders the current frame"""

            rtt = self.pinger.call()

            self.timestamps.append(dt.datetime.now())
            self.rtts.append(rtt)

            # Truncate data points to limit
            self.timestamps = self.timestamps[-self.limit:]
            self.rtts = self.rtts[-self.limit:]

            ax.clear()
            ax.grid(True)
            ax.plot_date(self.timestamps, self.rtts, 'b-')

            # Show labels
            host = self.pinger.host
            plt.title('Latency over time to {}'.format(host))
            plt.ylabel('Round-trip time (ms)')

        # Periodically update the graph
        a = animation.FuncAnimation(
            fig=fig,
            func=__render_frame,
            interval=self.interval,
        )

        plt.show()

    def stop(self):
        """Stops the plotter"""

        plt.close()
        self.timestamps = []
        self.rtts = []


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
