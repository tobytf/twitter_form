from bs4 import BeautifulSoup
import logging
import collections
import typeformio
import argparse

class monkey_to_typeform:

    def __init__(self,raw_html):
        self.typeform = typeformio.form('Test Form','https://1.com')
        self.raw_html = raw_html
        self.convert_form()

    def to_typeform(self):
        return self.typeform
 
    def convert_form(self):
        soup = BeautifulSoup(self.raw_html,'html5lib')
	questions = soup.find_all(class_='question-row')

	for question in questions:
	    q_class = question.find(class_='question-title-container')
	    if q_class is None: continue

	    if q_class.find(class_='required-asterisk'): 
		required = True
	    else: 
		required = False

	    if q_class.find(class_='user-generated'): 
		question_text = q_class.find(class_='user-generated').string
	    else:
		question_text = ''
	    logging.info("question: %s" % question_text)

	    question_body = question.find(class_='question-body')
	    if question_body is None: continue

	    # try and guess what type of question we are looking at
	    if question_body.find(class_="horizontal-answer-options"):
		field = self.get_option_question(question_body,question_text)
	    elif question_body.select("select"):
		field = self.get_select_question(question_body,question_text)
	    elif question_body.find("textarea"):
		field = self.get_textarea_question(question_body,question_text)
	    elif question_body.find("input",class_="text"):
		field = self.get_textfield_question(question_body,question_text)
	    elif question_body.select("input.open"):
		field = self.get_textfield_question(question_body,question_text)
	    else:
		logging.warn("** question %s not decodable" % question_text)
		continue
	     
	    question_data = {'question': question_text, 'required': required, 'field':field }
	    self.typeform.add_field(field)

    def get_option_question(self,html_frag,question):
        logging.info("option question")
        field = typeformio.multiple_choice_field(question)
        option_data = collections.OrderedDict()
        for i,option in enumerate(html_frag.find_all(class_="answer-option-cell")):
	    if option.find("input"):
	        option_text=''
	        id = option.find("input")['id']
	        if option.select("input.cb"): 
	           option_type = 'checkbox'
	        elif option.find(class_="radio-button-input"): 
	           option_text = ' '.join(option.find(class_='radio-button-label-text').stripped_strings)
	           field.add_option(option_text)
	           option_type = 'radiobutton'
	        else: option_type = 'unknown'
	        option_data[id] = {'type':option_type,'text':option_text.replace('\n',''),'text_input':False}

	# if we have any open text options update the dict
	open_text_fields = html_frag.find_all(class_="other-answer-container")
	for open_text in open_text_fields: 
	    open_text_id = open_text['id'].split('_')[2]
	    open_text_size = int(open_text['size'])
	    option_data[open_text_id]['text_input']=open_text_size
	# convert back to list
	option_list = option_data.values()

	return field

    def get_select_question(self,html_frag,question):
	logging.info("select question")
	option_data = []
	field = typeformio.dropdown_field(question)
	for i,option in enumerate(html_frag.find_all("option")):
	    # removing the repeating question in the text of the first option
	    option_text = ' '.join(option.stripped_strings)
	    option_data.append({'text':option_text,'text_input':False})
	    field.add_option(option_text)
	return field

    def get_textarea_question(self,html_frag,question):
	field = typeformio.short_text_field(question)
	logging.info("text area question") 
	rows = html_frag.select("textarea")[0]['rows']
	cols = html_frag.select("textarea")[0]['cols']
	return field 

    def get_textfield_question(self,html_frag,question):
	field = typeformio.long_text_field(question)
	logging.info("text field question") 
	size = html_frag.find(class_="text")['size']
	return field 

if __name__ == '__main__':
    TEST_URL = 'http://www.surveymonkey.com/s/JPH59QN'

    import argparse
    import sys
    parser = argparse.ArgumentParser(description='Convert a form')
    parser.add_argument('url', type=str, nargs='?', default = TEST_URL,
                         help='the url to convert')
    parser.add_argument('-s','--submit_flag', action='store_true')
    args = parser.parse_args()

    import requests
    r = requests.get(args.url)
    logging.warn("Form to convert %s" % (args.url))
    converter = monkey_to_typeform(r.text)
    typeform = converter.to_typeform()
    print typeform.to_json()
    if args.submit_flag:
        r = typeform.submit()
     

