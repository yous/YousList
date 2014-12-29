require 'webrick'

server = WEBrick::HTTPServer.new(Port: 8000, DocumentRoot: File.dirname(__FILE__))
trap('INT') { server.shutdown }
server.start
