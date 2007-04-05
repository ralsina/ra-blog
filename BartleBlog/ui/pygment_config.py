# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from BartleBlog.ui.Ui_pygment_config import Ui_Form
from pygments.styles import get_all_styles
from pygments.formatters import HtmlFormatter

import BartleBlog.backend.config as config

previewtext='''<html><div class="highlight"><pre><span class="n">bstring</span> <span class="nf">spf_query_expand_domain</span><span class="p">(</span> <span class="n">spf_query</span> <span class="o">*</span><span class="n">q</span><span class="p">,</span> <span class="n">bstring</span> <span class="n">arg</span> <span class="p">)</span>
<span class="p">{</span>
    <span class="kt">char</span> <span class="o">*</span><span class="n">s</span><span class="o">=</span><span class="n">bstr2cstr</span><span class="p">(</span><span class="n">arg</span><span class="p">,</span><span class="mi">0</span><span class="p">);</span>
    <span class="kt">int</span> <span class="n">res</span><span class="o">=</span><span class="n">validate_domain_spec</span><span class="p">(</span><span class="n">s</span><span class="p">);</span>
    <span class="n">free</span><span class="p">(</span><span class="n">s</span><span class="p">);</span>
    <span class="k">if</span> <span class="p">(</span><span class="n">res</span><span class="o">==</span><span class="mi">0</span><span class="p">)</span>
    <span class="p">{</span>
        <span class="n">bstring</span> <span class="n">msg</span><span class="o">=</span><span class="n">bformat</span><span class="p">(</span><span class="s">&quot;Invalid domain found (use FQDN): %s&quot;</span><span class="p">,</span> <span class="n">arg</span><span class="o">-&gt;</span><span class="n">data</span><span class="p">);</span>
        <span class="n">throw</span> <span class="p">(</span><span class="n">PERM_ERROR</span><span class="p">,</span><span class="n">msg</span><span class="p">);</span>
    <span class="p">}</span>
    <span class="k">else</span>
    <span class="p">{</span>
        <span class="k">return</span> <span class="n">spf_query_expand</span><span class="p">(</span><span class="n">q</span><span class="p">,</span><span class="n">arg</span><span class="p">,</span><span class="mi">1</span><span class="p">);</span>
    <span class="p">}</span>
<span class="p">}</span>
</pre></div>
</html>'''


class PygmentConfigWidget(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        
        # Set up the UI from designer
        self.ui=Ui_Form()
        self.ui.setupUi(self)

        self.ui.styles.addItems(list(get_all_styles()))
        
        QtCore.QObject.connect(self.ui.styles,QtCore.SIGNAL('activated(QString)'),
            self.loadStyle)
        
        curStyle=config.getValue('pygment','style','murphy')
        self.ui.styles.setCurrentIndex(self.ui.styles.findText(curStyle))
        self.loadStyle(curStyle)
        
    def loadStyle(self,style):
        style=str(style)
        formatter=HtmlFormatter(style=style)
        css=formatter.get_style_defs()
        self.ui.preview.document().setDefaultStyleSheet(css)
        self.ui.preview.setHtml(previewtext)
        config.setValue('pygment','style',style)
        
        print css
        
