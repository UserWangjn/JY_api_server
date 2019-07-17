from HGTP_server.run import run_server
from old_all_server.dingshi_run.dingshi_run import all_run
from old_all_server.THREAD.thrad_run import start

from multiprocessing import Process, freeze_support

if __name__ == '__main__':
    freeze_support()

    p_server = Process(target=run_server)
    p_scheduler = Process(target=all_run)
    p_thread = Process(target=start)
    for p in [p_server, p_scheduler, p_thread]:
        print p
        p.start()
        p.join()
