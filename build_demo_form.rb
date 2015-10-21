# app.rb
require 'rubygems'
require 'sinatra'
require 'json'
require_relative 'test_ruby'

class HelloWorldApp < Sinatra::Base
  get '/' do
    "Hello, world!"
  end

  post '/typeformize' do 
    jdata = JSON.parse(request.body.read)
    
    typeformizer = Typeverter.new
    
    jdata['fields'].each do |field|
       field_method = 'add_field_' + field['type']
       typeformizer.method(field_method).call(field)
    end
    
    typeformizer.save_form
    content_type :json
    { :url => 'http://hello.html'}.to_json
  end

end
