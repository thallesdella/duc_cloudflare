import requests as r
import json as j
import time as t
import sys as s
import re

zona = '%Nome_da_entrada%' # casa.bunana.com.br
zone_id = '%Id_da_zona%' # 970c55a5e3c70eb5703b582e9d939e19

def ipType(ip):
    ip = str(ip)
    v4 = re.compile('^(?:(?:^|\.)(?:2(?:5[0-5]|[0-4]\d)|1?\d?\d)){4}$')
    v6 = re.compile('(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))')
    
    if v4.match(ip):
        return 'A'
	
    if v6.match(ip):
        return 'AAAA'
        
    return False

if __name__ == "__main__":
    print('Init...')
    ip = ''
    zone_id = ''
    zone_ip = ''
	
    while True:
        try:
	        # Obtem endereço de IP
            while ip == '':
                print('Obtendo Endereço IP...')
                conn = r.get('https://api.myip.com/', headers={'Content-Type' : 'application/json'})
                if conn.status_code == r.codes.ok:
                    json = conn.json()
                    ip = json['ip']
                    print('Endereço IP: {}'.format(ip))
                else:
                    print('.')
                    t.sleep(5)
		
            headers = {
                'X-Auth-Email' : '%Email%', # teste@gmail.com
                'X-Auth-Key' : '%Auth_key%', # c46b7425ea00e9789e59897234df1529edc96
                'Content-Type' : 'application/json'
            }
		
            # Obtem informações da zona DNS
            print('Obtendo Informações da Zona!')
            url = 'https://api.cloudflare.com/client/v4/zones/{}/dns_records?name={}'.format(zone_id, zona)
            conn = r.get(url, headers=headers)
            if conn.status_code == r.codes.ok:
                json = conn.json()['result'][0]
                record_id = json['id']
                record_ip = json['content']
		
            # Atualiza IP na zona
            if ip != record_ip:
                print('Atualizando Zona!')
                url = 'https://api.cloudflare.com/client/v4/zones//dns_records/{}'.format(zone_id, record_id)
                payload = {
                    'type' : ipType(ip),
                    'name' : zona,
                    'content' : ip,
					'ttl' : 300
                }
			
                conn = r.put(url, data=j.dumps(payload), headers=headers)
                if conn.status_code == r.codes.ok:
                    print('Zona Atualizada!')
            else:
                print('Zona ja esta atualizada!')

            t.sleep(5 * 60)
        except KeyboardInterrupt:
            print('Saindo...')
            s.exit()