#!/usr/bin/env ruby
# encoding: utf-8

require "sinatra"
require "open-uri"
require "uri"
require "nokogiri"
require "json"

set :protection, :except=>:path_traversal

Dir.mkdir("logs") unless Dir.exist?("logs")
cache_log = File.new("logs/extraction_nocache.log", "a")

get "/" do
  "Usage: http://<hostname>[:<prt>]/api/<url>"
end

get "/api/*" do
  url = [params['splat'].first, request.query_string].reject(&:empty?).join("?")
  
  # SEM CACHE - sempre faz extração
  cache_status = "NO_CACHE"
  jsonlinks = JSON.pretty_generate(extract_links(url))

  cache_log.puts "#{Time.now.to_i}\t#{cache_status}\t#{url}"
  cache_log.flush

  status 200
  headers "content-type" => "application/json"
  body jsonlinks
end

def extract_links(url)
  links = []
  doc = Nokogiri::HTML(open(url))
  doc.css("a").each do |link|
    begin
      text = link.text.to_s.encode('UTF-8', invalid: :replace, undef: :replace, replace: '').strip.split.join(" ")
      links.push({
        text: text.empty? ? "[IMG]" : text,
        href: URI.join(url, link["href"])
      })
    rescue => e
      # Skip links that cause encoding or URI errors
    end
  end
  links
end
