class TP_HTTP_REQUEST_PARSER:
	def __init__(self, rawRequest, separator="||", parse_index="$", dupSign_start="{{{", dupSign_end="}}}", ordered_dict=False):
		import json_duplicate_keys as jdks
		import re
		import platform

		if platform.python_version_tuple()[0] == "3":
			from urllib.parse import urlparse
		else:
			from urlparse import urlparse

		## Request Method ##
		try:
			self.request_method = re.split("\r\n|\n", re.split("\r\n\r\n|\n\n", rawRequest, 1)[0])[0].split(" ")[0]
		except Exception as e:
			self.request_method = None
		##

		## Request Path ##
		try:
			self.request_path = urlparse(re.split("\r\n|\n", re.split("\r\n\r\n|\n\n", rawRequest, 1)[0])[0].split(" ")[1]).path
		except Exception as e:
			self.request_path = None
		##

		## Request Path Param ##
		self.request_pathParams = jdks.loads("{}", ordered_dict=ordered_dict)
		if self.request_path is not None:
			for path_split in self.request_path.split("/"):
				if len(path_split) > 0 and re.match("^<(.+?)>$", path_split):
					if self.request_pathParams.get(path_split) == "JSON_DUPLICATE_KEYS_ERROR":
						self.request_pathParams.set(path_split, path_split[1:-1], ordered_dict=ordered_dict)

		##

		## Request Query ##
		self.request_queryParams = jdks.loads("{}", ordered_dict=ordered_dict)
		try:
			parse_query = urlparse(re.split("\r\n|\n", re.split("\r\n\r\n|\n\n", rawRequest, 1)[0])[0].split(" ")[1]).query
			if len(parse_query) > 0:
				for param_query in parse_query.split("&"):
					if len(re.split("=", param_query, 1)) == 2:
						self.request_queryParams.set(re.split("=", param_query, 1)[0], re.split("=", param_query, 1)[1], ordered_dict=ordered_dict)
					else:
						self.request_queryParams.set(re.split("=", param_query, 1)[0], "", ordered_dict=ordered_dict)
		except Exception as e:
			pass
		##

		## Request Fragment ##
		try:
			self.request_fragment = urlparse(re.split("\r\n|\n", re.split("\r\n\r\n|\n\n", rawRequest, 1)[0])[0].split(" ")[1]).fragment
		except Exception as e:
			self.request_fragment = None
		##

		## Request HTTP Version ##
		try:
			self.request_httpVersion = re.split("\r\n|\n", re.split("\r\n\r\n|\n\n", rawRequest, 1)[0])[0].split(" ")[2]
		except Exception as e:
			self.request_httpVersion = None
		##

		## Request Headers ##
		self.request_headers = jdks.loads("{}", ordered_dict=ordered_dict)
		try:
			for header in re.split("\r\n|\n", re.split("\r\n\r\n|\n\n", rawRequest, 1)[0])[1:]:
				if re.match("^[^:]+: .*$", header):
					self.request_headers.set(re.findall("^([^:]+): (.*)$", header)[0][0], re.findall("^([^:]+): (.*)$", header)[0][1], ordered_dict=ordered_dict)
		except Exception as e:
			pass
		##

		## Request Body ##
		try:
			reqBody = re.split("\r\n\r\n|\n\n", rawRequest, 1)[1]
			if len(reqBody) > 0:
				# JSON Body
				JDKSObject = jdks.loads(reqBody, dupSign_start=dupSign_start, dupSign_end=dupSign_end, ordered_dict=ordered_dict)
				if JDKSObject:
					self.request_body = jdks.JSON_DUPLICATE_KEYS({
						"dataType": "json",
						"data": JDKSObject.getObject()
					})
				# Multipart Body
				# Line index 0: ------WebKitFormBoundarylSMLylneEk9ZsCHL
				# Line index 1: Content-Disposition: form-data; name="param_name_1"
				# Line index 2: 
				# Line index 3: param_value_1
				# Line index 4: ------WebKitFormBoundarylSMLylneEk9ZsCHL
				# Line index 5: Content-Disposition: form-data; name="param_name_1"; filename="test.txt"
				# Line index 6: Content-Type: text/plain
				# ...
				# Line index -4: 
				# Line index -3: param_value_2
				# Line index -2: ------WebKitFormBoundarylSMLylneEk9ZsCHL--
				# Line index -1: 
				elif re.split("\r\n|\n", reqBody)[-1] == "" and re.split("\r\n|\n", reqBody)[0]+"--"==re.split("\r\n|\n", reqBody)[-2]:
					boundary = re.split("\r\n|\n", reqBody)[0]

					try:
						params = jdks.loads("{}", ordered_dict=ordered_dict)

						for multipart_param in re.split("(?:\r?\n)?"+boundary+"(?:--)?\r?\n", reqBody)[1:-1]:
							# name , filename
							if re.match("^Content-Disposition: form-data; name=\".*?\"; filename=\".*?\"$", re.split("\r\n|\n", multipart_param)[0]):
								result = re.findall("^Content-Disposition: form-data; name=\"(.*?)\"; filename=\"(.*?)\"$", re.split("\r\n|\n", multipart_param)[0])
								name = result[0][0]
								filename = result[0][1]

								if params.get(name, separator=separator, parse_index=parse_index) != "JSON_DUPLICATE_KEYS_ERROR":
									i = 1
									while params.get(name + dupSign_start + "_" + str(i) + "_" + dupSign_end, separator=separator, parse_index=parse_index) != "JSON_DUPLICATE_KEYS_ERROR":
										i += 1
									name = name + dupSign_start + "_" + str(i) + "_" + dupSign_end

								params.set(name, {
									"filename": filename,
									"headers": {}
								}, separator=separator, parse_index=parse_index, dupSign_start=dupSign_start, dupSign_end=dupSign_end, ordered_dict=ordered_dict)
							# name
							elif re.match("^Content-Disposition: form-data; name=\".*?\"$", re.split("\r\n|\n", multipart_param)[0]):
								result = re.findall("^Content-Disposition: form-data; name=\"(.*?)\"$", re.split("\r\n|\n", multipart_param)[0])
								name = result[0]

								if params.get(name, separator=separator, parse_index=parse_index) != "JSON_DUPLICATE_KEYS_ERROR":
									i = 1
									while params.get(name + dupSign_start + "_" + str(i) + "_" + dupSign_end, separator=separator, parse_index=parse_index) != "JSON_DUPLICATE_KEYS_ERROR":
										i += 1
									name = name + dupSign_start + "_" + str(i) + "_" + dupSign_end

								params.set(name, {}, separator=separator, parse_index=parse_index, dupSign_start=dupSign_start, dupSign_end=dupSign_end, ordered_dict=ordered_dict)

							# Headers
							for h in re.split("\r\n|\n", re.split("\r\n\r\n|\n\n", multipart_param, 1)[0])[1:]:
								if re.match("^[^:]+: .*$", h):
									params.set(name+"||headers||"+re.findall("^([^:]+): (.*)$", h)[0][0], re.findall("^([^:]+): (.*)$", h)[0][1], separator=separator, parse_index=parse_index, dupSign_start=dupSign_start, dupSign_end=dupSign_end, ordered_dict=ordered_dict)

							# Value
							params.set(name+"||value", re.split("\r\n\r\n|\n\n", multipart_param, 1)[-1], separator=separator, parse_index=parse_index, dupSign_start=dupSign_start, dupSign_end=dupSign_end, ordered_dict=ordered_dict)

						self.request_body = jdks.JSON_DUPLICATE_KEYS({
							"dataType": "multipart",
							"boundary": boundary[2:],
							"data": params.getObject()
						})
					except Exception as e:
						self.request_body = jdks.JSON_DUPLICATE_KEYS({
							"dataType": "unknown",
							"data": reqBody
						})
				elif re.match("^application/x-www-form-urlencoded", self.request_headers.get("Content-Type")):
					params = jdks.loads("{}", ordered_dict=ordered_dict)

					for NameValue in reqBody.split("&"):
						if len(re.split("=", NameValue, 1)) == 2:
							params.set(re.split("=", NameValue, 1)[0], re.split("=", NameValue, 1)[1], ordered_dict=ordered_dict)
						else:
							params.set(re.split("=", NameValue, 1)[0], "", ordered_dict=ordered_dict)

					self.request_body = jdks.JSON_DUPLICATE_KEYS({
						"dataType": "form-urlencoded",
						"data": params.getObject()
					})
				else:
					self.request_body = jdks.JSON_DUPLICATE_KEYS({
						"dataType": "unknown",
						"data": reqBody
					})
			else:
				# No body
				self.request_body = jdks.JSON_DUPLICATE_KEYS({"dataType": None, "data": None})
		except Exception as e:
			# No body
			self.request_body = jdks.JSON_DUPLICATE_KEYS({"dataType": None, "data": None})
		##



class TP_HTTP_RESPONSE_PARSER:
	def __init__(self, rawResponse, separator="||", parse_index="$", dupSign_start="{{{", dupSign_end="}}}", ordered_dict=False):
		import json_duplicate_keys as jdks
		import re

		## Response HTTP Version ##
		try:
			self.response_httpVersion = re.split("\r\n|\n", re.split("\r\n\r\n|\n\n", rawResponse, 1)[0])[0].split(" ")[0]
		except Exception as e:
			self.response_httpVersion = None
		##

		## Response Status Code ##
		try:
			self.response_statusCode = int(re.split("\r\n|\n", re.split("\r\n\r\n|\n\n", rawResponse, 1)[0])[0].split(" ")[1])
		except Exception as e:
			self.response_statusCode = None
		##

		## Response Status Text ##
		try:
			self.response_statusText = " ".join(re.split("\r\n|\n", re.split("\r\n\r\n|\n\n", rawResponse, 1)[0])[0].split(" ")[2:])
		except Exception as e:
			self.response_statusText = None
		##

		## Response Headers ##
		self.response_headers = jdks.loads("{}", ordered_dict=ordered_dict)
		try:
			for header in re.split("\r\n|\n", re.split("\r\n\r\n|\n\n", rawResponse, 1)[0])[1:]:
				if re.match("^[^:]+: .*$", header):
					self.response_headers.set(re.findall("^([^:]+): (.*)$", header)[0][0], re.findall("^([^:]+): (.*)$", header)[0][1], ordered_dict=ordered_dict)
		except Exception as e:
			pass
		##

		## Response Body ##
		try:
			resBody = re.split("\r\n\r\n|\n\n", rawResponse, 1)[1]
			if len(resBody) > 0:
				# JSON Body
				JDKSObject = jdks.loads(resBody, dupSign_start=dupSign_start, dupSign_end=dupSign_end, ordered_dict=ordered_dict)
				if JDKSObject:
					self.response_body = jdks.JSON_DUPLICATE_KEYS({
						"dataType": "json",
						"data": JDKSObject.getObject()
					})
				else:

					self.response_body = jdks.JSON_DUPLICATE_KEYS({
						"dataType": "unknown",
						"data": resBody
					})
			else:
				# No body
				self.response_body = jdks.JSON_DUPLICATE_KEYS({"dataType": None, "data": None})
		except Exception as e:
			# No body
			self.response_body = jdks.JSON_DUPLICATE_KEYS({"dataType": None, "data": None})
		##