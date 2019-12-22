import requests
import unittest
from ddt import ddt, data, file_data, unpack
import xmlrunner

@ddt
class TaskTest(unittest.TestCase):

    @file_data("task_data.json")
    def test_file_data_json_dict_dict(self, url, method, par):
        if method == "post":
            r = requests.post(url, data=par)
            print(r.json())
        elif method == "get":
            r = requests.get(url,params=par)
            print(r.json())

if __name__ == '__main__':
    with open('./task_results.xml', 'wb') as output:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=output),
            failfast=False, buffer=False, catchbreak=False)