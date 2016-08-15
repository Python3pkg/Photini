# -*- coding: utf-8 -*-
##  Photini - a simple photo metadata editor.
##  http://github.com/jim-easterbrook/Photini
##  Copyright (C) 2012-15  Jim Easterbrook  jim@jim-easterbrook.me.uk
##
##  This program is free software: you can redistribute it and/or
##  modify it under the terms of the GNU General Public License as
##  published by the Free Software Foundation, either version 3 of the
##  License, or (at your option) any later version.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
##  General Public License for more details.
##
##  You should have received a copy of the GNU General Public License
##  along with this program.  If not, see
##  <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import locale
import os
import webbrowser

import six

from .configstore import key_store
from .photinimap import PhotiniMap
from .pyqt import QtCore, QtWebKit, QtWidgets

class BingMap(PhotiniMap):
    def __init__(self, *arg, **kw):
        self.copyright_widget = QtWidgets.QLabel()
        self.copyright_widget.setWordWrap(True)
        super(BingMap, self).__init__(*arg, **kw)
        self.map.settings().setAttribute(
            QtWebKit.QWebSettings.LocalContentCanAccessRemoteUrls, True)
        self.map.settings().setAttribute(
            QtWebKit.QWebSettings.LocalContentCanAccessFileUrls, True)

    def load_api(self):
        if self.app.test_mode:
            src = 'http://www.bing.com/api/maps/mapcontrol?callback=initialize'
            src += '&branch=experimental'
        else:
            src = 'http://ecn.dev.virtualearth.net/mapcontrol/mapcontrol.ashx?v=7.0'
        self.setProperty('api_key', key_store.get('bing', 'api_key'))
        if not self.app.test_mode:
            lang, encoding = locale.getdefaultlocale()
            if lang:
                src += '&mkt={0},ngt'.format(lang.replace('_', '-'))
            else:
                src += '&mkt=ngt'
        return """
    <script charset="UTF-8" type="text/javascript"
      src="{0}">
    </script>
""".format(src)

    def show_terms(self):
        # return widgets to display map terms and conditions
        yield self.copyright_widget
        load_tou = QtWidgets.QPushButton(self.tr('Terms of Use'))
        load_tou.clicked.connect(self.load_tou)
        yield load_tou

    @QtCore.pyqtSlot(six.text_type)
    def new_copyright(self, text):
        self.copyright_widget.setText(text)

    @QtCore.pyqtSlot()
    def load_tou(self):
        webbrowser.open_new(
            'http://www.microsoft.com/maps/assets/docs/terms.aspx')
