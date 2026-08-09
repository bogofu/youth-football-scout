#!/usr/bin/env python3
"""生成 50000+ 青年球员数据库 — 紧凑版"""

import json, random, gzip
from datetime import datetime, timezone, timedelta

BEIJING_TZ = timezone(timedelta(hours=8))
random.seed(2026)

# === 全球俱乐部池 (~200+) ===
CLUBS = [
    # England
    ("Arsenal","England","🏴󠁧󠁢󠁥󠁮󠁧󠁿"),("Chelsea","England","🏴󠁧󠁢󠁥󠁮󠁧󠁿"),("Liverpool","England","🏴󠁧󠁢󠁥󠁮󠁧󠁿"),
    ("Man City","England","🏴󠁧󠁢󠁥󠁮󠁧󠁿"),("Man United","England","🏴󠁧󠁢󠁥󠁮󠁧󠁿"),("Tottenham","England","🏴󠁧󠁢󠁥󠁮󠁧󠁿"),
    ("Newcastle","England","🏴󠁧󠁢󠁥󠁮󠁧󠁿"),("Brighton","England","🏴󠁧󠁢󠁥󠁮󠁧󠁿"),("Aston Villa","England","🏴󠁧󠁢󠁥󠁮󠁧󠁿"),
    ("West Ham","England","🏴󠁧󠁢󠁥󠁮󠁧󠁿"),("Everton","England","🏴󠁧󠁢󠁥󠁮󠁧󠁿"),("Crystal Palace","England","🏴󠁧󠁢󠁥󠁮󠁧󠁿"),
    ("Wolves","England","🏴󠁧󠁢󠁥󠁮󠁧󠁿"),("Bournemouth","England","🏴󠁧󠁢󠁥󠁮󠁧󠁿"),("Fulham","England","🏴󠁧󠁢󠁥󠁮󠁧󠁿"),
    ("Brentford","England","🏴󠁧󠁢󠁥󠁮󠁧󠁿"),("Nottingham Forest","England","🏴󠁧󠁢󠁥󠁮󠁧󠁿"),("Leeds","England","🏴󠁧󠁢󠁥󠁮󠁧󠁿"),
    ("Sunderland","England","🏴󠁧󠁢󠁥󠁮󠁧󠁿"),("Leicester","England","🏴󠁧󠁢󠁥󠁮󠁧󠁿"),("Norwich","England","🏴󠁧󠁢󠁥󠁮󠁧󠁿"),
    ("Watford","England","🏴󠁧󠁢󠁥󠁮󠁧󠁿"),("Millwall","England","🏴󠁧󠁢󠁥󠁮󠁧󠁿"),("WBA","England","🏴󠁧󠁢󠁥󠁮󠁧󠁿"),
    ("Stoke City","England","🏴󠁧󠁢󠁥󠁮󠁧󠁿"),("Cardiff","Wales","🏴󠁧󠁢󠁷󠁬󠁳󠁿"),("Middlesbrough","England","🏴󠁧󠁢󠁥󠁮󠁧󠁿"),
    # Spain
    ("Barcelona","Spain","🇪🇸"),("Real Madrid","Spain","🇪🇸"),("Atletico Madrid","Spain","🇪🇸"),
    ("Sevilla","Spain","🇪🇸"),("Real Sociedad","Spain","🇪🇸"),("Villarreal","Spain","🇪🇸"),
    ("Valencia","Spain","🇪🇸"),("Athletic Club","Spain","🇪🇸"),("Real Betis","Spain","🇪🇸"),
    ("Osasuna","Spain","🇪🇸"),("Celta Vigo","Spain","🇪🇸"),("Espanyol","Spain","🇪🇸"),
    ("Getafe","Spain","🇪🇸"),("Girona","Spain","🇪🇸"),("Rayo Vallecano","Spain","🇪🇸"),
    ("Mallorca","Spain","🇪🇸"),("Las Palmas","Spain","🇪🇸"),("Alaves","Spain","🇪🇸"),
    # Germany
    ("Bayern Munich","Germany","🇩🇪"),("Dortmund","Germany","🇩🇪"),("RB Leipzig","Germany","🇩🇪"),
    ("Leverkusen","Germany","🇩🇪"),("Frankfurt","Germany","🇩🇪"),("Stuttgart","Germany","🇩🇪"),
    ("Wolfsburg","Germany","🇩🇪"),("M'gladbach","Germany","🇩🇪"),("Freiburg","Germany","🇩🇪"),
    ("Hoffenheim","Germany","🇩🇪"),("Werder Bremen","Germany","🇩🇪"),("FC Koln","Germany","🇩🇪"),
    ("Augsburg","Germany","🇩🇪"),("Hertha Berlin","Germany","🇩🇪"),("Mainz","Germany","🇩🇪"),
    # Italy
    ("AC Milan","Italy","🇮🇹"),("Inter Milan","Italy","🇮🇹"),("Juventus","Italy","🇮🇹"),
    ("Napoli","Italy","🇮🇹"),("Atalanta","Italy","🇮🇹"),("AS Roma","Italy","🇮🇹"),
    ("Lazio","Italy","🇮🇹"),("Fiorentina","Italy","🇮🇹"),("Torino","Italy","🇮🇹"),
    ("Bologna","Italy","🇮🇹"),("Genoa","Italy","🇮🇹"),("Udinese","Italy","🇮🇹"),
    ("Monza","Italy","🇮🇹"),("Cagliari","Italy","🇮🇹"),("Parma","Italy","🇮🇹"),
    ("Como","Italy","🇮🇹"),("Lecce","Italy","🇮🇹"),("Empoli","Italy","🇮🇹"),
    # France
    ("PSG","France","🇫🇷"),("Lyon","France","🇫🇷"),("Marseille","France","🇫🇷"),
    ("Monaco","France","🇫🇷"),("Lille","France","🇫🇷"),("Rennes","France","🇫🇷"),
    ("Nice","France","🇫🇷"),("Strasbourg","France","🇫🇷"),("Nantes","France","🇫🇷"),
    ("Lens","France","🇫🇷"),("Montpellier","France","🇫🇷"),("Toulouse","France","🇫🇷"),
    ("Brest","France","🇫🇷"),("Reims","France","🇫🇷"),("Auxerre","France","🇫🇷"),
    # Netherlands
    ("Ajax","Netherlands","🇳🇱"),("PSV","Netherlands","🇳🇱"),("Feyenoord","Netherlands","🇳🇱"),
    ("AZ Alkmaar","Netherlands","🇳🇱"),("FC Twente","Netherlands","🇳🇱"),("Utrecht","Netherlands","🇳🇱"),
    # Portugal
    ("Benfica","Portugal","🇵🇹"),("FC Porto","Portugal","🇵🇹"),("Sporting CP","Portugal","🇵🇹"),
    ("Braga","Portugal","🇵🇹"),("Vitoria","Portugal","🇵🇹"),
    # Belgium
    ("KRC Genk","Belgium","🇧🇪"),("Club Brugge","Belgium","🇧🇪"),("Anderlecht","Belgium","🇧🇪"),
    ("Standard Liege","Belgium","🇧🇪"),("Antwerp","Belgium","🇧🇪"),
    # Brazil (16 teams)
    ("Palmeiras","Brazil","🇧🇷"),("Flamengo","Brazil","🇧🇷"),("Corinthians","Brazil","🇧🇷"),
    ("Sao Paulo","Brazil","🇧🇷"),("Santos","Brazil","🇧🇷"),("Fluminense","Brazil","🇧🇷"),
    ("Gremio","Brazil","🇧🇷"),("Atletico-MG","Brazil","🇧🇷"),("Cruzeiro","Brazil","🇧🇷"),
    ("Vasco","Brazil","🇧🇷"),("Botafogo","Brazil","🇧🇷"),("Internacional","Brazil","🇧🇷"),
    ("Bahia","Brazil","🇧🇷"),("Fortaleza","Brazil","🇧🇷"),("Coritiba","Brazil","🇧🇷"),
    ("Athletico-PR","Brazil","🇧🇷"),
    # Argentina (10)
    ("River Plate","Argentina","🇦🇷"),("Boca Juniors","Argentina","🇦🇷"),
    ("Racing","Argentina","🇦🇷"),("Independiente","Argentina","🇦🇷"),
    ("San Lorenzo","Argentina","🇦🇷"),("Velez","Argentina","🇦🇷"),
    ("Estudiantes","Argentina","🇦🇷"),("Newells","Argentina","🇦🇷"),
    ("Talleres","Argentina","🇦🇷"),("Defensa","Argentina","🇦🇷"),
    # South America extra
    ("Penarol","Uruguay","🇺🇾"),("Nacional","Uruguay","🇺🇾"),
    ("Olimpia","Paraguay","🇵🇾"),("Cerro Porteno","Paraguay","🇵🇾"),
    ("Colo-Colo","Chile","🇨🇱"),("U. de Chile","Chile","🇨🇱"),
    ("Barcelona SC","Ecuador","🇪🇨"),("LDU Quito","Ecuador","🇪🇨"),
    ("Millonarios","Colombia","🇨🇴"),("Atl. Nacional","Colombia","🇨🇴"),
    # Eastern Europe
    ("Shakhtar","Ukraine","🇺🇦"),("Dynamo Kyiv","Ukraine","🇺🇦"),
    ("D. Zagreb","Croatia","🇭🇷"),("Hajduk","Croatia","🇭🇷"),
    ("Crvena Zvezda","Serbia","🇷🇸"),("Partizan","Serbia","🇷🇸"),
    ("Sparta Praha","Czechia","🇨🇿"),("Slavia Praha","Czechia","🇨🇿"),
    ("RB Salzburg","Austria","🇦🇹"),("Sturm Graz","Austria","🇦🇹"),
    ("Legia","Poland","🇵🇱"),("Lech Poznan","Poland","🇵🇱"),
    # Turkey & Greece
    ("Galatasaray","Turkey","🇹🇷"),("Fenerbahce","Turkey","🇹🇷"),("Besiktas","Turkey","🇹🇷"),
    ("Olympiacos","Greece","🇬🇷"),("Panathinaikos","Greece","🇬🇷"),("AEK Athens","Greece","🇬🇷"),
    # Scotland
    ("Celtic","Scotland","🏴󠁧󠁢󠁳󠁣󠁴󠁿"),("Rangers","Scotland","🏴󠁧󠁢󠁳󠁣󠁴󠁿"),
    # Nordics
    ("FC Copenhagen","Denmark","🇩🇰"),("Midtjylland","Denmark","🇩🇰"),
    ("Malmo FF","Sweden","🇸🇪"),("Djurgarden","Sweden","🇸🇪"),
    ("Bodo/Glimt","Norway","🇳🇴"),("Rosenborg","Norway","🇳🇴"),
    # Switzerland
    ("Young Boys","Switzerland","🇨🇭"),("FC Basel","Switzerland","🇨🇭"),
    # Asia
    ("Urawa Reds","Japan","🇯🇵"),("Kawasaki F.","Japan","🇯🇵"),("Yokohama FM","Japan","🇯🇵"),
    ("FC Seoul","Korea Republic","🇰🇷"),("Jeonbuk","Korea Republic","🇰🇷"),("Pohang","Korea Republic","🇰🇷"),
    ("Ulsan HD","Korea Republic","🇰🇷"),("Gwangju FC","Korea Republic","🇰🇷"),
    ("Shanghai Port","China PR","🇨🇳"),("Beijing Guoan","China PR","🇨🇳"),
    ("Al-Hilal","Saudi Arabia","🇸🇦"),("Al-Nassr","Saudi Arabia","🇸🇦"),
    # North America
    ("LA Galaxy","USA","🇺🇸"),("Inter Miami","USA","🇺🇸"),
    ("Philadelphia","USA","🇺🇸"),("Atlanta Utd","USA","🇺🇸"),
    ("Club America","Mexico","🇲🇽"),("Chivas","Mexico","🇲🇽"),
    ("Monterrey","Mexico","🇲🇽"),("Tijuana","Mexico","🇲🇽"),
    # Africa
    ("Al Ahly","Egypt","🇪🇬"),("Zamalek","Egypt","🇪🇬"),
    ("Esperance","Tunisia","🇹🇳"),("Wydad","Morocco","🇲🇦"),
    ("Orlando Pirates","South Africa","🇿🇦"),("Sundowns","South Africa","🇿🇦"),
    # Other notable
    ("AEK Larnaca","Cyprus","🇨🇾"),("Ludogorets","Bulgaria","🇧🇬"),
    ("Ferencvaros","Hungary","🇭🇺"),("Slovan Bratislava","Slovakia","🇸🇰"),
]

# === 各国球员姓名池 ===
NAMES_BY_REGION = {
    "England": (["James","Oliver","Harry","Jack","George","Thomas","Charlie","William","Henry","Alfie","Leo","Oscar","Max","Archie","Freddie","Finley","Noah","Jacob","Ethan","Lucas","Mason","Logan","Alex","Theo","Toby","Ryan","Callum","Nathan","Liam","Joe"],
                ["Smith","Jones","Taylor","Brown","Wilson","Davies","Evans","Thomas","Roberts","Walker","Wright","Robinson","Thompson","White","Hughes","Edwards","Green","Hall","Wood","Harris"]),
    "Spain": (["Pablo","Alejandro","Carlos","Daniel","Hugo","David","Adrian","Javier","Marcos","Alvaro","Sergio","Miguel","Iker","Raul","Mario","Diego","Antonio","Juan","Francisco","Manuel"],
              ["Garcia","Fernandez","Lopez","Martinez","Gonzalez","Rodriguez","Sanchez","Perez","Gomez","Martin","Jimenez","Ruiz","Hernandez","Diaz","Moreno","Alvarez","Romero","Navarro","Torres","Ramos"]),
    "Germany": (["Leon","Luca","Maximilian","Paul","Felix","Noah","Elias","Jonas","Tim","Finn","Ben","Luis","Anton","Emil","Henry","Jakob","Moritz","Niklas","Philipp","Tom"],
                ["Muller","Schmidt","Schneider","Fischer","Weber","Wagner","Becker","Hoffmann","Schulz","Koch","Richter","Bauer","Wolf","Klein","Schroder","Neumann","Schwarz","Zimmermann","Braun","Kruger"]),
    "Italy": (["Lorenzo","Francesco","Andrea","Alessandro","Matteo","Riccardo","Federico","Leonardo","Gabriele","Tommaso","Edoardo","Nicolo","Davide","Marco","Giovanni","Simone","Luca","Pietro","Filippo","Samuele"],
              ["Rossi","Russo","Ferrari","Esposito","Bianchi","Romano","Colombo","Ricci","Marino","Greco","Bruno","Gallo","Conti","Costa","Mancini","Barbieri","Fontana","Rinaldi","Caruso","Moretti"]),
    "France": (["Lucas","Hugo","Louis","Gabriel","Jules","Leo","Arthur","Nathan","Raphael","Adam","Clement","Ethan","Mathis","Enzo","Theo","Sacha","Antoine","Pierre","Remy","Maxime"],
               ["Martin","Bernard","Dubois","Thomas","Robert","Richard","Petit","Durand","Leroy","Moreau","Simon","Laurent","Lefevre","Michel","Garcia","David","Bertrand","Roux","Vincent","Fournier"]),
    "Brazil": (["Lucas","Gabriel","Pedro","Joao","Felipe","Gustavo","Matheus","Rafael","Bruno","Marcos","Vinicius","Caio","Thiago","Eduardo","Arthur","Henrique","Victor","Guilherme","Leonardo","Luiz"],
               ["Silva","Santos","Oliveira","Souza","Lima","Pereira","Costa","Ferreira","Rodrigues","Almeida","Nascimento","Araujo","Ribeiro","Carvalho","Gomes","Martins","Barbosa","Correia","Fernandes","Dias"]),
    "Argentina": (["Mateo","Valentin","Benjamin","Joaquin","Santiago","Nicolas","Tomas","Thiago","Lautaro","Franco","Ignacio","Facundo","Agustin","Juan","Lucas","Matias","Federico","Gonzalo","Emiliano","Leonel"],
                  ["Garcia","Rodriguez","Gonzalez","Fernandez","Lopez","Martinez","Perez","Sanchez","Diaz","Torres","Ramirez","Flores","Acosta","Alvarez","Romero","Ruiz","Gutierrez","Sosa","Ponce","Castro"]),
    "Netherlands": (["Daan","Sem","Lucas","Levi","Finn","Milan","Jesse","Noah","Thomas","Max","Luuk","Tim","Lars","Ruben","Bram","Thijs","Syb","Jasper","Niels","Koen"],
                    ["de Jong","Jansen","de Vries","van Dijk","Bakker","Visser","Smit","Dekker","van Leeuwen","Brouwer","Kok","van Dam","Meijer","Prins","Koning","Post","Bos","Veenstra","Jonker","Mulder"]),
    "Portugal": (["Joao","Rodrigo","Diogo","Tiago","Goncalo","Rafael","Andre","Pedro","Rui","Nuno","Francisco","Miguel","Tomas","Filipe","Daniel","David","Jose","Ricardo","Vasco","Hugo"],
                 ["Silva","Santos","Oliveira","Pereira","Costa","Fernandes","Rodrigues","Lima","Gomes","Martins","Almeida","Ribeiro","Carvalho","Ferreira","Goncalves","Barbosa","Nunes","Correia","Marques","Lopes"]),
    "Japan": (["Ren","Haruto","Yuto","Sota","Daiki","Riku","Kaito","Takumi","Hiroto","Sho","Yuki","Ryusei","Hayate","Koki","Taiga","Sosuke","Keita","Shota","Tsubasa","Yuma"],
              ["Sato","Suzuki","Takahashi","Tanaka","Watanabe","Ito","Yamamoto","Nakamura","Kobayashi","Kato","Yoshida","Yamada","Sasaki","Yamaguchi","Matsumoto","Inoue","Kimura","Hayashi","Shimizu","Ogawa"]),
    "Korea Republic": (["Min-jun","Seo-jun","Ji-ho","Tae-hyun","Woo-jin","Hyun-woo","Dong-hyun","Seung-woo","Jae-min","Young-jae","Sung-min","Joon-ho","Kwang-soo","Hyuk","Jin-woo","Sang-woo","Do-yun","Yong-sik","Byung-ho","Chul-soo"],
                        ["Kim","Lee","Park","Choi","Jung","Kang","Cho","Yoon","Jang","Lim","Han","Oh","Shin","Seo","Kwon","Hwang","Ahn","Song","Jeon","Hong"]),
    "Mexico": (["Santiago","Emiliano","Mateo","Sebastian","Diego","Luis","Angel","Jose","Carlos","Jesus","Miguel","Alejandro","Eduardo","Ricardo","Fernando","Oscar","Javier","Antonio","Rafael","Andres"],
               ["Hernandez","Garcia","Lopez","Martinez","Gonzalez","Rodriguez","Perez","Sanchez","Ramirez","Flores","Cruz","Ortiz","Morales","Reyes","Gutierrez","Jimenez","Ruiz","Vazquez","Castillo","Mendoza"]),
    "USA": (["Liam","Noah","James","Ethan","Mason","Lucas","Benjamin","Jack","Henry","Alexander","Owen","Gabriel","Wyatt","Carter","Julian","Luke","Grayson","Levi","Isaac","Jayden"],
             ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Martinez","Anderson","Taylor","Thomas","Moore","Jackson","Martin","Lee","Thompson","White","Harris","Clark"]),
}

# Global mix for smaller nations
GLOBAL_FIRST = ["Lucas","Marco","Daniel","Nico","Hugo","Diego","Tiago","Matteo","David","Pablo","Rafael","Gabriel","Samuel","Thomas","Oliver","Leo","Oscar","Enzo","Liam","Noah","Adam","Felix","Emil","Victor","Max","Erik","Axel","Kai","Ezra","Malik","Zayn","Karim","Omar","Rayan"]
GLOBAL_LAST = ["Silva","Santos","Garcia","Muller","Rossi","Kim","Park","Lee","Sato","Tanaka","Kowalski","Nowak","Hernandez","Andersson","Johansson","Nielsen","Hansen","Okafor","Traore","Diallo","Coulibaly","Keita","Mensah","Eze"]

NATIONALITIES = [
    ("England","🏴󠁧󠁢󠁥󠁮󠁧󠁿"),("Spain","🇪🇸"),("France","🇫🇷"),("Germany","🇩🇪"),("Italy","🇮🇹"),
    ("Netherlands","🇳🇱"),("Portugal","🇵🇹"),("Brazil","🇧🇷"),("Argentina","🇦🇷"),("Belgium","🇧🇪"),
    ("Croatia","🇭🇷"),("Serbia","🇷🇸"),("Denmark","🇩🇰"),("Sweden","🇸🇪"),("Norway","🇳🇴"),
    ("Poland","🇵🇱"),("Czechia","🇨🇿"),("Austria","🇦🇹"),("Switzerland","🇨🇭"),("Turkey","🇹🇷"),
    ("Ukraine","🇺🇦"),("Greece","🇬🇷"),("Scotland","🏴󠁧󠁢󠁳󠁣󠁴󠁿"),("Ireland","🇮🇪"),("Wales","🏴󠁧󠁢󠁷󠁬󠁳󠁿"),
    ("Uruguay","🇺🇾"),("Colombia","🇨🇴"),("Ecuador","🇪🇨"),("Chile","🇨🇱"),("Paraguay","🇵🇾"),
    ("Mexico","🇲🇽"),("USA","🇺🇸"),("Canada","🇨🇦"),("Japan","🇯🇵"),("Korea Republic","🇰🇷"),
    ("Nigeria","🇳🇬"),("Ghana","🇬🇭"),("Senegal","🇸🇳"),("Cote d'Ivoire","🇨🇮"),("Cameroon","🇨🇲"),
    ("Morocco","🇲🇦"),("Algeria","🇩🇿"),("Egypt","🇪🇬"),("Tunisia","🇹🇳"),("South Africa","🇿🇦"),
    ("Australia","🇦🇺"),("China PR","🇨🇳"),("Iran","🇮🇷"),("Saudi Arabia","🇸🇦"),("Qatar","🇶🇦"),
    ("Peru","🇵🇪"),("Venezuela","🇻🇪"),("Bolivia","🇧🇴"),("Costa Rica","🇨🇷"),("Panama","🇵🇦"),
    ("Slovakia","🇸🇰"),("Slovenia","🇸🇮"),("Hungary","🇭🇺"),("Romania","🇷🇴"),("Bulgaria","🇧🇬"),
]

POSITIONS = ["ST","LW","RW","CAM","CM","CDM","CB","LB","RB","GK"]
FOOTS = ["Right","Left","Both"]

# Scout report text templates (compact)
SCOUT_TEXT = {
    "ST": {"t":"射术精湛，终结能力顶级","p":"爆发力出色，对抗能力强","c":"跑位聪明，射手天赋","i":"关键时刻改变比赛","u":"世界级中锋潜能"},
    "LW": {"t":"盘带技术出色，内切威胁大","p":"速度快，灵活性好","c":"边路空间利用出色","i":"边路持续制造威胁","u":"顶级边锋潜质"},
    "RW": {"t":"盘带出色，传中精准","p":"加速快，灵活敏捷","c":"边路战术理解到位","i":"进攻端关键输出","u":"顶级边锋前景"},
    "CAM": {"t":"传球精准，创造力出众","p":"灵巧，重心低","c":"善于两线间接球","i":"创造机会改变比赛","u":"世界级前腰潜能"},
    "CM": {"t":"传球高效，双足均衡","p":"体能充沛，覆盖大","c":"战术执行强，攻防兼备","i":"中场节拍器","u":"全能中场前景"},
    "CDM": {"t":"拦截精准，控球冷静","p":"身体强壮，对抗顶级","c":"防守位置感极佳","i":"后防屏障","u":"防守核心潜质"},
    "CB": {"t":"出球好，脚下技术扎实","p":"制空强，对抗出色","c":"防守预判顶级","i":"后防定海神针","u":"后防领袖前景"},
    "LB": {"t":"传中精准，控球好","p":"速度快，耐力强","c":"攻防转换意识好","i":"边路稳定输出","u":"顶级边卫潜质"},
    "RB": {"t":"传中好，推进有力","p":"速度快，体能好","c":"攻防平衡把握好","i":"边路攻防兼备","u":"顶级右后卫前景"},
    "GK": {"t":"扑救技术扎实","p":"身高优势，反应快","c":"指挥防线能力强","i":"关键扑救改变比赛","u":"顶级门将潜质"},
}

def get_name(nat):
    if nat in NAMES_BY_REGION:
        fns, lns = NAMES_BY_REGION[nat]
        return random.choice(fns), random.choice(lns)
    return random.choice(GLOBAL_FIRST), random.choice(GLOBAL_LAST)

def generate():
    print("Generating 50000+ players...")
    players = []
    used_ids = set()

    for i in range(50000):
        club, club_nat, club_flag = random.choice(CLUBS)
        nat, flag = random.choice(NATIONALITIES)
        pos = random.choice(POSITIONS)
        age = random.choices([16,17,18,19,20,21], weights=[8,12,18,22,22,18])[0]

        fn, ln = get_name(nat)
        pid = f"{fn.lower()}-{ln.lower()}-{i}"
        if pid in used_ids:
            pid = f"{pid}-{random.randint(1,99)}"
        used_ids.add(pid)

        birth_year = 2026 - age
        birth = f"{birth_year}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
        ht = random.randint(165, 198) if pos in ["GK","CB"] else random.randint(168, 192)
        foot = random.choice(FOOTS)

        # Stats based on position and age
        is_att = pos in ["ST","LW","RW","CAM"]
        apps = random.randint(2, 40) if age >= 18 else random.randint(0, 20)
        g = random.randint(0, 18) if is_att else random.randint(0, 6)
        a = random.randint(0, 15) if is_att else random.randint(0, 8)
        xg = round(random.uniform(0.05, 0.70), 2) if is_att else round(random.uniform(0.01, 0.20), 2)
        rating = round(random.uniform(6.0, 7.8), 2)
        mv = random.randint(10000, 150000000) if rating > 7.0 else random.randint(5000, 30000000)

        # Scout scores (correlated with overall quality)
        base = random.gauss(6.5, 1.5)
        base = max(4.0, min(9.8, base))
        scout = SCOUT_TEXT.get(pos, SCOUT_TEXT["CM"])
        report = {
            "t": {"s": round(max(4,min(10, base + random.uniform(-0.5,0.8))), 1), "d": scout["t"]},
            "p": {"s": round(max(4,min(10, base + random.uniform(-0.8,0.5))), 1), "d": scout["p"]},
            "c": {"s": round(max(4,min(10, base + random.uniform(-0.5,0.5))), 1), "d": scout["c"]},
            "i": {"s": round(max(4,min(10, base + random.uniform(-0.3,0.8))), 1), "d": scout["i"]},
            "u": {"s": round(max(4,min(10, base + random.uniform(-0.2,1.2))), 1), "d": scout["u"]},
        }

        overall = round(sum(r["s"] for r in report.values()) / 5, 1)

        players.append({
            "n": f"{fn} {ln}",
            "a": age,
            "f": flag,
            "c": club,
            "p": pos,
            "h": ht,
            "ft": foot[0],
            "s": [apps, g, a],
            "r": [round(xg,2), rating],
            "v": mv,
            "sc": report,
            "o": overall,
        })

        if (i+1) % 10000 == 0:
            print(f"  {i+1}/50000...")

    # Sort by overall rating descending
    players.sort(key=lambda p: p["o"], reverse=True)

    data = {
        "lu": datetime.now(BEIJING_TZ).strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "t": len(players),
        "pl": players,
    }

    # Save JSON
    path = "players_data.json"
    print(f"Saving {len(players)} players...")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

    # Also save gzipped for reference
    with gzip.open(path + ".gz", "wt", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

    import os
    size = os.path.getsize(path)
    gz_size = os.path.getsize(path + ".gz")
    print(f"Done: {size/1024/1024:.1f}MB (gzip: {gz_size/1024/1024:.1f}MB)")
    print(f"Top 5: {[(p['n'], p['o']) for p in players[:5]]}")

if __name__ == "__main__":
    generate()
