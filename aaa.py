import multiprocessing
import time

def cpu_stress():
    while True:
        # 执行大量计算
        x = 0
        for i in range(1, 2):
            x += (i ** 0.5) * (i ** 0.5)

if __name__ == '__main__':
    # 获取CPU核心数
    aaa = multiprocessing.cpu_count()
    num_cores = int(aaa/2)
    processes = []

    # 启动一个与核心数相等的进程数
    for _ in range(num_cores):
        p = multiprocessing.Process(target=cpu_stress)
        p.start()
        processes.append(p)

    # 保持主进程运行，防止子进程退出
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Interrupted by user")
        for p in processes:
            p.terminate()
            p.join()
