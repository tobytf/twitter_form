import re
import sys
import requests
import logging
from convert_monkey import monkey_to_typeform
from convert_google_forms import google_forms_to_typeform

monkey_url = re.compile('http[s]?://www.surveymonkey.com')
google_forms_url = re.compile('http[s]?://docs.google.com/forms')
forms_links = [
        {'class':'monkey_to_typeform', 're':monkey_url},
        {'class':'google_forms_to_typeform', 're':google_forms_url}
]

def convert(url):
    try:
        r = requests.get(url)
        actual_url = r.url
        logging.warn('got url %s' % actual_url)
    except Exception as e:
        print "couldn't get url - %s" % url
        print e
        return None

    # now see if we can convert this this url
    typeform_url = None
    for link_re in forms_links:
        match = re.search(link_re['re'],actual_url)
        if match:
            logging.warn("converting form ... %s %s" % (actual_url,link_re['class']))

            converter = getattr(sys.modules[__name__],link_re['class'])(r.text)
            typeform = converter.to_typeform()
            typeform_url = typeform.submit()
            logging.warn("generated typeform ... %s " % typeform_url)
            break

    return typeform_url

