===========
Recognize.im Api
===========

This package provides access to Recognize.im API. Typical usage
looks like this::

    from recognize.im import recognizeApi
	
	#here put your data from the Account tab at recognize.im
	api = recognizeApi('11','re37a5495a','c8081c84f4f59f7f44adfc937g56ed2')

	result = api.recognize("nasa.jpg")
	
Installation
=========

python setup.py install
