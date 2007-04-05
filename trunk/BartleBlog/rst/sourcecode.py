from docutils import nodes
from docutils.parsers.rst import directives
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

city={
    'cpp':'c',
    'hypertext':'html'
}

pygments_formatter = HtmlFormatter(cssclass='code-block')

def pygments_directive(name, arguments, options, content, lineno,
                       content_offset, block_text, state, state_machine):
    lexer=None
    lname=arguments[0].lower()
    try:
        lexer = get_lexer_by_name(lname)
    except ValueError:
        pass
    # First try one of the SilverCity names, just in case
    try:
        lexer = get_lexer_by_name(city[lname])
    except KeyError:
        pass
    if not lexer:
        print "No lexer found for "+lname
        # no lexer found - use the text one instead of an exception
        lexer = get_lexer_by_name('text')
    parsed = highlight(u'\n'.join(content), lexer, pygments_formatter)
    return [nodes.raw('', parsed, format='html')]
pygments_directive.arguments = (1, 0, 1)
pygments_directive.content = 1
directives.register_directive('sourcecode', pygments_directive)
directives.register_directive('code-block', pygments_directive)


if __name__ == "__main__":
  import docutils.core
  docutils.core.publish_cmdline(writer_name='html')
