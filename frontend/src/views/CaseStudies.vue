<template>
  <div class="cs">
    <div class="cs__grid-bg"></div>
    <div class="cs__orb cs__orb--orange"></div>
    <div class="cs__orb cs__orb--blue"></div>

    <!-- Topbar -->
    <header class="cs__topbar">
      <div class="cs__topbar-inner">
        <div class="cs__logo font-headline" @click="goHome" style="cursor:pointer">
          <span class="cs__logo-dot"></span>Predly
        </div>
        <nav class="cs__nav">
          <a class="cs__nav-link font-mono" @click.prevent="goHome" href="#">Simulations</a>
          <a class="cs__nav-link cs__nav-link--active font-mono" href="#">Case Studies</a>
        </nav>
        <button class="cs__inquiry-btn font-headline" @click="goHome">Inquiry</button>
      </div>
    </header>

    <!-- Main content -->
    <main class="cs__main">
      <!-- Header section -->
      <section class="cs__header">
        <div class="cs__badge font-mono">EVIDENCE OF PERFORMANCE</div>
        <h1 class="cs__title">Real-World Impact</h1>
        <p class="cs__subtitle">
          We don't just provide data; we provide outcomes. Explore how industry leaders
          utilize Predly Engine to architect their competitive advantage through
          cinematic-grade intelligence.
        </p>
      </section>

      <!-- Featured case study -->
      <section class="cs__featured">
        <div class="cs__featured-card" @click="openDetail(caseStudies[0])">
          <div class="cs__featured-left">
            <div class="cs__featured-sector font-mono">
              <span class="cs__sector-icon">{{ caseStudies[0].icon }}</span>
              {{ caseStudies[0].sector }}
            </div>
            <h2 class="cs__featured-title">{{ caseStudies[0].featuredTitle }}</h2>
            <div class="cs__featured-cols">
              <div class="cs__col">
                <div class="cs__col-label font-mono">THE CHALLENGE</div>
                <p class="cs__col-text">{{ caseStudies[0].challenge.slice(0, 120) }}…</p>
              </div>
              <div class="cs__col">
                <div class="cs__col-label font-mono">THE SOLUTION</div>
                <p class="cs__col-text">{{ caseStudies[0].solution.slice(0, 120) }}…</p>
              </div>
              <div class="cs__col">
                <div class="cs__col-label font-mono">THE RESULT</div>
                <p class="cs__col-text">{{ caseStudies[0].results[0] }}</p>
              </div>
            </div>
          </div>
          <div class="cs__featured-right">
            <div class="cs__stat-card cs__stat-card--accent">
              <div class="cs__stat-label font-mono">ACCURACY GAIN</div>
              <div class="cs__stat-value">{{ caseStudies[0].statMain }}</div>
              <p class="cs__stat-desc">{{ caseStudies[0].statDesc }}</p>
            </div>
            <div class="cs__stat-row">
              <div class="cs__stat-mini">
                <div class="cs__stat-mini-label font-mono">AGENTS</div>
                <div class="cs__stat-mini-value">{{ caseStudies[0].agents }}</div>
                <span class="material-symbols-outlined cs__stat-mini-icon">hub</span>
              </div>
              <div class="cs__stat-mini">
                <div class="cs__stat-mini-label font-mono">CYCLES</div>
                <div class="cs__stat-mini-value">{{ caseStudies[0].cycles }}</div>
                <span class="material-symbols-outlined cs__stat-mini-icon">bolt</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Quote -->
        <div class="cs__quote">
          <p class="cs__quote-text">"{{ caseStudies[0].insight }}"</p>
          <div class="cs__quote-author">
            <div class="cs__quote-avatar">{{ caseStudies[0].icon }}</div>
            <div>
              <div class="cs__quote-name">Predly Engine</div>
              <div class="cs__quote-role font-mono">Key Insight — {{ caseStudies[0].sector }}</div>
            </div>
          </div>
        </div>
      </section>

      <!-- More case studies grid -->
      <section class="cs__more">
        <div class="cs__more-header">
          <div>
            <h3 class="cs__more-title">More Success Stories</h3>
            <p class="cs__more-sub">Deep dives into how Predly Engine transforms diverse industry sectors.</p>
          </div>
          <button class="cs__view-all font-mono" @click="selectedAll = !selectedAll">
            {{ selectedAll ? 'SHOW LESS' : 'VIEW ALL CASE STUDIES' }} →
          </button>
        </div>
        <div class="cs__grid">
          <div
            v-for="cs in displayedStudies"
            :key="cs.id"
            class="cs__card"
            @click="openDetail(cs)"
          >
            <div class="cs__card-img">
              <div class="cs__card-icon-bg">{{ cs.icon }}</div>
              <div class="cs__card-sector-badge font-mono">{{ cs.sectorShort }}</div>
            </div>
            <div class="cs__card-body">
              <h4 class="cs__card-title">{{ cs.title }}</h4>
              <p class="cs__card-desc">{{ cs.challenge.slice(0, 100) }}…</p>
              <div class="cs__card-meta font-mono">
                <span>{{ cs.agents }} agents</span>
                <span class="cs__card-arrow">→</span>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>

    <!-- Footer -->
    <footer class="cs__footer">
      <div class="cs__footer-inner">
        <span class="cs__footer-brand font-headline">Predly Engine</span>
        <div class="cs__footer-links font-mono">
          <a href="#">Privacy Policy</a>
          <a href="#">Terms of Service</a>
          <a href="#">Security</a>
          <a href="#">Status</a>
          <a href="#">Contact</a>
        </div>
      </div>
      <div class="cs__footer-copy font-mono">© 2024 Predly Engine. Obsidian Architect Protocol.</div>
    </footer>

    <!-- Detail Modal -->
    <Transition name="modal">
      <div v-if="activeStudy" class="cs__modal-overlay" @click.self="closeDetail">
        <div class="cs__modal">
          <button class="cs__modal-close" @click="closeDetail">
            <span class="material-symbols-outlined">close</span>
          </button>
          <div class="cs__modal-sector font-mono">
            <span>{{ activeStudy.icon }}</span> {{ activeStudy.sector }}
          </div>
          <h2 class="cs__modal-title">{{ activeStudy.featuredTitle }}</h2>

          <div class="cs__modal-stats">
            <div class="cs__modal-stat">
              <div class="cs__modal-stat-val">{{ activeStudy.statMain }}</div>
              <div class="cs__modal-stat-lbl font-mono">Accuracy Gain</div>
            </div>
            <div class="cs__modal-stat">
              <div class="cs__modal-stat-val">{{ activeStudy.agents }}</div>
              <div class="cs__modal-stat-lbl font-mono">Agents Deployed</div>
            </div>
            <div class="cs__modal-stat">
              <div class="cs__modal-stat-val">{{ activeStudy.cycles }}</div>
              <div class="cs__modal-stat-lbl font-mono">Sim Cycles</div>
            </div>
          </div>

          <div class="cs__modal-sections">
            <div class="cs__modal-section">
              <div class="cs__modal-section-label font-mono">THE CHALLENGE</div>
              <p class="cs__modal-section-text">{{ activeStudy.challenge }}</p>
            </div>
            <div class="cs__modal-section">
              <div class="cs__modal-section-label font-mono">THE SOLUTION</div>
              <p class="cs__modal-section-text">{{ activeStudy.solution }}</p>
              <ul class="cs__modal-list">
                <li v-for="(item, i) in activeStudy.solutionPoints" :key="i">{{ item }}</li>
              </ul>
            </div>
            <div class="cs__modal-section">
              <div class="cs__modal-section-label font-mono">THE RESULTS</div>
              <ul class="cs__modal-results">
                <li v-for="(r, i) in activeStudy.results" :key="i">
                  <span class="cs__modal-result-dot"></span>{{ r }}
                </li>
              </ul>
            </div>
            <div class="cs__modal-insight">
              <div class="cs__modal-insight-label font-mono">KEY INSIGHT</div>
              <p class="cs__modal-insight-text">"{{ activeStudy.insight }}"</p>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const activeStudy = ref(null)
const selectedAll = ref(false)

function goHome() { router.push({ name: 'Home' }) }
function openDetail(study) { activeStudy.value = study }
function closeDetail() { activeStudy.value = null }

const displayedStudies = computed(() =>
  selectedAll.value ? caseStudies.slice(1) : caseStudies.slice(1, 4)
)

const caseStudies = [
  {
    id: 1,
    icon: '💰',
    sector: 'FINANCE SECTOR FOCUS',
    sectorShort: 'FINANCE',
    title: 'Financial Market Sentiment Prediction',
    featuredTitle: 'Rate Shock Simulation: Anticipating Market Volatility',
    challenge: 'Traditional financial models struggle to react to real-time macroeconomic shocks, particularly when unstructured data—news sentiment, analyst opinions, and social discourse—drives rapid shifts in market behavior. During central bank rate hikes, delayed interpretation often leads to missed opportunities and amplified losses.',
    solution: 'Predly Engine deployed a 1,200-agent simulation environment modeling retail investors, institutional traders, journalists, and analysts. By ingesting policy announcements, financial news, and economic forecasts, agents dynamically interacted across dual social environments (fast + deep reasoning layers).',
    solutionPoints: ['Real-time sentiment propagation tracking', 'Behavioral modeling across investor classes', 'Early detection of narrative-driven volatility'],
    results: ['Early identification of sell-off triggers before market execution', 'Improved volatility prediction accuracy by ~38–42%', 'Detection of sentiment-driven price divergence from fundamentals'],
    insight: 'Market volatility is not triggered by events alone—but by how those events are collectively interpreted and amplified.',
    statMain: '~40%',
    statDesc: 'Improved volatility prediction accuracy across simulation runs.',
    agents: '1,200',
    cycles: '48+',
  },
  {
    id: 2,
    icon: '🌍',
    sector: 'GEOPOLITICAL FOCUS',
    sectorShort: 'GEOPOLITICAL',
    title: 'Geopolitical Conflict Simulation',
    featuredTitle: 'Global Sentiment Mapping During Crisis Escalation',
    challenge: 'In geopolitical crises, information spreads faster than verification. Decision-makers lack visibility into how narratives evolve across populations, leading to delayed or misaligned responses.',
    solution: 'Predly simulated 2,000 agents across global regions, including citizens, media entities, governments, and activists. The system modeled real-time discourse using multi-source inputs—news, statements, and historical conflict patterns.',
    solutionPoints: ['Information propagation modeling', 'Bias-driven interpretation tracking', 'Influence amplification detection'],
    results: ['Polarization patterns detected within first 5 simulation cycles', 'Early identification of misinformation dominance zones', 'Prediction of trust collapse across media channels'],
    insight: 'Modern conflicts are shaped as much by information ecosystems as by physical events.',
    statMain: '5 cycles',
    statDesc: 'Polarization patterns detected within first 5 simulation cycles.',
    agents: '2,000',
    cycles: '60+',
  },
  {
    id: 3,
    icon: '🧠',
    sector: 'POLICY ANALYSIS',
    sectorShort: 'POLICY',
    title: 'Public Opinion on Policy Changes',
    featuredTitle: 'Decoding Public Reaction to Data Privacy Regulation',
    challenge: 'Complex policy rollouts often trigger public backlash—not due to opposition, but due to misunderstanding and poor communication. Governments lack tools to predict how policies will be perceived at scale.',
    solution: 'Predly deployed 900 agents representing users, policymakers, companies, and privacy advocates. Using legislative drafts and public discourse, agents simulated real-world interpretation cycles.',
    solutionPoints: ['Sentiment evolution tracking', 'Misinterpretation spread analysis', 'Narrative correction phase modeling'],
    results: ['Identification of initial backlash driven by ambiguity, not intent', 'Measurable reduction in resistance after simulated clarification campaigns', 'Prediction of phased adoption curve'],
    insight: 'Public resistance is primarily a function of communication clarity, not policy substance.',
    statMain: 'High',
    statDesc: 'Backlash reduction achieved through simulated clarification campaigns.',
    agents: '900',
    cycles: '36+',
  },
  {
    id: 4,
    icon: '🚀',
    sector: 'MARKET INTELLIGENCE',
    sectorShort: 'PRODUCT',
    title: 'Product Launch Reaction',
    featuredTitle: 'Simulating Market Adoption of a New AI Product',
    challenge: 'Product launches are heavily influenced by perception dynamics rather than actual product quality. Early narratives—especially from influencers—can determine long-term success or failure.',
    solution: 'Predly simulated 800 consumer agents, including early adopters, skeptics, influencers, and general users. Inputs included product announcements, reviews, and competitor positioning.',
    solutionPoints: ['Viral trend detection', 'Influence-weighted sentiment modeling', 'Adoption curve simulation'],
    results: ['Accurate prediction of early adoption spike followed by correction phase', 'Identification of key influencer nodes driving perception', 'Detection of localized negative sentiment clusters'],
    insight: 'Adoption is driven less by product capability and more by who shapes the initial narrative.',
    statMain: 'Precise',
    statDesc: 'Accurate prediction of early adoption spike and correction phase.',
    agents: '800',
    cycles: '30+',
  },
  {
    id: 5,
    icon: '📰',
    sector: 'INFORMATION DYNAMICS',
    sectorShort: 'INFODYN',
    title: 'Misinformation Spread Analysis',
    featuredTitle: 'Understanding the Velocity of False Narratives',
    challenge: 'Digital platforms enable misinformation to spread faster than factual content, making it difficult to control narratives or maintain information integrity.',
    solution: 'Predly simulated 1,500 agents with varying trust levels, biases, and verification behaviors. The system ingested mixed datasets of real and false information to model competitive narrative spread.',
    solutionPoints: ['Content consumption and resharing simulation', 'Emotional bias reaction modeling', 'Belief cluster reinforcement tracking'],
    results: ['Misinformation spread 2–3x faster than verified content in early cycles', 'Detection of high-engagement misinformation clusters', 'Limited effectiveness of late-stage corrections identified'],
    insight: 'Information ecosystems reward speed and emotional resonance over accuracy.',
    statMain: '2–3×',
    statDesc: 'Misinformation spread faster than verified content in early simulation cycles.',
    agents: '1,500',
    cycles: '50+',
  },
  {
    id: 6,
    icon: '🪙',
    sector: 'CRYPTO MARKETS',
    sectorShort: 'CRYPTO',
    title: 'Crypto Market Behavior',
    featuredTitle: 'Predicting Bitcoin Volatility Under Regulatory Pressure',
    challenge: 'Crypto markets are highly volatile and driven by sentiment loops rather than traditional fundamentals. Regulatory announcements often trigger disproportionate reactions.',
    solution: 'Predly deployed 1,100 agents, including traders, influencers, institutions, and automated bots. Inputs included regulatory news, crypto media, and social sentiment signals.',
    solutionPoints: ['Rapid sentiment cascade modeling', 'Bot-driven amplification tracking', 'Institutional delay strategy simulation'],
    results: ['Prediction of flash crash scenarios triggered by influencer sentiment', 'Identification of rebound zones driven by opportunistic buying', 'Mapping of volatility cycles driven by social amplification'],
    insight: 'Crypto markets operate as self-reinforcing sentiment systems, not purely economic systems.',
    statMain: 'Flash',
    statDesc: 'Accurate prediction of flash crash scenarios triggered by influencer sentiment.',
    agents: '1,100',
    cycles: '44+',
  },
  {
    id: 7,
    icon: '🎬',
    sector: 'CULTURAL INTELLIGENCE',
    sectorShort: 'CULTURE',
    title: 'Cultural Trend / Movie Release',
    featuredTitle: 'Forecasting Audience Perception in Entertainment Launches',
    challenge: 'Entertainment success depends heavily on early perception. Initial reviews and social reactions can permanently shape audience sentiment.',
    solution: 'Predly simulated 700 agents, including fans, critics, and general audiences. Inputs included trailers, critic reviews, and social discussions.',
    solutionPoints: ['Pre-release hype generation modeling', 'Post-release critique cycle simulation', 'Community-driven narrative reinforcement analysis'],
    results: ['Accurate prediction of strong opening driven by hype', 'Identification of long-term sentiment anchored to early reviews', 'Detection of fan-driven resistance to negative narratives'],
    insight: 'Audience perception is path-dependent—early narratives define long-term success.',
    statMain: 'Path',
    statDesc: 'Audience perception is path-dependent — early narratives define long-term success.',
    agents: '700',
    cycles: '28+',
  },
]
</script>

<style scoped>
.cs {
  min-height: 100vh;
  background: #0a0c0f;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  overflow-x: hidden;
}

.cs__grid-bg {
  position: fixed;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 181, 158, 0.025) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 181, 158, 0.025) 1px, transparent 1px);
  background-size: 60px 60px;
  pointer-events: none;
  z-index: 0;
}
.cs__orb {
  position: fixed;
  border-radius: 50%;
  filter: blur(90px);
  pointer-events: none;
  z-index: 0;
}
.cs__orb--orange {
  width: 700px; height: 700px;
  top: -280px; right: -180px;
  background: radial-gradient(circle, rgba(255, 90, 31, 0.28) 0%, transparent 70%);
}
.cs__orb--blue {
  width: 600px; height: 600px;
  bottom: -180px; left: -180px;
  background: radial-gradient(circle, rgba(14, 63, 174, 0.25) 0%, transparent 70%);
}

/* Topbar */
.cs__topbar {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 100;
  padding: 1.125rem 2rem;
  background: rgba(10, 12, 15, 0.8);
  backdrop-filter: blur(14px);
  border-bottom: 1px solid rgba(171, 137, 127, 0.1);
}
.cs__topbar-inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
}
.cs__logo {
  font-size: 1.125rem;
  font-weight: 700;
  color: #f4f6f9;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-shrink: 0;
  font-family: 'Space Grotesk', sans-serif;
}
.cs__logo-dot {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: #FF8C5A;
}
.cs__nav {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
}
.cs__nav-link {
  font-size: 0.8125rem;
  font-weight: 500;
  color: #9aa4b2;
  text-decoration: none;
  padding: 0.375rem 0.875rem;
  border-radius: 999px;
  letter-spacing: 0.04em;
  transition: color 0.15s;
  cursor: pointer;
}
.cs__nav-link:hover { color: #f4f6f9; }
.cs__nav-link--active {
  color: #FF8C5A;
  border-bottom: 1.5px solid #FF8C5A;
  border-radius: 0;
  padding-bottom: 0.25rem;
}
.cs__inquiry-btn {
  flex-shrink: 0;
  padding: 0.5rem 1.25rem;
  background: linear-gradient(135deg, #FF5A1F 0%, #FF8C5A 100%);
  border: none;
  border-radius: 12px;
  color: white;
  font-size: 0.875rem;
  font-weight: 700;
  cursor: pointer;
  letter-spacing: 0.01em;
  transition: all 0.2s ease;
  box-shadow: 0 2px 12px rgba(255, 90, 31, 0.35);
  font-family: 'Space Grotesk', sans-serif;
}
.cs__inquiry-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 20px rgba(255, 90, 31, 0.5);
}

/* Main */
.cs__main {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 1200px;
  padding: 7rem 2rem 4rem;
  display: flex;
  flex-direction: column;
  gap: 4rem;
}

/* Header */
.cs__header { max-width: 560px; }
.cs__badge {
  display: inline-block;
  font-size: 0.6875rem;
  letter-spacing: 0.12em;
  color: #FF8C5A;
  background: rgba(255, 90, 31, 0.08);
  border: 1px solid rgba(255, 90, 31, 0.2);
  border-radius: 4px;
  padding: 0.3rem 0.75rem;
  margin-bottom: 1.25rem;
  font-family: 'JetBrains Mono', monospace;
}
.cs__title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: clamp(2.5rem, 5vw, 3.5rem);
  font-weight: 800;
  color: #f4f6f9;
  line-height: 1.1;
  margin: 0 0 1rem;
  letter-spacing: -0.02em;
}
.cs__subtitle {
  color: #9aa4b2;
  font-size: 0.9375rem;
  line-height: 1.75;
  margin: 0;
}

/* Featured */
.cs__featured { display: flex; flex-direction: column; gap: 1.5rem; }
.cs__featured-card {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 1.5rem;
  background: rgba(16, 20, 25, 0.7);
  border: 1px solid rgba(171, 137, 127, 0.12);
  border-radius: 20px;
  padding: 2rem;
  backdrop-filter: blur(16px);
  cursor: pointer;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.cs__featured-card:hover {
  border-color: rgba(255, 90, 31, 0.3);
  box-shadow: 0 0 40px rgba(255, 90, 31, 0.06);
}
.cs__featured-sector {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.6875rem;
  letter-spacing: 0.12em;
  color: #FF8C5A;
  margin-bottom: 1rem;
  font-family: 'JetBrains Mono', monospace;
}
.cs__sector-icon { font-size: 1rem; }
.cs__featured-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: clamp(1.5rem, 3vw, 2.25rem);
  font-weight: 800;
  color: #f4f6f9;
  line-height: 1.2;
  margin: 0 0 2rem;
  letter-spacing: -0.02em;
}
.cs__featured-cols {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}
.cs__col-label {
  font-size: 0.6875rem;
  letter-spacing: 0.1em;
  color: #9aa4b2;
  margin-bottom: 0.5rem;
  font-family: 'JetBrains Mono', monospace;
}
.cs__col-text {
  font-size: 0.8125rem;
  color: #9aa4b2;
  line-height: 1.65;
  margin: 0;
}

/* Right stats */
.cs__featured-right { display: flex; flex-direction: column; gap: 1rem; }
.cs__stat-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(171, 137, 127, 0.12);
  border-radius: 14px;
  padding: 1.25rem;
  flex: 1;
}
.cs__stat-card--accent {
  border-color: rgba(255, 90, 31, 0.15);
  background: rgba(255, 90, 31, 0.04);
}
.cs__stat-label {
  font-size: 0.625rem;
  letter-spacing: 0.12em;
  color: #9aa4b2;
  margin-bottom: 0.5rem;
  font-family: 'JetBrains Mono', monospace;
}
.cs__stat-value {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 2.75rem;
  font-weight: 800;
  color: #FF8C5A;
  line-height: 1;
  margin-bottom: 0.75rem;
}
.cs__stat-desc { font-size: 0.75rem; color: #9aa4b2; line-height: 1.5; margin: 0; }
.cs__stat-row { display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; }
.cs__stat-mini {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(171, 137, 127, 0.1);
  border-radius: 12px;
  padding: 1rem;
  position: relative;
  overflow: hidden;
}
.cs__stat-mini-label {
  font-size: 0.5625rem;
  letter-spacing: 0.1em;
  color: #9aa4b2;
  margin-bottom: 0.25rem;
  font-family: 'JetBrains Mono', monospace;
}
.cs__stat-mini-value {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1.375rem;
  font-weight: 700;
  color: #f4f6f9;
}
.cs__stat-mini-icon {
  position: absolute;
  bottom: 0.5rem;
  right: 0.5rem;
  font-size: 1.25rem;
  color: rgba(255, 140, 90, 0.3);
}

/* Quote */
.cs__quote {
  background: rgba(16, 20, 25, 0.6);
  border: 1px solid rgba(171, 137, 127, 0.1);
  border-radius: 16px;
  padding: 1.75rem 2rem;
  backdrop-filter: blur(12px);
}
.cs__quote-text {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1.0625rem;
  color: #f4f6f9;
  line-height: 1.7;
  margin: 0 0 1.25rem;
  font-style: italic;
}
.cs__quote-author { display: flex; align-items: center; gap: 0.875rem; }
.cs__quote-avatar {
  width: 38px; height: 38px;
  border-radius: 50%;
  background: rgba(255, 90, 31, 0.1);
  border: 1px solid rgba(255, 90, 31, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.125rem;
  flex-shrink: 0;
}
.cs__quote-name {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 0.875rem;
  font-weight: 700;
  color: #f4f6f9;
}
.cs__quote-role {
  font-size: 0.6875rem;
  color: #9aa4b2;
  letter-spacing: 0.06em;
  font-family: 'JetBrains Mono', monospace;
}

/* More */
.cs__more { display: flex; flex-direction: column; gap: 2rem; }
.cs__more-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 1rem;
}
.cs__more-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1.75rem;
  font-weight: 700;
  color: #f4f6f9;
  margin: 0 0 0.5rem;
}
.cs__more-sub { font-size: 0.875rem; color: #9aa4b2; margin: 0; }
.cs__view-all {
  font-size: 0.6875rem;
  letter-spacing: 0.1em;
  color: #FF8C5A;
  background: none;
  border: none;
  cursor: pointer;
  white-space: nowrap;
  font-family: 'JetBrains Mono', monospace;
  transition: opacity 0.15s;
}
.cs__view-all:hover { opacity: 0.7; }

.cs__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.25rem;
}
.cs__card {
  background: rgba(16, 20, 25, 0.65);
  border: 1px solid rgba(171, 137, 127, 0.1);
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  transition: border-color 0.2s, transform 0.2s, box-shadow 0.2s;
  backdrop-filter: blur(12px);
}
.cs__card:hover {
  border-color: rgba(255, 90, 31, 0.3);
  transform: translateY(-3px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
}
.cs__card-img {
  height: 140px;
  background: linear-gradient(135deg, rgba(255, 90, 31, 0.08) 0%, rgba(14, 63, 174, 0.12) 100%);
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid rgba(171, 137, 127, 0.08);
}
.cs__card-icon-bg {
  font-size: 3rem;
  opacity: 0.7;
}
.cs__card-sector-badge {
  position: absolute;
  top: 0.75rem;
  left: 0.75rem;
  font-size: 0.5625rem;
  letter-spacing: 0.1em;
  color: #9aa4b2;
  background: rgba(10, 12, 15, 0.7);
  border: 1px solid rgba(171, 137, 127, 0.15);
  border-radius: 4px;
  padding: 0.2rem 0.5rem;
  font-family: 'JetBrains Mono', monospace;
}
.cs__card-body { padding: 1.25rem; }
.cs__card-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1rem;
  font-weight: 700;
  color: #f4f6f9;
  margin: 0 0 0.625rem;
  line-height: 1.3;
}
.cs__card-desc { font-size: 0.8125rem; color: #9aa4b2; line-height: 1.6; margin: 0 0 1rem; }
.cs__card-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 0.6875rem;
  color: #9aa4b2;
  letter-spacing: 0.06em;
  font-family: 'JetBrains Mono', monospace;
}
.cs__card-arrow { color: #FF8C5A; }

/* Footer */
.cs__footer {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 1200px;
  padding: 2rem;
  border-top: 1px solid rgba(171, 137, 127, 0.08);
  margin-top: 2rem;
}
.cs__footer-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.75rem;
  flex-wrap: wrap;
  gap: 1rem;
}
.cs__footer-brand {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1rem;
  font-weight: 700;
  color: #f4f6f9;
}
.cs__footer-links {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
  font-family: 'JetBrains Mono', monospace;
}
.cs__footer-links a {
  font-size: 0.75rem;
  color: #9aa4b2;
  text-decoration: none;
  transition: color 0.15s;
}
.cs__footer-links a:hover { color: #f4f6f9; }
.cs__footer-copy {
  font-size: 0.6875rem;
  color: rgba(154, 164, 178, 0.5);
  font-family: 'JetBrains Mono', monospace;
}

/* Modal */
.cs__modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(5, 7, 10, 0.85);
  backdrop-filter: blur(8px);
  z-index: 200;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}
.cs__modal {
  background: #0e1219;
  border: 1px solid rgba(171, 137, 127, 0.18);
  border-radius: 24px;
  padding: 2.5rem;
  max-width: 720px;
  width: 100%;
  max-height: 85vh;
  overflow-y: auto;
  position: relative;
  scrollbar-width: thin;
  scrollbar-color: rgba(171,137,127,0.2) transparent;
}
.cs__modal::-webkit-scrollbar { width: 4px; }
.cs__modal::-webkit-scrollbar-track { background: transparent; }
.cs__modal::-webkit-scrollbar-thumb { background: rgba(171,137,127,0.2); border-radius: 2px; }
.cs__modal-close {
  position: absolute;
  top: 1.5rem;
  right: 1.5rem;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(171,137,127,0.15);
  border-radius: 8px;
  width: 36px; height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #9aa4b2;
  transition: color 0.15s, background 0.15s;
}
.cs__modal-close:hover { color: #f4f6f9; background: rgba(255,255,255,0.08); }
.cs__modal-sector {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.6875rem;
  letter-spacing: 0.12em;
  color: #FF8C5A;
  margin-bottom: 1rem;
  font-family: 'JetBrains Mono', monospace;
}
.cs__modal-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: clamp(1.5rem, 3vw, 2rem);
  font-weight: 800;
  color: #f4f6f9;
  margin: 0 0 2rem;
  line-height: 1.2;
  letter-spacing: -0.02em;
  padding-right: 3rem;
}
.cs__modal-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 2.5rem;
}
.cs__modal-stat {
  background: rgba(255, 90, 31, 0.04);
  border: 1px solid rgba(255, 90, 31, 0.12);
  border-radius: 12px;
  padding: 1.125rem;
  text-align: center;
}
.cs__modal-stat-val {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1.75rem;
  font-weight: 800;
  color: #FF8C5A;
  margin-bottom: 0.25rem;
}
.cs__modal-stat-lbl {
  font-size: 0.5625rem;
  letter-spacing: 0.1em;
  color: #9aa4b2;
  font-family: 'JetBrains Mono', monospace;
}
.cs__modal-sections { display: flex; flex-direction: column; gap: 1.75rem; }
.cs__modal-section-label {
  font-size: 0.6875rem;
  letter-spacing: 0.12em;
  color: #9aa4b2;
  margin-bottom: 0.75rem;
  font-family: 'JetBrains Mono', monospace;
}
.cs__modal-section-text { font-size: 0.875rem; color: #9aa4b2; line-height: 1.75; margin: 0 0 0.875rem; }
.cs__modal-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.cs__modal-list li {
  font-size: 0.8125rem;
  color: #9aa4b2;
  padding-left: 1rem;
  position: relative;
  line-height: 1.6;
}
.cs__modal-list li::before {
  content: '—';
  position: absolute;
  left: 0;
  color: #FF8C5A;
}
.cs__modal-results {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.cs__modal-results li {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  font-size: 0.875rem;
  color: #c8d0db;
  line-height: 1.6;
}
.cs__modal-result-dot {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: #FF8C5A;
  margin-top: 0.45rem;
  flex-shrink: 0;
}
.cs__modal-insight {
  background: rgba(255, 90, 31, 0.04);
  border: 1px solid rgba(255, 90, 31, 0.12);
  border-radius: 14px;
  padding: 1.5rem;
}
.cs__modal-insight-label {
  font-size: 0.625rem;
  letter-spacing: 0.12em;
  color: #FF8C5A;
  margin-bottom: 0.75rem;
  font-family: 'JetBrains Mono', monospace;
}
.cs__modal-insight-text {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1rem;
  color: #f4f6f9;
  line-height: 1.7;
  margin: 0;
  font-style: italic;
}

/* Modal transition */
.modal-enter-active, .modal-leave-active { transition: opacity 0.2s ease; }
.modal-enter-active .cs__modal, .modal-leave-active .cs__modal { transition: transform 0.25s cubic-bezier(0.4,0,0.2,1), opacity 0.2s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
.modal-enter-from .cs__modal { transform: translateY(16px) scale(0.98); }
.modal-leave-to .cs__modal { transform: translateY(8px) scale(0.99); opacity: 0; }

@media (max-width: 900px) {
  .cs__featured-card { grid-template-columns: 1fr; }
  .cs__featured-right { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
  .cs__stat-card { grid-column: 1 / -1; }
  .cs__grid { grid-template-columns: repeat(2, 1fr); }
  .cs__featured-cols { grid-template-columns: 1fr; }
  .cs__modal-stats { grid-template-columns: repeat(3, 1fr); }
}
@media (max-width: 600px) {
  .cs__main { padding: 6rem 1rem 3rem; }
  .cs__grid { grid-template-columns: 1fr; }
  .cs__nav { display: none; }
  .cs__more-header { flex-direction: column; align-items: flex-start; }
  .cs__modal { padding: 1.5rem; }
  .cs__modal-stats { grid-template-columns: 1fr; }
  .cs__featured-right { grid-template-columns: 1fr; }
}
</style>
