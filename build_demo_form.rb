# app.rb
require 'sinatra'

class HelloWorldApp < Sinatra::Base
  get '/' do
    "Hello, world!"
  end

  get '/:greeting/?:name?' do
      "#{params[:greeting]}, #{params[:name] ? params[:name] : 'world'}!"
  end
end
