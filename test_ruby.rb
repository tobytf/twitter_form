require_relative 'ruby_setup'

# from hooks
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

# create fields
fields = ['Short text', 'Email']
fields.each do |field|
  on_page(BuildPage).add_field_with_default_text(field)
end

@name = 'test'
@email =  'test@test.com'
on_page(BuildPage).click_save_account
on_page(BuildPage).do_sign_up(@name, @email)

# close down
$browser.quit

if ENV['HEADLESS'] == 'true'
  @headless.destroy
end
