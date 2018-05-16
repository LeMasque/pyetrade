#!/usr/bin/python3

'''Accounts - ETrade Accounts API
   Calls
   TODO:
       * Fix init doc string
       * Check request response for error'''

import logging
from requests_oauthlib import OAuth1Session
from pyetrade.etrade import ETrade

# Set up logging
LOGGER = logging.getLogger(__name__)

class ETradeAccounts(ETrade):
    '''ETradeAccounts:'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set up logging
        self.log = logging.getLogger(__name__)


    @ETrade.Decorators.etrade_api_request
    def list_accounts(self, response_type='json'):
        '''list_account(dev, resp_format)
           param: dev
           type: bool
           description: API enviornment
           param: resp_format
           type: str
           description: Response format
           rformat: json
           rtype: dict
           rformat: other than json
           rtype: str'''

        return {
            'method': 'GET',
            'url': self.make_url(
                module='accounts',
                action='accountlist',
                response_type=response_type
            )
        }

    @ETrade.Decorators.etrade_api_request
    def get_account_balance(self, account_id, response_type='json'):
        '''get_account_balance(dev, resp_format)
           param: account_id
           type: int
           required: true
           description: Numeric account id
           param: dev
           type: bool
           description: API enviornment
           param: resp_format
           type: str
           description: Response format
           rformat: json
           rtype: dict
           rformat: other than json
           rtype: str'''

        return {
            'method': 'GET',
            'url': self.make_url(
                module='accounts',
                action='accountbalance/{account}'.format(account=account_id),
                response_type=response_type
            )
        }

    @ETrade.Decorators.etrade_api_request
    def get_account_positions(self, account_id, response_type='json'):
        '''get_account_positions(dev, account_id, resp_format) -> resp
           param: account_id
           type: int
           required: true
           description: Numeric account id
           param: dev
           type: bool
           description: API enviornment
           param: resp_format
           type: str
           description: Response format
           rformat: json
           rtype: dict
           rformat: other than json
           rtype: str'''

        return {
            'method': 'GET',
            'url': self.make_url(
                module='accounts',
                action='accountpositions/{account}'.format(account=account_id),
                response_type=response_type
            )
        }


    @ETrade.Decorators.etrade_api_request
    def list_alerts(self, response_type='json'):
        '''list_alerts(dev, resp_format) -> resp
           param: dev
           type: bool
           description: API enviornment
           param: resp_format
           type: str
           description: Response format
           rformat: json
           rtype: dict
           rformat: other than json
           rtype: str'''

        return {
            'method': 'GET',
            'url': self.make_url(
                module='accounts',
                action='alerts',
                response_type=response_type
            )
        }


    @ETrade.Decorators.etrade_api_request
    def read_alert(self, alert_id, response_type='json'):
        '''read_alert(alert_id, dev, resp_format) -> resp
           param: alert_id
           type: int
           description: Numaric alert ID
           param: dev
           type: bool
           description: API enviornment
           param: resp_format
           type: str
           description: Response format
           rformat: json
           rtype: dict
           rformat: other than json
           rtype: str'''

        return {
            'method': 'GET',
            'url': self.make_url(
                module='accounts',
                action='alerts/{alert}'.format(alert=alert_id),
                response_type=response_type
            )
        }


    @ETrade.Decorators.etrade_api_request
    def delete_alert(self, alert_id, response_type='json'):
        '''delete_alert(alert_id, dev, resp_format) -> resp
           param: alert_id
           type: int
           description: Numaric alert ID
           param: dev
           type: bool
           description: API enviornment
           param: resp_format
           type: str
           description: Response format
           rformat: json
           rtype: dict
           rformat: other than json
           rtype: str'''

        return {
            'method': 'DELETE',
            'url': self.make_url(
                module='accounts',
                action='alerts/{alert}'.format(alert=alert_id),
                response_type=response_type
            )
        }


    @ETrade.Decorators.etrade_api_request
    def get_transaction_history(self, account_id, dev=True,
                                group='ALL',
                                asset_type='ALL',
                                transaction_type='ALL',
                                ticker_symbol='ALL',
                                resp_format='json', **kwargs):
        '''get_transaction_history(account_id, dev, resp_format) -> resp
           param: account_id
           type: int
           required: true
           description: Numeric account ID
           param: group
           type: string
           default: 'ALL'
           description: Possible values are: DEPOSITS, WITHDRAWALS, TRADES.
           param: asset_type
           type: string
           default: 'ALL'
           description: Only allowed if group is TRADES. Possible values are:
                EQ (equities), OPTN (options), MMF (money market funds),
                MF (mutual funds), BOND (bonds). To retrieve all types,
                use ALL or omit this parameter.
           param: transaction_type
           type: string
           default: 'ALL'
           description: Transaction type(s) to include, e.g., check, deposit,
                fee, dividend, etc. A list of types is provided in documentation
           param: ticker_symbol
           type: string
           default: 'ALL'
           description: Only allowed if group is TRADES. A single market symbol,
                e.g., GOOG.
           param: marker
           type: str
           description: Specify the desired starting point of the set
                of items to return. Used for paging.
           param: count
           type: int
           description: The number of orders to return in a response.
                The default is 25. Used for paging.
           description: see ETrade API docs'''

        # add each optional argument not equal to 'ALL' to the uri
        optional_args = [group, asset_type, transaction_type, ticker_symbol]
        optional_args = map(lambda x: x.upper(), optional_args)
        optional_args = filter(lambda x: x != 'ALL', optional_args)

        #assemble the following:
        #self.base_url_dev: https://etws.etrade.com
        #uri:               /accounts/rest
        #account_id:        /{accountId}
        #format string:     /transactions
        # if not 'ALL' args:
        #   group:              /{Group}
        #   asset_type          /{AssetType}
        #   transaction_type:   /{TransactionType}
        #   ticker_symbol:      /{TickerSymbol}
        #resp_format:       {.json}
        #payload:           kwargs
        #

        return {
            'method': 'GET',
            'url': self.make_url(
                module='accounts',
                action='{account}/transactions{optionals}'.format(
                    account=account_id,
                    optionals='/{}'.format('/'.join(optional_args))
                ),
                response_type=response_type
            ),
            'params': kwargs
        }


    @ETrade.Decorators.etrade_api_request
    def get_transaction_details(self, account_id, transaction_id,
                                response_type='json', **kwargs):
        '''get_transaction_details(account_id, transaction_id, dev, resp_format) -> resp
           param: account_id
           type: int
           required: true
           description: Numeric account ID
           param: transaction_id
           type: int
           required: true
           description: Numeric transaction ID'''

        return {
            'method': 'GET',
            'url': self.make_url(
                module='account',
                action='{account}/transations/{transaction}'.format(
                    account=account_id,
                    transaction=transation_id
                ),
                response_type=response_type
            ),
            'params': kwargs
        }
