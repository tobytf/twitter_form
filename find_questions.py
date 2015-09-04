import logging
import collections
import typeformio

def get_option_question(html_frag,question):
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

def get_select_question(html_frag,question):
    logging.info("select question")
    option_data = []
    field = typeformio.dropdown_field(question)
    for i,option in enumerate(html_frag.find_all("option")):
        # removing the repeating question in the text of the first option
        option_text = ' '.join(option.stripped_strings)
        option_data.append({'text':option_text,'text_input':False})
        field.add_option(option_text)
    return field

def get_textarea_question(html_frag,question):
    field = typeformio.short_text_field(question)
    logging.info("text area question") 
    rows = html_frag.select("textarea")[0]['rows']
    cols = html_frag.select("textarea")[0]['cols']
    return field 

def get_textfield_question(html_frag,question):
    field = typeformio.long_text_field(question)
    logging.info("text field question") 
    size = html_frag.find(class_="text")['size']
    return field 


