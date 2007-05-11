#!/bin/sh

cd resources 
pyrcc4 icons.qrc > ../BartleBlog/ui/icons_rc.py
rst2html.py help.rst help.html
