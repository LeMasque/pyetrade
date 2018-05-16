#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Generic Object class for pyetrade
"""
from requests_oauthlib import OAuth1Session

class ETrade(object):
    """
        ETrade object
    """

    ENVIRONMENT_EXTENSION = {
        'dev': 'sandbox',
        'prod': ''
    }
    AUTH_TOKEN_URL = 'https://us.etrade.com/e/t/etws/authorize'

    class Decorators(object):
        """
            Decorators since we can't just make normal decorators in our
            class.
        """
        @classmethod
        def etrade_api_request(self, function):
            """
                decorator function to ease of making API calls
            """
            def decorated(response_type, *args, **kwargs):
                requests_params = function(*args, **kwargs)

                self.log.debug(requests_params['url'])
                response = self.session.request(**requests_params)


                response.raise_for_status()
                self.log.debug(response.text)
                response_type_map = {
                    '': lambda: response.text,
                    'json': response.json,
                    # TODO: see if there is a better response thing for xml
                    'xml': lambda: response.text,
                }
                return response_type_map[response_type]()

            return decorated
        

    def __init__(self, auth_info, environment='dev'):
        """
            Initialize generic ETrade API class object

            Parameters:
                auth_info is a tuple with
                    'client_key', (oauth_consumer_key)
                    'client_secret', (oauth_consumer_secret)
                    'resource_owner_key',
                    'resource_owner_secret'

        """
        c_key, c_secret, r_o_key, r_o_secret = auth_info
        self.session = OAuth1Session(
            c_key,
            c_secret,
            r_o_key,
            r_o_secret,
            signature_type='AUTH_HEADER'
        )
        self.environment = environment

        # Logger should be set up by child Classes so they are more specific
        self.log = None
    
    def make_url(self, module, action, response_type, rest=True, env_aware=True):
        """
            Helps make a URL for requesting to the ETrade API
        """

        env_ext = ETrade.ENVIRONMENT_EXTENSION[self.environment] if env_aware else ''

        # XML is their native format, so no format specifier is necessary
        if response_type == 'xml':
            response_type = ''

        url = 'https://{host}/{module}{env_ext}{rest}{action}{rtype}'.format(
            host='etws{env_ext}.etrade.com'.format(env_ext=env_ext),
            module=module,
            env_ext='/{}'.format(env_ext) if env_ext else '',
            rest='/rest/' if rest else '',
            action=action,
            rtype='.{}'.format(response_type) if response_type else ''
        )

        return url


    @staticmethod
    def is_missing_requirements(requirements, parameters):
        """
            Given a list of required parameters and supplied parameters,
            returns a boolean specifing if there are missing required parameters.
        """
        return any(requirement not in parameters for requirement in requirements)


