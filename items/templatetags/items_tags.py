"""
Template tags for working with lists of model instances which represent
trees.
"""
from __future__ import unicode_literals
from django import template

try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text


register = template.Library()


def parse_document_tree(input_string, source_path=None, destination_path=None,
              input_encoding='unicode', settings_overrides=None):
    """
    Return the document tree and publisher, for exploring Docutils internals.

    Parameters: see `html_parts()`.
    """
    if settings_overrides:
        overrides = settings_overrides.copy()
    else:
        overrides = {}
    overrides['input_encoding'] = input_encoding
    output, pub = core.publish_programmatically(
        source_class=io.StringInput, source=input_string,
        source_path=source_path,
        destination_class=io.NullOutput, destination=None,
        destination_path=destination_path,
        reader=None, reader_name='standalone',
        parser=None, parser_name='restructuredtext',
        writer=None, writer_name='html',
        settings=None, settings_spec=None, settings_overrides=overrides,
        config_section=None, enable_exit_status=None)
    return output, pub

from docutils import core
from docutils import frontend, io, utils, readers, writers
class ReStructuredTextNode(template.Node):
    def __init__(self, input_var, header_output_var):
        self.input_var = template.Variable(input_var)
        self.header_output_var = header_output_var

    def render(self, context):
        # fixme: Parse Header from Document tree
        #        traverse pub.document for title elements, extract them to header_output_var and
        #        write a template tag for generating navigation and stuff from it.

        try:
            output, pub = parse_document_tree(self.input_var.resolve(context), settings_overrides=dict(initial_header_level=2))
        except AttributeError:
            pass

        context[self.header_output_var] = ''
        return pub.writer.parts['html_body']


@register.tag
def parse_rst(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, input_var, header_output_var = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires exactly two arguments" % token.contents.split()[0])
    return ReStructuredTextNode(input_var, header_output_var)

@register.inclusion_tag('inventory_items_usage_tag.html')
def item_usage(element):
    return {'element': element}
