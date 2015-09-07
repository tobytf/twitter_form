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
            return r.json() 

class field:
    def __init__(self,question_text=''):
        self.type = None 
        self.question = question_text
        self.description = ''
        self.required = False
        self.tags = []
        self.options = None

    def set_question_text(self,question_text):
        self.question = question_text

    def set_description(self,description):
        self.description = description

    def set_required(self,required):
        self.required = required

    def set_tags(self,tag):
        self.tags.append(tag)

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        if self.options is None:
	    return {'question':self.question,
                    'type':self.type,
                    'description':self.description,
		    'required':self.required,
		    'tags':self.tags}
        else:
	    return {'question':self.question,
                    'type':self.type,
                    'description':self.description,
		    'required':self.required,
		    'tags':self.tags,
                    'choices':self.options}
            

class multiple_choice_field(field):
    def __init__(self,question_text=''):
        self.type = 'multiple_choice'
        self.question = question_text
        self.description = ''
        self.required = False
        self.tags = []
        self.options = []
        self.allow_multiple_choice_options = False

    def add_option(self,option):
        self.options.append({'label':option})

class dropdown_field(field):
    def __init__(self,question_text=''):
        self.type = 'dropdown'
        self.question = question_text
        self.description = ''
        self.required = False
        self.tags = []
        self.options = []

    def add_option(self,option):
        self.options.append({'label':option})

class short_text_field(field):
    def __init__(self,question_text=''):
        self.type = 'short_text'
        self.question = question_text
        self.description = ''
        self.required = False
        self.tags = []
        self.options = None

class long_text_field(field):
    def __init__(self,question_text=''):
        self.type = 'long_text'
        self.question = question_text
        self.description = ''
        self.required = False
        self.tags = []
        self.options = None

class opinion_scale_field(field):
    def __init__(self,question_text=''):
        self.type = 'opinion_scale'
        self.question = question_text
        self.description = ''
        self.required = False
        self.tags = []
        self.options = None

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


