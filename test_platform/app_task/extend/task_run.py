import os
import requests
import unittest
from ddt import ddt, data, file_data, unpack
import xmlrunner
import json

from django.http import JsonResponse

EXTEND_DIR = os.path.dirname(os.path.abspath(__file__))
TASK_DATA = os.path.join(EXTEND_DIR, "task_data.json")
TASK_RESULTS = os.path.join(EXTEND_DIR, "task_results.xml")

@ddt
class TaskTest(unittest.TestCase):

    @file_data(TASK_DATA)
    def test_file_data_json_dict_dict(self, url, method, header, parameter_type, parameter_body, assert_type, assert_text):
        if url == "":
            return JsonResponse({"code": 10101, "message": "URL不能为空！"})

        try:
            header = json.loads(header)
        except json.decoder.JSONDecodeError:
            return JsonResponse({"code": 10102, "message": "Header格式错误，必须是标准的JSON格式！"})

        try:
            parameter_body = json.loads(parameter_body)
        except json.decoder.JSONDecodeError:
            return JsonResponse({"code": 10103,
             "message": "参数格式错误，必须是标准的JSON格式！"})

        if method == 1:
            if parameter_type == 1:
                r = requests.get(url, params=parameter_body, headers=header)
                if assert_type == 1:
                    self.assertIn(assert_text, r.text)
                elif assert_type == 2:
                    self.assertEqual(r.text, assert_text)

        if method == 2:
            if parameter_type == 1:
                r = requests.post(url, data=parameter_body, headers=header)
                if assert_type == 1:
                    self.assertIn(assert_text, r.text)
                elif assert_type == 2:
                    self.assertEqual(r.text, assert_text)

if __name__ == '__main__':
    with open(TASK_RESULTS, 'wb') as output:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=output),
            failfast=False, buffer=False, catchbreak=False)