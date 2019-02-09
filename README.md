## IPTV proxy interneto.tv

### Kodėl?

interneto.tv realiai yra webinis iptv grotuvas, tad norit jį pasileisti per pvz Apple TV (kuris neturi naršyklės) reikia "išlukštenti" kanalų iptv stream'us ir paduoti į IPTV apps'ą (pvz GSE IPTV player).

Šis scriptas veikia kai paprastas proxy - grąžina playlistą IPTV app'sui kur yra paprasti adresai, o apps'ui atėjus kuriuo nors adresu autentifikuojasi į interneto.tv ir grąžina ju tikrąjį kanalo url'ą kuriuo rodomas specifinis kanalo stream'as

libinternetotv.py paimtas iš https://github.com/Vytax/plugin.video.interneto.tv ačių @vytax už tai

### Naudojimas:
- iš config_sample.py sukurti config.py ir nurodyti prisijungimo duomenis
- paleisti su python3: `python3 server.py` (prieš tai `pip3 install bs4`)
- nukreipti savo grotuvą į playlistą, pvz `http://kompo_ip_kur_paleistas_scriptas:6565/itv.m3u`