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
       method = 'add_' + field['type']
       typeformizer.method(str).call(field)
    end
    content_type :json
    { :url => 'http://hello.html'}.to_json
  end

end
