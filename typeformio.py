import simplejson as json
import requests
import CREDS
from collections import OrderedDict

API_URL = 'https://api.typeform.io/v0.4/forms'

class form:
    def __init__(self,title='',submit_webhook=''):
        self.title = title
        self.submit_webhook = submit_webhook
        self.fields = [] 

    def to_json(self):
        fields_array = [field.to_dict() for field in self.fields]
        out_data = OrderedDict({ 'title': self.title,
            'webhook_submit_url': self.submit_webhook, 
            'fields': fields_array})

        return json.dumps(out_data)

    def add_field(self,field):
        self.fields.append(field)

    def submit(self):
        headers = {
                "X-API-TOKEN" : CREDS.TYPEFORMIO_API_TOKEN
        }
        r = requests.post(API_URL, headers = headers, data=self.to_json())
        response = r.json()
        if '_links' in response:
            for link in response['_links']:
                if link['rel'] == 'form_render':
                    return link['href']
        else:
            return 'None'

class field:
    def __init__(self,question=''):
        self.type = None 
        self.question = question

    def to_json(self):
        return json.dumps({'question':self.question,'type':self.type})

    def to_dict(self):
        return {'question':self.question,'type':self.type}

class multiple_choice_field(field):
    def __init__(self,question):
        self.type = 'multiple_choice'
        self.question = question
        self.options = []

    def add_option(self,option):
        self.options.append({'label':option})

    def to_json(self):
        return json.dumps({'question':self.question,
                           'type':self.type,
                           'choices':self.options})

    def to_dict(self):
        return {'question':self.question,
                           'type':self.type,
                           'choices':self.options}

class dropdown_field(field):
    def __init__(self,question):
        self.type = 'dropdown'
        self.question = question
        self.options = []

    def add_option(self,option):
        self.options.append({'label':option})

    def to_json(self):
        return json.dumps({'question':self.question,
                           'type':self.type,
                           'choices':self.options})
    def to_dict(self):
        return {'question':self.question,
                           'type':self.type,
                           'choices':self.options}

class short_text_field(field):
    def __init__(self,question):
        self.type = 'short_text'
        self.question = question

class long_text_field(field):
    def __init__(self,question):
        self.type = 'long_text'
        self.question = question


if __name__ == '__main__':
    test_form = form('test','https://1@2.com')
    field1=multiple_choice_field('q1')
    field1.add_option('one')
    field1.add_option('two')
    field2 = dropdown_field('q2')
    field2.add_option('three')
    field2.add_option('four')
    test_form.add_field(field1)
    test_form.add_field(field2)
    print test_form.submit()
    #print test_form.to_json()


