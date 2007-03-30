# -*- coding: utf-8 -*-

class YahooGrids:
    def head(self):
        return ['<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.2.0/build/reset-fonts-grids/reset-fonts-grids.css">']

def factory (blog):
    return YahooGrids()
