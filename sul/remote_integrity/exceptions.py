#!/usr/bin/env python



class SulException(Exception):
    """
    """

class ConfigurationException(SulException):
    pass


class ServerException(SulException):
    pass


class DirectoryNotFoundException(SulException):
    pass


class IntegrityException(SulException):
    pass
