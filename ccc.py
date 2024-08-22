import multiprocessing
import time

def cpu_stress():
    while True:
        # 执行大量计算
        x = 0
        for i in range(1, 2):
            x += (i * 0.5)

if __name__ == '__main__':
    # 获取CPU核心数
    total_cores = multiprocessing.cpu_count()

    # 提示用户输入要减去的核心数，并转换为整数
    cores_to_reduce = int(input(f"Total cores: {total_cores}. Enter the number of cores to reduce: "))

    # 计算最终使用的核心数
    num_cores = total_cores - cores_to_reduce

    # 检查最终使用的核心数是否有效
    if num_cores <= 0:
        print("Invalid input: The number of cores to reduce is too large.")
    else:
        print(f"Using {num_cores} cores.")
        processes = []

        # 启动与核心数相等的进程数
        for _ in range(num_cores):
            p = multiprocessing.Process(target=cpu_stress)
            p.start()
            processes.append(p)

        # 保持主进程运行，防止子进程退出
        try:
            while True:
                time.sleep(50)
        except KeyboardInterrupt:
            print("Interrupted by user")
            for p in processes:
                p.terminate()
                p.join()
