import logging
import datetime
import os

def configure_logging(filename_prefix="NIDS"):
    """
    配置日志记录系统，生成带时间戳的日志文件
    
    参数:
        filename_prefix: 日志文件名前缀（默认: "NIDS"）
    返回:
        str: 生成的日志文件完整路径
    """
    try:
        # 创建日志目录
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        
        # 生成带时间戳的日志文件名
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        log_filename = f"NIDS_{timestamp}.log"
        log_path = os.path.join(log_dir, log_filename)
        
        # 配置日志格式
        logging.basicConfig(
            filename=log_path,
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        # 记录日志初始化信息
        logging.info("Logging system initialized")
        
        return log_path
    
    except Exception as e:
        print(f"Error initializing logging: {str(e)}")
        raise  # 重新抛出异常以便上层处理
