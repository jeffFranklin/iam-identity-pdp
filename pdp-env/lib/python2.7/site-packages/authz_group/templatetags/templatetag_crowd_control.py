from django import template
from django.utils.safestring import mark_safe
from django.template import RequestContext, loader

register = template.Library()

@register.tag
def crowd_control_js():
    return CrowdControlJsNode()

@register.tag
def crowd_control_css():
    return CrowdControlCssNode()

@register.tag
def crowd_control_templates():
    return CrowdControlTemplateNode()

@register.tag
def crowd_control(parser, token):
    return CrowdControlNode()

class CrowdControlNode(template.Node):
    def render(self, context):
        return CrowdControlCssNode().render(context) + CrowdControlTemplateNode().render(context) + CrowdControlJsNode().render(context)

class CrowdControlCssNode(template.Node):
    def render(self, context):
        t = loader.get_template('crowd_control/styles.html')
        return t.render(context)

class CrowdControlJsNode(template.Node):
    def render(self, context):
        t = loader.get_template('crowd_control/js.html')
        return t.render(context)

class CrowdControlTemplateNode(template.Node):
    def render(self, context):
        t = loader.get_template('crowd_control/templates.html')
        return t.render(context)
