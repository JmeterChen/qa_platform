from tapd.common.readLogger import ReadLogger

logger = None


def init_logger():
	global logger
	logger = ReadLogger().get_logger()
	
init_logger()