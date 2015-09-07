from bs4 import BeautifulSoup
import logging
import collections
import typeformio
import argparse

class google_forms_to_typeform:

    def __init__(self,raw_html):
        self.typeform = typeformio.form('Test Form','https://1.com')
        self.raw_html = raw_html
        self.convert_form()

    def to_typeform(self):
        return self.typeform
 
    def convert_form(self):
        soup = BeautifulSoup(self.raw_html,'html5lib')
	questions = soup.find_all(class_='ss-form-question')

	for question in questions:

	    question_text = question.select('label .ss-q-title')[0].contents[0].strip()
	    # try and guess what type of question we are looking at
	    if question.find(class_="ss-radio"):
		field = self.get_multiple_choice_question(question)
	    elif question.find(class_="ss-scale"):
		field = self.get_opinion_scale_question(question)
	    elif question.find(class_="ss-choices"):
		field = self.get_multiple_choice_question(question,allow_multi_selection=True)
	    elif question.find(class_="ss-text"):
		field = self.get_short_text_question(question)
	    elif question.find(class_="ss-paragraph-text"):
		field = self.get_long_text_question(question)
	    elif question.find(class_="ss-select"):
		field = self.get_dropdown_question(question)
	    else:
		logging.warn("** question %s not decodable" % question_text)
		continue

            field.set_question_text(question_text)
            description = question.find(class_='ss-secondary-text').string
            if description:
                field.set_description(description)

	    if question.find(class_='required-asterisk'): 
		field.set_required(True)
	    else: 
		field.set_required(False)
	    logging.info("question: %s" % question_text)
	    
	    self.typeform.add_field(field)

    def get_multiple_choice_question(self,html_frag,allow_multi_selection=False):
        logging.info("found multiple choice question")
        field = typeformio.multiple_choice_field()
        choices = [ l.text for l in html_frag.find_all(class_="ss-choice-label") if l.text != '' ]
        map(field.add_option,choices)

        field.set_tags((html_frag.select(".ss-choice-item input")[0]["name"]).replace(".",":"))
        # this should be coming soon
        #field.allow_multiple_selection(allow_multi_selection)

	return field

    def get_opinion_scale_question(self,html_frag):
        logging.info("found opinion scale question")
        field = typeformio.opinion_scale_field()
        field.set_tags((html_frag.select(".ss-scalerow-fieldcell input")[0]["name"]).replace(".",":"))

        return field

    def get_short_text_question(self,html_frag):
	field = typeformio.short_text_field()
	logging.info("found short text question") 
        field.set_tags((html_frag.find("input")["name"]).replace(".",":"))
	return field 

    def get_long_text_question(self,html_frag):
	field = typeformio.long_text_field()
	logging.info("found long text question") 
        field.set_tags((html_frag.find("textarea")["name"]).replace(".",":"))
	return field 

    def get_dropdown_question(self,html_frag):
	field = typeformio.dropdown_field()
	logging.info("dropdown field question") 
        choices = [ l.text for l in html_frag.find_all("option") if l.text !='' ]
        map(field.add_option,choices)
        field.set_tags((html_frag.find("select")["name"]).replace(".",":"))
	return field 

if __name__ == '__main__':
    #TEST_URL = 'https://docs.google.com/forms/d/1lxc7376GBtmrZQTNi72Ila2D_pFrHZ05EsWx1BruwQU/viewform'
    #TEST_URL = 'https://docs.google.com/forms/d/1XzrqUf7i42UzF5V9qFoz1W_d0l1TI799H2pYS4OJ7g0/viewform?c=0&w=1&usp=send_form'
    #TEST_URL = 'https://docs.google.com/forms/d/1s3bZo9t0SQIiRHysd9rinIEG1tBOlnXpzWm4j31jeXg/viewform?usp=send_form'
    TEST_URL = 'https://docs.google.com/forms/d/16trYDb8Ajzzhzsl1HtNT2iRzmWcPVHmLzWxID_wxdIQ/viewform?usp=send_form'

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
    converter = google_forms_to_typeform(r.text)
    typeform = converter.to_typeform()
    print typeform.to_json()
    if args.submit_flag:
        r = typeform.submit()
        print r
     

