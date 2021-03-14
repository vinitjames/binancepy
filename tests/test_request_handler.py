import json
import unittest
import httpretty
from collections.abc import Mapping
from requests import Session
from binance.request_handler import RequestHandler
from binance.exceptions import BinanceAPIError, BinanceResponseError
from binance.exceptions import RequestHandlerError


class TestRequestHandler(unittest.TestCase):
        
    def test_unauthenticated_attr(self):
        req_handle = RequestHandler()
        self.assertEqual(req_handle.api_key, None)
        self.assertEqual(req_handle.api_secret, None)
        self.assertEqual(req_handle.request_params, None)
        self.assertEqual(req_handle.authenticated, False)
        self.assertTrue(isinstance(req_handle.session, Session))
        self.assertEqual(req_handle.session.headers['Accept'],
                         'application/json')
        self.assertEqual(req_handle.session.headers['User-Agent'],
                         'binance/python')

    def test_authenticated_attr(self):
        req_handle = RequestHandler(api_key='TestAPIKey',
                                    api_secret='TestAPISecret')
        self.assertEqual(req_handle.api_key, 'TestAPIKey')
        self.assertEqual(req_handle.api_secret, 'TestAPISecret')
        self.assertEqual(req_handle.request_params, None)
        self.assertEqual(req_handle.authenticated, True)
        self.assertTrue(isinstance(req_handle.session, Session))
        self.assertEqual(req_handle.session.headers['Accept'],
                         'application/json')
        self.assertEqual(req_handle.session.headers['User-Agent'],
                         'binance/python')
        self.assertEqual(req_handle.session.headers['X-MBX-APIKEY'],
                         'TestAPIKey')
    
    def request_callback_v1(self, request, uri, response_headers):
        self.assertEqual(request.headers.get('Accept'), 'application/json')
        self.assertEqual(request.headers.get('User-Agent'), 'binance/python')
        return [response_headers.get('status'), response_headers,
                json.dumps({"msg": "testbody"})]

    def request_callback_v2(self, request, uri, response_headers):
        self.assertEqual(request.headers.get('Accept'), 'application/json')
        self.assertEqual(request.headers.get('User-Agent'), 'binance/python')
        self.assertEqual(request.headers.get('X-MBX-APIKEY'), 'TestAPIKey')
        return [response_headers.get('status'), response_headers,
                json.dumps({"msg": "testbody"})]

    def request_callback_v3(self, request, uri, response_headers):
        self.assertEqual(request.headers.get('Accept'), 'application/json')
        self.assertEqual(request.headers.get('User-Agent'), 'binance/python')
        self.assertEqual(request.headers.get('X-MBX-APIKEY'), 'TestAPIKey')
        return [response_headers.get('status'), response_headers,
                json.dumps({"msg": "Invalid binance api call",
                            "code": 1124})]

    def request_callback_v4(self, request, uri, response_headers):
        self.assertEqual(request.headers.get('Accept'), 'application/json')
        self.assertEqual(request.headers.get('User-Agent'), 'binance/python')
        self.assertEqual(request.headers.get('X-MBX-APIKEY'), 'TestAPIKey')
        return [response_headers.get('status'), response_headers,
                "This is a faulty binance response"]
        
    @httpretty.activate
    def test_request_get_v1(self):
        httpretty.register_uri(httpretty.GET,
                               "https://testuri.com",
                               status=200,
                               body=self.request_callback_v1
                               )
        req_handle = RequestHandler()
        response = req_handle.get("https://testuri.com")
        self.assertTrue(isinstance(response, Mapping))
        self.assertEqual(response, {"msg": "testbody"})
        with self.assertRaises(RequestHandlerError) as cm:
            req_handle.get("https://testuri.com", signed=True)
        self.assertEqual(cm.exception.message,
                         "Unauthenticated client issued "
                         "a signed GET http request")

    @httpretty.activate
    def test_request_get_v2(self):
        httpretty.register_uri(httpretty.GET,
                               "https://testuri.com",
                               status=200,
                               body=self.request_callback_v2
                               )
        req_handle = RequestHandler('TestAPIKey', 'TestAPISecret')
        response = req_handle.get("https://testuri.com")
        self.assertTrue(isinstance(response, Mapping))
        self.assertEqual(response, {"msg": "testbody"})

    @httpretty.activate
    def test_request_post_v1(self):
        httpretty.register_uri(httpretty.POST,
                               "https://testuri.com",
                               status=200,
                               body=self.request_callback_v1
                               )
        req_handle = RequestHandler()
        with self.assertRaises(RequestHandlerError) as cm:
            req_handle.post("https://testuri.com")
        self.assertEqual(cm.exception.message,
                         "Unauthenticated client issued a POST http request")

    @httpretty.activate
    def test_request_post_v2(self):
        httpretty.register_uri(httpretty.POST,
                               "https://testuri.com",
                               status=200,
                               body=self.request_callback_v2
                               )
        req_handle = RequestHandler('TestAPIKey', 'TestAPISecret')
        response = req_handle.post("https://testuri.com")
        self.assertTrue(isinstance(response, Mapping))
        self.assertEqual(response, {"msg": "testbody"})

    @httpretty.activate
    def test_request_put_v1(self):
        httpretty.register_uri(httpretty.PUT,
                               "https://testuri.com",
                               status=200,
                               body=self.request_callback_v1
                               )
        req_handle = RequestHandler()
        with self.assertRaises(RequestHandlerError) as cm:
            req_handle.put("https://testuri.com")
        self.assertEqual(cm.exception.message,
                         "Unauthenticated client issued a PUT http request")

    @httpretty.activate
    def test_request_put_v2(self):
        httpretty.register_uri(httpretty.PUT,
                               "https://testuri.com",
                               status=200,
                               body=self.request_callback_v2
                               )
        req_handle = RequestHandler('TestAPIKey', 'TestAPISecret')
        response = req_handle.put("https://testuri.com")
        self.assertTrue(isinstance(response, Mapping))
        self.assertEqual(response, {"msg": "testbody"})

    @httpretty.activate
    def test_request_delete_v1(self):
        httpretty.register_uri(httpretty.DELETE,
                               "https://testuri.com",
                               status=200,
                               body=self.request_callback_v1
                               )
        req_handle = RequestHandler()
        with self.assertRaises(RequestHandlerError) as cm:
            req_handle.delete("https://testuri.com")
        self.assertEqual(cm.exception.message,
                         "Unauthenticated client issued a DELETE http request")

    @httpretty.activate
    def test_request_delete_v2(self):
        httpretty.register_uri(httpretty.DELETE,
                               "https://testuri.com",
                               status=200,
                               body=self.request_callback_v2
                               )
        req_handle = RequestHandler('TestAPIKey', 'TestAPISecret')
        response = req_handle.delete("https://testuri.com")
        self.assertTrue(isinstance(response, Mapping))
        self.assertEqual(response, {"msg": "testbody"})

    @httpretty.activate
    def test_request_binance_api_error(self):
        httpretty.register_uri(httpretty.GET,
                               "https://testuri.com",
                               status=404,
                               body=self.request_callback_v3
                               )
        req_handle = RequestHandler('TestAPIKey', 'TestAPISecret')
        with self.assertRaises(BinanceAPIError) as cm:
            req_handle.get("https://testuri.com")
        self.assertEqual(cm.exception.message, "Invalid binance api call")
        self.assertEqual(cm.exception.code, 1124)

    @httpretty.activate
    def test_request_binance_response_error(self):
        httpretty.register_uri(httpretty.GET,
                               "https://testuri.com",
                               status=200,
                               body=self.request_callback_v4
                               )
        req_handle = RequestHandler('TestAPIKey', 'TestAPISecret')
        with self.assertRaises(BinanceResponseError) as cm:
            req_handle.get("https://testuri.com")
        self.assertEqual(cm.exception.message,
                         "Invalid Response: This is a faulty binance response")

        
if __name__ == '__main__':
    unittest.main()
