# app.rb
require 'sinatra'
require 'json'

class HelloWorldApp < Sinatra::Base
  get '/' do
    "Hello, world!"
  end

  post '/typeformize' do 
    jdata = JSON.parse(request.body.read)
    puts jdata
    "http://hello.hmtml"
  end

  get '/example.json' do
      content_type :json
      { :key1 => 'value1', :key2 => 'value2' }.to_json
  end

  get '/:greeting/?:name?' do
      "#{params[:greeting]}, #{params[:name] ? params[:name] : 'world'}!"
  end
end
