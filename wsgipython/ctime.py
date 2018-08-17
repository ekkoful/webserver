#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

def application(env, start_response):
    status = "200 OK"
    headers = [
        ("Content-Type", "Text/plain")

    ]
    start_response(status, headers)
    return time.ctime()

