#!/usr/bin/env python
#
# Copyright (C) 2007 Juan Manuel Caicedo.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""feedburner provides a library and source code that makes easy to use the
FeedBurner API from a Python program.

The following APIs are implemented:
 - FeedBurner Management API (MgmtAPI)

See: http://www.feedburner.com/fb/a/developers 

"""


import httplib2
from base64 import b64encode
from urllib import urlencode
try:
    from xml.etree import ElementTree
except ImportError:
    from elementtree import ElementTree



__author__ = "Juan Manuel Caicedo"
__copyright__ = "Copyright 2007, Juan Manuel Caicedo"
__version__ = "$Rev: 1$"
__revision__ = "$Rev: 1$"
__license__ = "Apache License 2.0"
__link__ = "http://code.google.com/p/feedburner-python-client/"

class FeedBurnerException(Exception):
    """
    Base class for errors
    """
    def __init__(self, code, message):
        self.code = code
        Exception.__init__(self, "%s (code=%s)" % (message, code))



class FeedBurnerHttp(httplib2.Http):
    """
    HTTP object for API requests.
    """
    USER_AGENT = 'feedburner-python-client/%s (%s)' % (__version__, __link__)

    def __init__(self, user, password, https=True):
        httplib2.Http.__init__(self)
        self.force_exception_to_status_code = True
        protocol = https and 'https' or 'http'
        self._prefix = protocol + '://api.feedburner.com/management/1.0/'
        self._headers = {
            'Authorization': 'Basic %s' % b64encode('%s:%s' % (user, password)),
            'user-agent': self.USER_AGENT
        }

    def _validate_response(self, rsp):
        """
        Validates the response, raising an exception when appropiate
        """
        if not rsp.get("stat") == "ok":
            err = rsp.find("err")
            raise FeedBurnerException(err.get("code"), err.get("msg"))


    def request(self, service, method, parameters=None, body=None):
        """
        Makes a HTTP request to the service.

        If the request was successful and the content is a response document,
        it returns an ElementTree object. If it was an empty response,
        returns None.

        Otherwise, if the response was an error document, it raises
        a FeedBurnerException
        """
        uri = self._prefix + service
        if parameters:
            uri = ''.join((uri, '?', urlencode(parameters)))

        headers = self._headers
        if body:
            headers['Content-Type'] = 'application/x-www-form-urlencoded'

        resp, content = httplib2.Http.request(self, uri, method, body,
                                              self._headers)
        if resp.status != 204:
            tree = ElementTree.fromstring(content)
            self._validate_response(tree)
            return tree


class Feed:
    """
    This class contains the information related to a feed.    
    """
    def __init__(self, id=None, uri=None, title=None, source=None, services = None):
        """
        Class constructor.

        One of ``id`` or ``uri`` must be provided
        """
        if None == id == uri:
            raise ValueError('One of feed id or uri must be provided')

        self.uri = uri
        self.title = title
        self.source = source
        self.id = id
        self.services = services or {}

    def _asElementTree(self):
        attributes = {}
        for attr in ('uri', 'title', 'id'):
            val = getattr(self, attr)
            if val:
                attributes[attr] = val

        feed = ElementTree.Element('feed', attributes)
        feed.append(ElementTree.Element('source', url=self.source))
        feed.append(ElementTree.Element('services'))
        for serv in self.services:
            feed.append(ElementTree.Element('service', {'class':serv}))

        return feed

    def __str__(self):
        return "Feed [id=%s, uri=%s, title=%s, source=%s]" % (
                    self.id, self.uri, self.title, self.source)

    @staticmethod
    def fromElementTree(tree):
        """
        Creates a Feed object from an ElementTree object
        """
        feed = Feed(**dict(tree.items()))

        elm_source = tree.find('source')
        if ElementTree.iselement(elm_source):
            feed.source = elm_source.get('url')

        for service in tree.findall('services/service'):
            clazz = service.get('class')
            feed.services[clazz] = {}
            for par in service.findall('param'):
                feed.services[clazz][par.get('name')] = par.text

        return feed


class Management:
    """
    Client for the FeedBurner Management API (MgmtAPI).

    See http://www.feedburner.com/fb/a/developers/feedapi
    """
    def __init__(self, user, password):
        self._http = FeedBurnerHttp(user, password)

    def find(self):
        """
        Finds the list of the feeds for the user

        Returns a list of Feed objects.

        See: http://www.feedburner.com/fb/a/developers/feedapi#Find_Feeds
        """
        tree = self._http.request("FindFeeds", "GET")
        feeds = []
        for elm_feed in tree.findall('*/feed'):
            feeds.append(Feed.fromElementTree(elm_feed))

        return feeds

    def get(self, feed_id=None, uri=None):
        """
        Gets a Feed object based on its id or uri

        See: http://www.feedburner.com/fb/a/developers/feedapi#Get_Feed
        """
        if None == feed_id == uri:
            raise ValueError('One of feed id or uri must be provided')

        pars = {'id': feed_id, 'uri': uri}
        tree = self._http.request("GetFeed", "GET", pars)
        elm_feed = tree.find('feed')
        if ElementTree.iselement(elm_feed):
            return Feed.fromElementTree(elm_feed)

        raise ValueError('Feed not found')

    def modify(self, feed):
        """
        Modifies a feed.
        Args:
            feed: Feed The object with the new information of the feed.

        Returns:
            The modified Feed object.

        See: http://www.feedburner.com/fb/a/developers/feedapi#Modify_Feed
        """
        tree = feed._asElementTree()
        body = urlencode({"feed" : ElementTree.tostring(tree)})
        tree = self._http.request("ModifyFeed", "POST", body=body)
        elm_feed = tree.find('feed')
        return Feed.fromElementTree(elm_feed)

    def add(self, feed):
        """
        Adds a new feed.
        Args:
            feed: Feed The object with the information of the feed.

        Returns:
            The new Feed object.

        See: http://www.feedburner.com/fb/a/developers/feedapi#Add_Feed
        """
        tree = feed._asElementTree()
        body = urlencode({"feed" : ElementTree.tostring(tree)})

        tree_resp = self._http.request("AddFeed", "POST", body=body)
        elm_feed = tree_resp.find('feed')
        return Feed.fromElementTree(elm_feed)

    def resync(self, feed):
        """
        Synchronizes the feed information
        Args:
            feed: Feed The object with the information of the feed.

        See: http://www.feedburner.com/fb/a/developers/feedapi#Resync_Feed
        """
        pars = {'id': feed.id, 'uri': feed.uri}
        self._http.request("ResyncFeed", "POST", pars)


    def delete(self, feed):
        """
        Deletes a feed.
        Args:
            feed: Feed The object that will be removed.

        See: http://www.feedburner.com/fb/a/developers/feedapi#Delete_Feed
        """
        pars = {'id': feed.id, 'uri': feed.uri}
        self._http.request("DeleteFeed", "POST", pars)

