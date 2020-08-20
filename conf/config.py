# -*- coding=utf-8 -*-
# Author: BoLin Chen
# @Date : 2020-08-10


MYSQL = {
    'production': {
	    'default': {
		    'ENGINE': 'django.db.backends.mysql',
		    'HOST': "10.50.255.161",
		    'PORT': 3306,
		    'USER': "root",
		    'PASSWORD': "261090dong",
		    'NAME': "qa_platform",
		    'TEST': {
			    'CHARSET': 'utf8',
			    'COLLATION': 'utf8_general_ci'
		    }
	    }
	},
	"test": {
		'default': {
			'ENGINE': 'django.db.backends.mysql',
			'HOST': "10.50.255.105",
			'PORT': 3306,
			'USER': "qa_platform_test",
			'PASSWORD': "fPaOw44UgXdWdoCA",
			'NAME': "qa_platform",
			'TEST': {
				'CHARSET': 'utf8',
				'COLLATION': 'utf8_general_ci'
			}
		}
	},
	"local": {
		'default': {
			# 配置使用mysql
			'ENGINE': 'django.db.backends.mysql',
			'HOST': "10.0.6.56",
			'PORT': 3306,
			'USER': "root",
			'PASSWORD': "Fdd*123",
			'NAME': "qa_platform",
			'TEST': {
				'CHARSET': 'utf8',
				'COLLATION': 'utf8_general_ci'
			}
		}
	}
}


db_mysql = {
    'master': {
	    'host': "10.50.255.161",
	    'port': 3306,
	    'user': "root",
	    'password': "261090dong",
	    'database': "newsonar"
    }
}