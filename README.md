===========
Recognize.im Api
===========

This package provides access to Recognize.im API. Typical usage
looks like this::

    from recognizeim import recognizeApi
	
	#here put your data from the Account tab at recognize.im
	api = recognizeApi('11','re37a5495a','c8081c84f4f59f7f44adfc937g56ed2')

	#image recognition in single mode
	result = api.recognize("nasa.jpg")
	
	#image recognition in single mode + allResults
	result = api.recognize("nasa.jpg", getAll=True)
	
	#image recognition in multi mode
	result = api.recognize("nasa.jpg", multi=True)
	
	#image recognition in multi mode + allInstances
	result = api.recognize("nasa.jpg", multi=True, getAll=True)
	
	
Installation
=========

python setup.py install
