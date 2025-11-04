import uuid
import platform
import subprocess
import re


def get_physical_mac():
    """获取设备的物理MAC地址（硬件地址）"""
    try:
        # 方法1：使用uuid模块获取通用MAC地址
        mac = uuid.getnode()
        mac_hex = ':'.join(("%012X" % mac)[i:i + 2] for i in range(0, 12, 2))

        # 方法2：尝试获取特定网络接口的物理地址（更可靠）
        if platform.system() == "Windows":
            # Windows系统
            output = subprocess.check_output("ipconfig /all", shell=True).decode('cp850')
            # 匹配物理地址行
            mac_pattern = re.compile(r"(?:Physical Address|物理地址)[\s.:-]+([0-9A-Fa-f\-:]+)")
            match = mac_pattern.search(output)
            if match:
                return match.group(1).replace('-', ':').upper()

        elif platform.system() == "Linux":
            # Linux系统
            output = subprocess.check_output("ip link show", shell=True).decode()
            mac_pattern = re.compile(r"link/ether\s+([0-9a-f]{2}(?::[0-9a-f]{2}){5})", re.I)
            match = mac_pattern.search(output)
            if match:
                return match.group(1).upper()

        elif platform.system() == "Darwin":  # macOS
            # macOS系统
            output = subprocess.check_output("ifconfig en0", shell=True).decode()
            mac_pattern = re.compile(r"ether\s+([0-9a-f]{2}(?::[0-9a-f]{2}){5})", re.I)
            match = mac_pattern.search(output)
            if match:
                return match.group(1).upper()

        # 如果特定平台方法失败，返回通用方法结果
        return mac_hex

    except Exception as e:
        print(f"获取物理MAC地址时出错: {e}")
        return None

