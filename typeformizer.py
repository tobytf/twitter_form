from bs4 import BeautifulSoup
import collections
import requests
import json
import logging
import find_questions
import argparse
import typeformio

#logging.basicConfig(level=logging.INFO)

survey_hash = []

def convert_monkey(raw_html):
    soup = BeautifulSoup(raw_html,'html5lib')
    form = typeformio.form('test form','https://1.com')

    questions = soup.find_all(class_='question-row')
    for question in questions:
        # first get the question

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
        #logging.info("question: %s" % question_text)

        question_body = question.find(class_='question-body')
        if question_body is None: continue

        # try and guess what type of question we are looking at
        if question_body.find(class_="horizontal-answer-options"):
            field = find_questions.get_option_question(question_body,question_text)
        elif question_body.select("select"):
            field = find_questions.get_select_question(question_body,question_text)
        elif question_body.find("textarea"):
            field = find_questions.get_textarea_question(question_body,question_text)
        elif question_body.find("input",class_="text"):
            field = find_questions.get_textfield_question(question_body,question_text)
        elif question_body.select("input.open"):
            field = find_questions.get_textfield_question(question_body,question_text)
        else:
            logging.warn("** question %s not decodable" % question_text)
            continue
         
        question_data = {'question': question_text, 'required': required, 'field':field }
        survey_hash.append(question_data)
        form.add_field(field)

    return form

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
    form = convert_monkey(r.text)
    logging.warn("Form to convert %s" % (args.url))
    print form.to_json()
    if args.submit_flag:
        r = form.submit()
        logging.warn("Generated typeform %s" % (r))
