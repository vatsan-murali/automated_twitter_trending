function FindProxyForURL(url, host) {
if (shExpMatch(url, "http*") && !isInNet(host, "192.168.0.0", "255.255.0.0"))
{ host = ["us-ca", "us-tx"][Math.floor(2 * Math.random())];
return "PROXY " + host + ".proxymesh.com:31280"; }
else { return "DIRECT"; } }
