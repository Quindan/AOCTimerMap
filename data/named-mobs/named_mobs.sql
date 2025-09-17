-- Named Mobs Data from Ashes Codex
-- Generated on: 2025-09-04 21:10:03

CREATE TABLE IF NOT EXISTS named_mobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    slug TEXT,
    level INTEGER,
    level_range TEXT,
    respawn_time TEXT,
    respawn_minutes INTEGER,
    codex_url TEXT,
    location_x REAL,
    location_y REAL,
    location_z REAL,
    type TEXT DEFAULT 'named_mob',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Administrator Crucia',
    'administrator-crucia',
    28,
    '28',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/administrator-crucia',
    -1260249.5409428,
    539619.06227983,
    12073.402559484
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Ahm''dar',
    'ahm''dar',
    25,
    '25',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/ahm''dar',
    -316843.41644051,
    847766.97943309,
    6349.6441352895
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Alecog, Eternal Guardian',
    'alecog-eternal-guardian',
    21,
    '21',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/alecog-eternal-guardian',
    -942723.38674811,
    433437.59535545,
    12299.904372181
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Alfaa Woof',
    'alfaa-woof',
    15,
    '15',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/alfaa-woof',
    -560349.87898926,
    646059.03741218,
    15576.68715638
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Alloyed Laborer',
    'alloyed-laborer',
    29,
    '29',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/alloyed-laborer',
    -1241600.0973913,
    565154.94514265,
    11043.815220496
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Arbiss, Broodmother',
    'arbiss-broodmother',
    23,
    '23',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/arbiss-broodmother',
    -934072.22843032,
    432913.98576081,
    12207.215661342
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Aria the Flamebearer',
    'aria-the-flamebearer',
    25,
    '25',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/aria-the-flamebearer',
    -1691416.4018103,
    380483.8959952,
    4172.999814911
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Arzach',
    'arzach',
    22,
    '22',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/arzach',
    NULL,
    NULL,
    NULL
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Ashcoil, the Stonebound',
    'ashcoil-the-stonebound',
    17,
    '17',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/ashcoil-the-stonebound',
    -1095377.2431476,
    -277235.83722947,
    15708.861062681
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Ashearis the Windlord',
    'ashearis-the-windlord',
    25,
    '25',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/ashearis-the-windlord',
    NULL,
    NULL,
    NULL
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Awful Stench',
    'awful-stench',
    11,
    '11',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/awful-stench',
    -1167047.1398274,
    -493490.38036933,
    10760.712840331
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Banished Seeker Hammond',
    'banished-seeker-hammond',
    20,
    '20',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/banished-seeker-hammond',
    -951299.47749479,
    773025.51631185,
    12289.891727052
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Barnacle Brenn',
    'barnacle-brenn',
    26,
    '26',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/barnacle-brenn',
    -1857323.3322297,
    720263.74243323,
    5355.1485948377
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Baron Baneswood',
    'baron-baneswood',
    9,
    '9',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/baron-baneswood',
    -643908.47948091,
    638455.78697819,
    16874.783718111
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Bartok the Heartless',
    'bartok-the-heartless',
    15,
    '15',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/bartok-the-heartless',
    -455000.6684533,
    734272.29179145,
    12595.375540744
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Bellowsmasher',
    'bellowsmasher',
    26,
    '26',
    '1800 seconds',
    30,
    'https://ashescodex.com/mobs/bellowsmasher',
    -1266229.7248987,
    580799.07741732,
    10990.715316504
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Beta Hauler C3-82',
    'beta-hauler-c3-82',
    7,
    '7',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/beta-hauler-c3-82',
    -1047551.5085001,
    -605841.86723075,
    18200.203249674
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Big Brother',
    'big-brother',
    20,
    '20',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/big-brother',
    -787603.81887505,
    436484.62743513,
    13412.007224449
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Bind-Master Hakoa',
    'bind-master-hakoa',
    30,
    '30',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/bind-master-hakoa',
    -1335475.3029934,
    1023146.7316034,
    7256.4646715955
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Bizhbug the Defiler',
    'bizhbug-the-defiler',
    6,
    '6',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/bizhbug-the-defiler',
    -772042.94091269,
    599688.18232754,
    17059.098874625
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Blister',
    'blister',
    15,
    '15',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/blister',
    -619013.23428322,
    473324.8687847,
    14133.936666767
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Blisterpyre',
    'blisterpyre',
    10,
    '10',
    '3570 - 3630 seconds',
    60.5,
    'https://ashescodex.com/mobs/blisterpyre',
    -819697.14409177,
    -644621.26957814,
    17355.333030901
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Bloodmage Triune',
    'bloodmage-triune',
    19,
    '19',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/bloodmage-triune',
    -934803.91092196,
    773921.3543755,
    14951.953435729
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Bloomthorn',
    'bloomthorn',
    28,
    '28 - 31',
    '180 seconds',
    3,
    'https://ashescodex.com/mobs/bloomthorn',
    -1071716.460134,
    1178797.7390172,
    11179.279694236
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Bluequill',
    'bluequill',
    8,
    '8',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/bluequill',
    -823085.54829478,
    595411.79777318,
    19799.219902367
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Bonebinder Outhouser',
    'bonebinder-outhouser',
    12,
    '12',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/bonebinder-outhouser',
    -1055988.7544204,
    633763.39308445,
    12012.667559838
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Boog',
    'boog',
    14,
    '14',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/boog',
    -972242.835954,
    539119.5979448,
    21512.968420218
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Boss NakNak',
    'boss-naknak',
    15,
    '15',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/boss-naknak',
    -975832.03876762,
    544584.77054734,
    21496.000014413
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Brightmound',
    'brightmound',
    16,
    '16',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/brightmound',
    -1488632.1682186,
    -3999.3209318315,
    4725.7070957586
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Brinebeard',
    'brinebeard',
    25,
    '25',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/brinebeard',
    -1858230.687473,
    716532.24129611,
    5374.4194598763
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Byer, The Last Sentinel',
    'byer-the-last-sentinel',
    27,
    '27',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/byer-the-last-sentinel',
    -965201.86197647,
    758601.63046533,
    14166.402212447
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Cairn',
    'cairn',
    31,
    '31',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/cairn',
    -787718.83521833,
    223218.520444,
    34388.984362909
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Calcitooth',
    'calcitooth',
    7,
    '7',
    '870 - 930 seconds',
    15.5,
    'https://ashescodex.com/mobs/calcitooth',
    -913325.62205566,
    -607273.78746653,
    13395.117854043
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Cap''n Knuckles',
    'cap''n-knuckles',
    15,
    '15',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/cap''n-knuckles',
    -631596.69680616,
    466070.18029924,
    12390.591020834
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Captain Bulwark',
    'captain-bulwark',
    28,
    '28',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/captain-bulwark',
    -1720327.4373754,
    -135340.69339645,
    8004.4424861702
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Captain Tharsus',
    'captain-tharsus',
    28,
    '28',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/captain-tharsus',
    NULL,
    NULL,
    NULL
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Chaplain Marion',
    'chaplain-marion',
    21,
    '21',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/chaplain-marion',
    -778777.352894,
    450985.086776,
    32142.945812412
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Chief Armorer Jannus',
    'chief-armorer-jannus',
    21,
    '21',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/chief-armorer-jannus',
    -778816.712894,
    450986.146776,
    32142.940985382
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Chief of Operations',
    'chief-of-operations',
    11,
    '11',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/chief-of-operations',
    -1162644.518455,
    -501328.68001742,
    12950.947304797
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Cindermirk, the Slagborn',
    'cindermirk-the-slagborn',
    7,
    '7',
    '870 - 930 seconds',
    15.5,
    'https://ashescodex.com/mobs/cindermirk-the-slagborn',
    -902124.93095013,
    -610748.24811854,
    11631.977635985
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Clawhold the Crag-Shelled',
    'clawhold-the-crag-shelled',
    7,
    '7',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/clawhold-the-crag-shelled',
    -1213040.5990826,
    -639413.35730113,
    15479.320227897
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Coalgrim the Fire-Fettered',
    'coalgrim-the-fire-fettered',
    10,
    '10',
    '3570 - 3630 seconds',
    60.5,
    'https://ashescodex.com/mobs/coalgrim-the-fire-fettered',
    -815647.89510584,
    -663730.89920814,
    17435.382367433
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Cognocker Eddis',
    'cognocker-eddis',
    17,
    '17 - 18',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/cognocker-eddis',
    -1479817.2196848,
    141836.55647646,
    12955.442521647
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Coral Colossus',
    'coral-colossus',
    25,
    '25',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/coral-colossus',
    -1698643.2754149,
    373446.25781713,
    5718.6205064767
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Corax',
    'corax',
    29,
    '29',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/corax',
    -837465.87790262,
    217363.89387566,
    34611.001920798
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Corvus',
    'corvus',
    28,
    '28',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/corvus',
    -823012.48635161,
    212906.78601355,
    33727.335964732
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Crunch Trunk',
    'crunch-trunk',
    24,
    '24',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/crunch-trunk',
    -474004.87098948,
    423771.33648993,
    12697.480436368
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Cursed Cuisinier',
    'cursed-cuisinier',
    27,
    '27',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/cursed-cuisinier',
    -518607.4731809,
    446567.28983755,
    30708.452411358
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Cursefang',
    'cursefang',
    18,
    '18',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/cursefang',
    -942330.67335375,
    746094.30840685,
    12414.402185018
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Deadman''s Armor',
    'deadman''s-armor',
    16,
    '16',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/deadman''s-armor',
    -1492450.2829278,
    -7663.1627638476,
    4620.923639511
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Demagogue Mosseus',
    'demagogue-mosseus',
    21,
    '21',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/demagogue-mosseus',
    -958468.27707313,
    753728.82043464,
    13466.380701911
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Djinnbound Golem',
    'djinnbound-golem',
    13,
    '13',
    '120 seconds',
    2,
    'https://ashescodex.com/mobs/djinnbound-golem',
    NULL,
    NULL,
    NULL
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Dom, Champion of Gom',
    'dom-champion-of-gom',
    31,
    '31',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/dom-champion-of-gom',
    -148412.46257048,
    1101714.3955019,
    5170.76015071
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Doomed Researcher',
    'doomed-researcher',
    16,
    '16',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/doomed-researcher',
    -593894.64862386,
    433760.06089866,
    14776.002368098
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Drooling Drawer',
    'drooling-drawer',
    25,
    '25',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/drooling-drawer',
    -517807.55665307,
    453205.18133436,
    21984.054692554
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Echo of Atrax',
    'echo-of-atrax',
    33,
    '33',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/echo-of-atrax',
    -778969.12488468,
    1370840.0138077,
    8774.576571982
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Echoplate, Last of the Line',
    'echoplate-last-of-the-line',
    14,
    '14',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/echoplate-last-of-the-line',
    -985843.2116392,
    -329710.90639784,
    3314.6910789943
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Elara of Duskenshade',
    'elara-of-duskenshade',
    10,
    '10',
    '3570 - 3630 seconds',
    60.5,
    'https://ashescodex.com/mobs/elara-of-duskenshade',
    -990354.71553397,
    -491428.06180545,
    11406.470338713
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Entangled Horticulturalist',
    'entangled-horticulturalist',
    31,
    '31',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/entangled-horticulturalist',
    -843042.68803486,
    1281339.3006486,
    8385.0617946511
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Eternal Sweeper',
    'eternal-sweeper',
    23,
    '23',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/eternal-sweeper',
    -483306.75189646,
    424841.53777056,
    16250.914572725
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Everlasting Sower',
    'everlasting-sower',
    13,
    '13',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/everlasting-sower',
    -1076249.7937277,
    645157.97536393,
    13223.569035585
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Eye of Amathar',
    'eye-of-amathar',
    30,
    '30',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/eye-of-amathar',
    -1667299.8720546,
    240961.6749777,
    4452.2569393776
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Failed Fleshsummon',
    'failed-fleshsummon',
    25,
    '25',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/failed-fleshsummon',
    -966037.2661413,
    758673.33463111,
    18860.380742047
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Fang',
    'fang',
    5,
    '5',
    '240 - 360 seconds',
    6,
    'https://ashescodex.com/mobs/fang',
    -687887.83969459,
    606651.38586576,
    14151.515427683
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Farajah''s Laborer',
    'farajah''s-laborer',
    27,
    '27',
    '5340 - 5400 seconds',
    90,
    'https://ashescodex.com/mobs/farajah''s-laborer',
    NULL,
    NULL,
    NULL
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Financier Carrig',
    'financier-carrig',
    21,
    '21',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/financier-carrig',
    -458113.1145314,
    447823.29271541,
    15284.477550798
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Flesh of the Forsaken',
    'flesh-of-the-forsaken',
    29,
    '29 - 30',
    '150 seconds',
    2.5,
    'https://ashescodex.com/mobs/flesh-of-the-forsaken',
    -84909.433403856,
    815398.00122006,
    9156.7112788022
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Forgeguard Lassix',
    'forgeguard-lassix',
    28,
    '28',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/forgeguard-lassix',
    -1256014.0853293,
    546051.2931621,
    8332.4590508035
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Forgelord Zammer',
    'forgelord-zammer',
    25,
    '25 - 29',
    '120 - 180 seconds',
    3,
    'https://ashescodex.com/mobs/forgelord-zammer',
    -1247660.5081779,
    557592.09851912,
    5309.815175151
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Forgewright Striger',
    'forgewright-striger',
    29,
    '29',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/forgewright-striger',
    -1251756.3312528,
    555807.25796263,
    8209.8151484235
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Forsaken Blades Sergeant',
    'forsaken-blades-sergeant',
    18,
    '15 - 22',
    '180 seconds',
    3,
    'https://ashescodex.com/mobs/forsaken-blades-sergeant',
    -779396.40954382,
    451983.69836514,
    14302.855941941
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Fynn, Scout Master',
    'fynn-scout-master',
    21,
    '21',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/fynn-scout-master',
    -778830.85768065,
    450957.6550763,
    32144.7256727
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'G''Lympes',
    'g''lympes',
    23,
    '23',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/g''lympes',
    -504896.80731088,
    423247.2413612,
    15575.11349697
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Garumart',
    'garumart',
    16,
    '16',
    '3300 - 3900 seconds',
    65,
    'https://ashescodex.com/mobs/garumart',
    NULL,
    NULL,
    NULL
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Gnashgut of Hearthsong',
    'gnashgut-of-hearthsong',
    7,
    '7',
    '540 - 660 seconds',
    11,
    'https://ashescodex.com/mobs/gnashgut-of-hearthsong',
    -725566.49626597,
    502565.56406451,
    22984.415500468
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Golbo Skinstrip',
    'golbo-skinstrip',
    23,
    '23',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/golbo-skinstrip',
    -951858.24525814,
    429179.66392094,
    12251.886607049
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Grathmar, Horn of the First Brand',
    'grathmar-horn-of-the-first-brand',
    20,
    '20',
    '3570 - 3630 seconds',
    60.5,
    'https://ashescodex.com/mobs/grathmar-horn-of-the-first-brand',
    -1349333.534759,
    -255835.81507819,
    15169.242842489
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Grinbar Skulkspite',
    'grinbar-skulkspite',
    16,
    '16',
    '3570 - 3630 seconds',
    60.5,
    'https://ashescodex.com/mobs/grinbar-skulkspite',
    -1371671.1270943,
    -387550.62247908,
    17552.503657384
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Grizzler',
    'grizzler',
    25,
    '25',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/grizzler',
    -811533.44583442,
    217393.77846506,
    25652.789830439
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Growler',
    'growler',
    14,
    '13 - 14',
    '1500 - 2100 seconds',
    35,
    'https://ashescodex.com/mobs/growler',
    -628042.25773474,
    476241.25908419,
    13182.99728402
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Hierophant Amari',
    'hierophant-amari',
    25,
    '25',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/hierophant-amari',
    -949585.90812553,
    751520.67247964,
    12956.380723476
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Hoarder',
    'hoarder',
    8,
    '5 - 30',
    '600 seconds',
    10,
    'https://ashescodex.com/mobs/hoarder',
    -814340.87530924,
    -664310.81823323,
    17375.382358876
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Hoist',
    'hoist',
    21,
    '21',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/hoist',
    -487677.72226716,
    474082.64105949,
    14230.00043332
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Honored Sacrifice',
    'honored-sacrifice',
    15,
    '15',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/honored-sacrifice',
    -454565.99290841,
    728501.64757765,
    13515.375549267
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Hoodwinx',
    'hoodwinx',
    16,
    '15 - 16',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/hoodwinx',
    -554689.83772617,
    470377.56628798,
    17513.988035193
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Ironhide Basilisk',
    'ironhide-basilisk',
    31,
    '31',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/ironhide-basilisk',
    -1575454.5256517,
    1063734.7359545,
    23053.015812511
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Jade Scorpion Crew',
    'jade-scorpion-crew',
    28,
    '28',
    '30 seconds',
    0.5,
    'https://ashescodex.com/mobs/jade-scorpion-crew',
    NULL,
    NULL,
    NULL
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Jade Scorpion Dreadlord',
    'jade-scorpion-dreadlord',
    28,
    '28',
    '30 seconds',
    0.5,
    'https://ashescodex.com/mobs/jade-scorpion-dreadlord',
    NULL,
    NULL,
    NULL
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Juicer',
    'juicer',
    14,
    '14',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/juicer',
    -628621.32667532,
    493664.72677385,
    13683.470264421
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Kain Moorling',
    'kain-moorling',
    8,
    '8',
    '1800 seconds',
    30,
    'https://ashescodex.com/mobs/kain-moorling',
    -796154.00458208,
    596033.44801343,
    23942.669476316
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Kavrok the Taxed',
    'kavrok-the-taxed',
    16,
    '16',
    '3570 - 3630 seconds',
    60.5,
    'https://ashescodex.com/mobs/kavrok-the-taxed',
    -1366916.1692351,
    -376931.24034525,
    10545.338611652
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Kesatal of the Old Ways',
    'kesatal-of-the-old-ways',
    30,
    '30',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/kesatal-of-the-old-ways',
    -1665106.2333255,
    241933.54588197,
    4539.0702445208
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Khalidur''s Harvester',
    'khalidur''s-harvester',
    26,
    '26',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/khalidur''s-harvester',
    -238436.31534043,
    892687.55557533,
    4743.1135542
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Kharaschess',
    'kharaschess',
    10,
    '1 - 10',
    '3570 - 3630 seconds',
    60.5,
    'https://ashescodex.com/mobs/kharaschess',
    NULL,
    NULL,
    NULL
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Khg-Izp',
    'khg-izp',
    18,
    '18',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/khg-izp',
    -251799.99209029,
    675411.49515353,
    15552.386475696
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Knight Commander Darrow',
    'knight-commander-darrow',
    14,
    '14',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/knight-commander-darrow',
    -919507.10937714,
    647135.14431071,
    29706.331493626
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Kuu''Shuu The Flame Forge',
    'kuu''shuu-the-flame-forge',
    27,
    '27',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/kuu''shuu-the-flame-forge',
    -1665625.4300185,
    805133.78468918,
    19164.163247739
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Lady Aislinn the Hawk',
    'lady-aislinn-the-hawk',
    23,
    '23',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/lady-aislinn-the-hawk',
    -1017641.3812282,
    949271.80459432,
    10961.546450957
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Leathermaw',
    'leathermaw',
    16,
    '16',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/leathermaw',
    NULL,
    NULL,
    NULL
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Little Brother',
    'little-brother',
    20,
    '20',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/little-brother',
    -787415.02334716,
    436243.36380345,
    13412.007231064
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Lokk the Ragebringer',
    'lokk-the-ragebringer',
    32,
    '32',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/lokk-the-ragebringer',
    -154411.05310831,
    1104437.6555422,
    5752.7693517599
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Lord Oakenbane',
    'lord-oakenbane',
    16,
    '16',
    '3300 - 3900 seconds',
    65,
    'https://ashescodex.com/mobs/lord-oakenbane',
    NULL,
    NULL,
    NULL
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Lost Hero',
    'lost-hero',
    18,
    '18',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/lost-hero',
    -252684.37750107,
    668691.84368899,
    15633.27701093
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Lotox',
    'lotox',
    28,
    '28',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/lotox',
    -1812295.7889089,
    451773.76275659,
    5591.5292886701
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Magnus the Cinderbound Colossus',
    'magnus-the-cinderbound-colossus',
    10,
    '10',
    '3570 - 3630 seconds',
    60.5,
    'https://ashescodex.com/mobs/magnus-the-cinderbound-colossus',
    -815710.60819908,
    -657957.25059501,
    19869.561190411
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Malgorach',
    'malgorach',
    22,
    '22',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/malgorach',
    NULL,
    NULL,
    NULL
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Malrhos, Dar''kuu Gravekeeper',
    'malrhos-dar''kuu-gravekeeper',
    30,
    '30',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/malrhos-dar''kuu-gravekeeper',
    -1341656.2226644,
    186394.72789549,
    6218.2839518403
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Marnak Ashlock, Broker of Chains',
    'marnak-ashlock-broker-of-chains',
    20,
    '20',
    '3570 - 3630 seconds',
    60.5,
    'https://ashescodex.com/mobs/marnak-ashlock-broker-of-chains',
    -1348409.6633809,
    -263716.58647356,
    15105.242817279
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Master Smith Eucidiaeh',
    'master-smith-eucidiaeh',
    27,
    '27',
    '270 - 330 seconds',
    5.5,
    'https://ashescodex.com/mobs/master-smith-eucidiaeh',
    -1257354.0279748,
    580424.5192968,
    8128.5809464332
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Matron Bruz',
    'matron-bruz',
    16,
    '16',
    '3570 - 3630 seconds',
    60.5,
    'https://ashescodex.com/mobs/matron-bruz',
    -1363565.8551048,
    -382799.36083018,
    16012.742685351
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Matron Mizzmet',
    'matron-mizzmet',
    7,
    '7',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/matron-mizzmet',
    -1213882.7848225,
    -636812.35085189,
    16990.295424627
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Maza''s Flame',
    'maza''s-flame',
    26,
    '26',
    '1170 - 1230 seconds',
    20.5,
    'https://ashescodex.com/mobs/maza''s-flame',
    -245646.28258362,
    910613.56985604,
    4438.9329466846
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Minereaver Spider',
    'minereaver-spider',
    30,
    '30',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/minereaver-spider',
    -1149555.1519478,
    1081535.0934893,
    8360.5389192386
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Mirk Vellin, Gravewright of Greed',
    'mirk-vellin-gravewright-of-greed',
    17,
    '17',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/mirk-vellin-gravewright-of-greed',
    -1075655.7218905,
    -306139.80371269,
    18778.718614944
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Miserable Dustpaw',
    'miserable-dustpaw',
    29,
    '29',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/miserable-dustpaw',
    58241.952152159,
    1088828.7103851,
    12549.198906029
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Molten Queen',
    'molten-queen',
    22,
    '22',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/molten-queen',
    NULL,
    NULL,
    NULL
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Morellius The Essence Gorged',
    'morellius-the-essence-gorged',
    22,
    '22',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/morellius-the-essence-gorged',
    -933667.85322648,
    415604.03451941,
    12458.874215853
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Muckmaw the Flayer',
    'muckmaw-the-flayer',
    3,
    '3',
    '300 seconds',
    5,
    'https://ashescodex.com/mobs/muckmaw-the-flayer',
    -817483.49893608,
    571181.54049287,
    12726.100727923
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Mukyuk',
    'mukyuk',
    14,
    '14',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/mukyuk',
    -536546.27687557,
    664136.37198063,
    17438.139224094
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Najash Huntmaster',
    'najash-huntmaster',
    20,
    '20 - 22',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/najash-huntmaster',
    -171819.00547259,
    727688.0870137,
    9431.664329237
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Nangolith the Spinner',
    'nangolith-the-spinner',
    6,
    '6',
    '240 - 360 seconds',
    6,
    'https://ashescodex.com/mobs/nangolith-the-spinner',
    -666647.00344336,
    619629.10080341,
    14022.435533882
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Nearly Dead Prisoner',
    'nearly-dead-prisoner',
    30,
    '30 - 33',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/nearly-dead-prisoner',
    -199176.17965583,
    901162.08641391,
    6603.1988251295
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Nordhorn',
    'nordhorn',
    20,
    '20',
    '3300 - 3900 seconds',
    65,
    'https://ashescodex.com/mobs/nordhorn',
    -944745.51301801,
    428585.46740093,
    14141.963164382
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Nurse Pelomneh',
    'nurse-pelomneh',
    27,
    '27',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/nurse-pelomneh',
    -1267181.3458831,
    565717.44416024,
    11375.408028931
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Ocular',
    'ocular',
    14,
    '14 - 23',
    '180 seconds',
    3,
    'https://ashescodex.com/mobs/ocular',
    -956865.24217487,
    819783.58331049,
    14334.236099383
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Old Lurky',
    'old-lurky',
    16,
    '16',
    '150 seconds',
    2.5,
    'https://ashescodex.com/mobs/old-lurky',
    NULL,
    NULL,
    NULL
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Ole Bloodmother',
    'ole-bloodmother',
    11,
    '11 - 12',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/ole-bloodmother',
    -1045709.0984056,
    641898.95398939,
    12064.028691105
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Olive Bootshredder',
    'olive-bootshredder',
    11,
    '11',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/olive-bootshredder',
    -1047817.0598346,
    659603.75431168,
    12407.25126521
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Panethos, Sighted Initiate',
    'panethos-sighted-initiate',
    17,
    '17',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/panethos-sighted-initiate',
    -969728.07573871,
    742940.62052549,
    13550.527470942
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Porceilion',
    'porceilion',
    14,
    '14',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/porceilion',
    -1074916.5250852,
    642840.81143261,
    13934.038554335
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Prisma',
    'prisma',
    26,
    '26',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/prisma',
    -518446.4575977,
    443771.02389747,
    28222.695267351
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Professor Gurax',
    'professor-gurax',
    17,
    '17',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/professor-gurax',
    -1478492.3906399,
    142471.49316298,
    12062.104991315
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Rabid Gander',
    'rabid-gander',
    11,
    '8 - 12',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/rabid-gander',
    -1068346.0865368,
    674455.59279221,
    11903.88110283
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Ravenous Lockbox',
    'ravenous-lockbox',
    30,
    '13 - 30',
    '600 seconds',
    10,
    'https://ashescodex.com/mobs/ravenous-lockbox',
    -777257.13043798,
    1361724.7215222,
    9290.3170889222
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Revenant Reaper',
    'revenant-reaper',
    14,
    '14',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/revenant-reaper',
    -1070508.8458433,
    658643.51504755,
    13405.264723796
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'River Runner Riggs',
    'river-runner-riggs',
    12,
    '12',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/river-runner-riggs',
    -600772.84484484,
    501550.43829613,
    11017.400595952
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Riverlord Otter',
    'riverlord-otter',
    10,
    '10',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/riverlord-otter',
    -834808.46254995,
    501194.66626565,
    11862.447924908
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Sand Chief Bikkmik',
    'sand-chief-bikkmik',
    25,
    '25',
    '0',
    0,
    'https://ashescodex.com/mobs/sand-chief-bikkmik',
    NULL,
    NULL,
    NULL
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Scarab Matriarch',
    'scarab-matriarch',
    20,
    '20',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/scarab-matriarch',
    -503333.99270238,
    873283.21758726,
    8463.985412972
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Scarab Patriarch',
    'scarab-patriarch',
    20,
    '20',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/scarab-patriarch',
    -506293.53355638,
    877737.59490551,
    6232.2938421391
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Seeker of Myths',
    'seeker-of-myths',
    23,
    '23',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/seeker-of-myths',
    -482039.80151957,
    439396.34429672,
    16268.908033007
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Sergeant of the Grove',
    'sergeant-of-the-grove',
    14,
    '14',
    '3300 - 3900 seconds',
    65,
    'https://ashescodex.com/mobs/sergeant-of-the-grove',
    NULL,
    NULL,
    NULL
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Shanty Shawn',
    'shanty-shawn',
    25,
    '25',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/shanty-shawn',
    -1853435.8698062,
    718765.94229984,
    4653.8583555431
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Shard of Undrahl',
    'shard-of-undrahl',
    21,
    '21',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/shard-of-undrahl',
    -1152033.1959005,
    -152844.77510429,
    18925.14257142
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Sharpclaw Talrith',
    'sharpclaw-talrith',
    29,
    '29',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/sharpclaw-talrith',
    -199179.7743436,
    901024.00745692,
    7549.19884009
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Shellback Sovereign',
    'shellback-sovereign',
    7,
    '7',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/shellback-sovereign',
    -1206284.2152849,
    -633961.64158262,
    15253.879972155
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Shrill-Master Gallea',
    'shrill-master-gallea',
    30,
    '30',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/shrill-master-gallea',
    -1331817.296928,
    1022380.7759352,
    7278.7562284465
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Silenced Shelver',
    'silenced-shelver',
    22,
    '22',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/silenced-shelver',
    -481749.05076509,
    439816.87736753,
    14847.797640838
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Singed Stomper',
    'singed-stomper',
    28,
    '28',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/singed-stomper',
    -1258899.7246523,
    549097.84625554,
    9126.3407488638
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Sir Jenry The Strong',
    'sir-jenry-the-strong',
    23,
    '23',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/sir-jenry-the-strong',
    -1013145.1249069,
    941152.58469029,
    8276.315689438
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Sir Morrow The Valorous',
    'sir-morrow-the-valorous',
    13,
    '13',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/sir-morrow-the-valorous',
    -927760.96356775,
    650044.03780087,
    26104.001708709
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Sirensong Box',
    'sirensong-box',
    16,
    '16',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/sirensong-box',
    -1486957.0420002,
    -3406.5760428614,
    4676.4185578224
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Skeletal Reaper',
    'skeletal-reaper',
    25,
    '7 - 29',
    '180 seconds',
    3,
    'https://ashescodex.com/mobs/skeletal-reaper',
    -1019733.9300107,
    872714.52734574,
    11170.291331918
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Slate Wolf',
    'slate-wolf',
    12,
    '1 - 25',
    '150 seconds',
    2.5,
    'https://ashescodex.com/mobs/slate-wolf',
    -1379050.6582497,
    -273603.54468213,
    23305.019364697
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Slayer Draags',
    'slayer-draags',
    16,
    '16',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/slayer-draags',
    -561998.74529906,
    629877.9241803,
    13844.349219759
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Slayer Rhaags',
    'slayer-rhaags',
    16,
    '16',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/slayer-rhaags',
    -551034.32432796,
    668791.45720926,
    17616.909643607
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Slayer Slaags',
    'slayer-slaags',
    16,
    '16',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/slayer-slaags',
    -549351.52281908,
    649250.47807096,
    19289.140335029
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Slaznug',
    'slaznug',
    15,
    '15',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/slaznug',
    -1068648.4996409,
    658053.99430437,
    13372.825796273
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Smithy Clang',
    'smithy-clang',
    14,
    '14',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/smithy-clang',
    -619402.81161785,
    481748.101648,
    13267.892200099
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Snar',
    'snar',
    3,
    '3 - 4',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/snar',
    -704348.66221876,
    573422.77251573,
    15968.007725896
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Snar, the Hungry Wolf',
    'snar-the-hungry-wolf',
    6,
    '6',
    '1500 - 2100 seconds',
    35,
    'https://ashescodex.com/mobs/snar-the-hungry-wolf',
    -694270.36846774,
    550539.54498235,
    15713.446867836
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Solace, Arificial Smithy',
    'solace-arificial-smithy',
    20,
    '20',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/solace-arificial-smithy',
    -932959.78705626,
    761231.03017469,
    12749.895866995
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Specimen Twelve',
    'specimen-twelve',
    30,
    '30',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/specimen-twelve',
    -1664417.3994366,
    240729.69377104,
    4464.5670949121
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Sungazer Murgo',
    'sungazer-murgo',
    17,
    '17',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/sungazer-murgo',
    -518761.99246687,
    828846.68977075,
    36686.303771971
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Swiftscreech',
    'swiftscreech',
    15,
    '15',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/swiftscreech',
    -573957.98081158,
    496568.25623792,
    13979.529717462
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Talon-Master Folkan',
    'talon-master-folkan',
    30,
    '30',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/talon-master-folkan',
    -1333922.9557834,
    1022962.7417289,
    7274.0596921184
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Tapmaster Percheh',
    'tapmaster-percheh',
    28,
    '28',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/tapmaster-percheh',
    -1252053.5832686,
    556134.11335321,
    11449.629557307
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Tavra',
    'tavra',
    29,
    '29',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/tavra',
    -1336981.0278468,
    190611.36168624,
    6975.2931910009
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Tawl''bura',
    'tawl''bura',
    26,
    '26',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/tawl''bura',
    -313810.14058305,
    844108.91931781,
    6925.3116469939
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Terramound',
    'terramound',
    16,
    '16',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/terramound',
    -503606.89108124,
    536440.5503561,
    13921.18637291
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Thalora, Thrice-Damned',
    'thalora-thrice-damned',
    32,
    '32',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/thalora-thrice-damned',
    -775849.12488468,
    1364150.0138077,
    9216.4409450533
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'The Anointer',
    'the-anointer',
    30,
    '30',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/the-anointer',
    -1331618.640424,
    1023889.7150346,
    7822.1534537539
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'The Arboris Historia',
    'the-arboris-historia',
    15,
    '15',
    '3300 - 3900 seconds',
    65,
    'https://ashescodex.com/mobs/the-arboris-historia',
    NULL,
    NULL,
    NULL
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'The Bloodied',
    'the-bloodied',
    21,
    '21',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/the-bloodied',
    -798776.38645678,
    304481.72296948,
    12729.213137407
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'The Bough Warden',
    'the-bough-warden',
    13,
    '13',
    '3300 - 3900 seconds',
    65,
    'https://ashescodex.com/mobs/the-bough-warden',
    NULL,
    NULL,
    NULL
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'The Brinefather',
    'the-brinefather',
    28,
    '28',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/the-brinefather',
    -1716400.985706,
    -133892.53416647,
    8000.4424251682
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'The Chain-Wound',
    'the-chain-wound',
    7,
    '7',
    '870 - 930 seconds',
    15.5,
    'https://ashescodex.com/mobs/the-chain-wound',
    -910026.36572612,
    -622548.00209398,
    10076.242701474
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'The Corvid Lord',
    'the-corvid-lord',
    27,
    '27',
    '3300 - 3900 seconds',
    65,
    'https://ashescodex.com/mobs/the-corvid-lord',
    -831484.39707119,
    204963.62422462,
    33550.881487781
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'The Crier',
    'the-crier',
    13,
    '13 - 25',
    '180 seconds',
    3,
    'https://ashescodex.com/mobs/the-crier',
    -475589.76259599,
    442846.36865093,
    13889.484586
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'The Crushed Curator',
    'the-crushed-curator',
    26,
    '26',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/the-crushed-curator',
    -517687.20336958,
    448550.67628048,
    25662.526277743
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'The Curio Peddler',
    'the-curio-peddler',
    20,
    '20',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/the-curio-peddler',
    -442721.88592266,
    454819.90743781,
    14980.687443038
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'The Desecrated Conscript',
    'the-desecrated-conscript',
    9,
    '9',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/the-desecrated-conscript',
    -643908.47948091,
    638455.78697819,
    16874.783718111
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'The Disciplinarian',
    'the-disciplinarian',
    29,
    '29',
    '1800 seconds',
    30,
    'https://ashescodex.com/mobs/the-disciplinarian',
    NULL,
    NULL,
    NULL
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'The Enchanted Cuirass',
    'the-enchanted-cuirass',
    21,
    '21',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/the-enchanted-cuirass',
    -491747.06083706,
    462051.46680973,
    14746.991242517
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'The Garden Steward',
    'the-garden-steward',
    18,
    '1 - 18',
    '0',
    0,
    'https://ashescodex.com/mobs/the-garden-steward',
    NULL,
    NULL,
    NULL
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'The Gravetender',
    'the-gravetender',
    24,
    '24',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/the-gravetender',
    -819708.48405896,
    218941.80240238,
    26750.848259616
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'The Groundskeeper',
    'the-groundskeeper',
    23,
    '23',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/the-groundskeeper',
    -839913.20520177,
    226617.90468679,
    26838.657924311
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'The Guardner',
    'the-guardner',
    32,
    '32',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/the-guardner',
    -1072218.2529839,
    1180534.742824,
    11524.874446369
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'The High Jubjub',
    'the-high-jubjub',
    16,
    '16',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/the-high-jubjub',
    -541861.83051767,
    665740.58557081,
    17826.602141188
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'The Hornhexer',
    'the-hornhexer',
    17,
    '17',
    '2400 - 3000 seconds',
    50,
    'https://ashescodex.com/mobs/the-hornhexer',
    -938748.0354211,
    469434.21616947,
    18155.662143916
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'The Hushed Librarian',
    'the-hushed-librarian',
    25,
    '25',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/the-hushed-librarian',
    -521195.32537529,
    449109.17200495,
    21970.054680997
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'The Kingfish',
    'the-kingfish',
    16,
    '16',
    '3300 - 3900 seconds',
    65,
    'https://ashescodex.com/mobs/the-kingfish',
    -621938.05363268,
    474710.79936358,
    15085.397537946
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'The Lamplighter',
    'the-lamplighter',
    27,
    '27',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/the-lamplighter',
    -1810690.4554855,
    453320.7013954,
    5537.5519041407
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'The Lore Warden',
    'the-lore-warden',
    32,
    '32',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/the-lore-warden',
    -835671.44666698,
    1287338.7685463,
    9311.1929631681
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'The Malevolant Mound',
    'the-malevolant-mound',
    13,
    '13',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/the-malevolant-mound',
    -919365.43662829,
    647094.11348778,
    26164.144816291
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'The Mindfrayed Historian',
    'the-mindfrayed-historian',
    27,
    '27',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/the-mindfrayed-historian',
    -513229.14058005,
    450406.87141229,
    30622.707752755
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'The Monitor',
    'the-monitor',
    24,
    '24',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/the-monitor',
    -501487.27849071,
    449557.70424607,
    15213.54177008
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'The Rotting Mass',
    'the-rotting-mass',
    20,
    '20 - 22',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/the-rotting-mass',
    -973885.64305348,
    529962.38634565,
    15284.442532532
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'The Shackled',
    'the-shackled',
    28,
    '28',
    '1800 seconds',
    30,
    'https://ashescodex.com/mobs/the-shackled',
    -1718487.4373737,
    -132490.6933934,
    7184.4425319465
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'The Shotcaller',
    'the-shotcaller',
    9,
    '9',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/the-shotcaller',
    -678650.93808118,
    526565.47097419,
    21613.505808817
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'The Tormented Invoker',
    'the-tormented-invoker',
    29,
    '29',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/the-tormented-invoker',
    -515951.49162289,
    450140.48763579,
    32447.591802559
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'The Untended Flame',
    'the-untended-flame',
    28,
    '28',
    '1800 seconds',
    30,
    'https://ashescodex.com/mobs/the-untended-flame',
    -1265423.5698377,
    579934.79974248,
    8135.5153088063
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'The Vaultbreaker',
    'the-vaultbreaker',
    17,
    '17',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/the-vaultbreaker',
    -1089988.5233332,
    -290907.82807212,
    17180.834833872
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'The Weary Constructor',
    'the-weary-constructor',
    29,
    '29',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/the-weary-constructor',
    -515582.63354226,
    447503.01238162,
    39349.259077235
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Throne, Prize of the Marble Court',
    'throne-prize-of-the-marble-court',
    14,
    '14',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/throne-prize-of-the-marble-court',
    -985677.22883422,
    -330993.39439794,
    5448.6892099236
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Tidewarden',
    'tidewarden',
    25,
    '25',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/tidewarden',
    -1695144.2067881,
    379456.62058872,
    4134.9418529449
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Timeless Tiller',
    'timeless-tiller',
    16,
    '16',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/timeless-tiller',
    -1045235.2705904,
    664112.48464061,
    14004.240422537
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Tolox',
    'tolox',
    18,
    '18',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/tolox',
    -1478486.94396,
    142108.61796257,
    8496.9050079867
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Tombstone',
    'tombstone',
    30,
    '30',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/tombstone',
    -790707.84214967,
    199188.63107677,
    33395.06360013
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Trailbreaker Tharok',
    'trailbreaker-tharok',
    12,
    '12',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/trailbreaker-tharok',
    -1179735.1899267,
    735122.71858965,
    11162.49609992
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Unclean Hands',
    'unclean-hands',
    17,
    '17',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/unclean-hands',
    -462189.14420961,
    476487.48158129,
    12251.083366994
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Undead Sycophant',
    'undead-sycophant',
    32,
    '32',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/undead-sycophant',
    -203124.25252469,
    899743.42377298,
    6603.198809826
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Undertaker Zon',
    'undertaker-zon',
    26,
    '26',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/undertaker-zon',
    -827470.4700562,
    209525.78825075,
    34095.262486058
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Vanguard Rowan',
    'vanguard-rowan',
    21,
    '21',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/vanguard-rowan',
    -778764.66139539,
    450955.13757164,
    32142.923150858
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Viirmythus the Spider Queen',
    'viirmythus-the-spider-queen',
    31,
    '31',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/viirmythus-the-spider-queen',
    -1135315.1108391,
    1079493.9995522,
    7675.809069601
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Viscera Slag',
    'viscera-slag',
    26,
    '26',
    '3300 - 3900 seconds',
    65,
    'https://ashescodex.com/mobs/viscera-slag',
    NULL,
    NULL,
    NULL
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Voice of the Flames',
    'voice-of-the-flames',
    27,
    '27',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/voice-of-the-flames',
    -1812539.8327876,
    452975.84462856,
    10485.785552133
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Voidspeaker Telmont',
    'voidspeaker-telmont',
    30,
    '30 - 27',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/voidspeaker-telmont',
    57363.18619809,
    1088858.0493279,
    13449.198883487
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Wailing Widow',
    'wailing-widow',
    19,
    '19',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/wailing-widow',
    -480345.59361319,
    445563.10905735,
    16127.094869102
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Warchief Zaags',
    'warchief-zaags',
    17,
    '17',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/warchief-zaags',
    -547067.98111545,
    649508.50840606,
    19735.472688654
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Warlord Silvertooth',
    'warlord-silvertooth',
    24,
    '14 - 24',
    '240 seconds',
    4,
    'https://ashescodex.com/mobs/warlord-silvertooth',
    -1070631.9566323,
    659098.75345235,
    12416.446381353
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Warlord Trugz',
    'warlord-trugz',
    7,
    '7',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/warlord-trugz',
    -860449.77007375,
    574006.0817143,
    26019.21641311
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Wartrainer Rhogan',
    'wartrainer-rhogan',
    29,
    '29',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/wartrainer-rhogan',
    57579.415516055,
    1088545.7487007,
    12558.203953929
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Waterlogged Liffy',
    'waterlogged-liffy',
    17,
    '17',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/waterlogged-liffy',
    -943951.98650383,
    782656.79392019,
    10656.55232359
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Wormwig',
    'wormwig',
    6,
    '6',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/wormwig',
    -706687.07770862,
    520419.79012307,
    14586.910007906
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Xirvethis, the Despoiler',
    'xirvethis-the-despoiler',
    32,
    '32',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/xirvethis-the-despoiler',
    11102.785310688,
    778084.98951639,
    5359.198864057
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Ysshokk',
    'ysshokk',
    9,
    '9',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/ysshokk',
    -620215.59419062,
    562506.7933321,
    19574.960262209
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Zagrazoo the Eyeless',
    'zagrazoo-the-eyeless',
    31,
    '31',
    '1200 seconds',
    20,
    'https://ashescodex.com/mobs/zagrazoo-the-eyeless',
    -1577992.450618,
    1055225.0946454,
    22973.253682623
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Zephras the Molten',
    'zephras-the-molten',
    22,
    '22',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/zephras-the-molten',
    NULL,
    NULL,
    NULL
);

INSERT INTO named_mobs (name, slug, level, level_range, respawn_time, respawn_minutes, codex_url, location_x, location_y, location_z) VALUES (
    'Zhultaresh',
    'zhultaresh',
    31,
    '31',
    '900 seconds',
    15,
    'https://ashescodex.com/mobs/zhultaresh',
    15183.240149092,
    784876.5302199,
    5334.789162604
);

