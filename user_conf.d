server {
	listen 80;
	server_name anand-tandon.duckdns.org;
	
	if ($host = anand-tandon.duckdns.org) {
		return 301 https://$host$redirecturi
	}
}

server {
	listen 443 ssl;
	server_name anand-tandon.duckdns.org;

	location / {
		proxy_pass http://myportfolio:5000/
	}

	# load certificate files
	ssl_certificate /etc/letsencrypt/live/myportfolio/fullchain.pem;
	ssl_certificate_key /etc/letsencrypt/live/myportfolio/privkey.pem;
	ssl_trusted_certificate /etc/letsencrypt/live/myportfolio/chain.pem
