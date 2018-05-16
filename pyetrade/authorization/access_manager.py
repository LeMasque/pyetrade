#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    authorization.py
       Description: ETrade API authorization
       TODO:
        * Lint this messy code
        * Catch events
"""

from requests_oauthlib import OAuth1Session
from pyetrade.etrade import ETrade

class ETradeAccessManager(ETrade):
    '''ETradeAccessManager - Renew and revoke ETrade OAuth Access Tokens'''

    @ETrade.Decorators.etrade_api_request
    def renew_access_token(self):
        '''renew_access_token() -> bool
           some params handled by requests_oauthlib but put in
           doc string for clarity into the API.
           param: oauth_consumer_key
           type: string
           required: true
           description: the value used by the consumer to identify
                        itself to the service provider.
           param: oauth_timestamp
           type: int
           required: true
           description: the date and time of the request, in epoch time.
                        must be accurate withiin five minutes.
           param: oauth_nonce
           type: str
           required: true
           description: a nonce, as described in the authorization guide
                        roughly, an arbitrary or random value that cannot
                        be used again with the same timestamp.
           param: oauth_signature_method
           type: str
           required: true
           description: the signature method used by the consumer to sign
                        the request. the only supported value is "HMAC-SHA1".
           param: oauth_signature
           type: str
           required: true
           description: signature generated with the shared secret and
                        token secret using the specified oauth_signature_method
                        as described in OAuth documentation.
           param: oauth_token
           type: str
           required: true
           description: the consumer's access token to be renewed.'''

        return {
            'method': 'GET',
            'url': self.make_url(
                module='oauth',
                module_action='renew_access_token',
                response_type='',
                rest=False,
                env_aware=False
            ),
        }


    @ETrade.Decorators.etrade_api_request
    def revoke_access_token(self):
        '''revoke_access_token() -> bool
           some params handled by requests_oauthlib but put in
           doc string for clarity into the API.
           param: oauth_consumer_key
           type: string
           required: true
           description: the value used by the consumer to identify
                        itself to the service provider.
           param: oauth_timestamp
           type: int
           required: true
           description: the date and time of the request, in epoch time.
                        must be accurate withiin five minutes.
           param: oauth_nonce
           type: str
           required: true
           description: a nonce, as described in the authorization guide
                        roughly, an arbitrary or random value that cannot
                        be used again with the same timestamp.
           param: oauth_signature_method
           type: str
           required: true
           description: the signature method used by the consumer to sign
                        the request. the only supported value is "HMAC-SHA1".
           param: oauth_signature
           type: str
           required: true
           description: signature generated with the shared secret and
                        token secret using the specified oauth_signature_method
                        as described in OAuth documentation.
           param: oauth_token
           type: str
           required: true
           description: the consumer's access token to be revoked.'''

        return {
            'method': 'GET',
            'url': self.make_url(
                module='oauth',
                module_action='revoke_access_token',
                response_type='',
                rest=False,
                env_aware=False
            ),
        }
