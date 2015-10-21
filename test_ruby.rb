
class Typeverter
    def initialize
        @browser = $browser
        @browser.cookies.clear

        Watir.default_timeout = $waits['watir_default_timeout']
        PageObject.default_page_wait = $waits['pageobject_default_page_wait']
        PageObject.default_element_wait = $waits['pageobject_default_element_wait']

        # create form
        go_to_sign_up_page_url
        on_page(WelcomePage).skip_welcome_page
        @form = 'example'
        on_page(WorkspacePage).create_form_from_scratch(@form)
    end

    def add_field_statement(field)
        on_page(BuildPage).add_field('Statement')
        on_page(BuildPage).fill_statement_field(field['question'])
        on_page(BuildPage).save_field_and_wait_for_popup_closed
    end

    def add_field_multiple_choice(field)
        choices ||= []
        field['choices'].each do |choice|
            choices << choice['label']
        end
        on_page(BuildPage).add_field('Multiple choice')
        on_page(BuildPage).fill_multiple_choice_field(field['question'],choices)
        on_page(BuildPage).save_field_and_wait_for_popup_closed
    end

    def add_field_rating(field)
        on_page(BuildPage).add_field('Rating')
        on_page(BuildPage).fill_rating_field(field['question'])
        on_page(BuildPage).save_field_and_wait_for_popup_closed
    end

    def add_field_opinion_scale(field)
        on_page(BuildPage).add_field('Opinion scale')
        on_page(BuildPage).fill_opinion_scale_field(field['question'])
        on_page(BuildPage).save_field_and_wait_for_popup_closed
    end

    def save_form
        @name = 'test'
        @email =  'test@test.com'
        on_page(BuildPage).click_save_account
        on_page(BuildPage).do_sign_up(@name, @email)
        on_page(BuildPage).go_to_distribute_panel

        # close down
        $browser.quit

        if ENV['HEADLESS'] == 'true'
            @headless.destroy
        end
    end
end

