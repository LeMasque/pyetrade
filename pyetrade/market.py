#!/usr/bin/python3

'''Market - ETrade Market API
   TODO:
    * Get Option Chains
    * Get Option Expire Dates
    * Look Up Product
    * Get Quote - Doc String'''

import logging
from pyetrade.etrade_exception import MarketQuoteException
from pyetrade.etrade import ETrade

class ETradeMarket(ETrade):
    '''ETradeMarket'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set up logging
        self.log = logging.getLogger(__name__)

    @ETrade.Decorators.etrade_api_request
    def look_up_product(self, company, security_type, response_type='json'):
        '''look_up_product() -> resp
           param: company
           type: string
           description: full or partial name of the company. Note
           that the system extensivly abbreviates common words
           such as company, industry and systems and generally
           skips punctuation
           param: s_type
           type: enum
           description: the type of security. possible values are:
               * EQ (equity)
               * MF (mutual fund)
           rparam: companyName
           rtype: string
           rdescription: the company name
           rparam: exhange
           rtype: string
           rdescription: the exchange that lists that company
           rparam: securityType
           rtype: string
           rdescription: the type of security. EQ or MF
           rparam: symbol
           rtype: string
           rdescription: the market symbol for the security'''

        return {
            'method': 'GET',
            'url': self.make_url(
                module='market',
                action='productlookup',
                response_type=response_type
            ),
            'params': {
                'company': company,
                'type': security_type
            }
        }

    @ETrade.Decorators.etrade_api_request
    def get_quote(self, *args, response_type='json', detail_flag='ALL'):
        '''get_quote(dev, resp_format, **kwargs) -> resp
           param: dev
           type: bool
           description: API enviornment
           param: resp_format
           type: str
           description: Response format JSON or None = XML
           param: detailFlag
           type: enum
           required: optional
           description: Optional parameter specifying which details to
                return in the response. The field set for each possible
                value is listed in separate tables below. The possible
                values are:
                    * FUNDAMENTAL - Instrument fundamentals and latest
                        price
                    * INTRADAY - Performance for the current of most
                        recent trading day
                    * OPTIONS - Information on a given option offering
                    * WEEK52 - 52-week high and low (highest high and
                        lowest low
                    * ALL (default) - All of the above information and
                        more
           args:
           param: symbol
           type: array
           required: true
           description: One or more (comma-seperated) symobols
                for equities or options, up to a maximum of 25 Symbols
                for equities are simple, e.g. GOOG. Symbols for options
                are more complex, consisting of six elements separated
                by colons, in this format:
                underlier:year:month:day:optionType:strikePrice
                        rparam: adjNonAdjFlag
            rtype: bool
            rdescription: Indicates whether an option has been adjusted
                due to a corporate action (e.g. a dividend or stock
                split). Possible values are TRUE, FALSE
            rparam: annualDividend
            rtype: double
            rdescription: Cash amount paid per share over the past year
            rparam: ask
            rtype: double
            rdescription: The current ask price for a security
            rtype: askExchange
            ...'''
        # exception if args > 25
        if len(args) > 25:
            raise MarketQuoteException

        return {
            'method': 'GET',
            'url': self.make_url(
                module='market',
                action='quote/{args_list}'.format(args_list=','.join(args)),
                response_type=response_type
            ),
            'params': {
                'detailFlag': detail_flag
            }
        }
