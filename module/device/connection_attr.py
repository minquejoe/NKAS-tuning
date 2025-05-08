import os
import re
from functools import cached_property

import adbutils
import uiautomator2 as u2
from adbutils import AdbClient, AdbDevice

from module.config.config import NikkeConfig
from module.logger import logger


class ConnectionAttr:
    config: NikkeConfig
    serial: str

    adb_binary_list = [
        './bin/adb/adb.exe',
        './toolkit/Lib/site-packages/adbutils/binaries/adb.exe',
        '/usr/bin/adb'
    ]

    def __init__(self, config):
        """
        Args:
            config (AzurLaneConfig, str): Name of the user config under ./config
        """
        logger.hr('Device', level=1)
        if isinstance(config, str):
            self.config = NikkeConfig(config, task=None)
        else:
            self.config = config

        # Init adb client
        logger.attr('AdbBinary', self.adb_binary)
        # Monkey patch to custom adb
        adbutils.adb_path = lambda: self.adb_binary
        # Cache adb_client
        _ = self.adb_client
        # Parse custom serial
        self.serial = str(self.config.Emulator_Serial).strip(' ').replace(' ', '')
        self.serial_check()

    def serial_check(self):
        """
            替换中文冒号
        """
        if '：' in self.serial:
            self.serial = self.serial.replace('：', ':')
            logger.warning(f'Serial {self.config.Emulator_Serial} is revised to {self.serial}')
            self.config.Emulator_Serial = self.serial

    @cached_property
    def adb_binary(self):
        """
            获取可执行的adb路径
        """

        # Try adb in deploy.yaml
        from module.webui.setting import State
        file = State.deploy_config.AdbExecutable
        file = file.replace('\\', '/')
        if os.path.exists(file):
            return os.path.abspath(file)

        # Try existing adb.exe
        for file in self.adb_binary_list:
            if os.path.exists(file):
                return os.path.abspath(file)

        # Try adb in python environment
        import sys
        file = os.path.join(sys.executable, '../Lib/site-packages/adbutils/binaries/adb.exe')
        file = os.path.abspath(file).replace('\\', '/')
        if os.path.exists(file):
            return file

        # Use adb in system PATH
        file = 'adb'
        return file

    @cached_property
    def adb_client(self) -> AdbClient:
        host = '127.0.0.1'
        port = 5037

        # Trying to get adb port from env
        env = os.environ.get('ANDROID_ADB_SERVER_PORT', None)
        if env is not None:
            try:
                port = int(env)
            except ValueError:
                logger.warning(f'Invalid environ variable ANDROID_ADB_SERVER_PORT={port}, using default port')

        logger.attr('AdbClient', f'AdbClient({host}, {port})')
        return AdbClient(host, port)

    @cached_property
    def adb(self) -> AdbDevice:
        return AdbDevice(self.adb_client, self.serial)

    @cached_property
    def u2(self) -> u2.Device:

        if self.serial.startswith('emulator-') or self.serial.startswith('127.0.0.1:'):
            device = u2.connect_usb(self.serial)
        else:
            device = u2.connect(self.serial)

        # Stay alive
        device.set_new_command_timeout(604800)

        logger.attr('u2.Device', f'Device(atx_agent_url={device._get_atx_agent_url()})')
        return device

    @cached_property
    def is_mumu12_family(self):
        # 127.0.0.1:16XXX
        return 16384 <= self.port <= 17408

    @cached_property
    def is_mumu_family(self):
        # 127.0.0.1:7555
        # 127.0.0.1:16384 + 32*n
        return self.serial == '127.0.0.1:7555' or self.is_mumu12_family

    @cached_property
    def is_ldplayer_bluestacks_family(self):
        # Note that LDPlayer and BlueStacks have the same serial range
        return self.serial.startswith('emulator-') or 5555 <= self.port <= 5587

    @cached_property
    def is_nox_family(self):
        return 62001 <= self.port <= 63025

    @cached_property
    def is_vmos(self):
        return 5667 <= self.port <= 5699

    @cached_property
    def is_emulator(self):
        return self.serial.startswith('emulator-') or self.serial.startswith('127.0.0.1:')

    @cached_property
    def is_network_device(self):
        return bool(re.match(r'\d+\.\d+\.\d+\.\d+:\d+', self.serial))

    @cached_property
    def is_local_network_device(self):
        return bool(re.match(r'192\.168\.\d+\.\d+:\d+', self.serial))

    @cached_property
    def is_over_http(self):
        return bool(re.match(r"^https?://", self.serial))

    @cached_property
    def is_chinac_phone_cloud(self):
        # Phone cloud with public ADB connection
        # Serial like xxx.xxx.xxx.xxx:301
        return bool(re.search(r":30[0-9]$", self.serial))