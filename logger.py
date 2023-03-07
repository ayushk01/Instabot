import time


class Logger:
    def info(self, text):
        print('[*] ', text)

    def warn(self, text):
        print('[!] ', text)

    def success(self, text):
        print('[+] ', text)

    def error(self, text):
        print('[x] ', text)

    def log_to_file(self, msg, log):
        with open('logs.txt', 'a') as f:
            f.write('\n\n')
            f.write(time.now().strftime("%d/%m/%Y %H:%M:%S"))
            f.write('\n')
            f.write(msg)
            f.write('\n')
            f.write(log)
