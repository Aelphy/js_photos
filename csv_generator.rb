require 'json'
require 'csv'
require 'time'

file = File.read('json')

data_hash = JSON.parse(file)

def color_to_rgb(color)
  if color == 'red'
    return '#FF0000'
  elsif color == 'blue'
    return '#0000FF'
  elsif color == 'azure'
    return '#9966FF'
  else
    return '#00FF00'
  end
end

CSV.open('data.csv', 'wb') do |csv|
  data_hash.each do |k, v|
    t = Time.strptime(v['date'], '%Y:%m:%d %H:%M:%S')
    csv << [t.strftime('%Y:%m:%d'), "'#{k}'", color_to_rgb(v['color']), t.strftime('%H.%M')]
  end
end
