from .base import BaseClient
from typing import Optional, Any, Dict, List, Union, Iterator
from .models import (
    MarketHoliday,
    MarketStatus,
    Ticker,
    TickerDetails,
    TickerNews,
    TickerTypes,
    Sort,
    Order,
    AssetClass,
    Locale,
    Split,
    Dividend,
    DividendType,
    Frequency,
    Condition,
    DataType,
    SIP,
    Exchange,
)
from urllib3 import HTTPResponse
from datetime import date


class MarketsClient(BaseClient):
    def get_market_holidays(
        self, params: Optional[Dict[str, Any]] = None, raw: bool = False
    ) -> Union[List[MarketHoliday], HTTPResponse]:
        """
        Get upcoming market holidays and their open/close times.

        :param params: Any additional query params
        :param raw: Return HTTPResponse object instead of results object
        :return: List of market holidays
        """
        url = "/v1/marketstatus/upcoming"

        return self._get(
            path=url,
            params=params,
            deserializer=MarketHoliday.from_dict,
            raw=raw,
            result_key="",
        )

    def get_market_status(
        self, params: Optional[Dict[str, Any]] = None, raw: bool = False
    ) -> Union[MarketStatus, HTTPResponse]:
        """
        Get the current trading status of the exchanges and overall financial markets.

        :param params: Any additional query params
        :param raw: Return HTTPResponse object instead of results object
        :return: Market status
        """
        url = "/v1/marketstatus/now"

        return self._get(
            path=url, params=params, deserializer=MarketStatus.from_dict, raw=raw
        )


class TickersClient(BaseClient):
    def list_tickers(
        self,
        ticker: Optional[str] = None,
        ticker_lt: Optional[str] = None,
        ticker_lte: Optional[str] = None,
        ticker_gt: Optional[str] = None,
        ticker_gte: Optional[str] = None,
        type: Optional[str] = None,
        market: Optional[str] = None,
        exchange: Optional[str] = None,
        cusip: Optional[int] = None,
        cik: Optional[int] = None,
        date: Optional[str] = None,
        active: Optional[bool] = None,
        search: Optional[str] = None,
        limit: Optional[int] = None,
        sort: Optional[Union[str, Sort]] = None,
        order: Optional[Union[str, Order]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
    ) -> Union[Iterator[Ticker], HTTPResponse]:
        """
        Query all ticker symbols which are supported by Polygon.io. This API currently includes Stocks/Equities, Crypto, and Forex.

        :param ticker: Specify a ticker symbol. Defaults to empty string which queries all tickers.
        :param ticker_lt: Ticker less than
        :param ticker_lte: Ticker less than or equal to
        :param ticker_gt: Ticker greater than
        :param ticker_gte: Ticker greater than or equal to
        :param type: Specify the type of the tickers. Find the types that we support via our Ticker Types API. Defaults to empty string which queries all types.
        :param market: Filter by market type. By default all markets are included.
        :param exchange: Specify the primary exchange of the asset in the ISO code format. Find more information about the ISO codes at the ISO org website. Defaults to empty string which queries all exchanges.
        :param cusip: Specify the CUSIP code of the asset you want to search for. Find more information about CUSIP codes at their website. Defaults to empty string which queries all CUSIPs.
        :param cik: Specify the CIK of the asset you want to search for. Find more information about CIK codes at their website. Defaults to empty string which queries all CIKs.
        :param date: Specify a point in time to retrieve tickers available on that date. Defaults to the most recent available date.
        :param search: Search for terms within the ticker and/or company name.
        :param active: Specify if the tickers returned should be actively traded on the queried date. Default is true.
        :param limit: Limit the size of the response, default is 100 and max is 1000.
        :param sort: The field to sort the results on. Default is ticker. If the search query parameter is present, sort is ignored and results are ordered by relevance.
        :param order: The order to sort the results on. Default is asc (ascending).
        :param params: Any additional query params
        :param raw: Return raw object instead of results object
        :return: List of tickers
        """
        url = "/v3/reference/tickers"

        return self._paginate(
            path=url,
            params=self._get_params(self.list_tickers, locals()),
            raw=raw,
            deserializer=Ticker.from_dict,
        )

    def get_ticker_details(
        self,
        ticker: Optional[str] = None,
        date: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
    ) -> Union[TickerDetails, HTTPResponse]:
        """
        Get a single ticker supported by Polygon.io. This response will have detailed information about the ticker and the company behind it.

        :param ticker: The ticker symbol of the asset.
        :param date: Specify a point in time to get information about the ticker available on that date. When retrieving information from SEC filings, we compare this date with the period of report date on the SEC filing.
        :param params: Any additional query params
        :param raw: Return raw object instead of results object
        :return: Ticker Details V3
        """
        url = f"/v3/reference/tickers/{ticker}"

        return self._get(
            path=url,
            params=params,
            deserializer=TickerDetails.from_dict,
            raw=raw,
            result_key="results",
        )

    def list_ticker_news(
        self,
        ticker: Optional[str] = None,
        ticker_lt: Optional[str] = None,
        ticker_lte: Optional[str] = None,
        ticker_gt: Optional[str] = None,
        ticker_gte: Optional[str] = None,
        published_utc: Optional[str] = None,
        published_utc_lt: Optional[str] = None,
        published_utc_lte: Optional[str] = None,
        published_utc_gt: Optional[str] = None,
        published_utc_gte: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
    ) -> Union[Iterator[TickerNews], HTTPResponse]:
        """
        Get the most recent news articles relating to a stock ticker symbol, including a summary of the article and a link to the original source.

        :param ticker: Return results that contain this ticker.
        :param published_utc: Return results published on, before, or after this date.
        :param limit: Limit the number of results returned, default is 10 and max is 1000.
        :param sort: Sort field used for ordering.
        :param order: Order results based on the sort field.
        :param params: Any additional query params
        :param raw: Return raw object instead of results object
        :return: Ticker News
        """
        url = "/v2/reference/news"

        return self._paginate(
            path=url,
            params=self._get_params(self.list_ticker_news, locals()),
            raw=raw,
            deserializer=TickerNews.from_dict,
        )

    def get_ticker_types(
        self,
        asset_class: Optional[Union[str, AssetClass]] = None,
        locale: Optional[Union[str, Locale]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
    ) -> Union[List[TickerTypes], HTTPResponse]:
        """
        List all ticker types that Polygon.io has.

        :param asset_class: Filter by asset class.
        :param locale: Filter by locale.
        :param params: Any additional query params
        :param raw: Return raw object instead of results object
        :return: Ticker Types
        """
        url = "/v3/reference/tickers/types"

        return self._get(
            path=url,
            params=params,
            deserializer=TickerTypes.from_dict,
            raw=raw,
            result_key="results",
        )


class SplitsClient(BaseClient):
    def list_splits(
        self,
        ticker: Optional[str] = None,
        ticker_lt: Optional[str] = None,
        ticker_lte: Optional[str] = None,
        ticker_gt: Optional[str] = None,
        ticker_gte: Optional[str] = None,
        execution_date: Optional[Union[str, date]] = None,
        execution_date_lt: Optional[Union[str, date]] = None,
        execution_date_lte: Optional[Union[str, date]] = None,
        execution_date_gt: Optional[Union[str, date]] = None,
        execution_date_gte: Optional[Union[str, date]] = None,
        reverse_split: Optional[bool] = None,
        limit: Optional[int] = None,
        sort: Optional[Union[str, Sort]] = None,
        order: Optional[Union[str, Order]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
    ) -> Union[Iterator[Split], HTTPResponse]:
        """
        Get a list of historical stock splits, including the ticker symbol, the execution date, and the factors of the split ratio.

        :param ticker: Return the stock splits that contain this ticker.
        :param ticker_lt: Ticker less than
        :param ticker_lte: Ticker less than or equal to
        :param ticker_gt: Ticker greater than
        :param ticker_gte: Ticker greater than or equal to
        :param execution_date: Query by execution date with the format YYYY-MM-DD.
        :param execution_date_lt: Execution date less than
        :param execution_date_lte: Execution date less than or equal to
        :param execution_date_gt: Execution date greater than
        :param execution_date_gte: Execution date greater than or equal to
        :param reverse_split: Query for reverse stock splits. A split ratio where split_from is greater than split_to represents a reverse split. By default this filter is not used.
        :param limit: Limit the number of results returned, default is 10 and max is 1000.
        :param sort: Sort field used for ordering.
        :param order: Order results based on the sort field.
        :param params: Any additional query params
        :param raw: Return raw object instead of results object
        :return: List of splits
        """
        url = "/v3/reference/splits"

        return self._paginate(
            path=url,
            params=self._get_params(self.list_splits, locals()),
            raw=raw,
            deserializer=Split.from_dict,
        )


class DividendsClient(BaseClient):
    def list_dividends(
        self,
        ticker: Optional[str] = None,
        ticker_lt: Optional[str] = None,
        ticker_lte: Optional[str] = None,
        ticker_gt: Optional[str] = None,
        ticker_gte: Optional[str] = None,
        ex_dividend_date: Optional[Union[str, date]] = None,
        ex_dividend_date_lt: Optional[Union[str, date]] = None,
        ex_dividend_date_lte: Optional[Union[str, date]] = None,
        ex_dividend_date_gt: Optional[Union[str, date]] = None,
        ex_dividend_date_gte: Optional[Union[str, date]] = None,
        record_date: Optional[Union[str, date]] = None,
        record_date_lt: Optional[Union[str, date]] = None,
        record_date_lte: Optional[Union[str, date]] = None,
        record_date_gt: Optional[Union[str, date]] = None,
        record_date_gte: Optional[Union[str, date]] = None,
        declaration_date: Optional[Union[str, date]] = None,
        declaration_date_lt: Optional[Union[str, date]] = None,
        declaration_date_lte: Optional[Union[str, date]] = None,
        declaration_date_gt: Optional[Union[str, date]] = None,
        declaration_date_gte: Optional[Union[str, date]] = None,
        pay_date: Optional[Union[str, date]] = None,
        pay_date_lt: Optional[Union[str, date]] = None,
        pay_date_lte: Optional[Union[str, date]] = None,
        pay_date_gt: Optional[Union[str, date]] = None,
        pay_date_gte: Optional[Union[str, date]] = None,
        frequency: Optional[Union[int, Frequency]] = None,
        cash_amount: Optional[float] = None,
        cash_amount_lt: Optional[float] = None,
        cash_amount_lte: Optional[float] = None,
        cash_amount_gt: Optional[float] = None,
        cash_amount_gte: Optional[float] = None,
        dividend_type: Optional[Union[str, DividendType]] = None,
        limit: Optional[int] = None,
        sort: Optional[Union[str, Sort]] = None,
        order: Optional[Union[str, Order]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
    ) -> Union[Iterator[Dividend], HTTPResponse]:
        """
        Get a list of historical cash dividends, including the ticker symbol, declaration date, ex-dividend date, record date, pay date, frequency, and amount.

        :param ticker: Return the dividends that contain this ticker.
        :param ticker_lt: Ticker less than
        :param ticker_lte: Ticker less than or equal to
        :param ticker_gt: Ticker greater than
        :param ticker_gte: Ticker greater than or equal to
        :param ex_dividend_date: Query by ex-dividend date with the format YYYY-MM-DD.
        :param ex_dividend_date_lt: Ex-dividend date less than
        :param ex_dividend_date_lte: Ex-dividend date less than or equal to
        :param ex_dividend_date_gt: Ex-dividend date greater than
        :param ex_dividend_date_gte: Ex-dividend date greater than or equal to
        :param record_date: Query by record date with the format YYYY-MM-DD.
        :param record_date_lt: Record date less than
        :param record_date_lte: Record date less than or equal to
        :param record_date_gt: Record date greater than
        :param record_date_gte: Record date greater than or equal to
        :param declaration_date: Query by declaration date with the format YYYY-MM-DD.
        :param declaration_date_lt: Declaration date less than
        :param declaration_date_lte: Declaration date less than or equal to
        :param declaration_date_gt: Declaration date greater than
        :param declaration_date_gte: Declaration date greater than or equal to
        :param pay_date: Query by pay date with the format YYYY-MM-DD.
        :param pay_date_lt: Pay date less than
        :param pay_date_lte: Pay date less than or equal to
        :param pay_date_gt: Pay date greater than
        :param pay_date_gte: Pay date greater than or equal to
        :param frequency: Query by the number of times per year the dividend is paid out. Possible values are 0 (one-time), 1 (annually), 2 (bi-annually), 4 (quarterly), and 12 (monthly).
        :param cash_amount: Query by the cash amount of the dividend.
        :param dividend_type: Query by the type of dividend. Dividends that have been paid and/or are expected to be paid on consistent schedules are denoted as CD. Special Cash dividends that have been paid that are infrequent or unusual, and/or can not be expected to occur in the future are denoted as SC.
        :param limit: Limit the number of results returned, default is 10 and max is 1000.
        :param sort: Sort field used for ordering.
        :param order: Order results based on the sort field.
        :param params: Any additional query params
        :param raw: Return raw object instead of results object
        :return: List of dividends
        """
        url = "/v3/reference/dividends"

        return self._paginate(
            path=url,
            params=self._get_params(self.list_dividends, locals()),
            raw=raw,
            deserializer=Dividend.from_dict,
        )


class ConditionsClient(BaseClient):
    def list_conditions(
        self,
        asset_class: Optional[Union[str, AssetClass]] = None,
        data_type: Optional[Union[str, DataType]] = None,
        id: Optional[int] = None,
        sip: Optional[Union[str, SIP]] = None,
        limit: Optional[int] = None,
        sort: Optional[Union[str, Sort]] = None,
        order: Optional[Union[str, Order]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
    ) -> Union[Iterator[Condition], HTTPResponse]:
        """
        List all conditions that Polygon.io uses.

        :param asset_class: Filter for conditions within a given asset class.
        :param data_type: Data types that this condition applies to.
        :param id: Filter for conditions with a given ID.
        :param sip: Filter by SIP. If the condition contains a mapping for that SIP, the condition will be returned.
        :param limit: Limit the number of results returned, default is 10 and max is 1000.
        :param sort: Sort field used for ordering.
        :param order: Order results based on the sort field.
        :param params: Any additional query params
        :param raw: Return raw object instead of results object
        :return: List of conditions
        """
        url = "/v3/reference/conditions"

        return self._paginate(
            path=url,
            params=self._get_params(self.list_conditions, locals()),
            raw=raw,
            deserializer=Condition.from_dict,
        )


class ExchangesClient(BaseClient):
    def get_exchanges(
        self,
        asset_class: Optional[Union[str, AssetClass]] = None,
        locale: Optional[Union[str, Locale]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
    ) -> Union[List[Exchange], HTTPResponse]:
        """
        List all exchanges that Polygon.io knows about.

        :param asset_class: Filter by asset class.
        :param locale: Filter by locale.
        :param params: Any additional query params
        :param raw: Return HTTPResponse object instead of results object
        :return: List of exchanges
        """
        url = "/v3/reference/exchanges"

        return self._get(
            path=url,
            params=params,
            deserializer=Exchange.from_dict,
            raw=raw,
            result_key="results",
        )
