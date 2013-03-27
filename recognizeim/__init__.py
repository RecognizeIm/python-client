import sys, os, string
from SOAPpy import WSDL,HTTPTransport,Config,SOAPAddress
import ClientCookie
import urllib2
import base64
import json
import hashlib
import ast
import Image

#limits for query images:
#for SingleIR
SINGLEIR_MAX_FILE_SIZE = 500    #KBytes
SINGLEIR_MIN_DIMENSION = 100    #pix
SINGLEIR_MIN_IMAGE_AREA = 0.05  #Mpix
SINGLEIR_MAX_IMAGE_AREA = 0.31  #Mpix
#for MultipleIR
MULTIIR_MAX_FILE_SIZE = 3500    #KBytes
MULTIIR_MIN_DIMENSION = 100     #pix
MULTIIR_MIN_IMAGE_AREA = 0.1    #Mpix
MULTIIR_MAX_IMAGE_AREA = 5.1    #Mpix

class CookieTransport(HTTPTransport):
  def call(self, addr, data, namespace, soapaction = None, encoding = None,
    http_proxy = None, config = Config):

    if not isinstance(addr, SOAPAddress):
      addr = SOAPAddress(addr, config)
    
    cookie_cutter = ClientCookie.HTTPCookieProcessor(config.cookieJar)
    hh = ClientCookie.HTTPHandler()

    opener = ClientCookie.build_opener(cookie_cutter, hh)

    t = 'text/xml';
    if encoding != None:
      t += '; charset="%s"' % encoding
    opener.addheaders = [("Content-Type", t),
              ("Cookie", "Username=foobar"), # ClientCookie should handle
              ("SOAPAction" , "%s" % (soapaction))]
              
    response = opener.open(addr.proto + "://" + addr.host + addr.path, data)
    data = response.read()

    # get the new namespace
    if namespace is None:
      new_ns = None
    else:
      new_ns = self.getNS(namespace, data)

    # return response payload
    return data, new_ns
# From xmethods.net

class recognizeApi(object):
  """Class to handle requests to recognize.im API.

  :param client_id: Your unique client ID. You can find it in the Account tab after logging in at recognize.im.
  :type client_id: str.
  :param api_key: Your unique API key. You can find it in the Account tab after logging in at recognize.im..
  :type api_key: str.
  :param clapi_key: Your unique secret client key. You can find it in the Account tab after logging in at recognize.im.
  :type clapi_key: str.
  :returns: dict -- the server response.
  """
  
  wsdl = "http://clapi.itraff.pl/wsdl"
  rest = "http://recognize.im/recognize/"
  
  Config.cookieJar = ClientCookie.MozillaCookieJar()

  def __init__(self, client_id, api_key, clapi_key):
    self.client_id = client_id
    self.clapi_key = clapi_key
    self.api_key = api_key
    self._server = WSDL.Proxy(self.wsdl, transport = CookieTransport)
    result = self._server.auth(client_id, clapi_key, None)
    
  def convertOutput(self, soap):
    """Converts SOAPpy.Types.structType to dict.

    :param soap: The URL to the method you want us to call.
    :type soap: SOAPpy.Types.structType.
    :returns: dict -- the server response converted to dict.
    """
    
    d = {}
    if type(soap).__name__=='instance' and 'item' in soap._keys():
        soap = soap[0]
    if type(soap).__name__=='list':
        for i in range(0,len(soap)):
            if type(soap[i]['value']).__name__=='instance':
                d[soap[i]['key']] = self.convertOutput(soap[i]['value'])
            else:
                d[soap[i]['key']] = soap[i]['value']
    elif type(soap).__name__=='instance':
        d[soap['key']] = soap['value']
    return d

  def imageInsert(self, image_id, image_name, path):
    """Add new picture to your pictures list

    :param image_id: A unique identifier of the inserted image.
    :type image_id: str.
    :param image_name: A label you want to assign to the inserted image.
    :type image_name: str.
    :param path: Path to the image file.
    :type path: str.
    :returns: dict -- the server response.
    """
    
    image = open(path, "rb").read()
    encoded = base64.b64encode(image)
    result = self._server.imageInsert(image_id, image_name, encoded);
    return self.convertOutput(result)

  def indexBuild(self):
    """You need to call indexBuild method in order to apply all your recent
    (from the previous call of this method) changes, including adding new images
    and deleting images. 

    :returns: dict -- the server response.
    """
    
    result = self._server.indexBuild()
    return self.convertOutput(result)

  def callback(self, callback_url):
    """There are some situations when we might need to call one of your methods.
    For example when we finish applying changes we may need to let you know that
    all your images are ready to be recognized.

    :param callback_url: The URL to the method you want us to call.
    :type callback_url: str.
    :returns: dict -- the server response.
    """
    
    result = self._server.callback(callback_url)
    return self.convertOutput(result)

  def imageDelete(self, image_id):
    """If you don't need an image to be recognizable anymore you have to remove
    this image from the database. You can do this by calling imageDelete method
    passing the ID of the image you want to remove. You can also remove all of
    your images with one call of this method. In order to achieve this you need
    to pass null value as a parameter.

    :param image_id: ID of the image you would like to remove (this is the same ID you pass a an argument to the imageInsert method). Pass null value if you want to remove all of your images.
    :type image_id: str.
    :returns: dict -- the server response.
    """
    
    result = self._server.imageDelete(image_id)
    return self.convertOutput(result)

  def imageUpdate(self, image_id, new_image_id, new_image_name):
    """There may be some situations when you would like to change the name or ID of
    an image stored in the database. You can do this by calling the imageUpdate method.

    :param image_id: ID of the image which data you would like to change (this is the same ID you pass a an argument to the imageInsert method).
    :type image_id: str.
    :param new_image_id: New ID of an image.
    :type new_image_id: str.
    :param new_image_name: New name of an image
    :type new_image_name: str.
    :returns: dict -- the server response.
    """
    
    data = {"id": new_image_id,
            "name": new_image_name}
    result = self._server.imageUpdate(image_id, data)
    return self.convertOutput(result)

  def indexStatus(self):
    """You may be curious what is the progress of applying your changes.
    In order to do this you need to call indexStatus method.

    :returns: dict -- the server response.
    """
    
    result = self._server.indexStatus()
    return self.convertOutput(result)

  def userLimits(self):
    """When using our API you are limited with regards the number of images
    and number of scans (recognition operations). The limits depend on the type
    of account you have. In order to check how many more images you can add and
    how many scans you have left use the userLimits method.

    :returns: dict -- the server response.
    """
    
    result = self._server.userLimits()
    return self.convertOutput(result)

  def imageCount(self):
    """Returns number of images in your list.

    :returns: dict -- the server response.
    """
    
    result = self._server.imageCount()
    return self.convertOutput(result)

  def imageGet(self, image_id):
    """Returns detailed information about image.

    :param image_id: ID of the image.
    :type image_id: str.
    :returns: dict -- the server response.
    """
    
    result = self._server.imageGet(image_id)
    return self.convertOutput(result)

  def modeGet(self):
    """Returns recognition mode.

    :returns: dict -- the server response.
    """
    
    result = self._server.modeGet()
    return self.convertOutput(result)

  def modeChange(self):
    """Changes recognition mode.

    :returns: dict -- the server response.
    """
    
    result = self._server.modeChange()
    return self.convertOutput(result)

  def recognize(self, path, getAll=False, multi=False): 
    """Sends image recognition request.

    :param path: Path to the image file.
    :type path: str.
    :returns: dict -- the server response.
    """
    
    #fetch image data
    size = os.stat(path).st_size / 1024.0 #KB
    image = Image.open(path)
    width, height = image.size
    area = width * height / 10.0**6 #Mpix

    #check image data
    if (multi):
      if (size > MULTIIR_MAX_FILE_SIZE or
          width < MULTIIR_MIN_DIMENSION or
          height < MULTIIR_MIN_DIMENSION or
          area < MULTIIR_MIN_IMAGE_AREA or
          area > MULTIIR_MAX_IMAGE_AREA):
        return "Image does not meet the requirements of multi mode query image.\n"
    else:
      if (size > SINGLEIR_MAX_FILE_SIZE or
          width < SINGLEIR_MIN_DIMENSION or
          height < SINGLEIR_MIN_DIMENSION or
          area < SINGLEIR_MIN_IMAGE_AREA or
          area > SINGLEIR_MAX_IMAGE_AREA):
        return "Image does not meet the requirements of single mode query image.\n"

    #get url
    url = self.rest
    if (multi):
      url += 'multi/'
      if (getAll):
        url += 'allInstances/'
    elif (getAll):
        url += 'allResults/'
    url += self.client_id
    
    imageData = open(path, "rb").read()
    
    m = hashlib.md5()
    m.update(self.api_key)
    m.update(imageData)
    md5hash = m.hexdigest()

    headers = { 'content-type':'image/jpeg',
                'x-itraff-hash' : md5hash}

    request = urllib2.Request(url, imageData, headers)
    response = urllib2.urlopen(request)
    result = response.read()

    return ast.literal_eval(result)
