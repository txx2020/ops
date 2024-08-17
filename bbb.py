import time

def memory_stress(target_size_gb):
    """
    Allocate and release memory between target_size_gb and target_size_gb - 1 GB.
    """
    memory_blocks = []
    block_size = 10**7  # 每次分配10MB的内存块
    interval = 0.01  # 分配/释放间隔时间（秒）
    allocated_size = 0

    min_size_gb = target_size_gb - 1  # 计算最小内存阈值

    try:
        while True:
            # 逐步分配内存，直到达到目标内存大小
            while allocated_size < target_size_gb * 1024**3:
                block = bytearray(block_size)
                memory_blocks.append(block)
                allocated_size += block_size
                print(f"Allocated {allocated_size / 1024**3:.2f} GB")
                time.sleep(interval)
            
            print(f"Reached {target_size_gb} GB. Starting to release memory...")

            # 逐步释放内存，直到达到最小内存阈值
            while allocated_size > min_size_gb * 1024**3:
                memory_blocks.pop()
                allocated_size -= block_size
                print(f"Released memory. Remaining: {allocated_size / 1024**3:.2f} GB")
                time.sleep(interval)
            
            print(f"Reached {min_size_gb} GB. Starting to allocate memory again...")

    except KeyboardInterrupt:
        print("Memory stress test interrupted by user.")
        print(f"Total allocated memory: {allocated_size / 1024**3:.2f} GB")

if __name__ == '__main__':
    target_size_gb = float(input("Enter target memory size in GB: "))
    
    if target_size_gb <= 1:
        print("Invalid size. Please enter a value greater than 1 GB.")
    else:
        memory_stress(target_size_gb)
