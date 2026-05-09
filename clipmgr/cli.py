import argparse, sys
from .monitor import ClipboardMonitor
from .search import search_history

def main():
    parser = argparse.ArgumentParser(description='Clipboard history manager')
    parser.add_argument('--search', '-s', help='Search clipboard history')
    parser.add_argument('--list', '-l', action='store_true', help='List recent entries')
    parser.add_argument('--count', '-n', type=int, default=10, help='Number of entries')
    args = parser.parse_args()

    monitor = ClipboardMonitor()
    monitor.start()

    if args.search:
        results = search_history(monitor.history, args.search, args.count)
        for r in results:
            print(r['text'][:80])
    elif args.list:
        for item in monitor.history[-args.count:]:
            print(item['text'][:80])
    else:
        print('Monitoring clipboard... Press Ctrl+C to stop.')
        try:
            import time
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            monitor.stop()
            print(f'\nCaptured {len(monitor.history)} entries.')

if __name__ == '__main__':
    main()
