#!/usr/bin/env python

##################################################################################################
#
#   openomy-python 0.1 : Python bindings for the Openomy REST API
#
#   v0.1 : Manpreet Singh 2006-01-02
#   		First release
#
#   Copyright (C) 2005-2006 Manpreet Singh ('manpreet_singh@users.sourceforge.net')
#
#   Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
#   associated documentation files (the "Software"), to deal in the Software without restriction,
#   including without limitation the rights to use, copy, modify, merge, publish, distribute,
#   sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
#   furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in all copies or substantial
#   portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
#   LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#   IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
#   WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#   SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
##################################################################################################


import urllib, md5, string, os, sys, time, urllib2, mimetools, mimetypes, webbrowser;

from string import find;

# This is where your personal private key should be
priv_key="1e31cb69be8d30070f7607b4f23d4f95";

# App key to be set here
app_key="39578658";

class File:
	__file_id = "";
	__file_name = "";

	def __init__(self, file_id, file_name):
		self.__file_id = file_id;
		self.__file_name = file_name;

	def get_id(self):
		return self.__file_id;

	def get_name(self):
		return self.__file_name;

	def download_file_url(self, base_url, file_token):
		paramlist = {};
		paramlist['fileToken'] = file_token;
		cksum = utils.get_md5_sig(paramlist);
		url = utils.download_url + "?" + utils.encode_params(paramlist, cksum);
		return url;
		
	# Retrieve the contents of the file in the local file 'local_filename'
	def retrieve_file(self, local_filename, timeout="10"):
		paramlist = {};
		paramlist['method'] = "Files.GetFile";
		paramlist['fileID'] = self.__file_id;
		paramlist['timeout'] = timeout;
		cksum = utils.get_md5_sig(paramlist);
		url = utils.base_api_url + "?" + utils.encode_params(paramlist, cksum);

		f = urllib.urlopen(url);
		resp_data = f.read();

		if (utils.is_success(resp_data)):
			base_url = utils.extract_string_from_resp(resp_data, "<baseurl>", "</baseurl>");	
			file_token = utils.extract_string_from_resp(resp_data, "<filetoken>", "</filetoken>");	
			url = self.download_file_url(base_url, file_token);
			urllib.urlretrieve(url, local_filename);
			
		else:
			print "Error in getting download info for file id", self.__file_id;
			print resp_data;
	
	# Retrieve the contents of the file	
	def retrieve_file_data(self, timeout="10"):
		paramlist = {};
		paramlist['method'] = "Files.GetFile";
		paramlist['fileID'] = self.__file_id;
		paramlist['timeout'] = timeout;
		cksum = utils.get_md5_sig(paramlist);
		url = utils.base_api_url + "?" + utils.encode_params(paramlist, cksum);

		f = urllib.urlopen(url);
		resp_data = f.read();

		if (utils.is_success(resp_data)):
			base_url = utils.extract_string_from_resp(resp_data, "<baseurl>", "</baseurl>");	
			file_token = utils.extract_string_from_resp(resp_data, "<filetoken>", "</filetoken>");	
			url = self.download_file_url(base_url, file_token);
			f = urllib.urlopen(url);
			file_data = f.read();
			return file_data;
		else:
			print "Error in getting download info for file id", self.__file_id;
			print resp_data;
		
	def get_all_files(self):
		return self.__file_list;


class Tag:
	__tag_id = "";
	__tag_name = "";
	__file_list = [];

	def __init__(self, tag_id, tag_name):
		self.__tag_id = tag_id;
		self.__tag_name = tag_name;

	def get_id(self):
		return self.__tag_id;

	def get_name(self):
		return self.__tag_name;

	def get_all_files(self):
		paramlist = {};
		paramlist['method'] = "Tags.GetTag";
		paramlist['tagID'] = self.__tag_id;
		cksum = utils.get_md5_sig(paramlist);
		url = utils.base_api_url + "?" + utils.encode_params(paramlist, cksum);

		f = urllib.urlopen(url);
		resp_data = f.read();
		self.__file_list = [];

		if (utils.is_success(resp_data)):
			self.__file_list = utils.extract_list(resp_data, "file id", File);
		else:
			print "Error getting the file list for tag", self.__tag_id;
		
		return self.__file_list;

	def get_file_by_name(self, filename):
		for file in self.__file_list:
			if (file.get_name() == filename):
				return file;

# Miscellaneous utilities
class OpenomyUtils:

	base_api_url = "http://www.openomy.com/api/rest/";
	download_url = "http://www.openomy.com/api/download/";
	base_login_url = "http://www.openomy.com/api/login/";
	conf_token = "";


	# Obtain an MD5 signature for the given paramater list. This has be to be passed for every command
	def get_md5_sig(self, paramlist, use_conf_token = 1):
		locallist = paramlist;
		locallist['applicationKey'] = app_key;
		if (use_conf_token == 1):
			locallist['confirmedToken'] = utils.conf_token;
		keylist = locallist.keys();
		keylist.sort();
		sig_str = "";
		for k in keylist:
			sig_str += k + "=" + locallist[k];
	
		sig_str += priv_key;
	
		return md5.new(sig_str).hexdigest();

	# Encode parameters for including in the URL
	def encode_params(self, paramlist, cksum, use_conf_token = 1):
		locallist = paramlist;
		locallist['applicationKey'] = app_key;
		if (use_conf_token == 1):
			locallist['confirmedToken'] = utils.conf_token;
		locallist['signature'] = cksum;

		return urllib.urlencode(locallist);

	# Create the body for a POST request
	# From: http://berserk.org/uploadr/
	def encode_multipart_formdata(self, fields, files, BOUNDARY = '-----'+mimetools.choose_boundary()+'-----'):
       		CRLF = '\r\n'
       		L = []
       		if isinstance(fields, dict):
       	    		fields = fields.items()
	
       		for (key, value) in fields:   
       		 	L.append('--' + BOUNDARY)
       		    	L.append('Content-Disposition: form-data; name="%s"' % key)
       	    		L.append('')
       	    		L.append(value)

       		for (key, filename, value) in files:
           		filetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
           		L.append('--' + BOUNDARY)
           		L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
           		L.append('Content-Type: %s' % filetype)
           		L.append('')
           		L.append(value)

        	L.append('--' + BOUNDARY + '--')
        	L.append('')
        	body = CRLF.join(L)
        	content_type = 'multipart/form-data; boundary=%s' % BOUNDARY        # XXX what if no files are encoded
        	return content_type, body

	# Build a urllib2 HTTP POST request
	# From: http://berserk.org/uploadr/
	def build_request(self, theurl, fields, files, txheaders=None):
       		content_type, body = self.encode_multipart_formdata(fields, files)
        	if not txheaders: txheaders = {}
        	txheaders['Content-type'] = content_type
        	txheaders['Content-length'] = str(len(body))

       		return urllib2.Request(theurl, body, txheaders)

	def is_success(self, resp_str):
		return (find(resp_str, "<success>") > 0);

	def extract_string_from_resp(self, resp_str, start_tag, end_tag):
		pos1 = find(resp_str, start_tag);
		pos1 += len(start_tag);
		pos2 = find(resp_str, end_tag);

		return resp_str[pos1:pos2];

	# Extract items of 'id_string' from the XML response 'xml_resp' and build a list of objects of type 'objtype'
	def extract_list(self, xml_resp, id_string, objtype):
		objlist = [];

		pos1 = xml_resp.find(id_string);

		while ( pos1 != -1 ):
			tag_id_start = pos1 + len(id_string) + 2;
			tag_id_end = xml_resp.find('"', tag_id_start); 
			tag_name_start = xml_resp.find('>', tag_id_start) + 1; 
			tag_name_end = xml_resp.find("<", tag_name_start); 
			pos1 = xml_resp.find(id_string, tag_name_end);

			objlist.append(objtype(xml_resp[tag_id_start:tag_id_end], xml_resp[tag_name_start:tag_name_end]));

		return objlist;

	def extract_id(self, xml_resp, id_string):
		pos1 = xml_resp.find(id_string);
		tag_id_start = pos1 + len(id_string) + 2;
		tag_id_end = xml_resp.find('"', tag_id_start); 

		return xml_resp[tag_id_start:tag_id_end];

utils = OpenomyUtils();


# The main class
class Openomy:
	__taglist = [];
	__filelist = [];


	def __init__(self):

		if (priv_key == "private key here"):
			print "Please obtain a private key and an application key at www.openomy.com";
			sys.exit(1);

		if (app_key == "application key here"):
			print "Please obtain a private key and an application key at www.openomy.com";
			sys.exit(1);

		homedir = os.getenv("HOME");
		configroot = homedir + "/" + ".openomy";

		if (not os.path.isdir(configroot) and os.mkdir(configroot)):
			print "Could not create the configuration directory, check your permissions";
			sys.exit(1);

		conf_file = configroot + "/" + "confirmed_token";

		# If there is no confirmed token specified, then obtain one: let the user authenticate
		if (not os.path.isfile(conf_file)):
			utils.conf_token = self._obtain_confirmed_token();
			f = open(conf_file, "w+");
			f.write(utils.conf_token);
			f.close();
		else:
			f = open(conf_file, "r");
			utils.conf_token = f.read();
			f.close();
			if (len(utils.conf_token) != 40):
				utils.conf_token = self._obtain_confirmed_token();
				f = open(conf_file, "w+");
				f.write(utils.conf_token);
				f.close();

	# Obtain a confirmed token for the application
	def _obtain_confirmed_token(self):

		# Get an unconfirmed token first
		uncfm_token = self._get_unconfirmed_token();
		if (uncfm_token == None):
			print "Could not get an unconfirmed token";
			sys.exit();
		
		# Prompt the user to authorize the app in the browser and respond back
		self._prompt_to_authorize(uncfm_token);

		# Now that the app is authorize, obtain a confirmed token
		cfm_token = self._get_confirmed_token(uncfm_token);
		if (cfm_token == None):
			print "Could not get an unconfirmed token";
			sys.exit();

		#print "Using confirmed token:", cfm_token;
		return cfm_token;

	def _get_unconfirmed_token(self):
		paramlist = {};
		paramlist['method'] = "Auth.GetUnconfirmedToken";
		cksum = utils.get_md5_sig(paramlist, 0);
		url = utils.base_api_url + "?" + utils.encode_params(paramlist, cksum, 0);

		f = urllib.urlopen(url);
		resp_data = f.read();
		
		if (utils.is_success(resp_data)):
			uncfm_token = utils.extract_string_from_resp(resp_data, "<unconfirmedtoken>", "</unconfirmedtoken>");
			return uncfm_token;
		else:
			print resp_data;
			return None;
		
	# Prompt the user to authorize the app in the browser and respond back
	def _prompt_to_authorize(self, uncfm_token):
		paramlist = {};
		paramlist['unconfirmedToken'] = uncfm_token;
		cksum = utils.get_md5_sig(paramlist, 0);
		url = utils.base_login_url + "?" + utils.encode_params(paramlist, cksum, 0);

		try:
            		webbrowser.open(url)
            		print "Please authenticate at the url in the browser just opened";
			print "so that this application can obtain a confirmation key";
			ans = raw_input("Have you authenticated yet? (y/n):");
        	except:
           		print str(sys.exc_info());

		if (ans.lower() == "n"):
			print "You need to either authenticate or provide an existing confirmation key";
            		sys.exit();
	
	def _get_confirmed_token(self, uncfm_token):
		paramlist = {};
		paramlist['method'] = "Auth.GetConfirmedToken";
		paramlist['unconfirmedToken'] = uncfm_token;
		cksum = utils.get_md5_sig(paramlist, 0);
		url = utils.base_api_url + "?" + utils.encode_params(paramlist, cksum, 0);

		f = urllib.urlopen(url);
		resp_data = f.read();
		
		if (utils.is_success(resp_data)):
			cfm_token = utils.extract_string_from_resp(resp_data, "<confirmedtoken>", "</confirmedtoken>");
			return cfm_token;
		else:
			print resp_data;
			return None;

	def set_application_key(new_app_key):
		app_key = new_app_key;

	def get_all_tags(self):
		paramlist = {};
		paramlist['method'] = "Tags.GetAllTags";
		cksum = utils.get_md5_sig(paramlist);
		url = utils.base_api_url + "?" + utils.encode_params(paramlist, cksum);

		f = urllib.urlopen(url);
		resp_data = f.read();
		self.__taglist = [];
		
		if (utils.is_success(resp_data)):
			self.__taglist = utils.extract_list(resp_data, "tag id", Tag);
		else:
			print "Error in retrieving the tag list";
			
		return self.__taglist;

	def create_tag(self, tag_name):
		paramlist = {};
		paramlist['method'] = "Tags.CreateTag";
		paramlist['tagName'] = tag_name;
		cksum = utils.get_md5_sig(paramlist);
		url = utils.base_api_url + "?" + utils.encode_params(paramlist, cksum);

		f = urllib.urlopen(url);
		resp_data = f.read();
		
		if (utils.is_success(resp_data)):
			#print "Tag", tag_name, "created successfully";
			tag_id = utils.extract_id(resp_data, "tag id");
			self.__taglist.append(Tag(tag_id, tag_name));
		else:
			print "Error in creating the new tag", tag_name;
			
	def delete_tag(self, tag_id):
		paramlist = {};
		paramlist['method'] = "Tags.DeleteTag";
		paramlist['tagID'] = tag_id;
		cksum = utils.get_md5_sig(paramlist);
		url = utils.base_api_url + "?" + utils.encode_params(paramlist, cksum);

		f = urllib.urlopen(url);
		resp_data = f.read();
		
		if (utils.is_success(resp_data)):
			#print "Tag", tag_id, "deleted successfully";
			self.__taglist.remove(self.get_tag_by_id(tag_id));
		else:
			print "Error in creating the new tag", tag_id;
			
	def add_file_to_tag(self, file_id, tag_id):
		paramlist = {};
		paramlist['method'] = "Tags.AddFileToTag";
		paramlist['tagID'] = tag_id;
		paramlist['fileID'] = file_id;
		cksum = utils.get_md5_sig(paramlist);
		url = utils.base_api_url + "?" + utils.encode_params(paramlist, cksum);

		f = urllib.urlopen(url);
		resp_data = f.read();
		
		if (utils.is_success(resp_data)):
			#print "File", file_id, "added to tag", tag_id, "successfully";

			# Refresh
			tag = self.get_tag_by_id(tag_id);
			tag.get_all_files();
		else:
			print "Error in adding file", file_id, "to tag", tag_id;
			print resp_data; 
			
	def delete_file_from_tag(self, file_id, tag_id):
		paramlist = {};
		paramlist['method'] = "Tags.DeleteFileFromTag";
		paramlist['tagID'] = tag_id;
		paramlist['fileID'] = file_id;
		cksum = utils.get_md5_sig(paramlist);
		url = utils.base_api_url + "?" + utils.encode_params(paramlist, cksum);

		f = urllib.urlopen(url);
		resp_data = f.read();
		
		if (utils.is_success(resp_data)):
			#print "File", file_id, "deleted from tag", tag_id, "successfully";
			tag = self.get_tag_by_id(tag_id);
			tag.get_all_files();
		else:
			print "Error in deleting file", file_id, "from tag", tag_id;
			print resp_data; 
			
	def get_all_files(self):
		paramlist = {};
		paramlist['method'] = "Files.GetAllFiles";
		cksum = utils.get_md5_sig(paramlist);
		url = utils.base_api_url + "?" + utils.encode_params(paramlist, cksum);

		f = urllib.urlopen(url);
		resp_data = f.read();
		self.__filelist = [];
		
		if (utils.is_success(resp_data)):
			self.__filelist = utils.extract_list(resp_data, "file id", File);
		else:
			print "Error in retrieving the file list";
			print resp_data;
			
		return self.__filelist;

	def get_all_files_from_tags(self):
		self.__filelist = [];

		for tag in self.__taglist:
			self.__filelist.extend(tag.get_all_files());

		return self.__filelist;

	def get_tag_id_by_name(self, tag_name):
		for tag in self.__taglist:
			if (tag.get_name() == tag_name):
				return tag.get_id();

	def get_tag_by_id(self, tag_id):
		for tag in self.__taglist:
			if (tag.get_id() == tag_id):
				return tag;

	def get_tag_by_name(self, tagname):
		for tag in self.__taglist:
			if (tag.get_name() == tagname):
				return tag;

	def get_file_id_by_name(self, file_name):
		for file in self.__filelist:
			if (file.get_name() == file_name):
				return file.get_id();

	def get_file_by_name(self, file_name):
		for file in self.__filelist:
			if (file.get_name() == file_name):
				return file;

	def add_file(self, local_filename, tag_id = "0"):
		paramlist = {};
		paramlist['method'] = "Files.AddFile";
		paramlist['tagID'] = tag_id;
		cksum = utils.get_md5_sig(paramlist);

		paramlist['applicationKey'] = app_key;
		paramlist['confirmedToken'] = utils.conf_token;
		paramlist['signature'] = cksum;

		upload_file = ('fileField', os.path.basename(local_filename), open(local_filename, 'rb').read());

		req = utils.build_request(utils.base_api_url, paramlist, (upload_file,));

		f = urllib2.urlopen(req);
		resp_data = f.read();
		
		if (utils.is_success(resp_data)):
			#print "File", local_filename, " uploaded successfully";

			# Ask all tags to refresh their file list
			self.get_all_files_from_tags();
			# Refresh the file list
			self.get_all_files();
		else:
			print "Error in uploading file", local_filename;
			print resp_data; 
			
	def modify_file(self, local_filename, file_id):
		paramlist = {};
		paramlist['method'] = "Files.ModifyFile";
		paramlist['fileID'] = file_id;
		cksum = utils.get_md5_sig(paramlist);

		paramlist['applicationKey'] = app_key;
		paramlist['confirmedToken'] = utils.conf_token;
		paramlist['signature'] = cksum;

		upload_file = ('fileField', local_filename, open(local_filename, 'rb').read());

		req = utils.build_request(utils.base_api_url, paramlist, (upload_file,));

		f = urllib2.urlopen(req);
		resp_data = f.read();
		
		if (utils.is_success(resp_data)):
			#print "File", local_filename, " uploaded(modified) successfully";

			# Refresh the file list
			self.get_all_files();
		else:
			print "Error in uploading file", local_filename;
			print resp_data; 
			
	def delete_file(self, file_id):
		paramlist = {};
		paramlist['method'] = "Files.DeleteFile";
		paramlist['fileID'] = file_id;

		cksum = utils.get_md5_sig(paramlist);
		url = utils.base_api_url + "?" + utils.encode_params(paramlist, cksum);

		f = urllib.urlopen(url);
		resp_data = f.read();
	
		if (utils.is_success(resp_data)):
			#print "File", file_id, "deleted successfully";

			# Ask all tags to refresh their file list
			self.get_all_files_from_tags();
			self.get_all_files();
		else:
			print "Error in deleting file", file_id;
			print resp_data; 
			

# Diagnostics
def dump_all():
	print "Dump ...";
	for t in op.get_all_tags():
		print "Tag id: ", t.get_id(), " name: ", t.get_name();
		for f in t.get_all_files():
			print "	File id: ", f.get_id(), " name: ", f.get_name();
			print "Downloading ...";
			f.retrieve_file("dir/" + f.get_name());
	print;

def dump_all_files():
	print "Dumping files ...";
	for f in op.get_all_files():
		print "	File id: ", f.get_id(), " name: ", f.get_name();
		print "Downloading ...";
		f.retrieve_file("dir/" + f.get_name());
	print;

