import logging
import time
from random import random

import requests

from tinder.exceptions import Unauthorized, Forbidden, NotFound, RequestFailed


class Request:

    def __init__(self, **kwargs):
        self.method = kwargs.get('method')
        self.route = kwargs.get('route')
        self.body = kwargs.get('body')


class Http:
    _base_url = "https://api.gotinder.com"
    _headers = {
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
                      "like Gecko) "
                      "Chrome/85.0.4183.102 Safari/537.36",
        "Content-Type": "application/json",
        "X-Auth-Token": "",
    }
    _queue = []
    _reattempt_count = {}
    _request_count = 0

    def __init__(self, token: str, max_reattempts: int = 3, timeout_factor: int = 10):
        self._headers["X-Auth-Token"] = token
        self._max_reattempts = max_reattempts
        self._timeout = timeout_factor

    def make_request(self, request: Request) -> requests.Response:
        self._request_count += 1

        if self._request_count > 2:
            timeout = self._timeout * random()
            logging.debug('Too many requests. Waiting for %f secs' % timeout)
            time.sleep(timeout)
            self._request_count = 0
            logging.debug("Continuing...")

        url = self._base_url + request.route
        method = request.method
        logging.debug("Sending {} request to {}".format(request.method, url))
        if method == "GET":
            response = requests.get(url, headers=self._headers)
        elif method == "POST":
            response = requests.post(url, headers=self._headers, json=request.body)
        elif method == "PUT":
            response = requests.put(url, headers=self._headers, json=request.body)
        elif method == "DELETE":
            response = requests.delete(url, headers=self._headers)
        else:
            raise ValueError("Invalid request method!")
        status = response.status_code

        if 200 <= status < 300:
            logging.debug("Got response: {}".format(response.json()))
            return response

        elif 400 <= status < 500:
            if status == 401:
                raise Unauthorized(response)
            elif status == 403:
                raise Forbidden(response)
            elif status == 404:
                raise NotFound(response)
            elif status == 429:
                timeout = self._timeout * random()
                logging.debug('Too many requests. Waiting for %f secs' % timeout)
                time.sleep(timeout)
                logging.debug('Reattempting...')
                self.make_request(request)
            else:
                raise RequestFailed(response)

        else:
            if request.__hash__() in self._reattempt_count:
                self._reattempt_count[request.__hash__()] += 1
            else:
                self._reattempt_count[request.__hash__()] = 1

            if self._reattempt_count[request.__hash__()] < self._max_reattempts:
                logging.warning('Something went wrong. Status Code %d. Reattempting Request (%d)...'
                                , self._reattempt_count[request.__hash__()], status)
                self.make_request(request)
            else:
                logging.error('Something went wrong. Status Code %d. Exceeded max retries.' %
                              status)
                raise RequestFailed(response)

        self._request_count = 0
