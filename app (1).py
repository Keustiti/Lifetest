import streamlit as st
import random
import json

st.set_page_config(page_title="Shinobi Life", page_icon="🍥", layout="centered")

# ───────────────────────── DONNÉES ─────────────────────────
UNIV = {
    "Naruto": {
        "icon": "🍥", "mait": "Ninjutsu", "monnaie": "ryōs",
        "job": "Faire une mission",
        "ranks": ["Élève de l'Académie", "Genin", "Chūnin", "Jōnin", "Élite ANBU", "Kage"],
        "intro": "Tu nais dans un village caché où le chakra coule dans toutes les veines.",
        "pnj": ["Haruto", "Mizuki", "Daichi", "Sakura-Hime", "Rentaro"],
    },
    "Kuroko": {
        "icon": "🏀", "mait": "Basket", "monnaie": "yens",
        "job": "Jouer un match rémunéré",
        "ranks": ["Joueur de banc", "Titulaire", "As de l'équipe", "Capitaine", "Génération des Miracles", "Légende du Basket"],
        "intro": "Tu grandis avec un ballon orange entre les mains et des rêves de Winter Cup.",
        "pnj": ["Akira", "Shiori", "Taiga-kun", "Midori", "Seiji"],
    },
    "Tokyo Revengers": {
        "icon": "🏍️", "mait": "Combat", "monnaie": "yens",
        "job": "Faire une ronde du quartier",
        "ranks": ["Simple membre", "Soldat", "Capitaine de division", "Commandant", "Bras droit", "Chef du gang"],
        "intro": "Tu grandis dans les rues de Tokyo, entre gangs, moto et loyauté.",
        "pnj": ["Takeru", "Emma", "Ryuji", "Hinata-chan", "Kazuma"],
    },
}
RANK_TH = [0, 50, 150, 300, 600, 1000]

NAT = {"Feu": "🔥", "Eau": "💧", "Vent": "🌪️", "Foudre": "⚡", "Terre": "🪨", "Glace": "❄️", "Bois": "🌳"}
BASE_NAT = ["Feu", "Eau", "Vent", "Foudre", "Terre"]

STATS = [("sante", "❤️ Santé"), ("bonheur", "😊 Bonheur"), ("intel", "🧠 Intelligence"),
         ("force", "💪 Force"), ("mait", "🎯 Maîtrise"), ("chakra", "🌀 Chakra"), ("rep", "⭐ Réputation")]

TECH = {
    # Naruto
    "clone": dict(n="Multi-clonage", u="Naruto", p=100, req=("mait", 10), pw=5),
    "subst": dict(n="Substitution", u="Naruto", p=150, req=("mait", 15), pw=6),
    "feu": dict(n="Boule de feu suprême", u="Naruto", p=400, req=("nat", "Feu", 2), pw=14),
    "eau": dict(n="Dragon d'eau", u="Naruto", p=400, req=("nat", "Eau", 2), pw=14),
    "vent": dict(n="Lame de vent", u="Naruto", p=400, req=("nat", "Vent", 2), pw=14),
    "foudre": dict(n="Éclair tranchant", u="Naruto", p=800, req=("nat", "Foudre", 3), pw=22),
    "terre": dict(n="Mur de terre", u="Naruto", p=300, req=("nat", "Terre", 2), pw=12),
    "glace": dict(n="Miroirs de glace", u="Naruto", p=1500, req=("nat", "Glace", 1), pw=30),
    "bois": dict(n="Forêt profonde", u="Naruto", p=1500, req=("nat", "Bois", 1), pw=30),
    "sage": dict(n="Mode Sage", u="Naruto", p=3000, req=("mait", 70), pw=40),
    # Kuroko
    "passe": dict(n="Passe fantôme", u="Kuroko", p=200, req=("mait", 20), pw=8),
    "trois": dict(n="Tir à trois points", u="Kuroko", p=400, req=("mait", 30), pw=12),
    "dribble": dict(n="Dribble brise-chevilles", u="Kuroko", p=700, req=("mait", 40), pw=16),
    "meteore": dict(n="Tir météore", u="Kuroko", p=1500, req=("mait", 60), pw=28),
    "zone": dict(n="La Zone", u="Kuroko", p=3000, req=("mait", 70), pw=38),
    # Tokyo Revengers
    "kick": dict(n="Coup de pied circulaire", u="Tokyo Revengers", p=200, req=("force", 25), pw=8),
    "contre": dict(n="Contre-attaque", u="Tokyo Revengers", p=400, req=("force", 35), pw=12),
    "charge": dict(n="Charge de division", u="Tokyo Revengers", p=900, req=("force", 50), pw=20),
    "acier": dict(n="Mental d'acier", u="Tokyo Revengers", p=1500, req=("rep", 50), pw=26),
    "leap": dict(n="Time Leap", u="Tokyo Revengers", p=4000, req=("mait", 70), pw=45),
}

SHOP = {
    "ramen": ("🍜 Bol de ramen", 80, "+15 santé, +5 bonheur", {"sante": 15, "bonheur": 5}, None),
    "boisson": ("🥤 Boisson énergétique", 60, "+1 action cette année", {"pa": 1}, None),
    "chakra": ("📜 Parchemin de chakra", 300, "+10 chakra", {"chakra": 10}, None),
    "manuel": ("📘 Manuel d'entraînement", 400, "+4 force, +4 maîtrise, +3 intel", {"force": 4, "mait": 4, "intel": 3}, None),
    "cadeau": ("🎁 Cadeau", 50, "Pour améliorer une relation", {"cadeau": 1}, None),
    "xp": ("🧪 Potion d'expérience", 500, "+40 XP", {"xp": 40}, None),
    "leap": ("⏳ Amulette Time Leap", 1500, "Te ramène à la vie une fois", {"revive": 1}, None),
    "nature": ("🔮 Parchemin de nature", 1000, "Éveille une nouvelle nature de chakra", {"nature": 1}, None),
    "kunai": ("🗡️ Kunai en acier trempé", 200, "+5 maîtrise", {"mait": 5}, "Naruto"),
    "shoes": ("👟 Chaussures de pro", 300, "+6 maîtrise", {"mait": 6}, "Kuroko"),
    "veste": ("🧥 Veste du gang", 250, "+8 réputation, +3 force", {"rep": 8, "force": 3}, "Tokyo Revengers"),
}

# (univers, âge min, âge max, texte, [(label, p, eff_ok, txt_ok, eff_ko, txt_ko)])
EV = [
    ("Naruto", 7, 12, "Un vieux ninja te voit jongler avec ton chakra et propose de te donner une leçon.",
     [("Accepter", .8, {"mait": 6, "chakra": 4}, "Tu apprends une astuce précieuse.", {"bonheur": -3}, "Il s'endort en plein cours..."),
      ("Refuser poliment", 1, {"bonheur": 2}, "Tu préfères jouer dehors.", {}, "")]),
    ("Naruto", 8, 25, "Mission de rang D : retrouver le chat d'une noble dame.",
     [("Foncer", .7, {"argent": 80, "xp": 10}, "Mission réussie, le chat t'a griffé mais tu es payé !", {"sante": -5, "bonheur": -3}, "Le chat t'a échappé."),
      ("Pister avec le chakra", .9, {"argent": 60, "xp": 12, "chakra": -3}, "Pisté sans effort !", {}, "")]),
    ("Naruto", 12, 20, "L'examen de promotion approche, le jury t'attend.",
     [("Participer", .55, {"xp": 60, "rep": 10}, "Tu réussis l'examen !", {"sante": -10, "bonheur": -8}, "Tu échoues de justesse."),
      ("Attendre l'an prochain", 1, {"intel": 3}, "Tu t'entraînes encore un an.", {}, "")]),
    ("Naruto", 15, 50, "Un ninja déserteur menace le village.",
     [("L'affronter", .5, {"xp": 50, "rep": 15, "argent": 150}, "Tu le mets hors d'état de nuire !", {"sante": -30, "rep": -3}, "Il t'inflige de graves blessures."),
      ("Alerter les anciens", .95, {"xp": 15, "rep": 3}, "Le village est sauvé grâce à ton alerte.", {}, "")]),
    ("Naruto", 6, 60, "Une rumeur parle d'un parchemin interdit caché dans une grotte.",
     [("Y aller", .4, {"chakra": 15, "mait": 8, "xp": 20}, "Tu trouves le parchemin !", {"sante": -20, "bonheur": -5}, "Piège ! Tu t'en sors de justesse."),
      ("Ignorer", 1, {}, "Tu restes prudent.", {}, "")]),
    ("Kuroko", 12, 15, "Le coach te propose de rejoindre l'équipe de basket du collège.",
     [("Rejoindre", .85, {"mait": 8, "force": 3, "rep": 3}, "Tu intègres l'équipe !", {"bonheur": -4}, "Tu finis sur le banc."),
      ("Passer", 1, {"intel": 2}, "Tu te concentres sur les études.", {}, "")]),
    ("Kuroko", 15, 18, "Match d'entraînement contre un lycée rival.",
     [("Jouer à fond", .6, {"mait": 6, "xp": 25, "rep": 6}, "Victoire !", {"bonheur": -6, "sante": -5}, "Défaite amère."),
      ("Rester sur le banc", 1, {"bonheur": -1}, "Tu regardes le match.", {}, "")]),
    ("Kuroko", 15, 18, "La Winter Cup commence !",
     [("Participer", .5, {"xp": 70, "rep": 15, "argent": 120}, "Ton équipe brille au tournoi !", {"bonheur": -10}, "Éliminés dès le premier tour."),
      ("Soutenir depuis les gradins", 1, {"bonheur": 3}, "Tu encourages l'équipe.", {}, "")]),
    ("Kuroko", 13, 40, "Un prodige te propose un 1 contre 1 sur un playground.",
     [("Relever le défi", .45, {"mait": 10, "rep": 8}, "Tu l'accroches jusqu'au bout !", {"mait": 4, "bonheur": -5}, "Écrasé, mais tu as appris."),
      ("Refuser", 1, {}, "Pas aujourd'hui.", {}, "")]),
    ("Kuroko", 14, 30, "Ta présence discrète pourrait devenir une arme : travailler la passe invisible ?",
     [("S'y consacrer", .8, {"mait": 7, "intel": 2}, "Plus personne ne te voit venir !", {"sante": -5}, "Tu te blesses en forçant."),
      ("Continuer comme avant", 1, {}, "Rien ne change.", {}, "")]),
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
    (None, 7, 17, "Contrôle surprise à l'école !",
     [("Réviser tard", .8, {"intel": 4, "bonheur": -2}, "Bonne note !", {"sante": -3}, "Tu t'endors sur ta copie."),
      ("Improviser", .4, {"bonheur": 3}, "Ça passe, incroyable.", {"intel": -1, "bonheur": -4}, "Zéro pointé.")]),
    (None, 14, 35, "Quelqu'un te plaît vraiment dans ton entourage.",
     [("Se déclarer", .5, {"bonheur": 12}, "Complicité immédiate !", {"bonheur": -8}, "Râteau..."),
      ("Rester ami", 1, {"bonheur": 2}, "Tu gardes ça pour toi.", {}, "")]),
    (None, 20, 75, "Tu tombes malade.",
     [("Aller voir un médecin", 1, {"argent": -40, "sante": 5}, "Tu guéris vite.", {}, ""),
      ("Ignorer", .5, {}, "Ça passe tout seul.", {"sante": -15}, "Ça empire.")]),
    (None, 16, 60, "Un inconnu te propose un pari risqué.",
     [("Parier 100", .45, {"argent": 200}, "Tu gagnes le double !", {"argent": -100}, "Tu perds ta mise."),
      ("Décliner", 1, {}, "Tu restes sage.", {}, "")]),
]

DEFIS = [
    ("d1", "Atteindre 18 ans", lambda g: g["age"] >= 18, {"argent": 200}),
    ("d2", "Apprendre 3 techniques", lambda g: len(g["tech"]) >= 3, {"argent": 300, "xp": 30}),
    ("d3", "Gagner 5 duels", lambda g: g["wins"] >= 5, {"argent": 400, "xp": 40}),
    ("d4", "Avoir 1000 d'argent", lambda g: g["argent"] >= 1000, {"xp": 50}),
    ("d5", "Atteindre 80 de réputation", lambda g: g["rep"] >= 80, {"argent": 500}),
    ("d6", "Maîtriser une nature niveau 3", lambda g: max(g["nat"].values() or [0]) >= 3, {"xp": 60}),
    ("d7", "Atteindre le 3e rang", lambda g: rang(g)[0] >= 2, {"argent": 600}),
    ("d8", "Débloquer une nature rare", lambda g: any(n in g["nat"] for n in ("Glace", "Bois")), {"xp": 100}),
    ("d9", "Être en couple", lambda g: bool(g["couple"]), {"bonheur": 20, "argent": 200}),
    ("d10", "Survivre jusqu'à 40 ans", lambda g: g["age"] >= 40, {"xp": 150}),
]

# ───────────────────────── LOGIQUE ─────────────────────────
def new_game(nom, u):
    g = dict(nom=nom, u=u, age=5, sante=80, bonheur=70, intel=random.randint(20, 40),
             force=random.randint(15, 30), mait=random.randint(5, 15), chakra=random.randint(10, 25),
             rep=10, argent=100, xp=0, pa=3, cadeau=1, revive=0, wins=0, couple="",
             nat={}, tech=[], defis_ok=[], dead=False, cause="", event=None,
             log=[f"🌱 {nom} naît. {UNIV[u]['intro']}"], pnj=[])
    roles = ["ami", "ami", "rival", "rival", "amour"]
    for nm, r in zip(UNIV[u]["pnj"], roles):
        g["pnj"].append(dict(nom=nm, role=r, aff=random.randint(20, 50), niv=round(random.uniform(.7, 1.3), 2)))
    return g

def ap(g, eff):
    for k, v in eff.items():
        if k == "argent": g[k] = max(0, g[k] + v)
        elif k in ("xp", "pa", "cadeau", "revive"): g[k] += v
        elif k == "nature": eveiller(g)
        else: g[k] = max(0, min(100, g[k] + v))

def eveiller(g):
    dispo = [n for n in BASE_NAT if n not in g["nat"]]
    if dispo:
        n = random.choice(dispo)
        g["nat"][n] = 1
        g["log"].append(f"🔮 Nature de chakra éveillée : {NAT[n]} {n} !")
    else:
        g["log"].append("🔮 Tu maîtrises déjà toutes les natures de base.")

def rang(g):
    i = max(i for i, t in enumerate(RANK_TH) if g["xp"] >= t)
    return i, UNIV[g["u"]]["ranks"][i]

def puissance(g):
    p = g["force"] * .5 + g["mait"] * .6 + g["chakra"] * .4 + sum(g["nat"].values()) * 3 + g["intel"] * .1
    return p + sum(TECH[t]["pw"] for t in g["tech"])

def mort(g, cause):
    if g["revive"] > 0:
        g["revive"] -= 1
        g["sante"] = 50
        g["log"].append("⏳ L'amulette Time Leap s'active : tu reviens à la vie !")
        return
    g["dead"] = True
    g["cause"] = cause

def score(g):
    return int(g["xp"] + g["rep"] * 5 + sum(g["nat"].values()) * 50 + len(g["tech"]) * 100 + g["age"] * 10)

def debloquer_rares(g):
    n = g["nat"]
    if "Glace" not in n and n.get("Eau", 0) >= 3 and n.get("Vent", 0) >= 3:
        n["Glace"] = 1; g["log"].append("❄️ Fusion Eau + Vent : nature rare GLACE débloquée !")
    if "Bois" not in n and n.get("Terre", 0) >= 3 and n.get("Eau", 0) >= 3:
        n["Bois"] = 1; g["log"].append("🌳 Fusion Terre + Eau : nature rare BOIS débloquée !")

def vieillir(g):
    g["age"] += 1
    g["pa"] = 3
    a = g["age"]
    g["log"].append(f"🎂 Tu as maintenant {a} ans.")
    ap(g, {"intel": random.randint(0, 2), "force": random.randint(0, 2) if a < 30 else -1})
    if a >= 45:
        ap(g, {"sante": -random.randint(1, 4)})
    if a >= 15:
        gain = (20 + 15 * rang(g)[0]) * random.randint(1, 3)
        g["argent"] += gain
        g["log"].append(f"💴 Revenus de l'année : +{gain} {UNIV[g['u']]['monnaie']}.")
    if a == 6:
        eveiller(g)
    for p in g["pnj"]:
        p["aff"] = max(0, p["aff"] - random.randint(0, 4))
    if g["sante"] <= 0:
        mort(g, "Épuisement et blessures."); return
    if a > 60 and random.random() < (a - 60) / 100:
        mort(g, "Mort de vieillesse, entouré de souvenirs."); return
    elig = [i for i, e in enumerate(EV) if e[0] in (None, g["u"]) and e[1] <= a <= e[2]]
    if elig and random.random() < .85:
        g["event"] = random.choice(elig)

def resoudre(g, ci):
    e = EV[g["event"]]
    lab, p, eo, to, ek, tk = e[4][ci]
    if random.random() < p:
        ap(g, eo); g["log"].append(f"✅ {lab} → {to}")
    else:
        ap(g, ek); g["log"].append(f"❌ {lab} → {tk}")
    g["event"] = None
    if g["sante"] <= 0:
        mort(g, "Tué par les événements de la vie.")

def duel(g, niv, nom):
    mine = puissance(g) * random.uniform(.8, 1.2)
    foe = (20 + g["age"] * 1.5 + rang(g)[0] * 15) * niv * random.uniform(.8, 1.2)
    if mine >= foe:
        g["wins"] += 1
        ap(g, {"xp": int(10 * niv) + 5, "rep": 3, "argent": 30})
        g["log"].append(f"⚔️ Tu bats {nom} ! (puissance {int(mine)} vs {int(foe)})")
        return True
    ap(g, {"sante": -random.randint(8, 20), "bonheur": -3})
    g["log"].append(f"💥 {nom} te bat... (puissance {int(mine)} vs {int(foe)})")
    if g["sante"] <= 0:
        mort(g, f"Tué lors d'un duel contre {nom}.")
    return False

def action(g, eff, txt):
    if g["pa"] <= 0:
        st.toast("Plus d'actions cette année ! Fais vieillir ton personnage.", icon="⏳"); return
    g["pa"] -= 1
    ap(g, eff)
    g["log"].append(txt)
    st.rerun()

# ───────────────────────── INTERFACE ─────────────────────────
if "g" not in st.session_state:
    st.session_state.g = None
g = st.session_state.g

if g is None:
    st.title("🍥🏀🏍️ Shinobi Life")
    st.caption("Un jeu de vie inspiré de BitLife, dans un monde mêlant l'univers ninja, le basket et les gangs de Tokyo.")
    nom = st.text_input("Nom de ton personnage", "Kenji")
    u = st.selectbox("Choisis ton univers", list(UNIV), format_func=lambda x: f"{UNIV[x]['icon']} {x}")
    if st.button("🌱 Commencer une nouvelle vie", use_container_width=True):
        st.session_state.g = new_game(nom or "Anonyme", u)
        st.rerun()
    up = st.file_uploader("…ou charge une sauvegarde (.json)", type="json")
    if up is not None and st.button("📂 Charger"):
        st.session_state.g = json.load(up)
        st.rerun()
    st.stop()

U = UNIV[g["u"]]
ri, rn = rang(g)
st.title(f"{U['icon']} {g['nom']} — {g['age']} ans")
st.caption(f"{g['u']} • Rang : **{rn}** • 💴 {g['argent']} {U['monnaie']} • XP {g['xp']} • Actions restantes : {g['pa']}")
cols = st.columns(2)
for i, (k, lab) in enumerate(STATS):
    cols[i % 2].progress(g[k] / 100, text=f"{lab} : {g[k]}")

if g["dead"]:
    st.error(f"💀 {g['nom']} est mort à {g['age']} ans. {g['cause']}")
    st.metric("Score final", score(g))
    with st.expander("Journal de vie", expanded=True):
        for l in reversed(g["log"][-40:]):
            st.write(l)
    if st.button("🔄 Nouvelle vie", use_container_width=True):
        st.session_state.g = None
        st.rerun()
    st.stop()

if g["event"] is not None:
    e = EV[g["event"]]
    st.warning(f"📣 **Événement** — {e[3]}")
    for i, c in enumerate(e[4]):
        if st.button(c[0], key=f"ev{i}", use_container_width=True):
            resoudre(g, i)
            st.rerun()
    st.stop()

t_vie, t_act, t_rel, t_tech, t_shop, t_defi, t_save = st.tabs(
    ["📖 Vie", "🏋️ Actions", "👥 Liens", "🌀 Techniques", "🛒 Boutique", "🏆 Défis", "💾 Sauver"])

with t_vie:
    if st.button("⏩ Vieillir d'un an", type="primary", use_container_width=True):
        vieillir(g)
        st.rerun()
    for l in reversed(g["log"][-15:]):
        st.write(l)

with t_act:
    st.subheader("Actions de l'année")
    c1, c2 = st.columns(2)
    if c1.button("📚 Étudier", use_container_width=True):
        action(g, {"intel": 4, "bonheur": -1}, "📚 Tu étudies sérieusement.")
    if c2.button("💪 Entraînement physique", use_container_width=True):
        action(g, {"force": 4, "sante": -1}, "💪 Séance intense.")
    if c1.button(f"🎯 Travailler le {U['mait'].lower()}", use_container_width=True):
        action(g, {"mait": 4, "sante": -1}, f"🎯 Tu progresses en {U['mait'].lower()}.")
    if c2.button("🧘 Méditer (chakra)", use_container_width=True):
        action(g, {"chakra": 4}, "🧘 Ton chakra se renforce.")
    if c1.button("😴 Se reposer", use_container_width=True):
        action(g, {"sante": 6, "bonheur": 3}, "😴 Repos bien mérité.")
    if c2.button(f"💼 {U['job']}", use_container_width=True):
        gain = random.randint(30, 80) * (1 + ri)
        action(g, {"argent": gain, "xp": 5}, f"💼 {U['job']} : +{gain} {U['monnaie']}.")
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
                    g["log"].append(f"✨ {NAT[n]} {n} passe niveau {g['nat'][n]} !")
                    debloquer_rares(g)
                else:
                    g["log"].append(f"😓 L'entraînement de {n} n'a pas porté ses fruits.")
                    ap(g, {"sante": -2})
                st.rerun()
    else:
        st.info("Ton chakra s'éveillera à 6 ans.")

with t_rel:
    st.subheader("Relations")
    if g["couple"]:
        st.success(f"💞 En couple avec {g['couple']}")
    for i, p in enumerate(g["pnj"]):
        ico = {"ami": "🤝", "rival": "😤", "amour": "💗"}[p["role"]]
        with st.expander(f"{ico} {p['nom']} ({p['role']}) — affinité {p['aff']}"):
            c1, c2 = st.columns(2)
            if c1.button("💬 Discuter", key=f"d{i}"):
                if g["pa"] > 0:
                    g["pa"] -= 1; p["aff"] = min(100, p["aff"] + 8)
                    g["log"].append(f"💬 Tu passes du temps avec {p['nom']}."); ap(g, {"bonheur": 3}); st.rerun()
            if c2.button("🎁 Offrir un cadeau", key=f"g{i}"):
                if g["cadeau"] > 0:
                    g["cadeau"] -= 1; p["aff"] = min(100, p["aff"] + 15)
                    g["log"].append(f"🎁 {p['nom']} adore ton cadeau !"); st.rerun()
                else:
                    st.toast("Achète un cadeau en boutique.", icon="🛒")
            if c1.button("⚔️ Défier en duel", key=f"x{i}"):
                if g["pa"] > 0:
                    g["pa"] -= 1; duel(g, p["niv"], p["nom"]); st.rerun()
            if p["role"] == "amour" and not g["couple"] and g["age"] >= 14:
                if c2.button("💍 Se déclarer", key=f"l{i}"):
                    if random.random() < p["aff"] / 100:
                        g["couple"] = p["nom"]; ap(g, {"bonheur": 15})
                        g["log"].append(f"💞 {p['nom']} accepte ! Vous êtes en couple.")
                    else:
                        ap(g, {"bonheur": -8}); g["log"].append(f"💔 {p['nom']} refuse tes sentiments.")
                    st.rerun()

with t_tech:
    st.subheader("🌀 Natures de chakra")
    if g["nat"]:
        for n, l in g["nat"].items():
            st.write(f"{NAT[n]} **{n}** — niveau {l}/5")
    else:
        st.write("Aucune nature éveillée pour l'instant.")
    st.caption("Fusionne Eau + Vent (niv. 3) pour la Glace, Terre + Eau (niv. 3) pour le Bois.")
    st.subheader("⚔️ Techniques")
    for k, t in TECH.items():
        if t["u"] != g["u"]:
            continue
        r = t["req"]
        ok = (g.get(r[0], 0) >= r[1]) if r[0] != "nat" else (g["nat"].get(r[1], 0) >= r[2])
        req_txt = f"{r[0]} ≥ {r[1]}" if r[0] != "nat" else f"{NAT[r[1]]} {r[1]} niv. {r[2]}"
        if k in g["tech"]:
            st.success(f"✅ {t['n']} (puissance +{t['pw']})")
        else:
            c1, c2 = st.columns([3, 1])
            c1.write(f"**{t['n']}** — +{t['pw']} puissance — requis : {req_txt} — {t['p']} 💴")
            if c2.button("Apprendre", key=f"t{k}", disabled=not ok):
                if g["argent"] >= t["p"]:
                    g["argent"] -= t["p"]; g["tech"].append(k)
                    g["log"].append(f"📖 Technique apprise : {t['n']} !"); st.rerun()
                else:
                    st.toast("Pas assez d'argent.", icon="💴")
    st.metric("Puissance totale", int(puissance(g)))

with t_shop:
    st.subheader("🛒 Boutique")
    for k, (nm, pr, ds, eff, uu) in SHOP.items():
        if uu and uu != g["u"]:
            continue
        c1, c2 = st.columns([3, 1])
        c1.write(f"**{nm}** — {ds}")
        if c2.button(f"{pr} 💴", key=f"s{k}"):
            if g["argent"] >= pr:
                g["argent"] -= pr
                ap(g, eff)
                g["log"].append(f"🛍️ Achat : {nm}")
                st.rerun()
            else:
                st.toast("Pas assez d'argent.", icon="💴")
    st.caption(f"🎁 Cadeaux : {g['cadeau']} • ⏳ Time Leap : {g['revive']}")

with t_defi:
    st.subheader("🏆 Défis")
    for did, txt, chk, rew in DEFIS:
        done = did in g["defis_ok"]
        c1, c2 = st.columns([3, 1])
        c1.write(("✅ " if done else "🎯 ") + txt + f"  *(récompense : {rew})*")
        if not done and chk(g) and c2.button("Réclamer", key=f"df{did}"):
            g["defis_ok"].append(did)
            ap(g, rew)
            g["log"].append(f"🏆 Défi réussi : {txt}")
            st.rerun()

with t_save:
    st.download_button("💾 Télécharger ma sauvegarde", json.dumps(g, ensure_ascii=False),
                       file_name=f"{g['nom']}_save.json", mime="application/json")
    if st.button("🗑️ Abandonner cette vie"):
        st.session_state.g = None
        st.rerun()
