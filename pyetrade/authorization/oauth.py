#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
    authorization.py
       Description: ETrade API authorization
       TODO:
        * Lint this messy code
        * Catch events
"""

import logging
import requests
from requests_oauthlib import OAuth1Session
from pyetrade.etrade import ETrade

class ETradeOAuth(ETrade):
    '''ETradeOAuth
       ETrade OAuth 1.0a Wrapper'''
    def __init__(self, auth_info, callback_url='oob', environment='dev'):
        '''__init__(consumer_key, consumer_secret, callback_url)
           param: consumer_key
           type: str
           description: etrade oauth consumer key
           param: consumer_secret
           type: str
           description: etrade oauth consumer secret
           param: callback_url
           type: str
           description: etrade oauth callback url default oob'''

        # We don't want to call our super's constructor here, since we're special

        # override instance session variable since we haven't actually done oauth yet.
        self.consumer_key, consumer_secret, _, __ = auth_info
        self.session = OAuth1Session(
            self.consumer_key,
            consumer_secret,
            callback_uri=callback_url,
            signature_type='AUTH_HEADER'
        )

        # Set up logging
        self.log = logging.getLogger(__name__)


    def get_request_token(self):
        '''get_request_token() -> auth url
           some params handled by requests_oauthlib but put in
           doc string for clarity into the API.
           param: oauth_consumer_key
           type: str
           description: the value used by the consumer to identify
                        itself to the service provider.
           param: oauth_timestamp
           type: int
           description: the date and time of the request, in epoch time.
                        must be accurate within five minutes.
           param: oauth_nonce
           type: str
           description: a nonce, as discribed in the authorization guide
                        roughly, an arbitrary or random value that cannot
                        be used again with the same timestamp.
           param: oauth_signature_method
           type: str
           description: the signature method used by the consumer to sign
                        the request. the only supported value is 'HMAC-SHA1'.
           param: oauth_signature
           type: str
           description: signature generated with the shared secret and token
                        secret using the specified oauth_signature_method
                        as described in OAuth documentation.
           param: oauth_callback
           type: str
           description: callback information, as described elsewhere. must
                        always be set to 'oob' whether using a callback or
                        not
           rtype: str
           description: Etrade autherization url'''

        request_token_url = self.make_url(
            module='oauth',
            action='request_token',
            response_type='',
            rest=False,
            env_aware=False
        )
        print('request_token_url: {}'.format(request_token_url))

        # get request token
        fetch_response = self.session.fetch_request_token(request_token_url)

        print('fetch_response: {}'.format(fetch_response))

        resource_owner_key = fetch_response['oauth_token']
        resource_owner_secret = fetch_response['oauth_token_secret']

        auth_url = '{}?key={c_key}&token={ro_key}'.format(
            ETrade.AUTH_TOKEN_URL,
            c_key=self.consumer_key,
            ro_key=resource_owner_key
        )
        return auth_url


    def get_access_token(self, verifier):
        '''get_access_token(verifier) -> access_token
           param: verifier
           type: str
           description: oauth verification code
           rtype: dict
           description: oauth access tokens

           OAuth API paramiters mostly handled by requests_oauthlib
           but illistrated here for clarity.
           param: oauth_consumer_key
           type: str
           description: the value used by the consumer to identify
                        itself to the service provider.
           param: oauth_timestamp
           type: int
           description: the date and time of the request, in epoch time.
                        must be accurate within five minutes.
           param: oauth_nonce
           type: str
           description: a nonce, as discribed in the authorization guide
                        roughly, an arbitrary or random value that cannot
                        be used again with the same timestamp.
           param: oauth_signature_method
           type: str
           description: the signature method used by the consumer to sign
                        the request. the only supported value is 'HMAC-SHA1'.
           param: oauth_signature
           type: str
           description: signature generated with the shared secret and token
                        secret using the specified oauth_signature_method
                        as described in OAuth documentation.
           param: oauth_token
           type: str
           description: the consumer's request token to be exchanged for an
                        access token
           param: oauth_verifier
           type: str
           description: the code received by the user to authenticate with
                        the third-party application'''

        # Set verifier
        self.session._client.client.verifier = verifier
        # Get access token
        oauth_tokens = self.session.fetch_access_token(self.make_url(
            module='oauth',
            action='access_token',
            response_type='',
            rest=False,
            env_aware=False
        ))

        #LOGGER.debug(self.access_token)
        self.log.debug(oauth_tokens)

        return (
            oauth_tokens['oauth_token'],
            oauth_tokens['oauth_token_secret']
        )

        #return self.access_token

