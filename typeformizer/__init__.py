import re
from convert_monkey import monkey_to_typeform
from convert_google_forms import google_forms_to_typeform

monkey_url = re.compile('http[s]?://www.surveymonkey.com')
google_forms_url = re.compile('http[s]?://docs.google.com/forms')
forms_links = [
        {'class':'monkey_to_typeform', 're':monkey_url},
        {'class':'google_forms_to_typeform', 're':google_forms_url}
]
