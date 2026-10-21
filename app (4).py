import streamlit as st
import random
import json
import time

st.set_page_config(page_title="Shinobi Life", page_icon="🍥", layout="centered")
st.markdown("""<style>
@keyframes fadeIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
@keyframes slideIn{from{opacity:0;transform:translateX(-40px)}to{opacity:1;transform:none}}
@keyframes pulse{0%,100%{box-shadow:0 0 0 0 rgba(255,170,0,.55)}50%{box-shadow:0 0 0 14px rgba(255,170,0,0)}}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes bounce{0%,100%{transform:translateY(0)}50%{transform:translateY(-24px)}}
@keyframes ride{from{left:-12%}to{left:104%}}
.stMarkdown p,div[data-testid="stExpander"],div[data-testid="stAlert"]{animation:fadeIn .5s ease}
div[data-testid="stProgress"] div[role="progressbar"]>div{transition:width .9s ease}
div.stButton>button{transition:transform .15s}
div.stButton>button:hover:not(:disabled){transform:scale(1.03)}
.ev-card{border:2px solid #ffaa00;border-radius:12px;padding:14px;margin:8px 0;background:rgba(255,170,0,.12);animation:slideIn .5s ease,pulse 1.6s ease 2}
.scene{position:relative;height:46px;overflow:hidden}
.sprite{position:absolute;top:4px;font-size:30px}
.s-nar{left:46%;animation:spin 3s linear infinite}
.s-kur{left:46%;animation:bounce .9s ease-in-out infinite}
.s-tr{animation:ride 5s linear infinite}
</style>""", unsafe_allow_html=True)

# ───────────────────────── DONNÉES ─────────────────────────
UNIV = {
    "Naruto": {
        "icon": "🍥", "cls": "nar", "fact": ["Clan Hyūga", "Clan Uchiwa", "Village du Sable", "Village de la Pierre"], "mait": "Ninjutsu", "monnaie": "ryōs", "job": "Faire une mission", "jobage": 12,
        "pre": "Élève de l'Académie",
        "ranks": ["Élève de l'Académie", "Genin", "Chūnin", "Jōnin", "Élite ANBU", "Kage"],
        "intro": "Tu viens au monde dans un village caché où le chakra coule dans toutes les veines.",
        "pnj": ["Haruto", "Mizuki", "Daichi", "Sakura-Hime", "Rentaro", "Kagero", "Tsubaki", "Ibuki"],
        "mile": {6: "Tu entres à l'Académie ninja.", 12: "Tu obtiens ton bandeau frontal : tu es Genin !",
                 15: "Tu peux désormais passer les examens supérieurs."},
    },
    "Kuroko": {
        "icon": "🏀", "cls": "kur", "fact": ["Lycée Seirin", "Lycée Shūtoku", "Lycée Kaijō", "Lycée Rakuzan", "Lycée Tōō", "Lycée Yōsen"], "mait": "Basket", "monnaie": "yens", "job": "Jouer un match rémunéré", "jobage": 14,
        "pre": "Collégien",
        "ranks": ["Joueur de banc", "Titulaire", "As de l'équipe", "Capitaine", "Génération des Miracles", "Légende du Basket"],
        "intro": "Tu viens au monde dans une famille où le basket est une religion.",
        "pnj": ["Akira", "Shiori", "Taiga-kun", "Midori", "Seiji", "Reo", "Nagisa", "Atsushi"],
        "mile": {6: "Tu entres à l'école primaire.", 12: "Tu entres au collège et touches un vrai ballon de match.",
                 15: "Tu entres au lycée : la Winter Cup t'attend."},
    },
    "Tokyo Revengers": {
        "icon": "🏍️", "cls": "tr", "fact": ["Moebius", "Valhalla", "Brahman", "Black Dragons"], "mait": "Combat", "monnaie": "yens", "job": "Faire une ronde du quartier", "jobage": 14,
        "pre": "Collégien",
        "ranks": ["Simple membre", "Soldat", "Capitaine de division", "Commandant", "Bras droit", "Chef du gang"],
        "intro": "Tu viens au monde dans un quartier de Tokyo où les gangs font la loi.",
        "pnj": ["Takeru", "Emma", "Ryuji", "Hinata-chan", "Kazuma", "Mikey-kun", "Chifuyu", "Nahoya"],
        "mile": {6: "Tu entres à l'école primaire.", 12: "Tu entres au collège, les premières bagarres commencent.",
                 15: "Tu entres au lycée : les gangs te remarquent."},
    },
}
RANK_TH = [0, 50, 150, 300, 600, 1000]
RANK_AGE = [0, 12, 14, 18, 25, 30]  # âge minimum pour chaque rang

NAT = {"Feu": "🔥", "Eau": "💧", "Vent": "🌪️", "Foudre": "⚡", "Terre": "🪨", "Glace": "❄️", "Bois": "🌳"}
BASE_NAT = ["Feu", "Eau", "Vent", "Foudre", "Terre"]

BIJU = [("Shukaku", "🦝"), ("Matatabi", "🐱"), ("Isobu", "🐢"), ("Son Gokū", "🐒"), ("Kokuō", "🐴"),
        ("Saiken", "🐌"), ("Chōmei", "🪲"), ("Gyūki", "🐙"), ("Kurama", "🦊")]

PUP = {"Sharingan": ("🔴", 70, 20), "Byakugan": ("⚪", 80, 20), "Mangekyō Sharingan": ("🩸", 130, 35), "Rinnegan": ("🟣", 170, 45)}

# nom, icône, description, bonus de naissance, puissance par niveau, rareté (poids)
TALENTS = {
    "fantome": ("Joueur fantôme", "👻", "Une présence quasi invisible : tes passes surgissent de nulle part.", dict(intel=10, mait=3), 4, 3),
    "freestyle": ("Freestyle", "🌀", "Un style de jeu imprévisible que personne ne sait lire.", dict(mait=6, force=3), 5, 1),
    "tir": ("Tir à trois points parfait", "🎯", "Depuis n'importe où, tes tirs retombent dans le panier.", dict(mait=8), 5, 2),
    "empereur": ("Œil de l'Empereur", "👁️", "Tu vois chaque mouvement avant qu'il n'arrive.", dict(intel=12, mait=4), 5, 1),
    "belial": ("Œil de Bélial", "😈", "Une vision sombre qui lit même les intentions adverses.", dict(intel=10, force=3), 5, 1),
    "copie": ("Copie parfaite", "🪞", "Tu reproduis les gestes de n'importe quel joueur.", dict(mait=5, intel=6), 5, 2),
    "bestial": ("Instinct bestial", "🐆", "Des réflexes et une agilité hors norme.", dict(force=8, mait=3), 5, 2),
    "viking": ("Viking", "🛡️", "Une défense titanesque : personne ne passe.", dict(force=10, sante=8), 5, 2),
    "rebond": ("Rebond prodigieux", "🦘", "Tu sautes plus haut que tout le monde.", dict(force=6, mait=4), 4, 3),
    "passe": ("Passe de génie", "🎼", "Chaque passe trouve son coéquipier.", dict(intel=8, mait=4), 4, 3),
}
# nom : (lycée, niveau de difficulté, talent)
GM = {
    "Akashi": ("Lycée Rakuzan", 1.8, "Œil de l'Empereur"),
    "Aomine": ("Lycée Tōō", 1.7, "Freestyle"),
    "Murasakibara": ("Lycée Yōsen", 1.6, "Viking"),
    "Midorima": ("Lycée Shūtoku", 1.5, "Tir parfait"),
    "Kise": ("Lycée Kaijō", 1.4, "Copie parfaite"),
}

# (multiplicateur de ton score, ajout de points, multiplicateur du score adverse)
TALENT_FX = {
    "fantome": (1.25, 4, 1.0), "freestyle": (1.3, 3, 1.0), "tir": (1.1, 10, 1.0), "empereur": (1.1, 0, .7),
    "belial": (1.15, 4, .75), "copie": (1.25, 4, .9), "bestial": (1.3, 3, .95), "viking": (1.0, 0, .6),
    "rebond": (1.15, 8, .95), "passe": (1.2, 6, 1.0),
}
TALK = {
    "Akashi": [
        ("Lui demander des conseils tactiques", .9, {"intel": 4, "gmi": 6}, "Akashi t'explique comment lire un match d'un seul regard.", {"gmi": -3}, "Il juge ta question trop naïve."),
        ("Lui proposer une partie de shōgi", .5, {"intel": 6, "gmi": 10, "bonheur": 3}, "Tu tiens bien plus longtemps que prévu.", {"gmi": -2, "bonheur": -3}, "Il te bat en dix coups."),
        ("Remettre en cause une de ses consignes", .4, {"rep": 6, "gmi": 12}, "Il apprécie ton audace.", {"gmi": -12, "rep": -4}, "Il déteste qu'on le contredise."),
    ],
    "Aomine": [
        ("Proposer un 1 contre 1 décontracté", .6, {"mait": 5, "gmi": 8}, "Il rit et te montre un geste.", {"gmi": -2, "sante": -4}, "Il te retourne en deux dribbles."),
        ("Lui demander de t'entraîner", .7, {"mait": 6, "force": 2, "gmi": 6}, "Une séance courte mais redoutable.", {"gmi": -4}, "Il s'endort sur un banc."),
        ("Lui reprocher sa nonchalance", .35, {"gmi": 12, "rep": 4}, "Ça le secoue, et il t'en respecte plus.", {"gmi": -10}, "Il te regarde de haut."),
    ],
    "Murasakibara": [
        ("Lui offrir des friandises", .9, {"gmi": 10, "argent": -20}, "Il est comblé de bonheur.", {"gmi": 2}, "Il n'aimait pas cette marque."),
        ("Lui demander de t'apprendre la défense", .6, {"force": 5, "gmi": 6}, "Il te montre comment fermer la raquette.", {"gmi": -2}, "Il a la flemme de t'expliquer."),
        ("Le défier de bloquer ton tir", .5, {"mait": 5, "gmi": 8}, "Tu le surprends une fois sur deux.", {"gmi": 1, "bonheur": -2}, "Il bloque tout en bâillant."),
    ],
    "Midorima": [
        ("Lui demander son objet porte-bonheur du jour", .8, {"bonheur": 4, "gmi": 6}, "Il te prête un petit objet étrange.", {"gmi": -2}, "Il refuse, 'ce n'est pas ton signe du jour'."),
        ("Observer son tir à l'entraînement", .8, {"mait": 5, "gmi": 5}, "Chaque tir est une leçon de précision.", {"gmi": -1}, "Il te chasse de la salle."),
        ("Le taquiner sur ses superstitions", .4, {"gmi": 8, "bonheur": 3}, "Il pique un fard mais sourit.", {"gmi": -8}, "Il se vexe profondément."),
    ],
    "Kise": [
        ("Lui demander de te montrer un de ses gestes", .85, {"mait": 5, "gmi": 8}, "Il reproduit le geste avec une facilité déconcertante.", {"gmi": -2}, "Il est trop occupé par ses fans."),
        ("Poser pour une photo avec lui", .9, {"rep": 4, "bonheur": 4, "gmi": 5}, "La photo fait le tour de l'école.", {"gmi": 1}, "Tu as les yeux fermés sur la photo."),
        ("Le défier en copiant ses mouvements", .45, {"mait": 6, "gmi": 10}, "Tu l'amuses beaucoup.", {"gmi": 1, "bonheur": -3}, "Il te copie en mieux."),
    ],
}
# nom : (âges, tours, récompense)
COMP = {
    "college": ("Tournoi inter-collèges", (12, 14), ["Premier tour", "Demi-finale", "Finale"], {"xp": 60, "rep": 10, "argent": 120}),
    "inter": ("Inter-High", (15, 18), ["Éliminatoires", "Quart de finale", "Demi-finale", "Finale"], {"xp": 100, "rep": 15, "argent": 250}),
    "winter": ("Winter Cup", (15, 18), ["Premier tour", "Quart de finale", "Demi-finale", "Finale"], {"xp": 150, "rep": 25, "argent": 400}),
}

ZONES = ["Aucune", "Zone", "Porte de la Zone", "Direct Drive Zone"]
ZONE_REQ = [(0, 0, 0), (3, 50, 15), (7, 65, 16), (12, 80, 17)]  # (entraînements, maîtrise, âge)
SPORTS = {"Boxe": "🥊", "Muay-thaï": "🦵", "Judo": "🥋", "Karaté": "👊", "Jiu-jitsu": "🤼", "Kickboxing": "🦶"}
WIN_PREFIX = ("🌟", "⚔️ Tu bats", "📖", "🏆", "✨", "👁️ Tu voles", "🤝", "🏀 Victoire")

STATS = [("sante", "❤️ Santé"), ("bonheur", "😊 Bonheur"), ("intel", "🧠 Intelligence"),
         ("force", "💪 Force"), ("mait", "🎯 Maîtrise"), ("chakra", "🌀 Chakra"), ("rep", "⭐ Réputation")]

# a = âge minimum
TECH = {
    "clone": dict(n="Multi-clonage", u="Naruto", a=8, p=100, req=("mait", 10), pw=5),
    "subst": dict(n="Substitution", u="Naruto", a=9, p=150, req=("mait", 15), pw=6),
    "terre": dict(n="Mur de terre", u="Naruto", a=11, p=300, req=("nat", "Terre", 2), pw=12),
    "feu": dict(n="Boule de feu suprême", u="Naruto", a=12, p=400, req=("nat", "Feu", 2), pw=14),
    "eau": dict(n="Dragon d'eau", u="Naruto", a=12, p=400, req=("nat", "Eau", 2), pw=14),
    "vent": dict(n="Lame de vent", u="Naruto", a=12, p=400, req=("nat", "Vent", 2), pw=14),
    "foudre": dict(n="Éclair tranchant", u="Naruto", a=15, p=800, req=("nat", "Foudre", 3), pw=22),
    "glace": dict(n="Miroirs de glace", u="Naruto", a=18, p=1500, req=("nat", "Glace", 1), pw=30),
    "bois": dict(n="Forêt profonde", u="Naruto", a=18, p=1500, req=("nat", "Bois", 1), pw=30),
    "sage": dict(n="Mode Sage", u="Naruto", a=25, p=3000, req=("mait", 70), pw=40),
    "genjutsu": dict(n="Genjutsu du Sharingan", u="Naruto", a=16, p=500, req=("pup", "Sharingan"), pw=18),
    "hakke": dict(n="Paume du Hakke", u="Naruto", a=16, p=500, req=("pup", "Byakugan"), pw=20),
    "tsukuyomi": dict(n="Tsukuyomi", u="Naruto", a=18, p=2500, req=("pup", "Mangekyō Sharingan"), pw=40),
    "shinra": dict(n="Shinra Tensei", u="Naruto", a=20, p=4000, req=("pup", "Rinnegan"), pw=55),
    "passe": dict(n="Passe fantôme", u="Kuroko", a=12, p=200, req=("mait", 20), pw=8),
    "trois": dict(n="Tir à trois points", u="Kuroko", a=13, p=400, req=("mait", 30), pw=12),
    "dribble": dict(n="Dribble brise-chevilles", u="Kuroko", a=14, p=700, req=("mait", 40), pw=16),
    "meteore": dict(n="Tir météore", u="Kuroko", a=16, p=1500, req=("mait", 60), pw=28),
    "zone": dict(n="La Zone", u="Kuroko", a=17, p=3000, req=("zone", 1), pw=38),
    "kick": dict(n="Coup de pied circulaire", u="Tokyo Revengers", a=12, p=200, req=("force", 25), pw=8),
    "contre": dict(n="Contre-attaque", u="Tokyo Revengers", a=13, p=400, req=("force", 35), pw=12),
    "charge": dict(n="Charge de division", u="Tokyo Revengers", a=15, p=900, req=("force", 50), pw=20),
    "acier": dict(n="Mental d'acier", u="Tokyo Revengers", a=16, p=1500, req=("rep", 50), pw=26),
    "leap": dict(n="Time Leap", u="Tokyo Revengers", a=20, p=4000, req=("mait", 70), pw=45),
}

# nom, prix, description, effets, univers, âge min
SHOP = {
    "cadeau": ("🎁 Cadeau", 50, "Pour améliorer une relation", {"cadeau": 1}, None, 4),
    "ramen": ("🍜 Bol de ramen", 80, "+15 santé, +5 bonheur", {"sante": 15, "bonheur": 5}, None, 3),
    "boisson": ("🥤 Boisson énergétique", 60, "+1 action cette année", {"pa": 1}, None, 6),
    "manuel": ("📘 Manuel d'entraînement", 400, "+4 force, +4 maîtrise, +3 intel", {"force": 4, "mait": 4, "intel": 3}, None, 8),
    "kunai": ("🗡️ Kunai en acier trempé", 200, "+5 maîtrise", {"mait": 5}, "Naruto", 8),
    "shoes": ("👟 Chaussures de pro", 300, "+6 maîtrise", {"mait": 6}, "Kuroko", 8),
    "chakra": ("📜 Parchemin de chakra", 300, "+10 chakra", {"chakra": 10}, "Naruto", 10),
    "nature": ("🔮 Parchemin de nature", 1000, "Éveille une nouvelle nature de chakra", {"nature": 1}, "Naruto", 10),
    "xp": ("🧪 Potion d'expérience", 500, "+40 XP", {"xp": 40}, None, 10),
    "veste": ("🧥 Veste du gang", 250, "+8 réputation, +3 force", {"rep": 8, "force": 3}, "Tokyo Revengers", 13),
    "leap": ("⏳ Amulette Time Leap", 1500, "Te ramène à la vie une fois", {"revive": 1}, None, 16),
}

# (univers, âge min, âge max, texte, [(label, p_succès, eff_ok, txt_ok, eff_ko, txt_ko)], condition optionnelle)
EV = [
    # Petite enfance
    (None, 1, 2, "Tu fais tes premiers pas devant tes parents.",
     [("Avancer seul", .75, {"force": 2, "bonheur": 4}, "Tu marches ! Tes parents applaudissent.", {"sante": -2}, "Tu tombes sur les fesses."),
      ("Rester dans les bras", 1, {"bonheur": 2}, "Câlins.", {}, "")]),
    (None, 2, 4, "C'est l'heure de tes premiers mots.",
     [("« Maman ! »", 1, {"bonheur": 3}, "Ta mère fond en larmes de joie.", {}, ""),
      ("« Papa ! »", 1, {"bonheur": 3}, "Ton père est aux anges.", {}, ""),
      ("« Ramen ! »", 1, {"bonheur": 4, "intel": 1}, "Toute la famille éclate de rire.", {}, "")]),
    (None, 3, 5, "À la garderie, un enfant te prend ton jouet.",
     [("Le reprendre", .5, {"force": 1, "rep": 2}, "Tu récupères ton jouet.", {"bonheur": -3}, "Tu pleures, la maîtresse te console."),
      ("Laisser faire", 1, {"bonheur": -1, "intel": 1}, "Tu te trouves un autre jeu.", {}, "")]),
    (None, 5, 8, "Contrôle surprise à l'école !",
     [("Réviser tard", .8, {"intel": 4, "bonheur": -2}, "Bonne note !", {"sante": -3}, "Tu t'endors sur ta copie."),
      ("Improviser", .4, {"bonheur": 3}, "Ça passe, incroyable.", {"intel": -1, "bonheur": -4}, "Zéro pointé.")]),
    (None, 9, 17, "Contrôle surprise à l'école !",
     [("Réviser tard", .8, {"intel": 4, "bonheur": -2}, "Bonne note !", {"sante": -3}, "Tu t'endors sur ta copie."),
      ("Improviser", .4, {"bonheur": 3}, "Ça passe, incroyable.", {"intel": -1, "bonheur": -4}, "Zéro pointé.")]),
    # Naruto
    ("Naruto", 6, 9, "À l'Académie, on t'apprend à lancer un kunai pour la première fois.",
     [("Viser la cible", .6, {"mait": 4, "rep": 2}, "En plein dans le mille !", {"bonheur": -2}, "Tu rates et tout le monde rit."),
      ("Jouer les clowns", 1, {"bonheur": 4, "intel": -1}, "Tu fais rire la classe.", {}, "")]),
    ("Naruto", 7, 12, "Un vieux ninja te voit jongler avec ton chakra et propose de te donner une leçon.",
     [("Accepter", .8, {"mait": 6, "chakra": 4}, "Tu apprends une astuce précieuse.", {"bonheur": -3}, "Il s'endort en plein cours..."),
      ("Refuser poliment", 1, {"bonheur": 2}, "Tu préfères jouer dehors.", {}, "")]),
    ("Naruto", 12, 25, "Mission de rang D : retrouver le chat d'une noble dame.",
     [("Foncer", .7, {"argent": 80, "xp": 10}, "Mission réussie, le chat t'a griffé mais tu es payé !", {"sante": -5, "bonheur": -3}, "Le chat t'a échappé."),
      ("Pister avec le chakra", .9, {"argent": 60, "xp": 12, "chakra": -3}, "Pisté sans effort !", {}, "")]),
    ("Naruto", 12, 20, "L'examen de promotion approche, le jury t'attend.",
     [("Participer", .55, {"xp": 60, "rep": 10}, "Tu réussis l'examen !", {"sante": -10, "bonheur": -8}, "Tu échoues de justesse."),
      ("Attendre l'an prochain", 1, {"intel": 3}, "Tu t'entraînes encore un an.", {}, "")]),
    ("Naruto", 15, 50, "Un ninja déserteur menace le village.",
     [("L'affronter", .5, {"xp": 50, "rep": 15, "argent": 150}, "Tu le mets hors d'état de nuire !", {"sante": -30, "rep": -3}, "Il t'inflige de graves blessures."),
      ("Alerter les anciens", .95, {"xp": 15, "rep": 3}, "Le village est sauvé grâce à ton alerte.", {}, "")]),
    ("Naruto", 10, 60, "Une rumeur parle d'un parchemin interdit caché dans une grotte.",
     [("Y aller", .4, {"chakra": 15, "mait": 8, "xp": 20}, "Tu trouves le parchemin !", {"sante": -20, "bonheur": -5}, "Piège ! Tu t'en sors de justesse."),
      ("Ignorer", 1, {}, "Tu restes prudent.", {}, "")]),
    # Kuroko
    ("Kuroko", 6, 11, "Des enfants jouent au basket dans un parc et te proposent de te joindre à eux.",
     [("Jouer avec eux", .8, {"mait": 4, "bonheur": 5}, "Tu t'amuses comme un fou.", {"sante": -2}, "Tu te tords la cheville."),
      ("Regarder de loin", 1, {"intel": 1}, "Tu observes leurs gestes.", {}, "")]),
    ("Kuroko", 12, 15, "Le coach te propose de rejoindre l'équipe de basket du collège.",
     [("Rejoindre", .85, {"mait": 8, "force": 3, "rep": 3}, "Tu intègres l'équipe !", {"bonheur": -4}, "Tu finis sur le banc."),
      ("Passer", 1, {"intel": 2}, "Tu te concentres sur les études.", {}, "")]),
    ("Kuroko", 15, 18, "Match d'entraînement contre un lycée rival.",
     [("Jouer à fond", .6, {"mait": 6, "xp": 25, "rep": 6}, "Victoire !", {"bonheur": -6, "sante": -5}, "Défaite amère."),
      ("Rester sur le banc", 1, {"bonheur": -1}, "Tu regardes le match.", {}, "")]),
    ("Kuroko", 13, 40, "Un prodige te propose un 1 contre 1 sur un playground.",
     [("Relever le défi", .45, {"mait": 10, "rep": 8}, "Tu l'accroches jusqu'au bout !", {"mait": 4, "bonheur": -5}, "Écrasé, mais tu as appris."),
      ("Refuser", 1, {}, "Pas aujourd'hui.", {}, "")]),
    ("Kuroko", 14, 30, "Ta présence discrète pourrait devenir une arme : travailler la passe invisible ?",
     [("S'y consacrer", .8, {"mait": 7, "intel": 2}, "Plus personne ne te voit venir !", {"sante": -5}, "Tu te blesses en forçant."),
      ("Continuer comme avant", 1, {}, "Rien ne change.", {}, "")]),
    # Tokyo Revengers
    ("Tokyo Revengers", 6, 11, "Un grand du quartier te propose de faire la course à vélo.",
     [("Accepter", .6, {"force": 2, "rep": 3, "bonheur": 4}, "Tu gagnes la course !", {"sante": -5, "bonheur": -2}, "Chute spectaculaire."),
      ("Refuser", 1, {}, "Tu rentres à la maison.", {}, "")]),
    ("Tokyo Revengers", 12, 20, "Un gang local te recrute après les cours.",
     [("Rejoindre", .8, {"rep": 8, "force": 4, "xp": 15}, "Tu portes la veste du gang.", {"sante": -8}, "Initiation brutale."),
      ("Refuser", 1, {"intel": 2}, "Tu gardes ta liberté.", {}, "")]),
    ("Tokyo Revengers", 13, 25, "Un gang rival t'attend à la sortie.",
     [("Se battre", .55, {"xp": 30, "rep": 10, "force": 3}, "Tu gagnes !", {"sante": -20, "rep": -4}, "Tu te fais rouer de coups."),
      ("Fuir", .9, {"bonheur": -3}, "Tu t'échappes.", {"sante": -5}, "Tu es rattrapé.")]),
    ("Tokyo Revengers", 14, 30, "Un ami est pris pour cible par une bande.",
     [("Le défendre", .6, {"rep": 12, "xp": 25, "bonheur": 5}, "Votre amitié en sort renforcée.", {"sante": -25}, "Tu encaisses les coups pour lui."),
      ("Appeler à l'aide", .9, {"xp": 8}, "Les renforts arrivent.", {}, "")]),
    ("Tokyo Revengers", 15, 40, "Réunion sous le temple : le chef cherche un volontaire.",
     [("Se porter volontaire", .65, {"xp": 40, "rep": 10, "argent": 100}, "Mission accomplie avec honneur.", {"sante": -15, "rep": -3}, "La mission tourne mal."),
      ("Rester discret", 1, {}, "Un autre s'en charge.", {}, "")]),
    ("Tokyo Revengers", 16, 60, "Un flash étrange : tu entrevois un autre futur...",
     [("Tenter de le changer", .5, {"mait": 8, "intel": 4, "xp": 30}, "Tu évites une tragédie.", {"bonheur": -8, "sante": -8}, "Tu t'épuises sans résultat."),
      ("Oublier", 1, {}, "Ce n'était qu'un rêve.", {}, "")]),
    # Vie générale
    (None, 14, 35, "Quelqu'un te plaît vraiment dans ton entourage.",
     [("Se déclarer", .5, {"bonheur": 12}, "Complicité immédiate !", {"bonheur": -8}, "Râteau..."),
      ("Rester ami", 1, {"bonheur": 2}, "Tu gardes ça pour toi.", {}, "")]),
    (None, 3, 75, "Tu tombes malade.",
     [("Voir un médecin", 1, {"argent": -40, "sante": 5}, "Tu guéris vite.", {}, ""),
      ("Ignorer", .5, {}, "Ça passe tout seul.", {"sante": -15}, "Ça empire.")]),
    (None, 18, 60, "Un inconnu te propose un pari risqué.",
     [("Parier 100", .45, {"argent": 200}, "Tu gagnes le double !", {"argent": -100}, "Tu perds ta mise."),
      ("Décliner", 1, {}, "Tu restes sage.", {}, "")]),
    # Bijū
    ("SPECIAL", 0, 99, "Une présence immense s'éveille en toi : une bête à queues cherche un hôte.",
     [("Accepter le pacte", .6, {"biju": 1, "xp": 30}, "Un bijū est scellé en toi !", {"sante": -30, "bonheur": -10}, "Le sceau échoue, tu survives de justesse."),
      ("Refuser", 1, {"bonheur": 2}, "La présence s'efface.", {}, "")], "pacte"),
    ("Naruto", 6, 90, "Le bijū te parle dans ton sommeil.",
     [("Lui répondre", .7, {"lien": 8, "chakra": 2}, "Une conversation étonnamment sincère.", {"bonheur": -5, "lien": -3}, "Il se moque de toi, cauchemar garanti."),
      ("L'ignorer", 1, {"lien": -5}, "Il boude dans sa cage.", {}, "")], "biju"),
    ("Naruto", 6, 90, "On se méfie de toi : on murmure que tu portes une bête.",
     [("Prouver ta valeur", .5, {"rep": 10, "xp": 20}, "Les regards changent peu à peu.", {"rep": -6, "bonheur": -8}, "Ça empire, on t'évite."),
      ("T'isoler", 1, {"bonheur": -4, "lien": 5}, "Seul ton bijū te tient compagnie.", {}, "")], "biju"),
    ("Naruto", 14, 60, "Des chasseurs traquent les porteurs de bijū.",
     [("Fuir", .6, {"xp": 10}, "Tu leur échappes.", {"sante": -15}, "Tu es blessé dans ta fuite."),
      ("Se battre avec la puissance du bijū", .65, {"xp": 60, "rep": 15, "lien": -4}, "Tu les terrasses !", {"sante": -35, "lien": -6}, "Tu perds le contrôle et tu es gravement blessé.")], "biju"),
    ("SPECIAL", 13, 18, "Un joueur de la Génération des Miracles t'a repéré lors d'un match et te propose de rejoindre son équipe.",
     [("Accepter l'invitation", .85, {"recrue": 1, "xp": 40, "rep": 8}, "Tu rejoins l'équipe d'un Miracle !", {"bonheur": -4}, "Le test se passe mal : il te laisse partir."),
      ("Refuser", 1, {"bonheur": -1}, "Tu restes sur ta propre route.", {}, "")], "gm"),
    # Alliances
    (None, 12, 70, "Un de tes alliés te demande de l'aide contre une faction rivale.",
     [("Envoyer des renforts", .65, {"alrel": 12, "xp": 30, "rep": 6}, "Votre alliance sort renforcée.", {"alrel": -5, "sante": -15}, "Vous perdez la bataille."),
      ("Refuser", 1, {"alrel": -12, "karma": -3}, "Ton allié est déçu.", {}, "")], "ally"),
    (None, 12, 70, "Tes alliés organisent un grand banquet pour célébrer votre pacte.",
     [("Y participer", 1, {"alrel": 6, "bonheur": 4, "argent": -30}, "Une soirée mémorable.", {}, ""),
      ("Décliner", 1, {"alrel": -3}, "Ton absence est remarquée.", {}, "")], "ally"),
    # Karma
    (None, 8, 60, "Tu trouves un portefeuille bien rempli dans la rue.",
     [("Le rapporter", 1, {"karma": 8, "rep": 3}, "Le propriétaire te remercie chaleureusement.", {}, ""),
      ("Le garder", .8, {"argent": 150, "karma": -8}, "Tu empoches l'argent.", {"karma": -8, "rep": -5}, "Quelqu'un t'a vu faire...")]),
    (None, 10, 60, "Un camarade blessé te demande de l'aide.",
     [("L'aider", .9, {"karma": 6, "bonheur": 3}, "Il t'est très reconnaissant.", {"sante": -3}, "Tu te blesses un peu en l'aidant."),
      ("Passer ton chemin", 1, {"karma": -4}, "Tu ne te retournes pas.", {}, "")]),
    (None, 12, 60, "Un marchand te propose un marché douteux : voler un client en échange d'une part.",
     [("Accepter", .7, {"argent": 120, "karma": -10}, "L'affaire est conclue, sans témoin.", {"rep": -10, "karma": -10, "bonheur": -4}, "Tu es démasqué."),
      ("Refuser", 1, {"karma": 4}, "Tu gardes la conscience tranquille.", {}, "")]),
    ("SPECIAL", 16, 60, "Un homme au manteau noir orné de nuages rouges t'observe depuis l'ombre : l'Akatsuki cherche des recrues.",
     [("Rejoindre l'Akatsuki", .85, {"akatsuki": 1, "karma": -15, "rep": -40, "xp": 40}, "Tu abandonnes ton village.", {"sante": -20, "karma": -5}, "Tu échoues à leur test et t'enfuis."),
      ("Refuser", 1, {"karma": 5}, "Tu tournes le dos à l'ombre.", {}, "")], "akat"),
]
BIJU_EV = [i for i, e in enumerate(EV) if e[0] == "SPECIAL" and e[5] == "pacte"][0]
GM_EV = [i for i, e in enumerate(EV) if e[0] == "SPECIAL" and e[5] == "gm"][0]
AKAT_EV = [i for i, e in enumerate(EV) if e[0] == "SPECIAL" and e[5] == "akat"][0]

DEFIS = [
    ("d1", "Atteindre 18 ans", lambda g: g["age"] >= 18, {"argent": 200}),
    ("d2", "Apprendre 3 techniques", lambda g: len(g["tech"]) >= 3, {"argent": 300, "xp": 30}),
    ("d3", "Gagner 5 duels", lambda g: g["wins"] >= 5, {"argent": 400, "xp": 40}),
    ("d4", "Avoir 1000 d'argent", lambda g: g["argent"] >= 1000, {"xp": 50}),
    ("d5", "Atteindre 80 de réputation", lambda g: g["rep"] >= 80, {"argent": 500}),
    ("d6", "Maîtriser une nature niveau 3", lambda g: max(list(g["nat"].values()) or [0]) >= 3, {"xp": 60}),
    ("d7", "Atteindre le 3e rang", lambda g: rang(g)[0] >= 2, {"argent": 600}),
    ("d8", "Débloquer une nature rare", lambda g: any(n in g["nat"] for n in ("Glace", "Bois")), {"xp": 100}),
    ("d9", "Être en couple", lambda g: bool(g["couple"]), {"bonheur": 20, "argent": 200}),
    ("d10", "Survivre jusqu'à 40 ans", lambda g: g["age"] >= 40, {"xp": 150}),
    ("d11", "Devenir porteur d'un bijū", lambda g: bool(g["biju"]), {"xp": 80}),
    ("d13", "Devenir un héros (karma ≥ 60)", lambda g: g["karma"] >= 60, {"rep": 10, "argent": 300}),
    ("d14", "Rejoindre l'Akatsuki", lambda g: g["akatsuki"], {"xp": 100}),
    ("d15", "Voler 2 pupilles", lambda g: len(g["pupilles"]) >= 2, {"xp": 200, "argent": 500}),
    ("d12", "Atteindre 60 de lien avec ton bijū", lambda g: bool(g["biju"]) and g["biju"]["lien"] >= 60, {"xp": 200, "argent": 500}),
]

# ───────────────────────── LOGIQUE ─────────────────────────
ICON = {k: lab.split()[0] for k, lab in STATS}
ICON.update(argent="💴", xp="✨", karma="☯️", lien="🔗")

def _delta(k, v):
    try: st.session_state.setdefault("dl", []).append((k, v))
    except Exception: pass

def L(g, txt):
    g["log"].append([g["age"], txt])
    if txt.startswith(WIN_PREFIX):
        try: st.session_state["fx"] = "win"
        except Exception: pass

def stage(g):
    a = g["age"]
    return "Bébé" if a < 3 else "Petit enfant" if a < 6 else "Enfant" if a < 13 else "Adolescent" if a < 18 else "Adulte" if a < 60 else "Senior"

def recruter(g, nom=None):
    if g["recrue"] or g["u"] != "Kuroko":
        return
    nom = nom or max(g["gm"], key=lambda n: (g["gm"][n], random.random()))
    g["recrue"] = nom
    lyc = GM[nom][0]
    f = g["fact"].get(lyc)
    if f and not f["allie"] and sum(x["allie"] for x in g["fact"].values()) < 3:
        f["allie"] = True
        f["rel"] = max(f["rel"], 60)
    ap(g, {"xp": 60, "rep": 10})
    L(g, f"🌟 {nom} te recrute dans le {lyc} !")

def karma_label(k):
    return "Héros" if k >= 60 else "Bon" if k >= 20 else "Neutre" if k > -20 else "Louche" if k > -60 else "Sombre"

def ajouter_pnj(g, role):
    pool = [n for n in UNIV[g["u"]]["pnj"] if n not in [p["nom"] for p in g["pnj"]]]
    if pool:
        p = dict(nom=random.choice(pool), role=role, aff=random.randint(25, 50), niv=round(random.uniform(.7, 1.3), 2))
        g["pnj"].append(p)
        txt = {"ami": "devient ton ami(e)", "rival": "devient ton rival(e)", "amour": "te fait battre le cœur"}[role]
        L(g, f"👥 {p['nom']} {txt}.")

def new_game(nom, u):
    g = dict(v=6, nom=nom, u=u, age=0, sante=random.randint(70, 95), bonheur=random.randint(60, 80),
             intel=random.randint(10, 40), force=random.randint(5, 20), mait=random.randint(0, 5),
             chakra=random.randint(5, 25) if u == "Naruto" else 0, rep=0, argent=0, xp=0, pa=3, cadeau=0, revive=0, wins=0,
             couple="", riche=random.randint(1, 3), nat={}, tech=[], defis_ok=[], dead=False, cause="",
             event=None, biju=None, log=[], pnj=[], karma=0, akatsuki=False, pupilles=[], zone=0, zxp=0, sports={}, talent=None, recrue="", gm={n: 0 for n in GM}, match=None, cup=None, cal={},
             fact={n: dict(rel=random.randint(10, 40), allie=False) for n in UNIV[u]["fact"]})
    L(g, f"🌱 {nom} naît. {UNIV[u]['intro']}")
    if u == "Kuroko":
        k = random.choices(list(TALENTS), weights=[t[5] for t in TALENTS.values()])[0]
        g["talent"] = dict(k=k, lvl=1)
        ap(g, TALENTS[k][3])
        L(g, f"✨ Tu naîs avec un talent inné : {TALENTS[k][1]} {TALENTS[k][0]} !")
    for nm, r in (("mère", random.choice(["Aiko", "Yumi", "Rin", "Naomi"])), ("père", random.choice(["Hiroshi", "Takashi", "Ren", "Isamu"]))):
        g["pnj"].append(dict(nom=f"{r} ({nm})", role="famille", aff=random.randint(50, 85), niv=1))
    if u == "Naruto" and random.random() < .08:
        get_biju(g)
        L(g, "😱 Un bijū a été scellé en toi dès la naissance !")
    return g

def get_biju(g):
    if g["biju"]:
        return
    i = random.randrange(9)
    g["biju"] = dict(nom=f"{BIJU[i][0]} ({i + 1} queue{'s' if i else ''})", ico=BIJU[i][1], lien=10)
    ap(g, {"chakra": 20, "force": 8})
    L(g, f"{BIJU[i][1]} {BIJU[i][0]} est maintenant scellé en toi !")

def ap(g, eff):
    for k, v in eff.items():
        _delta(k, v)
        if k == "alrel":
            for f in g["fact"].values():
                if f["allie"]: f["rel"] = max(0, min(100, f["rel"] + v))
        elif k == "argent": g[k] = max(0, g[k] + v)
        elif k in ("xp", "pa", "cadeau", "revive"): g[k] += v
        elif k == "nature": eveiller(g)
        elif k == "biju": get_biju(g)
        elif k == "recrue": recruter(g)
        elif k == "karma": g[k] = max(-100, min(100, g[k] + v))
        elif k == "akatsuki":
            g["akatsuki"] = True
            L(g, "🌑 Tu rejoins l'Akatsuki. Ton village te considère désormais comme un traître.")
        elif k == "lien":
            if g["biju"]: g["biju"]["lien"] = max(0, min(100, g["biju"]["lien"] + v))
        else: g[k] = max(0, min(100, g[k] + v))

def eveiller(g):
    dispo = [n for n in BASE_NAT if n not in g["nat"]]
    if dispo:
        n = random.choice(dispo)
        g["nat"][n] = 1
        L(g, f"🔮 Nature de chakra éveillée : {NAT[n]} {n} !")
    else:
        L(g, "🔮 Tu maîtrises déjà toutes les natures de base.")

def rang(g):
    a = g["age"]
    ix = max(i for i, t in enumerate(RANK_TH) if g["xp"] >= t)
    ia = max(i for i, t in enumerate(RANK_AGE) if a >= t)
    i = min(ix, ia)
    if a < 6: return 0, "Petit enfant"
    if a < 12: return 0, UNIV[g["u"]]["pre"]
    return i, UNIV[g["u"]]["ranks"][i]

def puissance(g):
    p = g["force"] * .5 + g["mait"] * .6 + (g["chakra"] * .4 if g["u"] == "Naruto" else 0) + sum(g["nat"].values()) * 3 + g["intel"] * .1
    p += sum(TECH[t]["pw"] for t in g["tech"])
    p += sum(PUP[n][2] for n in g["pupilles"])
    p += 7 * sum(f["allie"] for f in g["fact"].values()) + g["zone"] * 8 + sum(g["sports"].values()) * 3
    if sum(1 for v in g["sports"].values() if v >= 2) >= 3: p += 10
    if g["talent"]: p += TALENTS[g["talent"]["k"]][4] * g["talent"]["lvl"]
    if g["recrue"]: p += 12
    if g["biju"]:
        p += 15 + g["biju"]["lien"] * .4 + (25 if g["biju"]["lien"] >= 60 else 0)
    return p

def mort(g, cause):
    if g["revive"] > 0:
        g["revive"] -= 1
        g["sante"] = 50
        L(g, "⏳ L'amulette Time Leap s'active : tu reviens à la vie !")
        return
    g["dead"] = True
    g["cause"] = cause

def score(g):
    return int(g["xp"] + g["rep"] * 5 + sum(g["nat"].values()) * 50 + len(g["tech"]) * 100 + g["age"] * 10 + len(g["pupilles"]) * 80 + g["karma"] // 2 + (g["biju"]["lien"] * 3 if g["biju"] else 0))

def debloquer_rares(g):
    n = g["nat"]
    if "Glace" not in n and n.get("Eau", 0) >= 3 and n.get("Vent", 0) >= 3 and g["age"] >= 15:
        n["Glace"] = 1; L(g, "❄️ Fusion Eau + Vent : nature rare GLACE débloquée !")
    if "Bois" not in n and n.get("Terre", 0) >= 3 and n.get("Eau", 0) >= 3 and g["age"] >= 15:
        n["Bois"] = 1; L(g, "🌳 Fusion Terre + Eau : nature rare BOIS débloquée !")

def ev_ok(g, e):
    if e[0] not in (None, g["u"]) or not (e[1] <= g["age"] <= e[2]):
        return False
    c = e[5] if len(e) > 5 else None
    if c == "biju": return bool(g["biju"])
    if c == "ally": return any(f["allie"] for f in g["fact"].values())
    return True

def vieillir(g):
    g["age"] += 1
    g["pa"] = 3
    a = g["age"]
    g["match"] = None
    g["cup"] = None
    if g["u"] == "Kuroko":
        g["cal"] = {k: True for k, c in COMP.items() if c[1][0] <= a <= c[1][1]}
        if a >= 13:
            g["cal"]["camp"] = True
    L(g, f"🎂 Anniversaire : {a} an{'s' if a > 1 else ''} ({stage(g)}).")
    if g["u"] == "Kuroko" and g["cal"]:
        noms = [COMP[k][0] for k in g["cal"] if k in COMP]
        if noms:
            L(g, "📅 Cette année, tu peux participer à : " + ", ".join(noms) + ".")
    m = UNIV[g["u"]]["mile"].get(a)
    if m: L(g, f"🏫 {m}")
    if g["talent"] and a == 12 and g["talent"]["lvl"] < 5:
        g["talent"]["lvl"] += 1
        L(g, f"✨ Ton talent « {TALENTS[g['talent']['k']][0]} » s'éveille pleinement !")
    ap(g, {"intel": random.randint(0, 2) if a >= 3 else 1, "force": random.randint(0, 2) if a < 30 else -1})
    if a >= 45:
        ap(g, {"sante": -random.randint(1, 4)})
    if 6 <= a < UNIV[g["u"]]["jobage"]:
        s = 10 * g["riche"]
        g["argent"] += s
        L(g, f"👛 Argent de poche : +{s} {UNIV[g['u']]['monnaie']}.")
    elif a >= UNIV[g["u"]]["jobage"]:
        s = (20 + 15 * rang(g)[0]) * random.randint(1, 3)
        g["argent"] += s
        L(g, f"💴 Revenus de l'année : +{s} {UNIV[g['u']]['monnaie']}.")
    if g["karma"] >= 50:
        ap(g, {"rep": 2})
    elif g["karma"] <= -50 and not g["akatsuki"]:
        ap(g, {"rep": -2})
    if g["recrue"]:
        ap(g, {"xp": 10, "rep": 2})
    if a == 6 and g["u"] == "Naruto":
        eveiller(g)
    for age_p, role in ((4, "ami"), (7, "ami"), (9, "rival"), (13, "amour"), (15, "rival")):
        if a == age_p: ajouter_pnj(g, role)
    for p in g["pnj"]:
        p["aff"] = max(0, p["aff"] - random.randint(0, 4))
    for n, f in g["fact"].items():
        if f["allie"]:
            ap(g, {"xp": 5, "rep": 1, "argent": 15})
            f["rel"] = min(100, f["rel"] + random.randint(0, 3) - (6 if g["karma"] <= -40 else 0))
            if f["rel"] < 20:
                f["allie"] = False
                L(g, f"💔 {n} rompt l'alliance.")
        else:
            f["rel"] = max(0, f["rel"] - random.randint(0, 2))
    if g["biju"] and g["biju"]["lien"] < 25 and random.random() < .15:
        ap(g, {"sante": -20, "rep": -10, "bonheur": -8})
        L(g, f"👹 {g['biju']['nom']} prend le contrôle ! Tu causes des dégâts autour de toi...")
    if g["sante"] <= 0:
        mort(g, "Épuisement et blessures."); return
    if a > 60 and random.random() < (a - 60) / 100:
        mort(g, "Mort de vieillesse, entouré de souvenirs."); return
    if g["u"] == "Kuroko" and g["talent"] and not g["recrue"] and 13 <= a <= 18 and g["mait"] >= 45 and random.random() < .3:
        g["event"] = GM_EV; return
    if g["u"] == "Naruto" and not g["akatsuki"] and a >= 16 and g["karma"] <= -40 and random.random() < .5:
        g["event"] = AKAT_EV; return
    if g["u"] == "Naruto" and not g["biju"] and a >= 3 and random.random() < .04:
        g["event"] = BIJU_EV; return
    elig = [i for i, e in enumerate(EV) if ev_ok(g, e)]
    if elig and random.random() < .85:
        g["event"] = random.choice(elig)

def resoudre(g, ci):
    e = EV[g["event"]]
    lab, p, eo, to, ek, tk = e[4][ci]
    if random.random() < p:
        ap(g, eo); L(g, f"✅ {lab} → {to}")
    else:
        ap(g, ek); L(g, f"❌ {lab} → {tk}")
    g["event"] = None
    if g["sante"] <= 0:
        mort(g, "Tué par les événements de la vie.")

def duel(g, niv, nom):
    mine = puissance(g) * random.uniform(.8, 1.2)
    foe = (5 + g["age"] * 1.5 + rang(g)[0] * 15) * niv * random.uniform(.8, 1.2)
    if mine >= foe:
        g["wins"] += 1
        ap(g, {"xp": int(10 * niv) + 5, "rep": 3, "argent": 30})
        L(g, f"⚔️ Tu bats {nom} ! (puissance {int(mine)} vs {int(foe)})")
        return True
    else:
        ap(g, {"sante": -random.randint(8, 20), "bonheur": -3})
        L(g, f"💥 {nom} te bat... (puissance {int(mine)} vs {int(foe)})")
        if g["sante"] <= 0:
            mort(g, f"Tué lors d'un duel contre {nom}.")
        return False

def choisir(g, ch, nom):
    lab, p, eo, to, ek, tk = ch
    ok = random.random() < p
    eff = dict(eo if ok else ek)
    d = eff.pop("gmi", 0)
    g["gm"][nom] = max(0, min(100, g["gm"][nom] + d))
    ap(g, eff)
    L(g, f"{'💬' if ok else '😬'} {nom} — {lab} : {to if ok else tk}")

def opp_niv(g, opp):
    return 0.9 + 0.5 * list(g["fact"]).index(opp) / max(1, len(g["fact"]) - 1)

def adversaires(g):
    own = GM[g["recrue"]][0] if g["recrue"] else None
    return [n for n in g["fact"] if n != own]

def demarrer_match(g, opp, cup=False):
    g["match"] = dict(opp=opp, q=1, me=0, en=0, talent=0, zone=False, cup=cup, lines=[], fini=False)

def talent_usages(g):
    return 2 if g["talent"] and g["talent"]["lvl"] >= 3 else 1

def jouer_quart(g, tac):
    m = g["match"]
    allies = sum(f["allie"] for f in g["fact"].values())
    a = 12 + puissance(g) * .18 + 3 * allies
    b = (12 + g["age"] * .4 + rang(g)[0] * 4) * opp_niv(g, m["opp"])
    tag = ""
    if m["zone"]:
        a += 5 * g["zone"]; tag += " ⚡Zone"
    if tac == "def":
        a *= .9; b *= .75; tag += " 🛡️Défense"
    elif tac == "duo" and g["recrue"]:
        a += 12; g["gm"][g["recrue"]] = min(100, g["gm"][g["recrue"]] + 2); tag += f" 🌟Duo avec {g['recrue']}"
    elif tac == "talent" and g["talent"] and m["talent"] < talent_usages(g):
        t = g["talent"]; mm, ad, ma = TALENT_FX[t["k"]]; f = .6 + .1 * t["lvl"]
        a = a * (1 + (mm - 1) * f * 2) + ad * f * 2
        b *= 1 - (1 - ma) * f * 1.5
        m["talent"] += 1; tag += f" {TALENTS[t['k']][1]}{TALENTS[t['k']][0]}"
    qa = int(a * random.uniform(.8, 1.2))
    qb = int(b * random.uniform(.8, 1.2))
    m["me"] += qa; m["en"] += qb
    m["lines"].append(f"Q{m['q']} : {qa}-{qb}{tag}")
    m["q"] += 1
    if m["q"] > 4:
        finir_match(g)

def finir_match(g):
    m = g["match"]
    me, en = m["me"], m["en"]
    if m["zone"]:
        ap(g, {"sante": -6 * g["zone"]})
    if me == en:
        me += random.choice([-2, 2])
    win = me > en
    k = 1.5 if m["cup"] else 1
    if win:
        ap(g, {"xp": int(25 * k), "rep": int(6 * k), "argent": int(80 * k), "bonheur": 4})
        L(g, f"🏀 Victoire {me}-{en} contre {m['opp']} !")
    else:
        ap(g, {"xp": 5, "bonheur": -5})
        L(g, f"😞 Défaite {me}-{en} contre {m['opp']}.")
    m["fini"] = True
    m["res"] = [win, me, en]
    if m["cup"] and g["cup"]:
        c = g["cup"]
        if win:
            c["i"] += 1
            if c["i"] >= len(c["opps"]):
                ap(g, COMP[c["key"]][3])
                L(g, f"🏆 Tu remportes la {c['nom']} !")
                g["cup"] = None
        else:
            L(g, f"❌ Tu es éliminé de la {c['nom']} en {c['rounds'][c['i']].lower()}.")
            g["cup"] = None
    if g["sante"] <= 0:
        mort(g, "Épuisé par l'effort de la Zone.")

def demarrer_cup(g, key):
    nom, _, rounds, rew = COMP[key]
    g["cal"][key] = False
    pool = adversaires(g)
    opps = sorted(random.sample(pool, len(rounds)), key=lambda n: opp_niv(g, n))
    g["cup"] = dict(key=key, nom=nom, rounds=rounds, opps=opps, i=0)
    L(g, f"📣 Tu t'inscris à la {nom} !")
    demarrer_match(g, opps[0], True)

def action(g, eff, txt):
    if g["pa"] <= 0:
        st.toast("Plus d'actions cette année ! Fais vieillir ton personnage.", icon="⏳"); return
    g["pa"] -= 1
    ap(g, eff)
    L(g, txt)
    st.rerun()

# ───────────────────────── INTERFACE ─────────────────────────
if "g" not in st.session_state:
    st.session_state.g = None
g = st.session_state.g

if g is None:
    st.title("🍥🏀🏍️ Shinobi Life")
    st.caption("Vis une vie complète année par année, de la naissance à la mort, façon BitLife.")
    nom = st.text_input("Nom de ton personnage", "Kenji")
    u = st.selectbox("Choisis ton univers", list(UNIV), format_func=lambda x: f"{UNIV[x]['icon']} {x}")
    if st.button("🌱 Naître", use_container_width=True):
        st.session_state.g = new_game(nom or "Anonyme", u)
        st.session_state["dl"] = []
        st.rerun()
    up = st.file_uploader("…ou charge une sauvegarde (.json)", type="json")
    if up is not None and st.button("📂 Charger"):
        data = json.load(up)
        if data.get("v") in (5, 6):
            st.session_state.g = data
            st.rerun()
        else:
            st.error("Sauvegarde d'une ancienne version, incompatible.")
    st.stop()

for _k, _v in (("match", None), ("cup", None), ("cal", {})):
    g.setdefault(_k, _v)

fxn = st.session_state.pop("fx", None)
if fxn == "win":
    st.balloons()
agg = {}
for k, v in st.session_state.pop("dl", []):
    if k in ICON and isinstance(v, int):
        agg[k] = agg.get(k, 0) + v
msg = " · ".join(f"{ICON[k]} {v:+d}" for k, v in agg.items() if v)
if msg:
    st.toast(msg)

U = UNIV[g["u"]]
ri, rn = rang(g)
st.title(f"{U['icon']} {g['nom']} — {g['age']} an{'s' if g['age'] > 1 else ''}")
st.markdown(f'<div class="scene"><span class="sprite s-{U["cls"]}">{U["icon"]}</span></div>', unsafe_allow_html=True)
bj = f" • {g['biju']['ico']} Jinchūriki" if g["biju"] else ""
if g["akatsuki"]:
    bj += " • 🌑 Akatsuki"
if g["talent"]:
    bj += f" • {TALENTS[g['talent']['k']][1]} {TALENTS[g['talent']['k']][0]}"
if g["recrue"]:
    bj += f" • 🌟 Recruté par {g['recrue']}"
st.caption(f"{stage(g)} • {g['u']} • **{rn}**{bj} • 💴 {g['argent']} {U['monnaie']} • XP {g['xp']} • Actions : {g['pa']}")
cols = st.columns(2)
for i, (k, lab) in enumerate([x for x in STATS if x[0] != "chakra" or g["u"] == "Naruto"]):
    cols[i % 2].progress(g[k] / 100, text=f"{lab} : {g[k]}")
st.progress((g["karma"] + 100) / 200, text=f"☯️ Karma : {g['karma']} ({karma_label(g['karma'])})")

if g["dead"]:
    if not g.get("fx_dead"):
        st.snow()
        g["fx_dead"] = True
    st.error(f"💀 {g['nom']} est mort à {g['age']} ans. {g['cause']}")
    st.metric("Score final", score(g))
    with st.expander("Journal de vie", expanded=True):
        cur = None
        for a, t in reversed(g["log"][-60:]):
            if a != cur:
                st.markdown(f"**Âge {a}**"); cur = a
            st.write(t)
    if st.button("🔄 Nouvelle vie", use_container_width=True):
        st.session_state.g = None
        st.rerun()
    st.stop()

if g["event"] is not None:
    e = EV[g["event"]]
    st.markdown(f'<div class="ev-card">📣 <b>Événement</b> — {e[3]}</div>', unsafe_allow_html=True)
    for i, c in enumerate(e[4]):
        if st.button(c[0], key=f"ev{i}", use_container_width=True):
            resoudre(g, i)
            st.rerun()
    st.stop()

def ecran_match(g):
    m = g["match"]
    st.markdown(f"### 🏀 Toi vs {m['opp']}" + (" — 🏆 compétition" if m["cup"] else ""))
    c1, c2 = st.columns(2)
    c1.metric("Toi", m["me"])
    c2.metric(m["opp"], m["en"])
    st.progress(min(1.0, (m["q"] - 1) / 4), text=f"Quart-temps {min(m['q'], 4)}/4")
    for l in m["lines"]:
        st.write(l)
    if m["fini"]:
        win, me, en = m["res"]
        (st.success if win else st.error)(f"{'🏆 Victoire' if win else '😞 Défaite'} {me}-{en}")
        if st.button("Continuer", use_container_width=True):
            g["match"] = None
            st.rerun()
        return
    if g["zone"] >= 1 and not m["zone"] and m["q"] >= 2:
        if st.button(f"⚡ Entrer dans la Zone (coûte {6 * g['zone']} santé en fin de match)", use_container_width=True):
            m["zone"] = True
            st.rerun()
    if m["zone"]:
        st.info("⚡ Tu es dans la Zone : bonus à chaque quart-temps.")
    st.caption("Choisis ta tactique pour ce quart-temps :")
    b = st.columns(2)
    tac = None
    if b[0].button("⚔️ Attaquer", use_container_width=True): tac = "att"
    if b[1].button("🛡️ Défendre", use_container_width=True): tac = "def"
    if g["talent"]:
        td = TALENTS[g["talent"]["k"]]
        reste = talent_usages(g) - m["talent"]
        if b[0].button(f"{td[1]} Talent : {td[0]} ({reste})", use_container_width=True, disabled=reste <= 0): tac = "talent"
    if g["recrue"]:
        if b[1].button(f"🌟 Duo avec {g['recrue']}", use_container_width=True): tac = "duo"
    if tac:
        jouer_quart(g, tac)
        st.rerun()

def tournoi(g):
    ph = st.empty()
    for nom, niv in (("Quart de finale", .8), ("Demi-finale", 1.1), ("Finale", 1.4)):
        ph.info(f"🥊 {nom} : le combat commence !")
        time.sleep(.9)
        if not duel(g, niv, nom) or g["dead"]:
            ph.error(f"💥 Éliminé en {nom.lower()}.")
            return
        ph.success(f"✅ {nom} remportée !")
        time.sleep(.7)
    ap(g, {"argent": 300, "rep": 15, "xp": 60})
    L(g, "🏆 Tu remportes le tournoi de combat clandestin !")
    ph.success("🏆 Champion du tournoi clandestin !")

names = (["📖 Vie", "🏋️ Actions", "👥 Liens", "🌀 Techniques"] + (["🦊 Bijū"] if g["u"] == "Naruto" else [])
         + (["🌑 Akatsuki"] if g["akatsuki"] else []) + (["🏟️ Matchs", "⭐ Miracles"] if g["u"] == "Kuroko" else [])
         + (["🥊 Dojo"] if g["u"] == "Tokyo Revengers" else []) + ["🤝 Alliances", "🛒 Boutique", "🏆 Défis", "💾 Sauver"])
T = dict(zip(names, st.tabs(names)))

with T["📖 Vie"]:
    if st.button("⏩ Vieillir d'un an", type="primary", use_container_width=True):
        vieillir(g)
        st.rerun()
    cur = None
    for a, t in reversed(g["log"][-40:]):
        if a != cur:
            st.markdown(f"**Âge {a}**"); cur = a
        st.write(t)

with T["🏋️ Actions"]:
    st.subheader("Actions de l'année")
    acts = [
        ("🧸 Jouer", 0, {"bonheur": 4}, "🧸 Tu joues et tu t'amuses."),
        ("📚 Étudier", 5, {"intel": 4, "bonheur": -1}, "📚 Tu étudies sérieusement."),
        ("💪 Entraînement physique", 6, {"force": 4, "sante": -1}, "💪 Séance intense."),
        (f"🎯 Travailler le {U['mait'].lower()}", 6, {"mait": 4, "sante": -1}, f"🎯 Tu progresses en {U['mait'].lower()}."),
        ("🧘 Méditer (chakra)", 6, {"chakra": 4}, "🧘 Ton chakra se renforce."),
        ("😴 Se reposer", 0, {"sante": 6, "bonheur": 3}, "😴 Repos bien mérité."),
    ]
    acts = [x for x in acts if g["u"] == "Naruto" or "chakra" not in x[2]]
    cc = st.columns(2)
    for i, (lab, mn, eff, txt) in enumerate(acts):
        ok = g["age"] >= mn
        if cc[i % 2].button(lab if ok else f"🔒 {lab} (dès {mn} ans)", key=f"a{i}", disabled=not ok, use_container_width=True):
            action(g, eff, txt)
    ja = U["jobage"]
    if cc[0].button(f"💼 {U['job']}" if g["age"] >= ja else f"🔒 {U['job']} (dès {ja} ans)", disabled=g["age"] < ja, use_container_width=True):
        gain = random.randint(30, 80) * (1 + ri)
        action(g, {"argent": gain, "xp": 5}, f"💼 {U['job']} : +{gain} {U['monnaie']}.")
    st.markdown("**☯️ Actions morales**")
    k1, k2 = st.columns(2)
    if k1.button("🤲 Aider un inconnu" if g["age"] >= 8 else "🔒 Aider (dès 8 ans)", disabled=g["age"] < 8, use_container_width=True):
        action(g, {"karma": 5, "bonheur": 2}, "🤲 Tu aides un inconnu, ça fait du bien.")
    if k2.button("🎗️ Faire un don (50)" if g["age"] >= 10 else "🔒 Don (dès 10 ans)", disabled=g["age"] < 10, use_container_width=True):
        if g["argent"] >= 50:
            action(g, {"argent": -50, "karma": 6, "bonheur": 3}, "🎗️ Tu fais un don à un orphelinat.")
        else:
            st.toast("Pas assez d'argent.", icon="💴")
    if k1.button("😈 Intimider un camarade" if g["age"] >= 8 else "🔒 Intimider (dès 8 ans)", disabled=g["age"] < 8, use_container_width=True):
        action(g, {"karma": -6, "rep": 2, "bonheur": -1}, "😈 Tu intimides un camarade.")
    if k2.button("🗡️ Voler un marchand" if g["age"] >= 10 else "🔒 Voler (dès 10 ans)", disabled=g["age"] < 10, use_container_width=True):
        if random.random() < .65:
            gain = random.randint(40, 120)
            action(g, {"argent": gain, "karma": -8}, f"🗡️ Tu voles un marchand : +{gain}.")
        else:
            action(g, {"rep": -10, "bonheur": -5, "karma": -3}, "🚨 Tu te fais prendre en train de voler !")
    st.divider()
    if g["nat"]:
        st.subheader("Entraîner une nature de chakra")
        n = st.selectbox("Nature", list(g["nat"]), format_func=lambda x: f"{NAT[x]} {x} (niv. {g['nat'][x]})")
        if st.button("✨ S'entraîner", use_container_width=True):
            lvl = g["nat"][n]
            if g["pa"] <= 0:
                st.toast("Plus d'actions !", icon="⏳")
            elif lvl >= 5:
                st.toast("Niveau maximum atteint.", icon="🏆")
            else:
                g["pa"] -= 1
                if random.random() < max(.2, .75 - .12 * lvl + g["chakra"] / 300):
                    g["nat"][n] += 1
                    L(g, f"✨ {NAT[n]} {n} passe niveau {g['nat'][n]} !")
                    debloquer_rares(g)
                else:
                    L(g, f"😓 L'entraînement de {n} n'a pas porté ses fruits.")
                    ap(g, {"sante": -2})
                st.rerun()
    elif g["u"] == "Naruto":
        st.info("Ton chakra s'éveillera à 6 ans.")

with T["👥 Liens"]:
    st.subheader("Relations")
    if g["couple"]:
        st.success(f"💞 En couple avec {g['couple']}")
    for i, p in enumerate(g["pnj"]):
        ico = {"ami": "🤝", "rival": "😤", "amour": "💗", "famille": "👪"}[p["role"]]
        with st.expander(f"{ico} {p['nom']} — affinité {p['aff']}"):
            c1, c2 = st.columns(2)
            if c1.button("💬 Discuter", key=f"d{i}"):
                if g["pa"] > 0:
                    g["pa"] -= 1; p["aff"] = min(100, p["aff"] + 8)
                    L(g, f"💬 Tu passes du temps avec {p['nom']}."); ap(g, {"bonheur": 3}); st.rerun()
            if c2.button("🎁 Offrir un cadeau", key=f"g{i}"):
                if g["cadeau"] > 0:
                    g["cadeau"] -= 1; p["aff"] = min(100, p["aff"] + 15)
                    L(g, f"🎁 {p['nom']} adore ton cadeau !"); st.rerun()
                else:
                    st.toast("Achète un cadeau en boutique.", icon="🛒")
            if p["role"] in ("ami", "rival"):
                if c1.button("⚔️ Défier en duel" if g["age"] >= 7 else "🔒 Duel (dès 7 ans)", key=f"x{i}", disabled=g["age"] < 7):
                    if g["pa"] > 0:
                        g["pa"] -= 1; duel(g, p["niv"], p["nom"]); st.rerun()
            if p["role"] == "famille" and g["age"] >= 6:
                if c1.button("💰 Argent de poche", key=f"m{i}"):
                    if g["pa"] > 0:
                        g["pa"] -= 1
                        if random.random() < p["aff"] / 100:
                            s = random.randint(10, 30) * g["riche"]; g["argent"] += s
                            L(g, f"💰 {p['nom']} te donne {s} {U['monnaie']}.")
                        else:
                            L(g, f"🙅 {p['nom']} refuse de te donner de l'argent.")
                        st.rerun()
            if p["role"] == "amour" and not g["couple"] and g["age"] >= 13:
                if c2.button("💍 Se déclarer", key=f"l{i}"):
                    if random.random() < p["aff"] / 100:
                        g["couple"] = p["nom"]; ap(g, {"bonheur": 15})
                        L(g, f"💞 {p['nom']} accepte ! Vous êtes en couple.")
                    else:
                        ap(g, {"bonheur": -8}); L(g, f"💔 {p['nom']} refuse tes sentiments.")
                    st.rerun()

with T["🌀 Techniques"]:
    if g["u"] == "Naruto":
        st.subheader("🌀 Natures de chakra")
        if g["nat"]:
            for n, l in g["nat"].items():
                st.write(f"{NAT[n]} **{n}** — niveau {l}/5")
        else:
            st.write("Aucune nature éveillée pour l'instant (éveil à 6 ans).")
        st.caption("Fusion à partir de 15 ans : Eau + Vent (niv. 3) → Glace, Terre + Eau (niv. 3) → Bois.")
    st.subheader("⚔️ Techniques")
    for k, t in TECH.items():
        if t["u"] != g["u"]:
            continue
        r = t["req"]
        if r[0] == "nat":
            ok, req_txt = g["nat"].get(r[1], 0) >= r[2], f"{NAT[r[1]]} {r[1]} niv. {r[2]}"
        elif r[0] == "pup":
            ok, req_txt = r[1] in g["pupilles"], f"pupille {r[1]}"
        else:
            ok, req_txt = g.get(r[0], 0) >= r[1], f"{r[0]} ≥ {r[1]}"
        if k in g["tech"]:
            st.success(f"✅ {t['n']} (puissance +{t['pw']})")
        else:
            c1, c2 = st.columns([3, 1])
            c1.write(f"**{t['n']}** — +{t['pw']} puissance — dès {t['a']} ans — requis : {req_txt} — {t['p']} 💴")
            if c2.button("Apprendre", key=f"t{k}", disabled=not ok or g["age"] < t["a"]):
                if g["argent"] >= t["p"]:
                    g["argent"] -= t["p"]; g["tech"].append(k)
                    L(g, f"📖 Technique apprise : {t['n']} !"); st.rerun()
                else:
                    st.toast("Pas assez d'argent.", icon="💴")
    st.metric("Puissance totale", int(puissance(g)))

if "🦊 Bijū" in T:
    with T["🦊 Bijū"]:
        b = g["biju"]
        if not b:
            st.info("Tu n'abrites aucun bijū. Un événement rare peut survenir au fil des années (plus fréquent dans l'univers Naruto) : une bête à queues peut choisir de se sceller en toi.")
        else:
            st.subheader(f"{b['ico']} {b['nom']}")
            st.progress(b["lien"] / 100, text=f"Lien avec le bijū : {b['lien']}/100")
            st.caption("Sous 25, le bijū risque de prendre le contrôle. À 60, tu débloques le Mode Bijū (gros bonus de puissance).")
            if b["lien"] >= 60:
                st.success("🔥 Mode Bijū débloqué !")
            c1, c2 = st.columns(2)
            if c1.button("🗣️ Dialoguer avec lui", use_container_width=True):
                action(g, {"lien": 6, "bonheur": 2}, "🗣️ Tu discutes avec ton bijū, la confiance grandit.")
            if c2.button("🧘 Méditer dans ton esprit", use_container_width=True):
                action(g, {"lien": 4, "chakra": 3}, "🧘 Tu rencontres ton bijū dans ton monde intérieur.")
            if st.button("🔥 Puiser dans sa puissance", use_container_width=True):
                if g["pa"] <= 0:
                    st.toast("Plus d'actions !", icon="⏳")
                else:
                    g["pa"] -= 1
                    if random.random() < .3 + b["lien"] / 150:
                        ap(g, {"xp": 30, "chakra": 8, "rep": 3, "lien": -2})
                        L(g, "🔥 Tu maîtrises la puissance du bijū !")
                    else:
                        ap(g, {"sante": -25, "lien": -6})
                        L(g, "💢 La puissance du bijū te dépasse, tu es blessé.")
                        if g["sante"] <= 0:
                            mort(g, "Consumé par la puissance de son bijū.")
                    st.rerun()

if "🌑 Akatsuki" in T:
    with T["🌑 Akatsuki"]:
        st.subheader("🌑 Akatsuki")
        st.caption("Tu es un déserteur : ton village te traque, mais l'organisation t'offre des missions sombres.")
        if g["pupilles"]:
            st.write("👁️ Pupilles volées : " + ", ".join(f"{PUP[n][0]} {n}" for n in g["pupilles"]))
        restantes = [n for n in PUP if n not in g["pupilles"]]
        if restantes:
            cible = st.selectbox("Pupille à voler", restantes, format_func=lambda n: f"{PUP[n][0]} {n} (difficulté {PUP[n][1]})")
            pch = int(100 * min(.9, max(.15, puissance(g) / PUP[cible][1] * .6)))
            st.caption(f"Chances de succès estimées : {pch}%")
            if st.button("👁️ Voler la pupille", use_container_width=True):
                if g["pa"] <= 0:
                    st.toast("Plus d'actions !", icon="⏳")
                else:
                    g["pa"] -= 1
                    if random.random() < pch / 100:
                        g["pupilles"].append(cible)
                        ap(g, {"karma": -15, "xp": 40, "rep": -3})
                        L(g, f"👁️ Tu voles le {cible} ! Ta puissance grandit.")
                    else:
                        ap(g, {"sante": -30, "karma": -5})
                        L(g, f"💢 Tu échoues à voler le {cible} et tu es gravement blessé.")
                        if g["sante"] <= 0:
                            mort(g, "Tué en tentant de voler une pupille.")
                    st.rerun()
        else:
            st.success("Tu possèdes toutes les pupilles légendaires.")
        if st.button("🦊 Traquer un jinchūriki", use_container_width=True):
            if g["pa"] <= 0:
                st.toast("Plus d'actions !", icon="⏳")
            else:
                g["pa"] -= 1
                if random.random() < min(.85, max(.15, puissance(g) / 150)):
                    ap(g, {"argent": 300, "xp": 50, "karma": -20})
                    L(g, "🦊 Tu captures un jinchūriki pour l'organisation. Récompense : 300.")
                else:
                    ap(g, {"sante": -30, "karma": -5})
                    L(g, "💢 Le jinchūriki te repousse violemment.")
                    if g["sante"] <= 0:
                        mort(g, "Tué par un jinchūriki.")
                st.rerun()
        if st.button("🚪 Quitter l'organisation", use_container_width=True):
            if random.random() < .5:
                g["akatsuki"] = False
                ap(g, {"karma": 10})
                L(g, "🚪 Tu réussis à quitter l'Akatsuki.")
            else:
                ap(g, {"sante": -40})
                L(g, "🔪 L'organisation te punit pour ta tentative de fuite.")
                if g["sante"] <= 0:
                    mort(g, "Éliminé par l'Akatsuki pour trahison.")
            st.rerun()

if "⭐ Miracles" in T:
    with T["⭐ Miracles"]:
        tl = g["talent"]
        td = TALENTS[tl["k"]]
        st.subheader(f"{td[1]} Talent inné : {td[0]}")
        st.caption(td[2])
        st.progress(tl["lvl"] / 5, text=f"Niveau du talent : {tl['lvl']}/5 (+{td[4] * tl['lvl']} puissance)")
        if st.button("🔥 Entraîner mon talent", use_container_width=True, disabled=g["age"] < 6 or tl["lvl"] >= 5):
            if g["pa"] <= 0:
                st.toast("Plus d'actions !", icon="⏳")
            else:
                g["pa"] -= 1
                if random.random() < max(.2, .75 - .12 * tl["lvl"]):
                    tl["lvl"] += 1
                    ap(g, {"mait": 2})
                    L(g, f"✨ Ton talent « {td[0]} » passe niveau {tl['lvl']} !")
                else:
                    L(g, "😓 Ton talent refuse de progresser cette année.")
                st.rerun()
        if g["age"] < 6:
            st.caption("🔒 Entraînement du talent dès 6 ans.")
        st.divider()
        st.subheader("⭐ Génération des Miracles")
        if g["recrue"]:
            r = g["recrue"]
            st.success(f"🌟 Tu es recruté par {r} ({GM[r][0]}) : +12 puissance, +10 XP et +2 réputation par an.")
            st.markdown(f"**🤝 Équipe de {r}**")
            b1, b2, b3 = st.columns(3)
            if b1.button("🏋️ Duo d'entraînement", use_container_width=True):
                g["gm"][r] = min(100, g["gm"][r] + 5)
                action(g, {"mait": 6, "force": 3, "sante": -3}, f"🏋️ Entraînement intensif avec {r}.")
            if b2.button("🎯 Perfectionner mon talent", use_container_width=True):
                if g["pa"] <= 0:
                    st.toast("Plus d'actions !", icon="⏳")
                else:
                    g["pa"] -= 1
                    if tl["lvl"] < 5 and random.random() < .6:
                        tl["lvl"] += 1
                        L(g, f"✨ {r} t'aide à faire progresser ton talent (niveau {tl['lvl']}) !")
                    else:
                        ap(g, {"mait": 3})
                        L(g, f"🎯 {r} te donne des conseils précieux.")
                    st.rerun()
            if b3.button("🍜 Sortir manger", use_container_width=True):
                action(g, {"bonheur": 6, "rep": 2}, f"🍜 Tu passes la soirée avec {r}.")
        else:
            st.caption("Impressionne-les en 1 contre 1. À 60 d'intérêt, 30 de réputation et 50 de maîtrise, tu peux demander à les rejoindre. Ils peuvent aussi te repérer par eux-mêmes (13-18 ans).")
        use_t = st.checkbox(f"{td[1]} Activer mon talent pendant les 1 contre 1 (−3 santé)")
        for n, (lyc, niv, tal) in GM.items():
            it = g["gm"][n]
            with st.expander(f"{n} — {lyc} — intérêt {it}" + (" 🌟" if n == g["recrue"] else "")):
                st.caption(f"Talent : {tal}")
                st.progress(it / 100)
                i = st.selectbox("Que lui dire ?", list(range(len(TALK[n]))), format_func=lambda j, n=n: TALK[n][j][0], key=f"tk{n}")
                if st.button("💬 Lui parler", key=f"tb{n}", disabled=g["age"] < 8, use_container_width=True):
                    if g["pa"] <= 0:
                        st.toast("Plus d'actions !", icon="⏳")
                    else:
                        g["pa"] -= 1
                        choisir(g, TALK[n][i], n)
                        st.rerun()
                c1, c2 = st.columns(2)
                if c1.button("🏀 Défier en 1 contre 1", key=f"gm{n}", disabled=g["age"] < 13):
                    if g["pa"] <= 0:
                        st.toast("Plus d'actions !", icon="⏳")
                    else:
                        g["pa"] -= 1
                        mine = puissance(g) * random.uniform(.8, 1.2)
                        if use_t:
                            mine *= 1 + .08 * tl["lvl"]
                            ap(g, {"sante": -3})
                        foe = (30 + niv * 35) * random.uniform(.85, 1.15)
                        if mine >= foe:
                            g["gm"][n] = min(100, it + 18)
                            ap(g, {"rep": 8, "xp": 25})
                            L(g, f"🏀 Victoire en 1 contre 1 contre {n} ! Il te remarque." + (f" ({td[1]} talent activé)" if use_t else ""))
                        else:
                            g["gm"][n] = min(100, it + 6)
                            ap(g, {"sante": -5, "bonheur": -3})
                            L(g, f"😞 {n} te bat en 1 contre 1, mais apprécie ta combativité.")
                        st.rerun()
                if not g["recrue"] and c2.button("🤝 Demander à rejoindre", key=f"gr{n}", disabled=g["age"] < 14):
                    if it < 60 or g["rep"] < 30 or g["mait"] < 50:
                        st.toast("Il faut intérêt ≥ 60, réputation ≥ 30 et maîtrise ≥ 50.", icon="🔒")
                    elif random.random() < min(.9, .6 + it / 300):
                        recruter(g, n)
                        st.rerun()
                    else:
                        g["gm"][n] = max(0, it - 10)
                        L(g, f"🙅 {n} refuse pour l'instant ta demande.")
                        st.rerun()

with T["🤝 Alliances"]:
    nal = sum(f["allie"] for f in g["fact"].values())
    st.subheader(f"🤝 Alliances ({nal}/3)")
    st.caption("Chaque allié : +7 puissance, +XP, +réputation et +argent chaque année. Un karma très bas fait fuir tes alliés.")
    for n, f in g["fact"].items():
        with st.expander(f"{'🤝' if f['allie'] else '⚔️'} {n} — relation {f['rel']}"):
            st.progress(f["rel"] / 100)
            c1, c2 = st.columns(2)
            if c1.button("🎁 Offrir un tribut (80)", key=f"tr{n}", disabled=g["age"] < 10):
                if g["argent"] >= 80 and g["pa"] > 0:
                    g["argent"] -= 80; g["pa"] -= 1; f["rel"] = min(100, f["rel"] + 12)
                    L(g, f"🎁 {n} apprécie ton tribut."); st.rerun()
                else:
                    st.toast("Il faut 80 d'argent et une action.", icon="💴")
            if not f["allie"]:
                cout = 100 * (nal + 1)
                pa_ = int(100 * min(.9, f["rel"] / 100 * .8 + g["rep"] / 250))
                c2.caption(f"Coût {cout} • chances {pa_}%")
                if c2.button("📜 Proposer une alliance", key=f"al{n}", disabled=g["age"] < 12 or nal >= 3):
                    if g["argent"] < cout or g["pa"] <= 0:
                        st.toast("Argent ou action insuffisant.", icon="💴")
                    else:
                        g["argent"] -= cout; g["pa"] -= 1
                        if random.random() < pa_ / 100:
                            f["allie"] = True; ap(g, {"rep": 5})
                            L(g, f"🤝 Alliance conclue avec {n} !")
                        else:
                            f["rel"] = max(0, f["rel"] - 5)
                            L(g, f"🙅 {n} refuse ton alliance.")
                        st.rerun()
            elif c2.button("🗡️ Trahir cet allié", key=f"bt{n}"):
                f["allie"] = False; f["rel"] = 0
                ap(g, {"karma": -20, "argent": 200, "rep": -10})
                L(g, f"🗡️ Tu trahis {n} et pille leurs ressources.")
                st.rerun()

if "🏟️ Matchs" in T:
    with T["🏟️ Matchs"]:
        if g["match"]:
            ecran_match(g)
        else:
            if g["cup"]:
                c = g["cup"]
                st.info(f"🏆 {c['nom']} en cours — {c['rounds'][c['i']]} contre {c['opps'][c['i']]} ({c['i'] + 1}/{len(c['opps'])})")
                if st.button("▶️ Lancer le match", use_container_width=True):
                    demarrer_match(g, c["opps"][c["i"]], True)
                    st.rerun()
                if st.button("🏳️ Abandonner la compétition", use_container_width=True):
                    L(g, f"🏳️ Tu abandonnes la {c['nom']}.")
                    g["cup"] = None
                    st.rerun()
            else:
                st.subheader("📅 Calendrier de l'année")
                shown = False
                for key, (nom, (a0, a1), rounds, rew) in COMP.items():
                    if g["age"] < a0:
                        st.write(f"🔒 {nom} — dès {a0} ans")
                    elif g["age"] <= a1:
                        shown = True
                        dispo = g["cal"].get(key)
                        c1, c2 = st.columns([3, 1])
                        c1.write(f"{'🟢' if dispo else '✅'} **{nom}** — {len(rounds)} tours — récompense : {rew}")
                        if c2.button("S'inscrire", key=f"cp{key}", disabled=not dispo):
                            if g["pa"] <= 0:
                                st.toast("Plus d'actions !", icon="⏳")
                            else:
                                g["pa"] -= 1
                                demarrer_cup(g, key)
                                st.rerun()
                if g["age"] > 18:
                    st.caption("Plus de compétitions lycéennes à ton âge.")
                if g["age"] >= 13:
                    c1, c2 = st.columns([3, 1])
                    c1.write(f"{'🟢' if g['cal'].get('camp') else '✅'} **🏕️ Camp d'entraînement d'été** — +6 maîtrise, +4 force (150)")
                    if c2.button("Y aller", key="camp", disabled=not g["cal"].get("camp")):
                        if g["argent"] < 150:
                            st.toast("Pas assez d'argent.", icon="💴")
                        else:
                            g["argent"] -= 150
                            g["cal"]["camp"] = False
                            action(g, {"mait": 6, "force": 4, "sante": -4}, "🏕️ Tu passes une semaine intense au camp d'été.")
                st.divider()
                st.subheader("⚡ La Zone")
                st.progress(g["zone"] / 3, text=f"Niveau de Zone : {ZONES[g['zone']]}")
                if g["zone"] < 3:
                    r = ZONE_REQ[g["zone"] + 1]
                    st.caption(f"Prochain niveau ({ZONES[g['zone'] + 1]}) : {g['zxp']}/{r[0]} entraînements, maîtrise ≥ {r[1]}, âge ≥ {r[2]}.")
                st.caption("Tu actives la Zone pendant un match, à partir du 2e quart-temps.")
                if st.button("🧘 S'entraîner à entrer dans la Zone", use_container_width=True, disabled=g["age"] < 14 or g["zone"] >= 3):
                    if g["pa"] <= 0:
                        st.toast("Plus d'actions !", icon="⏳")
                    elif g["mait"] < 40:
                        L(g, "🧘 Ta maîtrise est trop faible pour approcher la Zone.")
                        g["pa"] -= 1; st.rerun()
                    else:
                        g["pa"] -= 1
                        if random.random() < .6 + g["intel"] / 300:
                            g["zxp"] += 1
                            r = ZONE_REQ[g["zone"] + 1]
                            if g["zxp"] >= r[0] and g["mait"] >= r[1] and g["age"] >= r[2]:
                                g["zone"] += 1
                                ap(g, {"mait": 5})
                                L(g, f"✨ Tu atteins le niveau : {ZONES[g['zone']]} !")
                            else:
                                L(g, "🧘 Tu approches de la Zone...")
                        else:
                            L(g, "😓 Impossible de te concentrer aujourd'hui.")
                        st.rerun()
                if g["age"] < 14:
                    st.caption("🔒 Entraînement de la Zone dès 14 ans.")
                st.divider()
                st.subheader("🏀 Match amical")
                opps = adversaires(g)
                if g["recrue"]:
                    st.caption(f"Tu ne peux pas affronter {GM[g['recrue']][0]} : c'est ton équipe.")
                opp = st.selectbox("Adversaire", opps)
                if st.button("▶️ Jouer le match" if g["age"] >= 12 else "🔒 Matchs dès 12 ans", use_container_width=True, disabled=g["age"] < 12):
                    if g["pa"] <= 0:
                        st.toast("Plus d'actions !", icon="⏳")
                    else:
                        g["pa"] -= 1
                        demarrer_match(g, opp)
                        st.rerun()

if "🥊 Dojo" in T:
    with T["🥊 Dojo"]:
        st.subheader("🥊 Dojo — sports de combat")
        st.caption("Chaque niveau : +3 puissance. Trois sports niveau 2 ou plus : bonus « Polyvalent » (+10). Dès 8 ans.")
        for n, ico in SPORTS.items():
            lvl = g["sports"].get(n, 0)
            cost = 40 * (lvl + 1)
            c1, c2 = st.columns([3, 1])
            c1.progress(lvl / 5, text=f"{ico} {n} — niveau {lvl}/5")
            if c2.button(f"{cost} 💴", key=f"sp{n}", disabled=g["age"] < 8 or lvl >= 5):
                if g["pa"] <= 0:
                    st.toast("Plus d'actions !", icon="⏳")
                elif g["argent"] < cost:
                    st.toast("Pas assez d'argent.", icon="💴")
                else:
                    g["pa"] -= 1; g["argent"] -= cost
                    if random.random() < max(.25, .85 - .12 * lvl):
                        g["sports"][n] = lvl + 1
                        ap(g, {"force": 2, "mait": 2})
                        L(g, f"{ico} Tu progresses en {n} (niveau {lvl + 1}) !")
                    else:
                        ap(g, {"sante": -2})
                        L(g, f"😓 Séance de {n} sans progrès.")
                    st.rerun()
        st.divider()
        if st.button("🏆 Tournoi clandestin (dès 14 ans)", use_container_width=True, disabled=g["age"] < 14):
            if g["pa"] <= 0:
                st.toast("Plus d'actions !", icon="⏳")
            else:
                g["pa"] -= 1
                tournoi(g)

with T["🛒 Boutique"]:
    st.subheader("🛒 Boutique")
    for k, (nm, pr, ds, eff, uu, ag) in SHOP.items():
        if uu and uu != g["u"]:
            continue
        c1, c2 = st.columns([3, 1])
        c1.write(f"**{nm}** — {ds} *(dès {ag} ans)*")
        if c2.button(f"{pr} 💴", key=f"s{k}", disabled=g["age"] < ag):
            if g["argent"] >= pr:
                g["argent"] -= pr
                ap(g, eff)
                L(g, f"🛍️ Achat : {nm}")
                st.rerun()
            else:
                st.toast("Pas assez d'argent.", icon="💴")
    st.caption(f"🎁 Cadeaux : {g['cadeau']} • ⏳ Time Leap : {g['revive']}")

with T["🏆 Défis"]:
    st.subheader("🏆 Défis")
    for did, txt, chk, rew in DEFIS:
        if g["u"] != "Naruto" and did in ("d6", "d8", "d11", "d12", "d14", "d15"):
            continue
        done = did in g["defis_ok"]
        c1, c2 = st.columns([3, 1])
        c1.write(("✅ " if done else "🎯 ") + txt + f"  *(récompense : {rew})*")
        if not done and chk(g) and c2.button("Réclamer", key=f"df{did}"):
            g["defis_ok"].append(did)
            ap(g, rew)
            L(g, f"🏆 Défi réussi : {txt}")
            st.rerun()

with T["💾 Sauver"]:
    st.download_button("💾 Télécharger ma sauvegarde", json.dumps(g, ensure_ascii=False),
                       file_name=f"{g['nom']}_save.json", mime="application/json")
    if st.button("🗑️ Abandonner cette vie"):
        st.session_state.g = None
        st.rerun()
