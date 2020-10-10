from io import BytesIO,StringIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}):
    print('ttttttttttttttttttttttttt')
    template = get_template(template_src)
    html  = template.render(context_dict)
    # print(html)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    print('9999999999999999999999999999999999999')
    if not pdf.err:
        print('=============================================')
        return HttpResponse(result.getvalue(), content_type='media/invoice')
    return None