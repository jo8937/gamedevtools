require 'psd'
psdfile = File.dirname(__FILE__) + "/test.psd"

#psd = PSD.new(psdfile).parse!

PSD.open(psdfile) do |psd|
    p psd.tree.to_hash
end