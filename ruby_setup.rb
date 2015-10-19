require 'watir-webdriver'
require 'watir-webdriver/wait'
require 'active_support/all'
require 'page-object'
require 'page-object/page_factory'
require 'headless'
require 'rest-client'
require 'json'
require 'configuration'
require 'yaml'

#World(PageObject::PageFactory)

Configuration.load 'ruby_config'

#############################
#  Load default test data   #
#############################

file_path = File.join(File.dirname(__FILE__), '..', 'TfAutomation')
puts file_path
$api = YAML.load_file(File.expand_path(File.join(file_path, 'data', 'api.yml')))
$data = YAML.load_file(File.expand_path(File.join(file_path, 'data', 'data.yml')))
$emails = YAML.load_file(File.expand_path(File.join(file_path, 'data', 'emails.yml')))
$nag_screens = YAML.load_file(File.expand_path(File.join(file_path, 'data', 'nag_screens.yml')))
$metadata = YAML.load_file(File.expand_path(File.join(file_path, 'data', 'metadata.yml')))
$default_answer = YAML.load_file(File.expand_path(File.join(file_path, 'data', 'default_answer.yml')))
$default_question = YAML.load_file(File.expand_path(File.join(file_path, 'data', 'default_question.yml')))
$logic_jumps = YAML.load_file(File.expand_path(File.join(file_path, 'data', 'logic_jumps.yml')))
$concurrency_popup = YAML.load_file(File.expand_path(File.join(file_path, 'data', 'concurrency_popup.yml')))
$waits = YAML.load_file(File.expand_path(File.join(file_path, 'data', 'waits.yml')))
$http_status_code = YAML.load_file(File.expand_path(File.join(file_path, 'data', 'http_status_code.yml')))


#########################
#  Load shared methods  #
#########################

require_relative File.join(file_path, 'features', 'support', 'paths_helper')
include PathsHelper

require_relative File.join(file_path, 'features', 'support', 'browser_helper')
include BrowserHelper

require_relative File.join(file_path, 'features', 'support', 'actions_helper')
include ActionsHelper

#require web page support
Dir[File.join(file_path, 'features', 'support', 'web_pages/*.rb')].each {|file| load file }

######################
#  Headless support  #
######################

if ENV['HEADLESS'] == 'true'
  puts 'INFO: Headless mode on'
  @headless = Headless.new
  @headless.start
end


############################
#  Browser initialization  #
############################

include PageObject::PageFactory

puts "INFO: Using #{ENV['BROWSER']} browser"
$browser = open_browser
