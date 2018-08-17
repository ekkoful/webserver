#!/usr/bin/env python
# -*- coding: utf-8 -*-

def application(env, start_response):
    status = "200 OK"
    headers = [
        ("Content-Type", "Text/plain")
    ]
    start_response(status, headers)
    return "Hello World"
