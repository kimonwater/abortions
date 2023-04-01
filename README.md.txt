#### DOCU
This repo is for putting down data and reflecting on **abortions**.

The **main product** is the abortions.ipynb jupyter notebook x medium style containing markdown and 3 graphs.

The 3 graphs are defined in the **separate** "utils.py" using standard pandas, matplotlib, folium, and squarify 🙏🏽 

#### DATA

unless stated differently all is retrieved from the Federal Statistical Office of Germany (Statistisches Bundesamt destatis) which has different views e.g. through the The Information System of the Federal Health Monitoring (Gesundheitsberichtserstattung des Bundes GBE Bund) in March 2023 

Abortions:
[total, family status, reason, previous live births](https://www.gbe-bund.de/gbe/pkg_olap_tables.prc_set_hierlevel?p_uid=gast&p_aid=34200902&p_sprache=D&p_help=2&p_indnr=240&p_ansnr=87425192&p_version=5&p_dim=D.000&p_dw=3722&p_direction=drill), [age group](https://www.gbe-bund.de/gbe/!pkg_olap_tables.prc_set_orientation?p_uid=gast&p_aid=29968742&p_sprache=D&p_help=2&p_indnr=238&p_ansnr=56517371&p_version=3&D.000=2&D.001=3&D.002=1&D.100=3), [live births](https://www-genesis.destatis.de/genesis/online?operation=abruftabelleBearbeiten&levelindex=1&levelid=1680351382023&auswahloperation=abruftabelleAuspraegungAuswaehlen&auswahlverzeichnis=ordnungsstruktur&auswahlziel=werteabruf&code=12612-0001&auswahltext=&werteabruf=Werteabruf#abreadcrumb), [still births](https://www-genesis.destatis.de/genesis/online?operation=abruftabelleBearbeiten&levelindex=1&levelid=1680351444834&auswahloperation=abruftabelleAuspraegungAuswaehlen&auswahlverzeichnis=ordnungsstruktur&auswahlziel=werteabruf&code=12612-0018&auswahltext=&wertauswahl=1399&wertauswahl=2874&werteabruf=Werteabruf#abreadcrumb) </br>
Cities: [population](https://www.destatis.de/DE/Themen/Laender-Regionen/Regionales/Gemeindeverzeichnis/Administrativ/05-staedte.html) (added category manually), [lon, lat](https://launix.de/launix/launix-gibt-plz-datenbank-frei/) (from the launix company lausitz + linux; added bottom 9 manually)


#### THANKS
🐣 Daniel for being the literal inspiration, 🦊 Sebastian for helping with the first jupyter notebook and python all the way back, 🐑 Alex for trusting me and my technical skills when in doubt, 🖤 God & family