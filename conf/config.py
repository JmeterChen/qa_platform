# -*- coding=utf-8 -*-
# Author: BoLin Chen
# @Date : 2020-08-10


MYSQL = {
    'production': {
	    'default': {
		    # 配置使用mysql
		    'ENGINE': 'django.db.backends.mysql',  # 数据库产品
		    'HOST': "10.50.255.161",  # 数据库ip
		    'PORT': 3306,  # 数据库端口
		    'USER': "root",
		    'PASSWORD': "261090dong",
		    'NAME': "qa_platform",  # 数据库名, 事先要创建
		    'TEST': {
			    'CHARSET': 'utf8',
			    'COLLATION': 'utf8_general_ci'
		    }
	    }
	},
	"staging": {
		'default': {
			# 配置使用mysql
			'ENGINE': 'django.db.backends.mysql',  # 数据库产品
			'HOST': "localhost",  # 数据库ip
			'PORT': 3306,  # 数据库端口
			'USER': "root",
			'PASSWORD': "19940415",
			'NAME': "qa_platform",  # 数据库名, 事先要创建
			'TEST': {
				'CHARSET': 'utf8',
				'COLLATION': 'utf8_general_ci'
			}
		}
	},
	"test": {
		'default': {
			# 配置使用mysql
			'ENGINE': 'django.db.backends.mysql',  # 数据库产品
			'HOST': "10.0.6.56",  # 数据库ip
			'PORT': 3306,  # 数据库端口
			'USER': "root",
			'PASSWORD': "Fdd*123",
			'NAME': "qa_platform",  # 数据库名, 事先要创建
			'TEST': {
				'CHARSET': 'utf8',
				'COLLATION': 'utf8_general_ci'
			}
		}
	},
	"local": {
		'default': {
			# 配置使用mysql
			'ENGINE': 'django.db.backends.mysql',  # 数据库产品
			'HOST': "localhost",  # 数据库ip
			'PORT': 3306,  # 数据库端口
			'USER': "root",
			'PASSWORD': "19940415",
			'NAME': "qa_platform",  # 数据库名, 事先要创建
			'TEST': {
				'CHARSET': 'utf8',
				'COLLATION': 'utf8_general_ci'
			}
		}
	}
}


db_mysql = {
    'prod': {
	    # 配置使用mysql
	    'host': "10.50.255.161",  # 数据库ip
	    'port': 3306,  # 数据库端口
	    'user': "root",
	    'password': "261090dong",
	    'database': "newsonar"  # 数据库名, 事先要创建
	},
	"staging": {
		# 配置使用mysql
		'host': "localhost",  # 数据库ip
		'port': 3306,  # 数据库端口
		'user': "root",
		'password': "19940415",
		'database': "qa_platform" # 数据库名, 事先要创建
	},
	"test": {
		# 配置使用mysql
		'host': "10.50.255.161",  # 数据库ip
		'port': 3306,  # 数据库端口
		'user': "root",
		'password': "261090dong",
		'database': "newsonar"  # 数据库名, 事先要创建
	},
	"local": {
		# 配置使用mysql
		'host': "localhost",  # 数据库ip
		'port': 3306,  # 数据库端口
		'user': "root",
		'password': "19940415",
		'database': "qa_platform"  # 数据库名, 事先要创建
	}
}