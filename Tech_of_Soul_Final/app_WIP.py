import streamlit as st
import plotly.graph_objects as go
import time
import math

st.set_page_config(
    page_title="Technologies of the Soul",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Custom CSS ──────────────────────────────────────────────────────────────
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
  background: var(--deep) !important;
  color: var(--text) !important;
  font-family: 'Crimson Pro', serif;
}

button[kind="secondary"] {
  border: 1px solid #2A2A4A !important;
  background: #111120 !important;
  color: #C9A84C !important;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { display: none; }

h1, h2, h3 {
  font-family: 'Cinzel Decorative', serif !important;
  color: var(--gold) !important;
  letter-spacing: 0.06em;
}

.hero {
  text-align: center;
  padding: 2.5rem 1rem 1.5rem;
  border-bottom: 1px solid var(--border);
  margin-bottom: 1.5rem;
  background: radial-gradient(ellipse at 50% 0%, rgba(201,168,76,0.08) 0%, transparent 70%);
}
.hero h1 { font-size: clamp(1.4rem, 3vw, 2.4rem); margin: 0; line-height: 1.3; }
.hero .subtitle {
  font-family: 'Crimson Pro', serif;
  font-style: italic;
  font-size: 1.1rem;
  color: var(--amber);
  margin-top: 0.5rem;
  letter-spacing: 0.04em;
}

[data-testid="stSlider"] > div > div > div > div {
  background: var(--gold) !important;
}
[data-testid="stSlider"] label {
  font-family: 'Space Mono', monospace !important;
  font-size: 0.75rem !important;
  color: var(--muted) !important;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.event-panel {
  background: var(--panel);
  border: 1px solid var(--border);
  border-left: 3px solid var(--gold);
  border-radius: 4px;
  padding: 1.4rem 1.6rem;
  margin-top: 0.5rem;
}
.event-panel h3 {
  font-size: 1.1rem !important;
  margin-bottom: 0.3rem;
}
.event-year {
  font-family: 'Space Mono', monospace;
  font-size: 0.78rem;
  color: var(--amber);
  margin-bottom: 0.8rem;
  letter-spacing: 0.1em;
}
.event-panel p { font-size: 1rem; line-height: 1.7; color: var(--text); margin: 0.5rem 0; }
.event-panel strong { color: var(--gold); }
.tag {
  display: inline-block;
  background: rgba(123,104,238,0.18);
  color: var(--accent);
  border: 1px solid rgba(123,104,238,0.35);
  border-radius: 2px;
  font-family: 'Space Mono', monospace;
  font-size: 0.65rem;
  letter-spacing: 0.08em;
  padding: 0.15rem 0.5rem;
  margin: 0.15rem 0.15rem 0.15rem 0;
}
.section-label {
  font-family: 'Space Mono', monospace;
  font-size: 0.65rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--muted);
  margin: 0.9rem 0 0.25rem;
}
.legend-row {
  display: flex; gap: 1.2rem; flex-wrap: wrap;
  padding: 0.6rem 1rem;
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 4px;
  margin-bottom: 0.8rem;
  align-items: center;
}
.legend-item { display: flex; align-items: center; gap: 0.4rem; }
.legend-dot {
  width: 12px; height: 12px; border-radius: 50%;
  flex-shrink: 0;
}
.legend-txt { font-family: 'Space Mono', monospace; font-size: 0.65rem; color: var(--muted); letter-spacing: 0.05em; }
.counter-badge {
  font-family: 'Space Mono', monospace;
  font-size: 0.7rem;
  color: var(--amber);
  letter-spacing: 0.1em;
  text-align: right;
  padding: 0.2rem 0;
}

/* Autoplay button styling */
.stButton > button {
  font-family: 'Space Mono', monospace !important;
  font-size: 0.7rem !important;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}

div[data-testid="stSelectbox"] label {
  font-family: 'Space Mono', monospace !important;
  font-size: 0.7rem !important;
  color: var(--muted) !important;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

/* Flow line legend */
.flow-legend {
  font-family: 'Space Mono', monospace;
  font-size: 0.62rem;
  color: var(--muted);
  letter-spacing: 0.07em;
  padding: 0.3rem 0;
}

/* Detail anchor */
#detail-anchor {
  scroll-margin-top: 80px;
}
</style>

<script>
function scrollToDetail() {
  const el = document.getElementById('detail-anchor');
  if (el) { el.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
}
</script>
""", unsafe_allow_html=True)

# ── DATA ────────────────────────────────────────────────────────────────────
# year_end = None means ongoing/present; year_end = integer means it faded out
EVENTS = [
  {
    "id": 1, "name": "Swedenborg's Mystical Visions",
    "year_start": 1743, "year_end": 1772,
    "lat": 59.33, "lon": 18.07, "origin_city": "Stockholm, Sweden",
    "category": "Esoteric / Proto-Spiritualism",
    "color": "#E8A87C",
    "description": "Emanuel Swedenborg, a Swedish scientist turned mystic, reported elaborate visions of heaven, hell, and angelic realms. He wrote voluminously about spiritual cosmology and direct communication with spirits, foundationally influencing Western esotericism, New Thought, and 19th-century spiritualism.",
    "key_figures": ["Emanuel Swedenborg"],
    "beliefs": ["Direct spirit communication", "Correspondence between physical and spiritual worlds", "Heaven as a continuation of earthly life", "Rejection of traditional atonement theology"],
    "impact": "Influenced William Blake, Ralph Waldo Emerson, and the Spiritualist movement. His ideas on the inner spiritual life seeded the New Thought and Theosophical traditions.",
    "spread": [],
    "readings": ["Kant and Swedenborg (syllabus)"],
    "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/54/Emanuel_Swedenborg_full_portrait.jpg/440px-Emanuel_Swedenborg_full_portrait.jpg"
  },
  {
    "id": 2, "name": "Mesmerism",
    "year_start": 1774, "year_end": 1850,
    "lat": 48.21, "lon": 16.37, "origin_city": "Vienna, Austria",
    "category": "Proto-Psychology / Healing",
    "color": "#7EC8A8",
    "description": "Franz Anton Mesmer proposed the existence of 'animal magnetism' — an invisible natural force in living things that could be channeled for healing. His theatrical healing sessions prefigured hypnosis, psychosomatic medicine, and later spiritual healing movements.",
    "key_figures": ["Franz Anton Mesmer"],
    "beliefs": ["Animal magnetism / universal fluid", "Healing through energetic transfer", "Altered states of consciousness as therapeutic"],
    "impact": "Precursor to hypnotherapy, psychoanalysis, and modern energy healing. Influenced the New Thought movement and Christian Science.",
    "spread": [{"lat": 48.85, "lon": 2.35, "city": "Paris, France", "year": 1778}],
    "readings": ["Mesmer (Film, syllabus)"],
    "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Mesmer_Being_Depicted_as_a_Quack.jpg/440px-Mesmer_Being_Depicted_as_a_Quack.jpg"
  },
  {
    "id": 3, "name": "Marian Apparitions (Lourdes / Fatima)",
    "year_start": 1858, "year_end": None,
    "lat": 43.09, "lon": -0.05, "origin_city": "Lourdes, France",
    "category": "Catholic Mysticism",
    "color": "#87CEEB",
    "description": "Visions of the Virgin Mary reported by peasant children at Lourdes (1858) and Fatima (1917) became mass pilgrimage sites and sparked intense debate about miracles, modernity, and the boundaries of official religion versus popular spirituality.",
    "key_figures": ["Bernadette Soubirous", "Lúcia Santos", "Francisco Marto"],
    "beliefs": ["Miraculous healing", "Divine intercession outside official church hierarchy", "Ecstatic visionary experience", "Popular Marian devotion"],
    "impact": "Millions of pilgrims annually; institutionalized Catholic mysticism; raised questions about gender, class, and the sacred body in modernity.",
    "spread": [{"lat": 39.66, "lon": -8.67, "city": "Fatima, Portugal", "year": 1917}],
    "readings": ["Zimdars-Swartz, Encountering Mary", "Harris, Lourdes", "Song of Bernadette (Film)", "Fatima (Film)"],
    "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Lourdes_2007.jpg/440px-Lourdes_2007.jpg"
  },
  {
    "id": 4, "name": "Christian Science",
    "year_start": 1866, "year_end": None,
    "lat": 42.36, "lon": -71.06, "origin_city": "Boston, USA",
    "category": "New Religious Movement",
    "color": "#DDA0DD",
    "description": "Mary Baker Eddy founded Christian Science after claiming miraculous self-healing, arguing that illness and matter are illusions resolvable through spiritual understanding. It became a major 19th-century American religious movement blending Christianity with metaphysical idealism.",
    "key_figures": ["Mary Baker Eddy"],
    "beliefs": ["Matter is illusion", "Disease healed through prayer and right thinking", "God as divine Mind", "Rejection of material medicine"],
    "impact": "Influenced New Thought, Unity Church, and prosperity gospel. First major religion founded by an American woman.",
    "spread": [{"lat": 51.51, "lon": -0.13, "city": "London, UK", "year": 1895}],
    "readings": ["Science and Health With Key to the Scriptures (Eddy, syllabus)"],
    "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Mary_Baker_Eddy.jpg/440px-Mary_Baker_Eddy.jpg"
  },
  {
    "id": 5, "name": "Theosophical Society",
    "year_start": 1875, "year_end": None,
    "lat": 40.71, "lon": -74.01, "origin_city": "New York, USA",
    "category": "Esoteric / Occult",
    "color": "#C9A84C",
    "description": "Helena Blavatsky and Henry Olcott founded the Theosophical Society, synthesizing Eastern religions, Western esotericism, and occult philosophy. Theosophy proposed a hidden spiritual wisdom underlying all religions, accessible through esoteric study.",
    "key_figures": ["Helena Petrovna Blavatsky", "Henry Steel Olcott", "Annie Besant"],
    "beliefs": ["Universal brotherhood", "Hidden masters (Mahatmas)", "Karma and reincarnation", "Root races and cosmic evolution", "Synthesis of science, religion, philosophy"],
    "impact": "Enormously influenced modern art (Mondrian, Kandinsky, Hilma af Klint), the independence movement in India, and virtually all subsequent New Age thought.",
    "spread": [
      {"lat": 13.08, "lon": 80.27, "city": "Adyar, India", "year": 1882},
      {"lat": 51.51, "lon": -0.13, "city": "London, UK", "year": 1883},
      {"lat": -33.87, "lon": 151.21, "city": "Sydney, Australia", "year": 1890}
    ],
    "readings": ["Santucci, 'The Theosophical Society'", "Goodrick-Clarke, 'Helena Blavatsky and the Theosophical Society'"],
    "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Helena_Petrovna_Blavatsky.jpg/440px-Helena_Petrovna_Blavatsky.jpg"
  },
  {
    "id": 6, "name": "Anthroposophy (Rudolf Steiner)",
    "year_start": 1912, "year_end": None,
    "lat": 47.54, "lon": 7.59, "origin_city": "Dornach, Switzerland",
    "category": "Esoteric / Occult",
    "color": "#F4A460",
    "description": "Rudolf Steiner broke from Theosophy to found Anthroposophy — a spiritual science emphasizing Christ's unique cosmic role and the development of human spiritual faculties. He applied it to education (Waldorf schools), biodynamic farming, architecture, and medicine.",
    "key_figures": ["Rudolf Steiner"],
    "beliefs": ["Spiritual science bridging religion and knowledge", "Christ event as cosmic turning point", "Clairvoyant perception of spiritual worlds", "Human freedom as spiritual development"],
    "impact": "Waldorf education is now a global school network. Biodynamic farming is a major organic agriculture movement. Deeply influenced esoteric Christianity worldwide.",
    "spread": [
      {"lat": 52.52, "lon": 13.40, "city": "Berlin, Germany", "year": 1913},
      {"lat": 51.51, "lon": -0.13, "city": "London, UK", "year": 1923},
      {"lat": 40.71, "lon": -74.01, "city": "New York, USA", "year": 1928}
    ],
    "readings": ["Staudenmeier, DCE 'Anthroposophy Entry'"],
    "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Rudolf_Steiner_3.jpg/440px-Rudolf_Steiner_3.jpg"
  },
  {
    "id": 7, "name": "Vedanta & Self-Realization Fellowship",
    "year_start": 1893, "year_end": None,
    "lat": 22.57, "lon": 88.36, "origin_city": "Calcutta, India",
    "category": "Hindu-derived / Neo-Vedanta",
    "color": "#FF8C00",
    "description": "Swami Vivekananda's address at the 1893 Parliament of World's Religions launched Vedanta to Western audiences. Paramahansa Yogananda's arrival in 1920 and his Self-Realization Fellowship institutionalized yogic spirituality in America, blending Hindu philosophy with Western seekers.",
    "key_figures": ["Swami Vivekananda", "Paramahansa Yogananda", "Sri Ramakrishna"],
    "beliefs": ["Universal divinity (Atman = Brahman)", "Kriya Yoga as systematic spiritual practice", "All religions as paths to one truth", "Self-realization as life's purpose"],
    "impact": "Yoga's global proliferation traces directly to this lineage. Influenced the Beatles, George Harrison, Steve Jobs, and millions of Western practitioners.",
    "spread": [
      {"lat": 41.88, "lon": -87.63, "city": "Chicago, USA", "year": 1893},
      {"lat": 34.05, "lon": -118.24, "city": "Los Angeles, USA", "year": 1920},
      {"lat": 51.51, "lon": -0.13, "city": "London, UK", "year": 1895}
    ],
    "readings": ["Foxen, Biography of a Yogi", "Segady, 'Globalization, Syncretism, and Identity'", "Raja Yoga (Primary Source)", "Awake (Documentary Film)"],
    "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f9/Yogananda.jpg/440px-Yogananda.jpg"
  },
  {
    "id": 8, "name": "Hare Krishna (ISKCON)",
    "year_start": 1966, "year_end": None,
    "lat": 40.71, "lon": -74.01, "origin_city": "New York, USA",
    "category": "Hindu-derived / Vaishnava",
    "color": "#FFD700",
    "description": "A.C. Bhaktivedanta Swami Prabhupada founded ISKCON (International Society for Krishna Consciousness) in New York, bringing Gaudiya Vaishnava devotion to the Western counterculture. Hare Krishna became iconic in the 1960s–70s, merging Indian bhakti with Western youth rebellion.",
    "key_figures": ["A.C. Bhaktivedanta Swami Prabhupada", "George Harrison"],
    "beliefs": ["Devotional service (bhakti) to Krishna as supreme", "Chanting the Hare Krishna mantra", "Vegetarianism and non-violence", "Rejection of materialism"],
    "impact": "Global network of temples on every continent; influenced George Harrison's spiritual music; normalized public chanting and prasadam distribution in the West.",
    "spread": [
      {"lat": 51.51, "lon": -0.13, "city": "London, UK", "year": 1969},
      {"lat": 27.17, "lon": 78.04, "city": "Vrindavan, India", "year": 1967},
      {"lat": 48.85, "lon": 2.35, "city": "Paris, France", "year": 1972}
    ],
    "readings": ["KRSNA (Primary Source)", "Hare Krishna! (Documentary Film)"],
    "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/A.C._Bhaktivedanta_Swami_Prabhupada.jpg/440px-A.C._Bhaktivedanta_Swami_Prabhupada.jpg"
  },
  {
    "id": 9, "name": "Beat Generation Spirituality",
    "year_start": 1950, "year_end": 1970,
    "lat": 37.78, "lon": -122.41, "origin_city": "San Francisco, USA",
    "category": "Literary / Counterculture",
    "color": "#708090",
    "description": "The Beat writers — Kerouac, Ginsberg, Corso — developed a literary spirituality fusing Zen Buddhism, Catholicism, jazz mysticism, and drug experience. Their work declared the sacred dimensions of everyday life and the road, deeply influencing American spiritual seeking.",
    "key_figures": ["Jack Kerouac", "Allen Ginsberg", "Gary Snyder", "William S. Burroughs"],
    "beliefs": ["The sacred in the profane and marginal", "Zen spontaneity and non-attachment", "Bodily and ecstatic experience as spiritual", "Rejection of suburban conformism"],
    "impact": "Opened American culture to Eastern spirituality and psychedelic consciousness. Ginsberg became a central figure connecting the Beat and hippie spiritual networks.",
    "spread": [
      {"lat": 40.71, "lon": -74.01, "city": "New York, USA", "year": 1950},
      {"lat": 48.85, "lon": 2.35, "city": "Paris, France", "year": 1957}
    ],
    "readings": ["Course readings on counterculture"],
    "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Allen_Ginsberg_in_1979.jpg/440px-Allen_Ginsberg_in_1979.jpg"
  },
  {
    "id": 10, "name": "The Jesus Movement",
    "year_start": 1967, "year_end": 1985,
    "lat": 34.05, "lon": -118.24, "origin_city": "Los Angeles, USA",
    "category": "Christian Counterculture",
    "color": "#98FB98",
    "description": "The Jesus Movement emerged from the California counterculture as young hippies converted to a personal, experiential Christianity. 'Jesus Freaks' rejected institutional church but embraced evangelical spirituality, producing Christian rock, communal living, and youth ministries.",
    "key_figures": ["Lonnie Frisbee", "Chuck Smith", "Keith Green"],
    "beliefs": ["Born-again personal salvation", "Holy Spirit gifts (charismatic)", "Communal intentional living", "Evangelism through music and street witnessing"],
    "impact": "Gave birth to contemporary Christian music (CCM), the Calvary Chapel movement, and charismatic Christianity's global explosion.",
    "spread": [
      {"lat": 37.78, "lon": -122.41, "city": "San Francisco, USA", "year": 1967},
      {"lat": 51.51, "lon": -0.13, "city": "London, UK", "year": 1972}
    ],
    "readings": ["Shires, 'The Countercultural Christians'", "Eskridge, 'Jesus Knocked Me Off My Metaphysical Ass'"],
    "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/JesusPeople.jpg/440px-JesusPeople.jpg"
  },
  {
    "id": 11, "name": "5% Nation of Gods and Earths",
    "year_start": 1964, "year_end": None,
    "lat": 40.71, "lon": -74.01, "origin_city": "Harlem, New York, USA",
    "category": "Black Spiritual Movement",
    "color": "#DC143C",
    "description": "Clarence 13X (Allah the Father) left the Nation of Islam to found the Five Percenters, teaching that the Black man is God — the original human — and that 5% of humanity possesses divine knowledge. Their Supreme Mathematics became a major influence on hip-hop culture.",
    "key_figures": ["Clarence 13X (Allah the Father)", "RZA (Wu-Tang Clan)", "Lord Jamar"],
    "beliefs": ["Black man as original God", "Supreme Mathematics and Supreme Alphabet", "85/10/5 model of humanity", "Self-knowledge as liberation"],
    "impact": "Profoundly shaped hip-hop theology, particularly Wu-Tang Clan, Poor Righteous Teachers, Brand Nubian. A distinct African-American alternative spirituality.",
    "spread": [
      {"lat": 34.05, "lon": -118.24, "city": "Los Angeles, USA", "year": 1975},
      {"lat": 42.36, "lon": -71.06, "city": "Boston, USA", "year": 1970}
    ],
    "readings": ["Knight, Five Percent Nation", "Walker, 'The Black Muslims in American Society'", "Tao of Wu (RZA)"],
    "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Wu-Tang_Clan.jpg/440px-Wu-Tang_Clan.jpg"
  },
  {
    "id": 12, "name": "Kabbalah Center",
    "year_start": 1969, "year_end": None,
    "lat": 31.78, "lon": 35.22, "origin_city": "Jerusalem, Israel",
    "category": "Jewish Mysticism / New Age",
    "color": "#9370DB",
    "description": "Philip Berg founded the Kabbalah Centre to democratize Jewish mysticism, making Kabbalistic teachings accessible to non-Jews and non-observant Jews. The Centre became a global celebrity phenomenon in the 1990s–2000s, most famously associated with Madonna.",
    "key_figures": ["Philip Berg", "Karen Berg", "Madonna"],
    "beliefs": ["Kabbalah as universal wisdom beyond Judaism", "Red string for protection", "Zohar as spiritual technology", "Consciousness transformation through study"],
    "impact": "Brought Kabbalah to global popular culture. Raised significant debate about commodification of sacred knowledge and authenticity.",
    "spread": [
      {"lat": 34.05, "lon": -118.24, "city": "Los Angeles, USA", "year": 1984},
      {"lat": 51.51, "lon": -0.13, "city": "London, UK", "year": 1999},
      {"lat": 48.85, "lon": 2.35, "city": "Paris, France", "year": 2001}
    ],
    "readings": ["Myers, 'Kabbalah at the Turn of the 21st Century'", "Huss, 'All You Need is LAV – Madonna and Postmodern Kabbalah'"],
    "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Philip_Berg.jpg/440px-Philip_Berg.jpg"
  },
  {
    "id": 13, "name": "Mindfulness & Corporate Wellness",
    "year_start": 1979, "year_end": None,
    "lat": 42.36, "lon": -71.06, "origin_city": "Boston, USA",
    "category": "Secular Spirituality / Wellness",
    "color": "#20B2AA",
    "description": "Jon Kabat-Zinn's development of Mindfulness-Based Stress Reduction (MBSR) at UMass Medical School in 1979 launched a global secular mindfulness movement. By the 2000s–2010s, mindfulness had been absorbed into corporate culture, healthcare, and Silicon Valley as 'McMindfulness'.",
    "key_figures": ["Jon Kabat-Zinn", "Thich Nhat Hanh", "Sam Harris"],
    "beliefs": ["Present-moment non-judgmental awareness", "Separation of meditation from Buddhist ethics", "Wellbeing as personal productivity", "Neurological basis of meditation"],
    "impact": "Multi-billion dollar wellness industry. Raises critical questions about the commodification of contemplative practice and spiritual bypassing.",
    "spread": [
      {"lat": 37.39, "lon": -122.08, "city": "Silicon Valley, USA", "year": 2007},
      {"lat": 51.51, "lon": -0.13, "city": "London, UK", "year": 2000},
      {"lat": 35.69, "lon": 139.69, "city": "Tokyo, Japan", "year": 2010}
    ],
    "readings": ["Purser, McMindfullness", "Carette, Selling Spirituality", "Taylor, A Secular Age"],
    "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Jon_Kabat-Zinn.jpg/440px-Jon_Kabat-Zinn.jpg"
  },
  {
    "id": 14, "name": "Communal Living / Hippie Communes",
    "year_start": 1965, "year_end": 1982,
    "lat": 36.17, "lon": -106.08, "origin_city": "New Mexico, USA",
    "category": "Counterculture / Communal",
    "color": "#6B8E23",
    "description": "Thousands of intentional communities formed across America during the late 1960s–70s, from Drop City in Colorado to The Farm in Tennessee. These experiments blended ecological living, psychedelic mysticism, Eastern philosophy, and neo-pagan practice into new social forms.",
    "key_figures": ["Stephen Gaskin", "Ram Dass", "Timothy Leary"],
    "beliefs": ["Return to the land as spiritual practice", "Communal property and shared living", "Psychedelics as sacrament", "Ecological consciousness as sacred"],
    "impact": "Seeds of modern organic farming, intentional community movement, ecovillage networks, and festival culture.",
    "spread": [
      {"lat": 35.66, "lon": -87.04, "city": "Tennessee, USA", "year": 1971},
      {"lat": 51.51, "lon": -0.13, "city": "England, UK", "year": 1969}
    ],
    "readings": ["Altglas, 'From Yoga To Kabbalah'", "Course materials on counterculture"],
    "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Woodstock_redmond_hair.JPG/440px-Woodstock_redmond_hair.JPG"
  },
  {
    "id": 15, "name": "Yoga as Global Practice",
    "year_start": 1980, "year_end": None,
    "lat": 12.97, "lon": 77.59, "origin_city": "Mysore, India",
    "category": "Yoga / Wellness",
    "color": "#FF6347",
    "description": "From the 1980s onward, yoga exploded from a niche spiritual practice into a global multi-billion dollar industry. Styles like Ashtanga, Bikram, Kundalini, and Yin spread through studios, celebrity culture, and media, raising debates about commodification, cultural appropriation, and deracination.",
    "key_figures": ["K. Pattabhi Jois", "B.K.S. Iyengar", "Bikram Choudhury", "Yogi Bhajan"],
    "beliefs": ["Union of body, mind, spirit", "Asana as gateway to deeper practice", "Breathwork (pranayama) as consciousness tool"],
    "impact": "Over 300 million practitioners worldwide. A central site of debate about authentic spirituality vs. commodified wellness.",
    "spread": [
      {"lat": 34.05, "lon": -118.24, "city": "Los Angeles, USA", "year": 1980},
      {"lat": 51.51, "lon": -0.13, "city": "London, UK", "year": 1985},
      {"lat": -33.87, "lon": 151.21, "city": "Sydney, Australia", "year": 1990},
      {"lat": 48.85, "lon": 2.35, "city": "Paris, France", "year": 1992}
    ],
    "readings": ["Peace, Love and Yoga (Jain)", "Yoga for the City (Documentary Short)"],
    "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Yoga_at_a_Gym.jpg/440px-Yoga_at_a_Gym.jpg"
  }
]

CATEGORIES = sorted(list(set(e["category"] for e in EVENTS)))
CAT_COLORS = {e["category"]: e["color"] for e in EVENTS}
MIN_YEAR = min(e["year_start"] for e in EVENTS)
MAX_YEAR = 2024

# ── SESSION STATE ────────────────────────────────────────────────────────────
if "selected_event" not in st.session_state:
    st.session_state.selected_event = None
if "year" not in st.session_state:
    st.session_state.year = 1900
if "autoplay" not in st.session_state:
    st.session_state.autoplay = False
if "scroll_to_detail" not in st.session_state:
    st.session_state.scroll_to_detail = False

# ── HEADER ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>✦ Technologies of the Soul ✦</h1>
  <div class="subtitle">A Cartography of Modern Spirituality · 1740 – Present</div>
</div>
""", unsafe_allow_html=True)

# ── AUTOPLAY LOGIC ───────────────────────────────────────────────────────────
# Advance year if autoplay is running
if st.session_state.autoplay:
    current_year = st.session_state.year
    next_year = current_year + 1
    if next_year > MAX_YEAR:
        next_year = MIN_YEAR  # loop back
    st.session_state.year = next_year

# ── CONTROLS ROW ────────────────────────────────────────────────────────────
col_slider, col_ap = st.columns([3, 0.7])

with col_slider:
    year = st.slider(
        "DRAG TO TRAVEL THROUGH TIME",
        min_value=MIN_YEAR,
        max_value=MAX_YEAR,
        value=st.session_state.year,
        step=1,
        key="year_slider"
    )
    # Sync slider with session state (manual drag overrides autoplay)
    if year != st.session_state.year and not st.session_state.autoplay:
        st.session_state.year = year
    elif not st.session_state.autoplay:
        st.session_state.year = year
    year = st.session_state.year

with col_ap:
    ap_label = "⏸ PAUSE" if st.session_state.autoplay else "▶ AUTOPLAY"
    if st.button(ap_label, key="autoplay_btn", width="stretch"):
        st.session_state.autoplay = not st.session_state.autoplay
        st.rerun()

# ── FILTER EVENTS (respecting both start and end year) ───────────────────────
def is_event_visible(e, yr):
    started = e["year_start"] <= yr
    ended = (e["year_end"] is not None) and (yr > e["year_end"])
    in_cat = e["category"] in selected_cats
    return started and not ended and in_cat

visible_events = [e for e in EVENTS if is_event_visible(e, year)]

# ── BUILD MAP ────────────────────────────────────────────────────────────────
fig = go.Figure()

# Always add a hidden trace so the geo map renders even with 0 events
fig.add_trace(go.Scattergeo(
    lon=[0],
    lat=[0],
    mode="markers",
    marker=dict(size=0, opacity=0),
    hoverinfo="skip",
    showlegend=False
))

fig.update_layout(
    geo=dict(
        showframe=False,
        showcoastlines=True, coastlinecolor="#2A2A5A", coastlinewidth=0.8,
        showland=True, landcolor="#151530",
        showocean=True, oceancolor="#080818",
        showlakes=True, lakecolor="#0D0D22",
        showcountries=True, countrycolor="#1E1E40", countrywidth=0.5,
        showrivers=False,
        projection_type="natural earth",
        bgcolor="#080818",
        lataxis_range=[-60, 80],
        resolution=110,
    ),
    paper_bgcolor="#0A0A12",
    plot_bgcolor="#0A0A12",
    margin=dict(l=0, r=0, t=0, b=0),
    height=540,
    showlegend=False,
    font=dict(family="Space Mono", color="#8884AA"),
)

# ── ANIMATED FLOW LINES ───────────────────────────────────────────────────────
# We simulate animation by drawing multiple overlapping segments with
# decreasing opacity to create a "trail" / comet effect showing direction.
# The denser end = origin, sparser end = destination = visual movement cue.
def draw_flow_line(fig, origin_lat, origin_lon, dest_lat, dest_lon, color, year_spread, current_year):
    """Draw a directional flow line with a gradient trail effect."""
    years_since = current_year - year_spread
    if years_since < 0:
        return

    # Overall fade — lines older than 60 years become very subtle
    age_opacity = max(0.08, 0.7 - years_since * 0.008)

    # Draw 6 segments along the path with decreasing opacity (origin → dest)
    # This gives the line a "comet tail" look: bright at origin, dim at dest
    N = 6
    lats = [origin_lat + (dest_lat - origin_lat) * i / N for i in range(N + 1)]
    lons = [origin_lon + (dest_lon - origin_lon) * i / N for i in range(N + 1)]

    for i in range(N):
        frac = i / N  # 0 = near origin, 1 = near dest
        # Segment opacity: fade out toward destination
        seg_opacity = age_opacity * (1 - frac * 0.75)
        seg_width = 2.5 - frac * 1.5  # thicker at origin

        fig.add_trace(go.Scattergeo(
            lon=[lons[i], lons[i + 1]],
            lat=[lats[i], lats[i + 1]],
            mode="lines",
            line=dict(width=seg_width, color=color),
            opacity=seg_opacity,
            hoverinfo="skip",
            showlegend=False,
        ))

    # Arrowhead at destination (small bright dot)
    arrow_opacity = age_opacity * 0.9
    fig.add_trace(go.Scattergeo(
        lon=[dest_lon], lat=[dest_lat],
        mode="markers",
        marker=dict(
            size=6,
            color=color,
            symbol="circle",
            opacity=arrow_opacity,
            line=dict(width=1.5, color="#FFFFFF")
        ),
        hoverinfo="skip",
        showlegend=False,
    ))

# Draw flow lines
for e in visible_events:
    for sp in e.get("spread", []):
        if sp["year"] <= year:
            draw_flow_line(
                fig,
                e["lat"], e["lon"],
                sp["lat"], sp["lon"],
                e["color"],
                sp["year"], year
            )

# Origin dots — size grows with age, brighten if selected
for e in visible_events:
    age = year - e["year_start"]
    # Pulse grows logarithmically
    pulse = max(12, min(30, 10 + math.log1p(age) * 5))
    is_selected = st.session_state.selected_event == e["id"]

    # Glow ring behind selected
    if is_selected:
        fig.add_trace(go.Scattergeo(
            lon=[e["lon"]], lat=[e["lat"]],
            mode="markers",
            marker=dict(
                size=pulse + 14,
                color=e["color"],
                symbol="circle",
                opacity=0.15,
                line=dict(width=0)
            ),
            hoverinfo="skip",
            showlegend=False,
        ))

    fig.add_trace(go.Scattergeo(
        lon=[e["lon"]], lat=[e["lat"]],
        mode="markers+text",
        marker=dict(
            size=pulse if not is_selected else pulse + 4,
            color=e["color"],
            symbol="circle",
            opacity=0.92,
            line=dict(
                width=2.5 if is_selected else 1,
                color="#FFFFFF" if is_selected else "#0A0A12"
            )
        ),
        text=e["name"] if (age < 8 or is_selected) else "",
        textposition="top center",
        textfont=dict(size=9, color="#E8E4D8", family="Space Mono"),
        customdata=[e["id"]],
        hovertemplate=(
            f"<b>{e['name']}</b><br>"
            f"<span style='color:#C9A84C'>{e['year_start']}</span> · {e['origin_city']}<br>"
            f"<i>{e['category']}</i><br>"
            "<span style='color:#8884AA'>Click to explore ↓</span>"
            "<extra></extra>"
        ),
        showlegend=False,
    ))

# Year watermark — much brighter and more legible
fig.add_annotation(
    text=str(year),
    x=0.02, y=0.05, xref="paper", yref="paper",
    showarrow=False,
    font=dict(family="Cinzel Decorative", size=40, color="rgba(232,197,109,0.65)"),
    align="left"
)

# Autoplay indicator
if st.session_state.autoplay:
    fig.add_annotation(
        text="▶ AUTOPLAY",
        x=0.98, y=0.05, xref="paper", yref="paper",
        showarrow=False,
        font=dict(family="Space Mono", size=10, color="rgba(201,168,76,0.7)"),
        align="right"
    )

# ── RENDER ────────────────────────────────────────────────────────────────────
map_col, legend_col, panel_col = st.columns([2.2, 0.7, 1])

with map_col:
    with legend_col:
      st.markdown("### ✦ Legend")

      selected_cats = []
      current_selection = st.session_state.get("cat_filter", CATEGORIES)

      for cat in CATEGORIES:
          col_hex = CAT_COLORS.get(cat, "#888")

          c1, c2 = st.columns([0.25, 0.75])

          with c1:
              st.markdown(
                  f"<div style='width:12px;height:12px;border-radius:50%;background:{col_hex};margin-top:8px'></div>",
                  unsafe_allow_html=True
              )

          with c2:
              checked = st.checkbox(
                  cat,
                  value=(cat in current_selection),
                  key=f"chk_{cat}"
              )

          if checked:
              selected_cats.append(cat)

      st.session_state.cat_filter = selected_cats
    
    st.markdown(
      f"<div class='counter-badge'>Showing {len(selected_cats)} categories</div>",
      unsafe_allow_html=True
    )


    st.markdown(
        f'<div class="counter-badge">✦ {len(visible_events)} movements active in {year}</div>',
        unsafe_allow_html=True
    )

    click = st.plotly_chart(fig, width="stretch", key="main_map",
                            on_select="rerun", selection_mode="points")

    # Handle map click
    if click and click.get("selection") and click["selection"].get("points"):
        pts = click["selection"]["points"]
        if pts:
            pt = pts[0]
            cdata = pt.get("customdata")
            if cdata:
                eid = cdata[0] if isinstance(cdata, list) else cdata
                if st.session_state.selected_event != eid:
                    st.session_state.selected_event = eid
                    st.session_state.scroll_to_detail = True
                    st.session_state.autoplay = False  # pause autoplay on click
                    st.rerun()

    # Flow line legend
    st.markdown("""
    <div class="flow-legend">
      ── Flow lines show geographic spread &nbsp;·&nbsp; Brighter origin = more recent &nbsp;·&nbsp;
      Dot at arrow tip = city of arrival
    </div>
    """, unsafe_allow_html=True)

with panel_col:
    st.markdown("### ✦ Movements")
    for e in sorted(visible_events, key=lambda x: x["year_start"]):
        is_sel = st.session_state.selected_event == e["id"]
        end_str = "present" if e["year_end"] is None else str(e["year_end"])
        label = f"{'▶ ' if is_sel else ''}{e['name']} ({e['year_start']}–{end_str})"
        if st.button(label, key=f"btn_{e['id']}", width="stretch"):
            if is_sel:
                st.session_state.selected_event = None
                st.session_state.scroll_to_detail = False
            else:
                st.session_state.selected_event = e["id"]
                st.session_state.scroll_to_detail = True
                st.session_state.autoplay = False
            st.rerun()

# ── DETAIL PANEL ─────────────────────────────────────────────────────────────
if st.session_state.selected_event:
    ev = next((e for e in EVENTS if e["id"] == st.session_state.selected_event), None)
    if ev:
        st.markdown("---")

        # Anchor div + auto-scroll JS
        scroll_js = ""
        if st.session_state.scroll_to_detail:
            scroll_js = """
            <script>
              setTimeout(function() {
                var el = document.getElementById('detail-anchor');
                if (el) { el.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
              }, 200);
            </script>
            """
            st.session_state.scroll_to_detail = False

        st.markdown(
            f'<div id="detail-anchor"></div>{scroll_js}',
            unsafe_allow_html=True
        )

        end_label = "present" if ev["year_end"] is None else str(ev["year_end"])
        img_col, info_col = st.columns([1, 2.5])

        with img_col:
            try:
                st.image(ev["image_url"], width="stretch")
            except Exception:
                c = ev["color"]
                st.markdown(
                    f"<div style='background:{c}22;border:1px solid {c}44;height:180px;"
                    f"border-radius:4px;display:flex;align-items:center;justify-content:center;"
                    f"color:{c};font-family:Cinzel Decorative;font-size:2rem'>✦</div>",
                    unsafe_allow_html=True
                )

        with info_col:
            tags_html = "".join(
                f'<span class="tag">{t}</span>'
                for t in [ev["category"], ev["origin_city"]]
            )
            spread_cities = " → ".join(sp["city"] for sp in ev.get("spread", []) if sp["year"] <= year)
            spread_section = f"""
  <div class="section-label">Geographic Spread</div>
  <p>{ev['origin_city']}{(' → ' + spread_cities) if spread_cities else ' (origin only)'}</p>
""" if ev.get("spread") else ""

            st.markdown(f"""
<div class="event-panel" style="border-left-color:{ev['color']}">
  <h3>{ev['name']}</h3>
  <div class="event-year">◈ {ev['year_start']} — {end_label} &nbsp;|&nbsp; {ev['origin_city']}</div>
  {tags_html}
  <div class="section-label">Overview</div>
  <p>{ev['description']}</p>
  <div class="section-label">Core Beliefs & Practices</div>
  <p>{"&nbsp;&nbsp;·&nbsp;&nbsp;".join(ev['beliefs'])}</p>
  <div class="section-label">Key Figures</div>
  <p>{" · ".join(ev['key_figures'])}</p>
  {spread_section}
  <div class="section-label">Lasting Impact</div>
  <p>{ev['impact']}</p>
  <div class="section-label">Related Readings</div>
  <p style="font-style:italic;font-size:0.88rem;color:var(--muted)">{" · ".join(ev['readings'])}</p>
</div>
""", unsafe_allow_html=True)

# ── AUTOPLAY RERUN LOOP ───────────────────────────────────────────────────────
# When autoplay is active, sleep briefly then trigger a rerun
if st.session_state.autoplay:
    time.sleep(0.12)  # ~8 years/second
    st.rerun()

# ── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:2rem 0 1rem;border-top:1px solid #2A2A4A;margin-top:2rem">
  <span style="font-family:'Space Mono',monospace;font-size:0.65rem;color:#3A3A5A;letter-spacing:0.12em">
    ARTE2101 · TECHNOLOGIES OF THE SOUL · HKU SCHOOL OF HUMANITIES
  </span>
</div>
""", unsafe_allow_html=True)