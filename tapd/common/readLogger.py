# -*- coding=utf-8 -*-
# Author: BoLin Chen
# @Date : 2020-06-17


"""基础类，用于读取日志配置文件及定义日志类"""
import os
import logging
import logging.config
import time

sep = os.sep


class ReadLogger:
	def __init__(self):
		""" 读取日志配置 """
		containerRoot = os.getenv("LOGS_DIR")
		print(containerRoot)
		p_root = os.path.abspath(os.path.join(__file__, f'..{sep}..{sep}..'))  # 项目根路径
		# root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 项目根路径
		if not containerRoot:
			root_dir = p_root
		else:
			root_dir = containerRoot
		logConfFileName = 'logs.conf'  # 指定日志配置文件名称
		logConfFilePath = p_root + sep + 'conf' + sep + logConfFileName  # 指定日志配置文件绝对路径
		now_day = time.strftime("%Y_%m_%d")
		runLogPath = f'{root_dir}{sep}output{sep}logs{sep}logs_{now_day}'
		
		while not os.path.exists(runLogPath):
			try:
				os.makedirs(runLogPath)
				break
			except OSError as e:
				if e.errno != os.errno.EEXIST:
					raise
				# time.sleep might help here
				pass
			
		logging.config.fileConfig(logConfFilePath, defaults={"LogPath": runLogPath})
		self.logger = logging.getLogger(name='rotatingFileLogger')
	
	def get_logger(self):
		""" 获取logger容器 """
		return self.logger


if __name__ == "__main__":
	read_logger = ReadLogger()
	logger = read_logger.get_logger()
	logger.debug('debug message')
