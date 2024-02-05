import setuptools

setuptools.setup(
	name="TP-HTTP-Request-Response-Parser",
	version="2024.2.5",
	author="TP Cyber Security",
	license="MIT",
	author_email="tpcybersec2023@gmail.com",
	description="Parse the raw HTTP Request/ Response to the Object",
	long_description=open("README.md").read(),
	long_description_content_type="text/markdown",
	install_requires=open("requirements.txt").read().split(),
	url="https://github.com/truocphan/TP-HTTP-Request-Response-Parser",
	classifiers=[
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 2",
		"Programming Language :: Python :: Implementation :: Jython"
	],
	keywords=["TPCyberSec", "HTTP Request Parser", "HTTP Response Parser"],
	packages=["TP_HTTP_Request_Response_Parser"],
)