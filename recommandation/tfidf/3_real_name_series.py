import psycopg2

from PTUT import DATABASES

conn = psycopg2.connect(
        "dbname='{0}' user='{1}' host='{2}' password='{3}'".format(DATABASES['default']['NAME'],
                                                                DATABASES['default']['USER'],
                                                                DATABASES['default']['HOST'],
                                                                DATABASES['default']['PASSWORD']))


serie = dict()
serie['24'] = '24'
serie['trucalling'] = 'Tru Calling'
serie['eureka'] = 'Eureka'
serie['onetreehill'] = 'one tree hill'
serie['womensmurderclub'] = "womens murder club"
serie['eleventhhour'] = 'eleventh hour'
serie['friends'] = 'Friends'
serie['desperatehousewives'] = 'Desperate Housewives'
serie['knightrider'] = 'Knight Rider'
serie['greysanatomy'] = "Greys Anatomy"
serie['community'] = 'Community'
serie['jake'] = 'Jake'
serie['jericho'] = 'Jericho'
serie['samanthawho'] = 'Samantha Who'
serie['blade'] = 'Blade'
serie['psych'] = 'psych'
serie['sixfeetunder'] = 'Six Feet Under'
serie['moonlight'] = 'Moonlight'
serie['whitechapel'] = 'Whitechapel'
serie['bones'] = 'Bones'
serie['extras'] = 'Extras'
serie['invasion'] = 'Invasion'
serie['theshield'] = 'The Shield'
serie['	dirt'] = 'Dirt'
serie['sexandthecity'] = 'Sex and the City'
serie['battlestargalactica'] = 'Battlestar Galactica'
serie['howimetyourmother'] = 'How I Met Your Mother'
serie['burnnotice'] = 'Burn Notice'
serie['dexter'] = 'Dexter'
serie['spaced'] = 'Spaced'
serie['futurama'] = 'Futurama'
serie['theoc'] = 'The O.C.'
serie['caprica'] = 'Caprica'
serie['entourage'] = 'Entourage'
serie['breakingbad'] = 'Breaking Bad'
serie['supernatural'] = 'Supernatural'
serie['mynameisearl'] = 'My Name Is Earl'
serie['gossipgirl'] = 'Gossip Girl'
serie['theriches'] = 'The Riches'
serie['thevampirediaries'] = 'Vampire Diaries'
serie['jekyll'] = 'Jekyll'
serie['mental'] = 'Mental'
serie['flashforward'] = 'Flashforward'
serie['oz'] = 'Oz'
serie['theblackdonnellys'] = 'The Black Donnellys'
serie['dirtysexymoney'] = 'Dirty Sexy Money'
serie['primeval'] = 'Primeval'
serie['swingtown'] = 'Swingtown'
serie['coldcase'] = 'Cold Case'
serie['v'] = 'V'
serie['torchwood'] = 'Torchwood'
serie['niptuck'] = 'Nip/Tuck'
serie['thewire'] = 'The Wire'
serie['prisonbreak'] = 'Prison Break'
serie['thementalist'] = 'Mentalist'
serie['rome'] = 'Rome'
serie['ghostwhisperer'] = 'Ghost Whisperer'
serie['madmen'] = 'Mad Men'
serie['flightoftheconchords'] = 'Flight of the Conchords'
serie['angel'] = 'Angel'
serie['fearitself'] = 'Fear Itself'
serie['bionicwoman'] = 'Bionic Woman'
serie['cupid'] = 'Cupid'
serie['doctorwho'] = 'Doctor Who'
serie['ncislosangeles'] = 'NCIS : Los Angeles'
serie['thesarahconnorchronicles'] = 'Terminator: The Sarah Connor Chronicles'
serie['intreatment'] = 'In Treatment'
serie['southpark'] = 'South Park'
serie['dollhouse'] = 'Dollhouse'
serie['daybreak'] = 'Day Break'
serie['robinhood'] = 'Robin Hood'
serie['pushingdaisies'] = 'Pushing Daisies'
serie['fringe'] = 'Fringe'
serie['heroes'] = 'Heroes'
serie['sanctuary'] = 'Sanctuary'
serie['californication'] = 'Californication'
serie['thelostroom'] = 'The Lost Room'
serie['chuck'] = 'Chuck'
serie['painkillerjane'] = 'Painkiller Jane'
serie['weeds'] = 'Weeds'
serie['house'] = 'House'
serie['kylexy'] = 'Kyle XY'
serie['buffy'] = 'Buffy the Vampire Slayer'
serie['leverage'] = 'Leverage'
serie['trueblood'] = 'True Blood'
serie['alias'] = 'Alias'
serie['traveler'] = 'Traveler'
serie['johnfromcincinnati'] = 'John from Cincinnati'
serie['reaper'] = 'Reaper'
serie['the4400'] = 'The 4400'
serie['lietome'] = 'Lie to Me'
serie['thekillpoint'] = 'Kill Point'
serie['mastersofscifi'] = 'Masters of Science Fiction'
serie['veronicamars'] = 'Veronica Mars'
serie['ncis'] = 'Ncis'
serie['skins'] = 'Skins'
serie['thepretender'] = 'The Pretender'
serie['sonsofanarchy'] = 'Sons of Anarchy'
serie['medium'] = 'Medium'
serie['betteroffted'] = 'Better Off Ted'
serie['legendoftheseeker'] = 'Legend of the Seeker'
serie['stargatesg1'] = 'Stargate SG-1'
serie['scrubs'] = 'Scrubs'
serie['flashpoint'] = 'Flashpoint'
serie['greek'] = 'Greek'
serie['uglybetty'] = 'Ugly Betty'
serie['thenine'] = 'The Nine'
serie['charmed'] = 'Charmed'
serie['life'] = 'Life'
serie['criminalminds'] = 'Criminal Minds'
serie['demons'] = 'Demons'
serie['thesopranos'] = 'The Sopranos'
serie['smallville'] = 'Smallville'
serie['bloodties'] = 'Blood Ties'
serie['thebigbangtheory'] = 'The Big Bang Theory'
serie['privatepractice'] = 'Private Practice'
serie['melroseplace'] = 'Melrose Place'
serie['garyunmarried'] = 'Gary Unmarried'
serie['lost'] = 'Lost'
serie['stargateuniverse'] = 'Stargate Universe'
serie['90210'] = '90210'
serie['stargateatlantis'] = 'Stargate Atlantis'
serie['xfiles'] = 'X-Files'
serie['raines'] = 'Raines'
serie['merlin'] = 'Merlin'
serie['fridaynightlights'] = 'Friday Night Lights'
serie['thetudors'] = 'The Tudors'
serie['dirt'] = 'Dirt'







for s in serie.items():


    cur = conn.cursor()
    cur.execute("UPDATE recommandation_series s SET real_name = '{}' WHERE name = '{}'".format(s[1], s[0]))







conn.commit()