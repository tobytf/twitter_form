require_relative 'ruby_setup'

# from hooks
@browser = $browser
@browser.cookies.clear

Watir.default_timeout = $waits['watir_default_timeout']
PageObject.default_page_wait = $waits['pageobject_default_page_wait']
PageObject.default_element_wait = $waits['pageobject_default_element_wait']

# enter form
go_to_sign_up_page_url
on_page(WelcomePage).skip_welcome_page
