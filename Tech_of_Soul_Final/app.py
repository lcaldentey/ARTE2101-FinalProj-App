import streamlit as st
import plotly.graph_objects as go
import math

st.set_page_config(
    page_title="Technologies of the Soul",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700&family=Crimson+Pro:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Space+Mono:wght@400;700&display=swap');

:root {
  --gold:    #C9A84C;
  --amber:   #E8C56D;
  --deep:    #0A0A12;
  --panel:   #111120;
  --surface: #181830;
  --border:  #2A2A4A;
  --text:    #E8E4D8;
  --muted:   #8884AA;
  --accent:  #7B68EE;
}

html, body, [data-testid="stAppViewContainer"] {
  background: var(--deep) !important; color: var(--text) !important;
  font-family: 'Crimson Pro', serif;
}
[data-testid="stHeader"]  { background: transparent !important; }
[data-testid="stToolbar"] { display: none; }
h1, h2, h3 { font-family: 'Cinzel Decorative', serif !important; color: var(--gold) !important; letter-spacing: 0.06em; }

.hero {
  text-align: center; padding: 2.5rem 1rem 1.5rem;
  border-bottom: 1px solid var(--border); margin-bottom: 1.5rem;
  background: radial-gradient(ellipse at 50% 0%, rgba(201,168,76,0.08) 0%, transparent 70%);
}
.hero h1 { font-size: clamp(1.4rem, 3vw, 2.4rem); margin: 0; line-height: 1.3; }
.hero .subtitle { font-family:'Crimson Pro',serif; font-style:italic; font-size:1.1rem; color:var(--amber); margin-top:0.5rem; letter-spacing:0.04em; }

[data-testid="stSlider"] > div > div > div > div { background: var(--gold) !important; }
[data-testid="stSlider"] label { font-family:'Space Mono',monospace !important; font-size:0.75rem !important; color:var(--muted) !important; letter-spacing:0.08em; text-transform:uppercase; }

.stButton > button { font-family:'Space Mono',monospace !important; font-size:0.7rem !important; letter-spacing:0.1em; text-transform:uppercase; }

/* Filter dropdown panel */
.filter-panel {
  background: var(--panel); border: 1px solid var(--border);
  border-top: none; border-radius: 0 0 4px 4px;
  padding: 0.6rem 0.8rem 0.8rem; margin-top: -2px;
}
.filter-cat-header {
  font-family: 'Space Mono', monospace; font-size: 0.56rem;
  letter-spacing: 0.1em; text-transform: uppercase;
  margin: 0.55rem 0 0.05rem; padding-bottom: 0.15rem;
}
[data-testid="stCheckbox"] label p {
  font-family: 'Space Mono', monospace !important; font-size: 0.62rem !important;
  color: var(--text) !important; letter-spacing: 0.03em; line-height: 1.35 !important;
}

/* Legend */
.legend-row { display:flex; gap:1.2rem; flex-wrap:wrap; padding:0.6rem 1rem; background:var(--panel); border:1px solid var(--border); border-radius:4px; margin-bottom:0.8rem; align-items:center; }
.legend-item { display:flex; align-items:center; gap:0.4rem; }
.legend-dot  { width:12px; height:12px; border-radius:50%; flex-shrink:0; }
.legend-txt  { font-family:'Space Mono',monospace; font-size:0.65rem; color:var(--muted); letter-spacing:0.05em; }

/* Detail panel */
.event-panel { background:var(--panel); border:1px solid var(--border); border-left:3px solid var(--gold); border-radius:4px; padding:1.4rem 1.6rem; margin-top:0.5rem; }
.event-panel h3 { font-size:1.1rem !important; margin-bottom:0.3rem; }
.event-year { font-family:'Space Mono',monospace; font-size:0.78rem; color:var(--amber); margin-bottom:0.8rem; letter-spacing:0.1em; }
.event-panel p { font-size:1rem; line-height:1.7; color:var(--text); margin:0.5rem 0; }
.tag { display:inline-block; background:rgba(123,104,238,0.18); color:var(--accent); border:1px solid rgba(123,104,238,0.35); border-radius:2px; font-family:'Space Mono',monospace; font-size:0.65rem; letter-spacing:0.08em; padding:0.15rem 0.5rem; margin:0.15rem 0.15rem 0.15rem 0; }
.section-label { font-family:'Space Mono',monospace; font-size:0.65rem; letter-spacing:0.12em; text-transform:uppercase; color:var(--muted); margin:0.9rem 0 0.25rem; }
.counter-badge { font-family:'Space Mono',monospace; font-size:0.7rem; color:var(--amber); letter-spacing:0.1em; text-align:right; padding:0.2rem 0; }
.flow-legend { font-family:'Space Mono',monospace; font-size:0.62rem; color:var(--muted); letter-spacing:0.07em; padding:0.3rem 0; }
#detail-anchor { scroll-margin-top: 80px; }
</style>
""", unsafe_allow_html=True)

# ── DATA ──────────────────────────────────────────────────────────────────────
EVENTS = [
  {
    "id": 1, "name": "Swedenborg's Mystical Visions",
    "year_start": 1743, "year_end": 1772,
    "lat": 59.33, "lon": 18.07, "origin_city": "Stockholm, Sweden",
    "category": "Esoteric / Proto-Spiritualism", "color": "#E8A87C",
    "description": (
        "Emanuel Swedenborg was a celebrated Swedish engineer, anatomist, and cosmologist "
        "who in 1743–44 underwent a dramatic spiritual crisis and emerged as one of Western history's "
        "most influential mystics. He claimed access to the spiritual world through methodical visionary "
        "exploration. His multi-volume works served to describe the architecture of heaven and hell in "
        "extraordinary detail, presented spirits as former humans continuing social lives, and proposed "
        "a 'doctrine of correspondences' in which every physical thing mirrors a spiritual reality. "
        "Swedenborg insisted that the interior sense of Scripture, not its literal surface, contained "
        "divine truth. This was largely seen as a hermeneutical move that licensed countless later esotericists. "
        "His rejection of substitutionary atonement and his vision of a God of love rather than judgment made his "
        "theology hospitable to liberal Protestantism. The New Church (Swedenborgian Church) was "
        "founded after his death in 1787 by followers in London."
    ),
    "key_figures": ["Emanuel Swedenborg"],
    "beliefs": [
        "Direct spirit communication through trained visionary faculty",
        "Doctrine of correspondences: physical world mirrors spiritual world",
        "Heaven and hell as states of character, not geography",
        "Inner spiritual sense of Scripture over literal reading",
        "God as infinite Divine Love and Wisdom, not judge"
    ],
    "impact": (
        "Swedenborg's influence spread silently through intellectual culture. William Blake absorbed "
        "his cosmology. Kant wrote a critical pamphlet. Emerson, Baudelaire, Strindberg, and Jung all "
        "engaged him seriously. He pioneered the model of the individual mystic as spiritual "
        "cartographer — mapping hidden realities through disciplined inner sight — a template that "
        "Theosophy, Rudolf Steiner, and the New Age all inherited."
    ),
    "spread": [
        {"lat": 51.51, "lon": -0.13,  "city": "London, UK",     "year": 1787},
        {"lat": 42.36, "lon": -71.06, "city": "Boston, USA",     "year": 1818},
        {"lat": 48.85, "lon": 2.35,   "city": "Paris, France",   "year": 1820},
        {"lat": 52.52, "lon": 13.40,  "city": "Berlin, Germany", "year": 1845},
    ],
    "readings": ["Kant and Swedenborg"],
    "image_file": "swedenborg_Img.png"
  },
  {
    "id": 2, "name": "Mesmerism",
    "year_start": 1774, "year_end": 1850,
    "lat": 48.21, "lon": 16.37, "origin_city": "Vienna, Austria",
    "category": "Proto-Psychology / Healing", "color": "#7EC8A8",
    "description": (
        "Franz Anton Mesmer proposed in 1774 that a subtle magnetic fluid permeated all living bodies "
        "and that disease arose from its blockage. His treatment — theatrical group sessions around a "
        "magnetized 'baquet' tub, with patients experiencing tremors and cathartic 'crises' — was "
        "simultaneously spectacle, medical innovation, and popular sensation. Mesmer lated moved to Paris in 1778, "
        "and attracted aristocratic patrons before a royal commission (including Benjamin Franklin "
        "and Lavoisier) debunked animal magnetism in 1784. This debunking, however, did not kill the movement. "
        "Armand de Puységur discovered the somnambulistic trance — the direct precursor of hypnosis. "
        "By the mid-19th century, itinerant mesmerists had spread through Europe and America, creating "
        "publics fascinated with altered states, telepathy, and the powers of the unconscious. "
        "Mesmerism fed directly into Spiritualism, New Thought, and Christian Science."
    ),
    "key_figures": ["Franz Anton Mesmer", "Armand de Puységur", "James Braid"],
    "beliefs": [
        "Universal magnetic fluid flowing through all living things",
        "Disease as blockage of animal magnetism",
        "Healing through energetic transfer from practitioner to patient",
        "The somnambulistic trance as gateway to hidden mental faculties",
        "Imagination and suggestion as legitimate medical forces"
    ],
    "impact": (
        "Mesmerism was the 19th century's first mass psychological movement. Braid renamed it "
        "'hypnosis' in 1843. Charcot and Janet's work on hysteria and the unconscious — which Freud "
        "attended — grew directly from mesmerist traditions. The idea that an invisible force can "
        "transfer healing between bodies persists in Reiki, therapeutic touch, and energy medicine."
    ),
    "spread": [
        {"lat": 48.85, "lon": 2.35,   "city": "Paris, France",   "year": 1778},
        {"lat": 51.51, "lon": -0.13,  "city": "London, UK",      "year": 1838},
        {"lat": 40.71, "lon": -74.01, "city": "New York, USA",   "year": 1836},
        {"lat": 42.36, "lon": -71.06, "city": "Boston, USA",     "year": 1838},
        {"lat": 52.52, "lon": 13.40,  "city": "Berlin, Germany", "year": 1812},
        {"lat": 55.75, "lon": 37.62,  "city": "Moscow, Russia",  "year": 1818},
    ],
    "readings": ["Mesmer (Film, syllabus)"],
    "image_file": "mesmerism_Img.png"
  },
  {
    "id": 3, "name": "Marian Apparitions (Global)",
    "year_start": 1858, "year_end": None,
    "lat": 43.09, "lon": -0.05, "origin_city": "Lourdes, France",
    "category": "Catholic Mysticism", "color": "#87CEEB",
    "description": (
        "The Marian apparition tradition achieved global cultural mass beginning with Bernadette "
        "Soubirous at Lourdes in 1858, where the Virgin Mary reportedly appeared eighteen times in "
        "the Grotto of Massabielle. Each new apparition site re-enacts the same grammar: children or "
        "simple visionaries receive messages, crowds gather, healings are reported, ecclesiastical "
        "investigation follows, and — sometimes — official recognition transforms a local site into a "
        "global pilgrimage destination. Knock, Ireland (1879) drew the suffering post-Famine "
        "population. Fátima, Portugal (1917) brought geopolitical urgency — the Virgin warned of "
        "Russia's errors and called for consecration, a message weaponized throughout the Cold War. "
        "Zeitoun, Egypt (1968) drew millions of Coptic Christians and Muslims alike. Medjugorje in "
        "Yugoslavia (1981) became the most visited apparition site in history. Kibeho, Rwanda "
        "(1981–89) gained tragic retrospective significance for its warnings before the 1994 genocide. "
        "The phenomenon has occurred on every inhabited continent — Akita (Japan), Betania "
        "(Venezuela), Cuapa (Nicaragua), Naju (South Korea), Manila (Philippines) — constituting "
        "a vast decentralized global network of Marian devotion."
    ),
    "key_figures": [
        "Bernadette Soubirous (Lourdes)", "Lúcia Santos & Francisco Marto (Fátima)",
        "Segatashya Emmanuel (Kibeho)", "Agnes Sasagawa (Akita)"
    ],
    "beliefs": [
        "The Virgin Mary as active intercessor in contemporary history",
        "Miraculous healing at sacred sites",
        "Prophetic messages warning of geopolitical and spiritual catastrophe",
        "The body of the visionary as theological text",
        "Popular devotion operating alongside — and sometimes against — official church hierarchy"
    ],
    "impact": (
        "Lourdes alone receives 4–6 million pilgrims annually. Fátima's 'third secret' shaped Vatican "
        "geopolitics for decades. The apparition tradition has been a major vehicle through which lay "
        "Catholics — often women, children, and peasants — have asserted religious authority. Scholars "
        "Sandra Zimdars-Swartz and Ruth Harris have analyzed these events as sites where modernity, "
        "gender, medicine, nationalism, and popular religion collide."
    ),
    "spread": [
        {"lat": 46.17,  "lon": 5.90,   "city": "La Salette, France",      "year": 1858},
        {"lat": 47.85,  "lon": 0.61,   "city": "Pontmain, France",        "year": 1871},
        {"lat": 53.79,  "lon": -8.92,  "city": "Knock, Ireland",          "year": 1879},
        {"lat": 39.66,  "lon": -8.67,  "city": "Fátima, Portugal",        "year": 1917},
        {"lat": 50.07,  "lon": 4.96,   "city": "Beauraing, Belgium",      "year": 1932},
        {"lat": 50.48,  "lon": 5.68,   "city": "Banneux, Belgium",        "year": 1933},
        {"lat": 43.12,  "lon": -2.41,  "city": "Garabandal, Spain",       "year": 1961},
        {"lat": 52.38,  "lon": 4.90,   "city": "Amsterdam, Netherlands",  "year": 1945},
        {"lat": 44.57,  "lon": 18.65,  "city": "Medjugorje, Bosnia",      "year": 1981},
        {"lat": 30.07,  "lon": 31.26,  "city": "Zeitoun, Cairo, Egypt",   "year": 1968},
        {"lat": -2.47,  "lon": 29.34,  "city": "Kibeho, Rwanda",          "year": 1981},
        {"lat": -25.90, "lon": 32.57,  "city": "Maputo, Mozambique",      "year": 1992},
        {"lat": 19.36,  "lon": -99.12, "city": "Mexico City, Mexico",     "year": 1895},
        {"lat": 8.00,   "lon": -66.00, "city": "Betania, Venezuela",      "year": 1976},
        {"lat": 12.33,  "lon": -85.18, "city": "Cuapa, Nicaragua",        "year": 1980},
        {"lat": 33.76,  "lon": -84.39, "city": "Conyers, Georgia, USA",   "year": 1987},
        {"lat": -22.91, "lon": -43.17, "city": "Rio de Janeiro, Brazil",  "year": 1950},
        {"lat": -34.61, "lon": -58.38, "city": "Buenos Aires, Argentina", "year": 1983},
        {"lat": 14.60,  "lon": 120.98, "city": "Manila, Philippines",     "year": 1948},
        {"lat": 39.72,  "lon": 140.10, "city": "Akita, Japan",            "year": 1973},
        {"lat": 35.90,  "lon": 126.97, "city": "Naju, South Korea",       "year": 1985},
        {"lat": -6.21,  "lon": 106.85, "city": "Jakarta, Indonesia",      "year": 1953},
        {"lat": 28.61,  "lon": 77.21,  "city": "New Delhi, India",        "year": 1970},
    ],
    "readings": ["Zimdars-Swartz, Encountering Mary", "Harris, Lourdes", "Song of Bernadette (Film)", "Fatima (Film)"],
    "image_file": "marian_Img.png"
  },
  {
    "id": 4, "name": "Christian Science",
    "year_start": 1866, "year_end": None,
    "lat": 42.36, "lon": -71.06, "origin_city": "Boston, USA",
    "category": "New Religious Movement", "color": "#DDA0DD",
    "description": (
        "In 1866, Mary Baker Eddy slipped on ice in Lynn, Massachusetts, suffered serious injuries, "
        "and claimed to have healed herself by reading the Gospel account of Jesus healing the "
        "paralytic. This experience became the foundation of Christian Science: the claim that matter, "
        "including the body and its diseases, is ultimately unreal — a false belief of mortal mind — "
        "and that true understanding of God as divine Mind dissolves illness. Eddy systematized this "
        "in Science and Health with Key to the Scriptures (1875), one of the bestselling religious "
        "books in American history. She founded the First Church of Christ, Scientist in Boston in "
        "1879 and the Christian Science Monitor newspaper in 1908. Her movement was the first major "
        "American religion founded by a woman, attracting a predominantly female following and "
        "offering women a role as spiritual healers ('practitioners') at a time when medicine was a "
        "male domain. Christian Science reached its peak in the 1920s–30s with thousands of branch "
        "churches worldwide."
    ),
    "key_figures": ["Mary Baker Eddy", "Augusta Stetson"],
    "beliefs": [
        "Matter and disease are illusions of mortal mind",
        "God as divine Mind: omnipresent, omnipotent, omniscient",
        "Healing through prayer and spiritual understanding, not medicine",
        "Jesus as Way-shower demonstrating divine law",
        "Sin and death as errors to be overcome through right thinking"
    ],
    "impact": (
        "Christian Science pioneered what became the New Thought movement: the idea that consciousness "
        "creates reality and that disease is fundamentally mental. Unity Church, Religious Science, "
        "and eventually the prosperity gospel all inherit this framework. The Christian Science Monitor "
        "became an internationally respected newspaper. The movement's emphasis on female spiritual "
        "authority influenced 20th-century feminist theology."
    ),
    "spread": [
        {"lat": 40.71, "lon": -74.01,  "city": "New York, USA",     "year": 1885},
        {"lat": 41.88, "lon": -87.63,  "city": "Chicago, USA",      "year": 1887},
        {"lat": 34.05, "lon": -118.24, "city": "Los Angeles, USA",  "year": 1892},
        {"lat": 51.51, "lon": -0.13,   "city": "London, UK",        "year": 1895},
        {"lat": 48.85, "lon": 2.35,    "city": "Paris, France",     "year": 1903},
        {"lat": 52.52, "lon": 13.40,   "city": "Berlin, Germany",   "year": 1902},
        {"lat": -33.87,"lon": 151.21,  "city": "Sydney, Australia", "year": 1898},
        {"lat": 43.65, "lon": -79.38,  "city": "Toronto, Canada",   "year": 1906},
    ],
    "readings": ["Science and Health With Key to the Scriptures (Eddy, syllabus)"],
    "image_file": "christian_science_Img.png"
  },
  {
    "id": 5, "name": "Theosophical Society",
    "year_start": 1875, "year_end": None,
    "lat": 40.71, "lon": -74.01, "origin_city": "New York, USA",
    "category": "Esoteric / Occult", "color": "#C9A84C",
    "description": (
        "In September 1875, Helena Petrovna Blavatsky and Henry Steel Olcott gathered in a New York "
        "drawing room to found the Theosophical Society. Blavatsky synthesized Hindu cosmology, "
        "Buddhist metaphysics, Neoplatonism, Kabbalah, and evolutionary theory into Theosophy — "
        "'divine wisdom.' Her works, Isis Unveiled (1877) and The Secret Doctrine (1888), proposed "
        "that all world religions encode a single esoteric wisdom-tradition, that humanity undergoes "
        "spiritual evolution across vast cosmic timeframes, and that an invisible Brotherhood of "
        "Masters (Mahatmas) guides human progress from the Himalayas. Moving headquarters to Adyar, "
        "India in 1882, Blavatsky and Olcott helped catalyze Buddhist revivalism in Ceylon and "
        "framed Eastern religions as sophisticated philosophical systems — a reframing with enormous "
        "anti-colonial significance. Annie Besant, who led after 1891, brought Theosophy into Indian "
        "nationalism and popularized ideas of chakras and the 'etheric body.'"
    ),
    "key_figures": ["Helena Petrovna Blavatsky", "Henry Steel Olcott", "Annie Besant", "Charles Leadbeater", "Jiddu Krishnamurti"],
    "beliefs": [
        "Universal brotherhood transcending race, creed, and nation",
        "Hidden Masters (Mahatmas) guiding human spiritual evolution",
        "Karma and reincarnation as universal laws",
        "Root races and cosmic rounds: evolution as spiritual ascent",
        "All religions as expressions of one perennial wisdom-tradition"
    ],
    "impact": (
        "Theosophy introduced karma, reincarnation, chakras, and the 'astral plane' to Western mass "
        "culture. Mondrian, Kandinsky, and Hilma af Klint created abstract art under direct "
        "Theosophical influence. Independence movements in India, Ireland, and Egypt all had "
        "Theosophical figures. Virtually every New Age concept — channeling, energy healing, the "
        "'Aquarian Age' — is refracted Theosophy."
    ),
    "spread": [
        {"lat": 13.08,  "lon": 80.27,  "city": "Adyar, India (HQ)",       "year": 1882},
        {"lat": 51.51,  "lon": -0.13,  "city": "London, UK",               "year": 1883},
        {"lat": 48.85,  "lon": 2.35,   "city": "Paris, France",            "year": 1884},
        {"lat": -33.87, "lon": 151.21, "city": "Sydney, Australia",        "year": 1890},
        {"lat": 52.52,  "lon": 13.40,  "city": "Berlin, Germany",          "year": 1896},
        {"lat": 6.93,   "lon": 79.85,  "city": "Colombo, Sri Lanka",       "year": 1880},
        {"lat": -34.61, "lon": -58.38, "city": "Buenos Aires, Argentina",  "year": 1905},
        {"lat": 30.06,  "lon": 31.25,  "city": "Cairo, Egypt",             "year": 1908},
        {"lat": 52.37,  "lon": 4.90,   "city": "Amsterdam, Netherlands",   "year": 1897},
        {"lat": -23.55, "lon": -46.63, "city": "São Paulo, Brazil",        "year": 1923},
        {"lat": 35.69,  "lon": 139.69, "city": "Tokyo, Japan",             "year": 1896},
        {"lat": 55.75,  "lon": 37.62,  "city": "Moscow, Russia",           "year": 1908},
    ],
    "readings": ["Santucci, 'The Theosophical Society'"],
    "image_file": "theosophy_Img.png"
  },
  {
    "id": 6, "name": "Anthroposophy (Rudolf Steiner)",
    "year_start": 1912, "year_end": None,
    "lat": 47.54, "lon": 7.59, "origin_city": "Dornach, Switzerland",
    "category": "Esoteric / Occult", "color": "#F4A460",
    "description": (
        "Rudolf Steiner gave over 6,000 lectures, founded two new arts (Eurythmy and biodynamic "
        "agriculture), designed the Goetheanum — a landmark of organic architecture — and applied his "
        "'spiritual science' to education, medicine, pharmacy, theater, and painting. A former leader "
        "of the German Theosophical Society, Steiner broke with Blavatsky's system in 1912 to found "
        "Anthroposophy, insisting on the unique cosmic significance of Christ's incarnation and on the "
        "possibility of a rigorous, verifiable science of the spirit. Where Blavatsky looked East for "
        "wisdom, Steiner looked to the Western esoteric tradition: Goethe, Meister Eckhart, and "
        "Rosicrucianism. His Waldorf school (Stuttgart, 1919), designed for the children of factory "
        "workers, embodied his conviction that education must address body, soul, and spirit together."
    ),
    "key_figures": ["Rudolf Steiner", "Marie Steiner von Sivers"],
    "beliefs": [
        "Christ's incarnation as the unique turning-point of cosmic evolution",
        "Spiritual science: clairvoyant investigation as rigorous method",
        "Karma and reincarnation within a Western esoteric framework",
        "Human freedom as the goal of spiritual development",
        "Education, agriculture, and medicine as expressions of spiritual insight"
    ],
    "impact": (
        "Waldorf (Rudolf Steiner) schools now number over 1,100 worldwide in 65 countries — the "
        "world's largest independent school network. Biodynamic farming preceded the organic "
        "agriculture movement. Anthroposophical medicine (including Weleda products) is a global "
        "industry. Hilma af Klint and Kandinsky created abstract art under direct Anthroposophical "
        "influence."
    ),
    "spread": [
        {"lat": 48.78,  "lon": 9.18,   "city": "Stuttgart, Germany",        "year": 1919},
        {"lat": 52.52,  "lon": 13.40,  "city": "Berlin, Germany",           "year": 1913},
        {"lat": 51.51,  "lon": -0.13,  "city": "London, UK",                "year": 1923},
        {"lat": 40.71,  "lon": -74.01, "city": "New York, USA",             "year": 1928},
        {"lat": -33.87, "lon": 151.21, "city": "Sydney, Australia",         "year": 1957},
        {"lat": 59.91,  "lon": 10.75,  "city": "Oslo, Norway",              "year": 1920},
        {"lat": 52.37,  "lon": 4.90,   "city": "Amsterdam, Netherlands",    "year": 1925},
        {"lat": 48.20,  "lon": 16.37,  "city": "Vienna, Austria",           "year": 1922},
        {"lat": -34.61, "lon": -58.38, "city": "Buenos Aires, Argentina",   "year": 1948},
        {"lat": -23.55, "lon": -46.63, "city": "São Paulo, Brazil",         "year": 1956},
    ],
    "readings": ["Staudenmeier, DCE 'Anthroposophy Entry'"],
    "image_file": "anthroposophy_Img.png"
  },
  {
    "id": 7, "name": "Vedanta & Self-Realization Fellowship",
    "year_start": 1893, "year_end": None,
    "lat": 22.57, "lon": 88.36, "origin_city": "Calcutta, India",
    "category": "Hindu-derived / Neo-Vedanta", "color": "#FF8C00",
    "description": (
        "On September 11, 1893, Swami Vivekananda rose before the Parliament of the World's Religions "
        "in Chicago and began: 'Sisters and brothers of America.' The crowd responded with a "
        "two-minute standing ovation. His message — that all religions are paths to the same divine "
        "reality, that the soul's nature is already divine — electrified the West and transformed how "
        "Hinduism was perceived globally. Vivekananda's Vedanta societies, founded in New York (1894) "
        "and London (1895), were the first Hindu institutions in the West. His framework blended "
        "Enlightenment values with his guru Sri Ramakrishna's devotional, ecstatic Bengali religiosity. "
        "Paramahansa Yogananda's arrival in America in 1920 continued this work through the "
        "Self-Realization Fellowship, offering Kriya Yoga as a systematic, scientific path to "
        "God-contact available to all. His Autobiography of a Yogi (1946) became one of the most "
        "widely read spiritual books of the 20th century — reportedly the only book on Steve Jobs's "
        "iPad at his death."
    ),
    "key_figures": ["Swami Vivekananda", "Sri Ramakrishna", "Paramahansa Yogananda", "Swami Prabhavananda"],
    "beliefs": [
        "Atman (individual soul) = Brahman (universal consciousness): non-dual identity",
        "All religions as valid paths to the same divine reality",
        "Kriya Yoga as systematic, scientific method for God-realization",
        "The guru-disciple relationship as spiritual transmission",
        "Self-realization — direct knowledge of one's divine nature — as life's purpose"
    ],
    "impact": (
        "Vivekananda's 1893 address is the inaugural moment of global yoga and Hindu philosophy in the "
        "West. The Neo-Vedanta framework — all religions share an esoteric core, spiritual practice "
        "can be scientific, Eastern wisdom corrects Western materialism — became the template for "
        "virtually all subsequent Western appropriations of Hindu philosophy, from the Beatles to the "
        "New Age to Silicon Valley mindfulness culture."
    ),
    "spread": [
        {"lat": 41.88, "lon": -87.63,  "city": "Chicago, USA",        "year": 1893},
        {"lat": 40.71, "lon": -74.01,  "city": "New York, USA",       "year": 1894},
        {"lat": 51.51, "lon": -0.13,   "city": "London, UK",          "year": 1895},
        {"lat": 34.05, "lon": -118.24, "city": "Los Angeles, USA",    "year": 1920},
        {"lat": 37.78, "lon": -122.41, "city": "San Francisco, USA",  "year": 1906},
        {"lat": 38.91, "lon": -77.04,  "city": "Washington DC, USA",  "year": 1927},
        {"lat": 48.85, "lon": 2.35,    "city": "Paris, France",       "year": 1948},
        {"lat": 52.52, "lon": 13.40,   "city": "Berlin, Germany",     "year": 1960},
        {"lat": -33.87,"lon": 151.21,  "city": "Sydney, Australia",   "year": 1972},
        {"lat": -23.55,"lon": -46.63,  "city": "São Paulo, Brazil",   "year": 1978},
        {"lat": 35.69, "lon": 139.69,  "city": "Tokyo, Japan",        "year": 1967},
    ],
    "readings": ["Foxen, Biography of a Yogi", "Raja Yoga (Primary Source)", "Awake (Documentary Film)"],
    "image_file": "vedanta_Img.png"
  },
  {
    "id": 8, "name": "Hare Krishna (ISKCON)",
    "year_start": 1966, "year_end": None,
    "lat": 40.71, "lon": -74.01, "origin_city": "New York, USA",
    "category": "Hindu-derived / Vaishnava", "color": "#FFD700",
    "description": (
        "In 1965, A.C. Bhaktivedanta Swami Prabhupada arrived in New York City with $40 and a trunk "
        "of Bengali-language scriptures. Within a year he had attracted a community of "
        "counterculturalists in the Bowery, incorporated ISKCON, and was chanting the Hare Krishna "
        "maha-mantra in Tompkins Square Park. ISKCON spread along the counterculture's international "
        "networks: San Francisco (1967), London's Radha-Krishna Temple (1969), where George Harrison "
        "produced the UK hit record 'Hare Krishna Mantra,' launching bhakti into the pop charts. "
        "Harrison's devotional anthem 'My Sweet Lord' (1970) gave ISKCON a global cultural platform "
        "few new religious movements have ever matched. The theology is classical Gaudiya Vaishnavism: "
        "Krishna as the Supreme Personality of Godhead, devotional service (bhakti) as the highest "
        "path, and chanting the Holy Name as the most powerful spiritual practice for this age. "
        "Prabhupada established 108 temples and personally initiated over 5,000 disciples before his "
        "death in 1977."
    ),
    "key_figures": ["A.C. Bhaktivedanta Swami Prabhupada", "George Harrison", "Jayananda Thakura"],
    "beliefs": [
        "Krishna as the Supreme Personality of Godhead — supreme above all deities",
        "Devotional service (bhakti-yoga) as the highest spiritual path",
        "Chanting the Hare Krishna mahamantra as liberation in this age",
        "Vegetarianism, non-violence, and simplified material life",
        "The Bhagavad-gita As It Is as literal divine instruction"
    ],
    "impact": (
        "ISKCON operates over 600 temples worldwide on every inhabited continent. Its Food for Life "
        "program distributes over a million free meals daily. George Harrison's music introduced "
        "Vaishnava bhakti to hundreds of millions of listeners. ISKCON has grown significantly in "
        "Eastern Europe, Latin America, and Africa since 1990."
    ),
    "spread": [
        {"lat": 37.78, "lon": -122.41, "city": "San Francisco, USA",     "year": 1967},
        {"lat": 27.17, "lon": 78.04,   "city": "Vrindavan, India",       "year": 1967},
        {"lat": 43.65, "lon": -79.38,  "city": "Montreal, Canada",       "year": 1967},
        {"lat": 51.51, "lon": -0.13,   "city": "London, UK",             "year": 1969},
        {"lat": 50.11, "lon": 8.68,    "city": "Frankfurt, Germany",     "year": 1969},
        {"lat": 52.37, "lon": 4.90,    "city": "Amsterdam, Netherlands", "year": 1970},
        {"lat": 48.85, "lon": 2.35,    "city": "Paris, France",          "year": 1972},
        {"lat": -33.87,"lon": 151.21,  "city": "Sydney, Australia",      "year": 1971},
        {"lat": -23.55,"lon": -46.63,  "city": "São Paulo, Brazil",      "year": 1974},
        {"lat": 18.97, "lon": 72.82,   "city": "Mumbai, India",          "year": 1978},
        {"lat": 55.75, "lon": 37.62,   "city": "Moscow, Russia",         "year": 1987},
        {"lat": 50.07, "lon": 14.44,   "city": "Prague, Czech Republic", "year": 1990},
        {"lat": -1.29, "lon": 36.82,   "city": "Nairobi, Kenya",         "year": 1995},
    ],
    "readings": ["KRSNA (Primary Source)", "Hare Krishna! (Documentary Film)"],
    "image_file": "iskcon_Img.png"
  },
  {
    "id": 9, "name": "Beat Generation Spirituality",
    "year_start": 1950, "year_end": 1970,
    "lat": 37.78, "lon": -122.41, "origin_city": "San Francisco, USA",
    "category": "Literary / Counterculture", "color": "#708090",
    "description": (
        "The Beat Generation emerged from the collision of Columbia University literary bohemia and "
        "the San Francisco poetry renaissance in the late 1940s–50s. Their spiritual project was "
        "explicit and urgent: to find sacred experience outside institutional religion, using "
        "literature, jazz, sex, drugs, and the open road as vehicles. Kerouac wrote On the Road in a "
        "semi-trance state — saturated with what he called 'IT': moments of ecstatic presence. Allen "
        "Ginsberg's 1948 Blake vision (hearing William Blake's voice and feeling the universe open) "
        "became the founding mystical event of his career. Gary Snyder, who lived in Japan studying "
        "Zen for a decade, brought rigorous contemplative practice into the Beat orbit. Burroughs, in "
        "Tangier and Paris, experimented with hallucinogens as consciousness tools and developed the "
        "'cut-up' technique as a spiritual technology for breaking through conditioned perception. The "
        "Beats were the first American cultural movement to treat Buddhism, Hinduism, and indigenous "
        "shamanism as equal or superior to Christianity as paths to authentic experience."
    ),
    "key_figures": ["Jack Kerouac", "Allen Ginsberg", "Gary Snyder", "William S. Burroughs", "Lawrence Ferlinghetti"],
    "beliefs": [
        "The sacred in the profane, the marginal, and the rejected",
        "Zen spontaneity, no-mind, and the present moment as spiritual states",
        "The ecstatic and the visionary available to all, not just saints",
        "The body and its desires as spiritual, not sinful",
        "Rejection of postwar consumer society as spiritual death"
    ],
    "impact": (
        "The Beats opened the aperture of American spiritual life decisively and permanently. "
        "Ginsberg's HOWL (1956) made Buddhist compassion and psychedelic mysticism countercultural "
        "common property. Kerouac and Snyder's Buddhism made Zen accessible to millions before a "
        "single Zen center existed in America. Ginsberg's friendship with Chögyam Trungpa Rinpoche "
        "gave Tibetan Buddhism its first major American institution (Naropa Institute, 1974)."
    ),
    "spread": [
        {"lat": 40.71, "lon": -74.01, "city": "New York, USA",    "year": 1950},
        {"lat": 48.85, "lon": 2.35,   "city": "Paris, France",    "year": 1957},
        {"lat": 35.67, "lon": -5.84,  "city": "Tangier, Morocco", "year": 1954},
        {"lat": 51.51, "lon": -0.13,  "city": "London, UK",       "year": 1960},
        {"lat": 28.61, "lon": 77.21,  "city": "New Delhi, India", "year": 1962},
        {"lat": 35.69, "lon": 139.69, "city": "Tokyo, Japan",     "year": 1963},
    ],
    "readings": ["Course readings on counterculture"],
    "image_file": "beat_generation_Img.png"
  },
  {
    "id": 10, "name": "The Jesus Movement",
    "year_start": 1967, "year_end": 1985,
    "lat": 37.78, "lon": -122.41, "origin_city": "San Fransisco, USA",
    "category": "Christian Counterculture", "color": "#98FB98",
    "description": (
        "In the late 1960s, large numbers of hippies, runaways, and dropouts began converting to a "
        "radical, experiential Christianity. The Jesus Movement emerged from youth hostels, "
        "coffeehouses, and beach baptisms in California, and spread nationally within a few years. Its "
        "central identity was applying the countercultural model to evangelism: informal dress, rock "
        "music, communal living, and the language of 'experience' and 'encounter' transmitted an "
        "essentially conservative Protestant theology. A charismatic figure who "
        "performed mass baptisms in the Pacific named Lonnie Frisbee was the movement's most electric figure, though his "
        "later revelation as a gay man caused him to be largely written out of official history. "
        "Chuck Smith's Calvary Chapel in Costa Mesa became the movement's institutional home. The "
        "Jesus Movement led the way in the entire genre of Contemporary Christian Music: Larry Norman, "
        "Keith Green, and later Amy Grant among others translated the emotional register of rock and pop into "
        "Christian devotion."
    ),
    "key_figures": ["Lonnie Frisbee", "Chuck Smith", "Keith Green", "Larry Norman"],
    "beliefs": [
        "Born-again personal salvation through direct encounter with Jesus",
        "Gifts of the Holy Spirit (tongues, prophecy, healing) for today",
        "Communal intentional living as Kingdom expression",
        "Scripture as sufficient and inerrant guide",
        "Evangelism through music, street witnessing, and relational presence"
    ],
    "impact": (
        "Contemporary Christian Music (CCM) is now a billion-dollar industry. Calvary Chapel spawned "
        "the Vineyard Church movement. The charismatic renewal it accelerated has become one of the "
        "most globally dynamic forms of Christianity. The Jesus Movement's fusion of countercultural "
        "form with conservative theology became the template for evangelical megachurch culture."
    ),
    "spread": [
        {"lat": 34.05, "lon": -118.24, "city": "Los Angelos, USA",  "year": 1967},
        {"lat": 47.61, "lon": -122.33, "city": "Seattle, USA",        "year": 1969},
        {"lat": 40.71, "lon": -74.01,  "city": "New York, USA",       "year": 1970},
        {"lat": 51.51, "lon": -0.13,   "city": "London, UK",          "year": 1972},
        {"lat": 52.52, "lon": 13.40,   "city": "Berlin, Germany",     "year": 1975},
        {"lat": -33.87,"lon": 151.21,  "city": "Sydney, Australia",   "year": 1971},
        {"lat": 43.65, "lon": -79.38,  "city": "Toronto, Canada",     "year": 1972},
    ],
    "readings": ["Shires, 'The Countercultural Christians'", "Eskridge, 'Jesus Knocked Me Off My Metaphysical Ass'"],
    "image_file": "jesus_movement_Img.png"
  },
  {
    "id": 11, "name": "5% Nation of Gods and Earths",
    "year_start": 1964, "year_end": None,
    "lat": 40.71, "lon": -74.01, "origin_city": "Harlem, New York, USA",
    "category": "Black Spiritual Movement", "color": "#DC143C",
    "description": (
        "In 1964, Clarence 13X broke with the Nation of Islam and began teaching on the streets of "
        "Harlem under the name Allah the Father. His most radical move: if the Original (Black) Man "
        "is God, then there is no need for a distant deity. Allah the Father taught Supreme Mathematics "
        "and the Supreme Alphabet — numerical and alphabetical keys to divine reality — enabling "
        "initiates to read the world as divine text. The theology was deliberately street-level: "
        "Allah spent his time in Harlem's parks reaching young Black men. His followers called "
        "themselves 'Five Percenters': 85% of humanity is mentally enslaved, 10% are bloodsuckers "
        "who maintain their control, and 5% are the poor righteous teachers who know the truth and "
        "share it freely. The scholar Michael Muhammad Knight has called the Five Percenters 'the "
        "most underappreciated religious movement in American history.'"
    ),
    "key_figures": ["Clarence 13X (Allah the Father)", "RZA (Wu-Tang Clan)", "Lord Jamar (Brand Nubian)", "Rakim"],
    "beliefs": [
        "The Black man is God — the Original Man, the Asiatic Blackman",
        "Supreme Mathematics: numerical keys to divine reality",
        "Supreme Alphabet: letters as cosmic principles",
        "The 85/10/5 model of human consciousness and knowledge",
        "Self-knowledge (knowing who you are) is the supreme spiritual act"
    ],
    "impact": (
        "Five Percenter theology is embedded in hip-hop culture so deeply most listeners are unaware "
        "of it. The vocabulary — 'word is bond,' 'the cipher,' 'building,' 'peace,' addressing men as "
        "'God' and women as 'Earth,' 'dropping science' — all derive from 5% Nation. Wu-Tang Clan's "
        "entire cosmology is Five Percenter theology. Poor Righteous Teachers, Brand Nubian, Big "
        "Daddy Kane, Busta Rhymes, and Jay-Z have all engaged the tradition."
    ),
    "spread": [
        {"lat": 40.71, "lon": -74.01,  "city": "New York (Brooklyn/Bronx)", "year": 1966},
        {"lat": 42.36, "lon": -71.06,  "city": "Boston, USA",               "year": 1970},
        {"lat": 41.88, "lon": -87.63,  "city": "Chicago, USA",              "year": 1972},
        {"lat": 34.05, "lon": -118.24, "city": "Los Angeles, USA",          "year": 1975},
        {"lat": 43.65, "lon": -79.38,  "city": "Toronto, Canada",           "year": 1982},
        {"lat": 51.51, "lon": -0.13,   "city": "London, UK",                "year": 1990},
    ],
    "readings": ["Knight, Five Percent Nation", "Tao of Wu (RZA)"],
    "image_file": "five_percent_Img.png"
  },
  {
    "id": 12, "name": "Kabbalah Centre",
    "year_start": 1969, "year_end": None,
    "lat": 31.78, "lon": 35.22, "origin_city": "Jerusalem, Israel",
    "category": "Jewish Mysticism / New Age", "color": "#9370DB",
    "description": (
        "Philip Berg (born Feivel Gruberger) was a former insurance salesman who studied under "
        "Yehuda Brandwein, a kabbalist in the tradition of the 16th-century Safed mystics. After "
        "Brandwein's death, Berg reinterpreted his teacher's mission radically: where traditional "
        "Kabbalah was an elite, male, observant-Jewish practice, Berg's Kabbalah Centre would be "
        "open to everyone. The Centre packaged a simplified, therapeutic Kabbalah — the Zohar as "
        "'spiritual technology' for scanning; the red string as protective amulet; the 72 Names of "
        "God as consciousness tools — and sold it through a global network. By the 1990s, the Los "
        "Angeles centre had become a celebrity destination: Madonna's 1996 immersion transformed the "
        "Kabbalah Centre into an international media phenomenon. The red Kabbalah string became the "
        "decade's most recognizable item of celebrity spiritual fashion. Academic Kabbalists were "
        "horrified; sociologists of religion were fascinated."
    ),
    "key_figures": ["Philip Berg", "Karen Berg", "Yehuda Berg", "Madonna"],
    "beliefs": [
        "Kabbalah as universal technology of consciousness, beyond Jewish exclusivity",
        "The Zohar as a spiritual instrument activated by scanning, not understanding",
        "The red string (from Rachel's Tomb) as protection against the evil eye",
        "The 72 Names of God as meditation tools for specific consciousness states",
        "Transformation of ego (desire to receive) into sharing as spiritual practice"
    ],
    "impact": (
        "The Kabbalah Centre raised fundamental questions about the commodification of sacred "
        "knowledge: who owns a tradition? Can spiritual wisdom be packaged and sold? Is "
        "democratization inevitably distortion? Scholars Boaz Huss and Jody Myers have analyzed it "
        "as a case study of religious globalization and New Age hybridization."
    ),
    "spread": [
        {"lat": 34.05, "lon": -118.24, "city": "Los Angeles, USA",    "year": 1984},
        {"lat": 40.71, "lon": -74.01,  "city": "New York, USA",       "year": 1991},
        {"lat": 32.08, "lon": 34.78,   "city": "Tel Aviv, Israel",    "year": 1990},
        {"lat": 51.51, "lon": -0.13,   "city": "London, UK",          "year": 1999},
        {"lat": 48.85, "lon": 2.35,    "city": "Paris, France",       "year": 2001},
        {"lat": 43.65, "lon": -79.38,  "city": "Toronto, Canada",     "year": 2003},
        {"lat": -23.55,"lon": -46.63,  "city": "São Paulo, Brazil",   "year": 2007},
        {"lat": -33.87,"lon": 151.21,  "city": "Melbourne, Australia","year": 2005},
    ],
    "readings": ["Myers, 'Kabbalah at the Turn of the 21st Century'", "Huss, 'All You Need is LAV – Madonna and Postmodern Kabbalah'"],
    "image_file": "kabbalah_Img.png"
  },
  {
    "id": 13, "name": "Mindfulness & Corporate Wellness",
    "year_start": 1979, "year_end": None,
    "lat": 42.36, "lon": -71.06, "origin_city": "Boston, USA",
    "category": "Secular Spirituality / Wellness", "color": "#20B2AA",
    "description": (
        "In 1979, Jon Kabat-Zinn, a molecular biologist with a Zen practice, introduced "
        "Mindfulness-Based Stress Reduction (MBSR) at the University of Massachusetts Medical School. "
        "His innovation was methodological and strategic: by stripping mindfulness meditation of its "
        "Buddhist philosophical context — no karma, no rebirth, no ethical framework — and reframing "
        "it in the language of neuropsychology and evidence-based medicine, he made it acceptable to "
        "secular healthcare institutions. By the 2010s, mindfulness had migrated from medicine to "
        "corporations: Google's Search Inside Yourself program, McKinsey's mindfulness offerings, the "
        "World Economic Forum's meditation sessions, and tens of thousands of corporate wellness apps "
        "had transformed a Buddhist liberation practice into a productivity tool. Ron Purser's "
        "McMindfulness (2019) mounted the most sustained critique: that corporate mindfulness removes "
        "the ethical and political dimensions of Buddhist practice, teaching workers to manage the "
        "stress of unjust conditions rather than to challenge them."
    ),
    "key_figures": ["Jon Kabat-Zinn", "Thich Nhat Hanh", "Mark Williams", "Zindel Segal"],
    "beliefs": [
        "Present-moment non-judgmental awareness as trainable mental skill",
        "Separation of meditation practice from Buddhist metaphysics and ethics",
        "Wellbeing as quantifiable and optimizable through practice",
        "The brain as plastic: meditation changes neural architecture",
        "Individual stress management as the primary application of contemplative insight"
    ],
    "impact": (
        "The global mindfulness industry — apps, retreats, corporate programs, therapy — is estimated "
        "at $4–5 billion annually. MBCT is recommended by the UK National Health Service. Headspace "
        "has over 70 million users. The debate about secular mindfulness is a microcosm of broader "
        "questions about what happens when spiritual practices are translated across cultural and "
        "institutional boundaries."
    ),
    "spread": [
        {"lat": 40.71, "lon": -74.01,  "city": "New York, USA",          "year": 1990},
        {"lat": 37.39, "lon": -122.08, "city": "Silicon Valley, USA",    "year": 2007},
        {"lat": 51.51, "lon": -0.13,   "city": "London, UK",             "year": 2000},
        {"lat": 52.37, "lon": 4.90,    "city": "Amsterdam, Netherlands", "year": 2008},
        {"lat": 48.85, "lon": 2.35,    "city": "Paris, France",          "year": 2009},
        {"lat": 35.69, "lon": 139.69,  "city": "Tokyo, Japan",           "year": 2010},
        {"lat": -33.87,"lon": 151.21,  "city": "Melbourne, Australia",   "year": 2010},
        {"lat": 12.97, "lon": 77.59,   "city": "Bangalore, India",       "year": 2012},
        {"lat": 37.57, "lon": 126.98,  "city": "Seoul, South Korea",     "year": 2013},
        {"lat": -23.55,"lon": -46.63,  "city": "São Paulo, Brazil",      "year": 2014},
        {"lat": 1.35,  "lon": 103.82,  "city": "Singapore",              "year": 2011},
    ],
    "readings": ["Purser, McMindfulness", "Carette, Selling Spirituality", "Taylor, A Secular Age"],
    "image_file": "mindfulness_Img.png"
  },
  {
    "id": 14, "name": "Communal Living / Hippie Communes",
    "year_start": 1965, "year_end": 1982,
    "lat": 36.17, "lon": -106.08, "origin_city": "New Mexico, USA",
    "category": "Counterculture / Communal", "color": "#6B8E23",
    "description": (
        "Between 1965 and 1975, an estimated 10,000 intentional communities formed across the United "
        "States alone. Drop City in Colorado (1965), the first rural hippie commune, established the "
        "basic template: geodesic domes, communal property, psychedelic sacraments, and the attempt "
        "to build a counter-society outside capitalism. The Farm in Summertown, Tennessee, founded by "
        "Stephen Gaskin and 320 of his San Francisco students in 1971, became the most durable: at "
        "its peak it had 1,500 residents, its own school, publishing house, medical clinic, and "
        "midwifery program (Ina May Gaskin's work there transformed American natural childbirth). "
        "Spiritual frameworks varied: neo-pagan, Buddhist, vaguely Christian, explicitly psychedelic. "
        "What united communes was a shared set of rejections — wage labor, nuclear family, private "
        "property — and affirmations: ecological consciousness, communal childcare, sexual liberation, "
        "and the sacred dimensions of nature."
    ),
    "key_figures": ["Stephen Gaskin", "Ina May Gaskin", "Ram Dass (Richard Alpert)", "Timothy Leary", "Ken Kesey"],
    "beliefs": [
        "Return to the land as spiritual and political practice",
        "Communal property, shared labor, and collective decision-making",
        "Psychedelics (LSD, psilocybin, mescaline) as sacraments of consciousness expansion",
        "Ecological consciousness: nature as sacred, not merely resource",
        "The personal as political: transforming daily life is revolutionary action"
    ],
    "impact": (
        "The commune movement's direct legacy includes: organic farming and the modern food co-op "
        "movement; the modern homebirth and natural childbirth movement; the ecovillage and "
        "intentional community network (now global); and festival culture (Burning Man, Rainbow "
        "Gatherings trace directly to commune culture). The Whole Earth Catalog, published from the "
        "commune network, was Steve Jobs's 'bible' and a direct ancestor of the internet's "
        "information-sharing ethos."
    ),
    "spread": [
        {"lat": 35.66, "lon": -87.04,  "city": "The Farm, Tennessee, USA", "year": 1971},
        {"lat": 51.51, "lon": -0.13,   "city": "England, UK",              "year": 1969},
        {"lat": 59.91, "lon": 10.75,   "city": "Oslo, Norway",             "year": 1972},
        {"lat": 48.85, "lon": 2.35,    "city": "Paris, France",            "year": 1968},
        {"lat": -33.87,"lon": 151.21,  "city": "Sydney, Australia",        "year": 1970},
        {"lat": 52.52, "lon": 13.40,   "city": "Berlin, Germany",          "year": 1968},
    ],
    "readings": ["Altglas, 'From Yoga To Kabbalah'"],
    "image_file": "communes_Img.png"
  },
  {
    "id": 15, "name": "Yoga as Global Practice",
    "year_start": 1980, "year_end": None,
    "lat": 12.97, "lon": 77.59, "origin_city": "Mysore, India",
    "category": "Yoga / Wellness", "color": "#FF6347",
    "description": (
        "The global yoga phenomenon has roots in the Neo-Vedanta mission of Vivekananda and Yogananda, "
        "but its mass cultural form — studios, mats, Lululemon, teacher trainings, Instagram asanas — "
        "is a product of the 1980s–2000s. Krishnamacharya's lineage (Iyengar Yoga, Ashtanga, "
        "Viniyoga) provided the technical vocabulary. B.K.S. Iyengar's Light on Yoga (1966) and "
        "K. Pattabhi Jois's Ashtanga Vinyasa system attracted Western students to Mysore. Bikram "
        "Choudhury's Hot Yoga franchise (Los Angeles, 1974) was yoga's first mass commercialization. "
        "By the 2000s, yoga had fully detached from its Hindu philosophical moorings in much of the "
        "West and become a secular wellness practice: a supplement to gym culture, a stress management "
        "tool, a lifestyle brand. The debate — 'yoga appropriation' vs. 'universally available "
        "body-wisdom' — has been one of the defining cultural controversies of globalized spirituality."
    ),
    "key_figures": ["K. Pattabhi Jois", "B.K.S. Iyengar", "T. Krishnamacharya", "Bikram Choudhury", "Yogi Bhajan"],
    "beliefs": [
        "Union of body, mind, and spirit (yoga = 'yoke')",
        "Asana practice as gateway to deeper states of consciousness",
        "Pranayama (breath work) as the primary tool for consciousness regulation",
        "The subtle body (chakras, nadis, prana) as real and trainable",
        "Self-transformation through disciplined practice and detachment"
    ],
    "impact": (
        "Over 300 million practitioners worldwide. The global yoga industry — studios, clothing, "
        "retreats, teacher training — is estimated at $80+ billion annually. Yoga's globalization "
        "has been one of the most significant transfers of embodied spiritual knowledge in history, "
        "though its commercial form raises profound questions about what is transmitted and what "
        "is lost in translation."
    ),
    "spread": [
        {"lat": 34.05, "lon": -118.24, "city": "Los Angeles, USA",   "year": 1980},
        {"lat": 40.71, "lon": -74.01,  "city": "New York, USA",      "year": 1982},
        {"lat": 43.65, "lon": -79.38,  "city": "Toronto, Canada",    "year": 1983},
        {"lat": 51.51, "lon": -0.13,   "city": "London, UK",         "year": 1985},
        {"lat": 18.97, "lon": 72.82,   "city": "Mumbai, India",      "year": 1985},
        {"lat": -33.87,"lon": 151.21,  "city": "Sydney, Australia",  "year": 1990},
        {"lat": 48.85, "lon": 2.35,    "city": "Paris, France",      "year": 1992},
        {"lat": 52.52, "lon": 13.40,   "city": "Berlin, Germany",    "year": 1988},
        {"lat": -23.55,"lon": -46.63,  "city": "São Paulo, Brazil",  "year": 1995},
        {"lat": 35.69, "lon": 139.69,  "city": "Tokyo, Japan",       "year": 1993},
        {"lat": 37.57, "lon": 126.98,  "city": "Seoul, South Korea", "year": 1998},
        {"lat": 39.91, "lon": 116.39,  "city": "Beijing, China",     "year": 2000},
        {"lat": 55.75, "lon": 37.62,   "city": "Moscow, Russia",     "year": 2000},
        {"lat": 1.35,  "lon": 103.82,  "city": "Singapore",          "year": 1997},
        {"lat": -1.29, "lon": 36.82,   "city": "Nairobi, Kenya",     "year": 2005},
    ],
    "readings": ["Peace, Love and Yoga (Jain)", "Yoga for the City (Documentary Short)"],
    "image_file": "yoga_Img.png"
  },
]

CATEGORIES = sorted(list(set(e["category"] for e in EVENTS)))
CAT_COLORS  = {e["category"]: e["color"] for e in EVENTS}
MIN_YEAR    = min(e["year_start"] for e in EVENTS)
MAX_YEAR    = 2024

# ── SESSION STATE (initialise once) ──────────────────────────────────────────
if "year_slider"    not in st.session_state: st.session_state["year_slider"]    = 1900
if "autoplay"       not in st.session_state: st.session_state["autoplay"]       = False
if "selected_event" not in st.session_state: st.session_state["selected_event"] = None
if "scroll_to_det"  not in st.session_state: st.session_state["scroll_to_det"]  = False
if "filter_open"    not in st.session_state: st.session_state["filter_open"]    = False
for ev in EVENTS:
    if f"ev_{ev['id']}" not in st.session_state:
        st.session_state[f"ev_{ev['id']}"] = True

# ── STATIC HEADER (never reruns) ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>✦ Technologies of the Soul ✦</h1>
  <div class="subtitle">A Cartography of Modern Spirituality · 1743 – Present</div>
</div>
""", unsafe_allow_html=True)

# ── CAPTURE autoplay state BEFORE defining the fragment ──────────────────────
# This value is captured once per full-page run and controls run_every.
_autoplay_for_fragment = st.session_state["autoplay"]

# ── FRAGMENT ─────────────────────────────────────────────────────────────────
# Everything interactive lives here. During autoplay the fragment auto-reruns
# every 0.2 s WITHOUT triggering a full-page rerender, so the map is smooth
# and all controls outside the fragment remain fully responsive.
@st.fragment(run_every=0.2 if _autoplay_for_fragment else None)
def interactive_body():

    # ── Advance year for autoplay (inside fragment) ──────────────────────────
    if st.session_state["autoplay"]:
        cur = st.session_state["year_slider"]
        st.session_state["year_slider"] = (cur + 1) if cur < MAX_YEAR else MIN_YEAR

    # ── Controls row ─────────────────────────────────────────────────────────
    col_s, col_ap, col_f = st.columns([3, 0.7, 1.2])

    with col_s:
        year = st.slider(
            "DRAG TO TRAVEL THROUGH TIME",
            min_value=MIN_YEAR, max_value=MAX_YEAR,
            step=1, key="year_slider"
        )

    with col_ap:
        is_playing = st.session_state["autoplay"]
        if st.button("⏸ PAUSE" if is_playing else "▶ AUTOPLAY",
                     key="ap_btn", use_container_width=True):
            st.session_state["autoplay"] = not is_playing
            # Force a full-page rerun so the fragment is recreated with the
            # new run_every value. Works across Streamlit versions.
            try:
                st.rerun(scope="app")
            except TypeError:
                st.rerun()

    with col_f:
        # Button-toggle: state lives in session_state, never auto-closes
        n_shown = sum(1 for ev in EVENTS if st.session_state.get(f"ev_{ev['id']}", True))
        arrow   = "▴" if st.session_state["filter_open"] else "▾"
        if st.button(f"{n_shown}/{len(EVENTS)} {arrow}",
                     key="filter_toggle_btn", use_container_width=True):
            st.session_state["filter_open"] = not st.session_state["filter_open"]

    # ── Filter dropdown panel ─────────────────────────────────────────────────
    if st.session_state["filter_open"]:
        st.markdown('<div class="filter-panel">', unsafe_allow_html=True)
        sa_c, da_c, _ = st.columns([1, 1, 3])
        with sa_c:
            if st.button("SELECT ALL",   key="sel_all_btn", use_container_width=True):
                for ev in EVENTS: st.session_state[f"ev_{ev['id']}"] = True
        with da_c:
            if st.button("DESELECT ALL", key="desel_all_btn", use_container_width=True):
                for ev in EVENTS: st.session_state[f"ev_{ev['id']}"] = False

        st.markdown("<hr style='margin:0.35rem 0;border-color:#2A2A4A;border-top-width:1px'>",
                    unsafe_allow_html=True)

        for cat in CATEGORIES:
            color = CAT_COLORS[cat]
            st.markdown(
                f'<div class="filter-cat-header" '
                f'style="color:{color};border-bottom:1px solid {color}44">◆ {cat}</div>',
                unsafe_allow_html=True
            )
            for ev in EVENTS:
                if ev["category"] == cat:
                    st.checkbox(ev["name"], key=f"ev_{ev['id']}")

        st.markdown('</div>', unsafe_allow_html=True)

    # ── Derive visible event IDs ──────────────────────────────────────────────
    vis_ids = {ev["id"] for ev in EVENTS if st.session_state.get(f"ev_{ev['id']}", True)}

    # ── Legend ────────────────────────────────────────────────────────────────
    active_cats = {ev["category"] for ev in EVENTS if ev["id"] in vis_ids}
    leg = '<div class="legend-row">'
    for cat in CATEGORIES:
        if cat in active_cats:
            c = CAT_COLORS[cat]
            leg += (f'<div class="legend-item">'
                    f'<div class="legend-dot" style="background:{c}"></div>'
                    f'<span class="legend-txt">{cat}</span></div>')
    leg += '</div>'
    st.markdown(leg, unsafe_allow_html=True)

    # ── Visible events ────────────────────────────────────────────────────────
    def vis(ev, yr):
        return (ev["year_start"] <= yr
                and not ((ev["year_end"] is not None) and yr > ev["year_end"])
                and ev["id"] in vis_ids)

    visible = [ev for ev in EVENTS if vis(ev, year)]

    # ── Build Plotly map ──────────────────────────────────────────────────────
    fig = go.Figure()
    fig.add_trace(go.Scattergeo(lon=[0], lat=[0], mode="markers",
                                marker=dict(size=0, opacity=0),
                                hoverinfo="skip", showlegend=False))

    fig.update_layout(
        uirevision="stable",           # keeps zoom/pan across fragment reruns
        geo=dict(
            showframe=False,
            showcoastlines=True,  coastlinecolor="#2A2A5A", coastlinewidth=0.8,
            showland=True,        landcolor="#151530",
            showocean=True,       oceancolor="#080818",
            showlakes=True,       lakecolor="#0D0D22",
            showcountries=True,   countrycolor="#1E1E40", countrywidth=0.5,
            showrivers=False,
            projection_type="natural earth",
            bgcolor="#080818",
            lataxis_range=[-60, 80],
            resolution=110,
        ),
        paper_bgcolor="#0A0A12", plot_bgcolor="#0A0A12",
        margin=dict(l=0, r=0, t=0, b=0),
        height=540, showlegend=False,
        font=dict(family="Space Mono", color="#8884AA"),
    )

    # ── Selection state for dimming ──────────────────────────────────────────
    sel_id       = st.session_state["selected_event"]
    has_sel      = sel_id is not None

    # ── Flow lines: ONE line-trace + ONE dot-trace per movement (batched) ────
    # Using None-separator technique: trace count = O(movements), not O(spread×segments)
    for ev in visible:
        is_sel   = (ev["id"] == sel_id)
        is_dimmed = has_sel and not is_sel

        line_lons, line_lats = [], []
        dot_lons,  dot_lats  = [], []

        for sp in ev.get("spread", []):
            if sp["year"] <= year:
                line_lons += [ev["lon"], sp["lon"], None]
                line_lats += [ev["lat"], sp["lat"], None]
                dot_lons.append(sp["lon"])
                dot_lats.append(sp["lat"])

        if not line_lons:
            continue

        line_op = 0.08 if is_dimmed else (0.72 if is_sel else 0.45)
        line_w  = 0.5  if is_dimmed else (2.8  if is_sel else 1.6)
        dot_op  = 0.06 if is_dimmed else (0.95 if is_sel else 0.75)
        dot_sz  = 4    if is_dimmed else (9    if is_sel else 7)

        fig.add_trace(go.Scattergeo(
            lon=line_lons, lat=line_lats, mode="lines",
            line=dict(width=line_w, color=ev["color"]),
            opacity=line_op,
            hoverinfo="skip", showlegend=False,
        ))
        fig.add_trace(go.Scattergeo(
            lon=dot_lons, lat=dot_lats, mode="markers",
            marker=dict(size=dot_sz, color=ev["color"], opacity=dot_op,
                        line=dict(width=1.2 if not is_dimmed else 0,
                                  color="#FFFFFF")),
            hoverinfo="skip", showlegend=False,
        ))

    # ── Origin dots ───────────────────────────────────────────────────────────
    for ev in visible:
        age      = year - ev["year_start"]
        pulse    = max(12, min(32, 10 + math.log1p(age) * 5))
        is_sel   = (ev["id"] == sel_id)
        is_dimmed = has_sel and not is_sel

        dot_op   = 0.12 if is_dimmed else 0.93
        dot_color = "#444466" if is_dimmed else ev["color"]
        ring_w   = 0 if is_dimmed else (2.5 if is_sel else 1)
        ring_col = "#FFFFFF" if is_sel else "#0A0A12"
        sz_boost = 4 if is_sel else 0

        # Glow ring for selected
        if is_sel:
            fig.add_trace(go.Scattergeo(
                lon=[ev["lon"]], lat=[ev["lat"]], mode="markers",
                marker=dict(size=pulse + 18, color=ev["color"], opacity=0.18,
                            line=dict(width=0)),
                hoverinfo="skip", showlegend=False,
            ))

        # Show name label: always for selected, briefly for newly appeared
        show_text = is_sel or (age < 8)
        fig.add_trace(go.Scattergeo(
            lon=[ev["lon"]], lat=[ev["lat"]],
            mode="markers+text",
            marker=dict(
                size=pulse + sz_boost, color=dot_color, opacity=dot_op,
                line=dict(width=ring_w, color=ring_col)
            ),
            text=ev["name"] if show_text else "",
            textposition="top center",
            textfont=dict(size=9,
                          color="#E8E4D8" if not is_dimmed else "#33334A",
                          family="Space Mono"),
            customdata=[ev["id"]],
            hovertemplate=(
                f"<b>{ev['name']}</b><br>"
                f"<span style='color:#C9A84C'>{ev['year_start']}</span> · {ev['origin_city']}<br>"
                f"<i>{ev['category']}</i><br>"
                "<span style='color:#8884AA'>Click to explore ↓</span><extra></extra>"
            ),
            showlegend=False,
        ))

    fig.add_annotation(text=str(year), x=0.02, y=0.05, xref="paper", yref="paper",
                       showarrow=False,
                       font=dict(family="Cinzel Decorative", size=40,
                                 color="rgba(232,197,109,0.65)"), align="left")
    if st.session_state["autoplay"]:
        fig.add_annotation(text="▶ AUTOPLAY", x=0.98, y=0.05, xref="paper", yref="paper",
                           showarrow=False,
                           font=dict(family="Space Mono", size=10,
                                     color="rgba(201,168,76,0.7)"), align="right")

    # ── Render map + sidebar ──────────────────────────────────────────────────
    map_col, panel_col = st.columns([2.2, 1])

    with map_col:
        st.markdown(
            f'<div class="counter-badge">✦ {len(visible)} movements active in {year}</div>',
            unsafe_allow_html=True
        )
        click = st.plotly_chart(fig, use_container_width=True, key="main_map",
                                on_select="rerun", selection_mode="points")

        if click and click.get("selection") and click["selection"].get("points"):
            pts = click["selection"]["points"]
            if pts:
                cdata = pts[0].get("customdata")
                if cdata:
                    eid = cdata[0] if isinstance(cdata, list) else cdata
                    if st.session_state["selected_event"] != eid:
                        st.session_state["selected_event"] = eid
                        st.session_state["scroll_to_det"]  = True

        st.markdown("""
        <div class="flow-legend">
          ── Flow lines show geographic spread &nbsp;·&nbsp;
          Brighter origin = more recent &nbsp;·&nbsp; Dot at tip = city of arrival
        </div>
        """, unsafe_allow_html=True)

    with panel_col:
        st.markdown("### ✦ Movements")
        for ev in sorted(visible, key=lambda x: x["year_start"]):
            is_sel  = st.session_state["selected_event"] == ev["id"]
            end_str = "present" if ev["year_end"] is None else str(ev["year_end"])
            label   = f"{'▶ ' if is_sel else ''}{ev['name']} ({ev['year_start']}–{end_str})"
            if st.button(label, key=f"btn_{ev['id']}", use_container_width=True):
                if is_sel:
                    st.session_state["selected_event"] = None
                    st.session_state["scroll_to_det"]  = False
                else:
                    st.session_state["selected_event"] = ev["id"]
                    st.session_state["scroll_to_det"]  = True

    # ── Detail panel ──────────────────────────────────────────────────────────
    if st.session_state["selected_event"]:
        det = next((e for e in EVENTS if e["id"] == st.session_state["selected_event"]), None)
        if det:
            st.markdown("---")
            scroll_js = ""
            if st.session_state["scroll_to_det"]:
                scroll_js = """<script>setTimeout(function(){
                  var el=document.getElementById('detail-anchor');
                  if(el){el.scrollIntoView({behavior:'smooth',block:'start'});}
                },200);</script>"""
                st.session_state["scroll_to_det"] = False
            st.markdown(f'<div id="detail-anchor"></div>{scroll_js}', unsafe_allow_html=True)

            end_label = "present" if det["year_end"] is None else str(det["year_end"])
            img_col, info_col = st.columns([1, 2.5])

            with img_col:
                import os
                img_path = os.path.join("Images", det["image_file"])
                if os.path.exists(img_path):
                    st.image(img_path, use_container_width=True)
                else:
                    c = det["color"]
                    st.markdown(
                        f"<div style='background:{c}22;border:1px solid {c}44;height:180px;"
                        f"border-radius:4px;display:flex;align-items:center;justify-content:center;"
                        f"color:{c};font-family:Cinzel Decorative;font-size:2rem'>✦</div>",
                        unsafe_allow_html=True
                    )

            with info_col:
                tags = "".join(f'<span class="tag">{t}</span>'
                               for t in [det["category"], det["origin_city"]])
                spread_str = " → ".join(
                    sp["city"] for sp in det.get("spread", []) if sp["year"] <= year
                )
                spread_sec = (
                    f'<div class="section-label">Geographic Spread</div>'
                    f'<p>{det["origin_city"]}{(" → " + spread_str) if spread_str else " (origin only)"}</p>'
                ) if det.get("spread") else ""

                beliefs_str = "&nbsp;&nbsp;·&nbsp;&nbsp;".join(det["beliefs"])

                st.markdown(f"""
<div class="event-panel" style="border-left-color:{det['color']}">
  <h3>{det['name']}</h3>
  <div class="event-year">◈ {det['year_start']} — {end_label} &nbsp;|&nbsp; {det['origin_city']}</div>
  {tags}
  <div class="section-label">Overview</div>
  <p>{det['description']}</p>
  <div class="section-label">Core Beliefs &amp; Practices</div>
  <p>{beliefs_str}</p>
  <div class="section-label">Key Figures</div>
  <p>{" · ".join(det['key_figures'])}</p>
  {spread_sec}
  <div class="section-label">Lasting Impact</div>
  <p>{det['impact']}</p>
  <div class="section-label">Related Readings</div>
  <p style="font-style:italic;font-size:0.88rem;color:var(--muted)">{" · ".join(det['readings'])}</p>
</div>
""", unsafe_allow_html=True)

# ── Call the fragment ─────────────────────────────────────────────────────────
interactive_body()

# ── Footer (static, outside fragment) ────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:2rem 0 1rem;border-top:1px solid #2A2A4A;margin-top:2rem">
  <span style="font-family:'Space Mono',monospace;font-size:0.65rem;color:#dadaf5;letter-spacing:0.12em">
    ARTE2101 · TECHNOLOGIES OF THE SOUL · HKU SCHOOL OF HUMANITIES
  </span>
</div>
""", unsafe_allow_html=True)