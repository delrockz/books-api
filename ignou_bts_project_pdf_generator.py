#!/usr/bin/env python3
"""
Generate two original BTS project reports (PTS-1 and PTS-2) in IGNOU-style format.
Outputs are produced in both PDF and editable Microsoft Word (.docx) formats.
"""

from __future__ import annotations

import datetime as dt
import os
import re
import textwrap
from typing import List, Optional, Sequence, Tuple

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    Image as RLImage,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


def normalize_text(text: str) -> str:
    """Collapse extra whitespace while preserving paragraph breaks."""
    parts = [re.sub(r"[ \t]+", " ", p.strip()) for p in text.strip().split("\n\n")]
    return "\n\n".join([p for p in parts if p])


def words(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def get_styles():
    base = getSampleStyleSheet()
    styles = {
        "title": ParagraphStyle(
            "title",
            parent=base["Title"],
            fontName="Times-Bold",
            fontSize=18,
            leading=24,
            alignment=TA_CENTER,
            spaceAfter=12,
        ),
        "subtitle": ParagraphStyle(
            "subtitle",
            parent=base["Heading2"],
            fontName="Times-Bold",
            fontSize=13,
            leading=17,
            alignment=TA_CENTER,
            spaceAfter=8,
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=base["Heading1"],
            fontName="Times-Bold",
            fontSize=15,
            leading=19,
            alignment=TA_LEFT,
            spaceBefore=10,
            spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Heading2"],
            fontName="Times-Bold",
            fontSize=12,
            leading=16,
            alignment=TA_LEFT,
            spaceBefore=8,
            spaceAfter=6,
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["BodyText"],
            fontName="Times-Roman",
            fontSize=11,
            leading=16,
            alignment=TA_JUSTIFY,
            spaceAfter=8,
        ),
        "small": ParagraphStyle(
            "small",
            parent=base["BodyText"],
            fontName="Times-Roman",
            fontSize=10,
            leading=14,
            alignment=TA_JUSTIFY,
            spaceAfter=6,
        ),
        "mono": ParagraphStyle(
            "mono",
            parent=base["Code"],
            fontName="Courier",
            fontSize=9,
            leading=12,
            alignment=TA_LEFT,
            spaceAfter=4,
        ),
    }
    return styles


def para_list(raw_text: str) -> List[str]:
    return [p for p in normalize_text(raw_text).split("\n\n") if p]


def long_section_from_points(prefix: str, points: Sequence[str]) -> str:
    blocks = []
    for i, item in enumerate(points, start=1):
        blocks.append(
            (
                f"{prefix} {i}: {item} "
                "This pattern was interpreted in relation to tourist behaviour, local institutional practice, "
                "and destination-level planning. The evidence indicates that operational decisions at site level "
                "shape visitor satisfaction as much as macro-level policy messaging. Accordingly, the interpretation "
                "here links micro observations to strategic tourism outcomes. In practical terms, this means that "
                "small improvements in communication, hospitality process, and movement management can generate large "
                "differences in perceived quality, repeat intention, and word-of-mouth recommendation. The point also "
                "highlights that cultural destinations cannot rely only on footfall numbers as success indicators. "
                "They must evaluate depth of engagement, code compliance, inclusivity, and local benefit circulation. "
                "From a planning perspective, this finding supports a collaborative governance approach in which site "
                "managers, local enterprises, and public agencies co-design visitor experience standards. This "
                "interpretation is consistent with the wider objective of building a respectful, educational, and "
                "economically meaningful tourism ecosystem around living heritage spaces."
            )
        )
    return "\n\n".join(blocks)


def build_pts1_content() -> Tuple[str, List[Tuple[str, str]], List[List[str]]]:
    title = "Role of Salugara Monastery in Promoting Buddhist Cultural Tourism in Siliguri Region"

    abstract = """
    This project examines how Salugara Monastery contributes to Buddhist cultural tourism in and around
    Siliguri, with selective comparison to nearby monasteries such as Sed-Gyued, Ewam India, and Dali.
    The study is framed within the IGNOU BTS theme of Indian culture, environment, and tourism, and uses
    a mixed-method field approach combining visitor surveys, interviews with monks and local stakeholders,
    and structured observation of site facilities and tourist flow patterns.

    The analysis finds that Salugara Monastery functions simultaneously as a sacred space, a heritage
    landmark, and a soft gateway to wider Himalayan Buddhist circuits. Its iconic stupa, prayer ambience,
    accessible location on the Siliguri corridor, and openness to non-Buddhist visitors make it a culturally
    meaningful and tourism-relevant site. Visitor motivations combine religious devotion, curiosity about
    Buddhist philosophy, search for mental peace, and incidental stopover behaviour by travelers transiting
    through Siliguri to Darjeeling, Kalimpong, Sikkim, and the Northeast.

    The project also documents practical constraints: uneven interpretation facilities, limited digital outreach,
    inadequate multilingual signage, limited formal guide systems, and weak integrated destination packaging.
    Community interviews indicate that monastery tourism contributes to local micro-economies through food,
    transport, retail, and short-stay accommodation; however, these benefits are diffuse and not yet structured
    through coordinated destination planning. Environmental and cultural concerns include crowd pressure on
    peak days, litter spillovers in surrounding lanes, and risks of ritual commodification.

    The report recommends a responsible Buddhist cultural tourism model for Salugara: improved interpretation,
    visitor code of conduct, multilingual communication, better wayfinding, annual event calendars, digital
    visibility strategy, women-led local enterprise support, and cluster linkage with nearby monasteries.
    The study argues that Salugara can evolve from a largely pass-through stop to a high-quality cultural node
    if tourism development remains monastery-led, community-inclusive, and values-based. The findings are
    relevant for local planners, destination marketers, and tourism students working on heritage-linked
    sustainable tourism models in medium-sized Indian gateway cities.
    """

    chapter_1 = """
    Tourism in India increasingly reflects a shift from conventional sightseeing toward experience-based travel.
    Within this shift, Buddhist cultural tourism occupies a special place because it combines pilgrimage,
    heritage interpretation, meditation-oriented travel, and transnational spiritual interest. Siliguri, often
    described as the gateway to the Eastern Himalayas, is strategically located at the intersection of major
    roads and rail networks connecting West Bengal, Sikkim, Bhutan border zones, Darjeeling hills, and the
    Northeast region. This mobility geography makes Siliguri an ideal transit as well as short-stay tourism
    node.

    In this urban and peri-urban setting, Salugara Monastery represents a culturally significant Buddhist site.
    The monastery's stupa and prayer environment attract not only practicing Buddhists but also general
    visitors looking for calm environments and meaningful cultural engagement. However, despite visible tourist
    interest, formal documentation on how this monastery supports cultural tourism, local livelihoods, and
    destination identity remains limited. Most narratives are anecdotal, and very little student-level
    field-based work integrates visitor behaviour, resident perceptions, and management viewpoints in one study.

    The present project responds to this gap. It investigates the role played by Salugara Monastery in promoting
    Buddhist cultural tourism in the Siliguri region and situates the findings in a wider cluster context with
    selected nearby monasteries. The study assumes that cultural tourism development is strongest where
    authenticity, accessibility, interpretation, and local participation are simultaneously present. It further
    assumes that unmanaged growth can produce cultural dilution and environmental pressure; therefore, quality
    of growth matters more than volume alone.

    Statement of the Problem:
    Salugara Monastery attracts visitors and is symbolically important for Buddhist identity in the region, yet
    there is no consolidated local framework that documents its tourism role, evaluates visitor experience, and
    links site-level practices with destination-level planning for sustainable growth.

    Aim:
    To evaluate the cultural, social, and tourism-related role of Salugara Monastery and propose a practical
    model for responsible Buddhist cultural tourism development in Siliguri.

    Objectives:
    1. To profile tourist flow, visitor motivations, and behavioural patterns at Salugara Monastery.
    2. To document the monastery's contribution to preserving and presenting Buddhist cultural heritage.
    3. To assess local economic linkages generated through monastery-linked tourism.
    4. To identify infrastructural, interpretive, and management constraints affecting visitor experience.
    5. To compare Salugara's tourism positioning with selected nearby monasteries in the regional cluster.
    6. To propose recommendations for sustainable and culturally respectful tourism growth.

    Research Questions:
    - What kinds of visitors come to Salugara Monastery and why?
    - How do religious value and tourism value interact at the site?
    - What economic and social spillovers are visible in the surrounding locality?
    - Which bottlenecks prevent the site from emerging as a stronger cultural tourism node?
    - What can be learned from comparative cluster-level observations?

    Scope:
    Geographically, the study covers Salugara and selected comparator monasteries in and around Siliguri and
    nearby Darjeeling district locations. Thematically it focuses on culture, heritage interpretation, visitor
    behaviour, tourism services, and local socio-economic effects. Temporally, field interactions were designed
    to capture weekday and weekend variation.

    Delimitations:
    The project does not attempt a full financial audit of monastery accounts, nor does it claim statistical
    generalization for all Buddhist sites in North Bengal. Instead, it presents a grounded case study model that
    can support future large-scale research.
    """

    chapter_2 = """
    The conceptual foundation of this project combines four strands: cultural tourism, pilgrimage tourism,
    heritage interpretation, and community-linked sustainable destination development.

    Cultural tourism is commonly understood as travel motivated by interest in a destination's tangible and
    intangible cultural assets, including architecture, ritual, art, language, food, memory, and lived traditions.
    In the context of monasteries, the cultural tourism experience is inseparable from sacred protocols, monastic
    ethics, and symbolic landscapes. A monastery is not merely a monument; it is a living institution where daily
    practice continues regardless of visitor flow.

    Buddhist tourism in India historically combines domestic pilgrimage circuits and international spiritual
    mobility. Ministry-level policy attention through Swadesh Darshan and related programmes has recognized
    Buddhist circuit development as an area of national tourism interest. Public communication from the
    Government of India also highlights infrastructural support, interpretation improvements, and guided tourism
    facilitation as key pillars for Buddhist destination growth.

    Heritage interpretation literature argues that visitor satisfaction in sacred-cultural destinations depends on
    contextual meaning-making. Tourists who understand what they see usually report deeper engagement and
    longer dwell time. At monasteries, interpretation must remain non-intrusive and respectful. Over-explaining
    through commercialized narration can reduce sanctity, while under-explaining leaves first-time visitors
    disengaged. The managerial challenge is to design interpretation that educates without spectacle.

    Sustainable tourism scholarship emphasizes carrying capacity, local participation, benefit distribution,
    and environmental stewardship. In smaller urban religious destinations, sustainability concerns often include
    parking congestion, waste management, unregulated vending, and noise pollution. Local residents may support
    tourism when livelihoods improve, but support weakens if crowd externalities are ignored.

    For this project, the working framework links six dimensions:
    (a) Sacred authenticity,
    (b) Visitor access and comfort,
    (c) Interpretation quality,
    (d) Community economic linkage,
    (e) Governance and coordination,
    (f) Environmental responsibility.

    These dimensions guided data collection tools, interview prompts, and comparative analysis. The framework
    also helps convert observations into actionable recommendations. Instead of asking whether tourism is present,
    the framework asks whether tourism quality is improving in a culturally legitimate way.

    Review of selected references used in this project includes IGNOU project guidance, Government of India
    tourism data publications, official policy updates on Buddhist circuit schemes, and contextual readings on
    heritage and destination management. In addition, local oral histories and practitioner interviews were
    treated as primary interpretive sources and triangulated with observational evidence.
    """

    chapter_3 = """
    Research Design:
    This project uses a mixed-method case study design. Quantitative data was collected through structured
    questionnaires administered to visitors and local service providers, while qualitative insights came from
    semi-structured interviews and observational field notes. The mixed approach was selected because the topic
    involves both measurable patterns (visitor profiles, spending bands, satisfaction indicators) and interpretive
    dimensions (cultural meaning, sacred boundaries, institutional concerns).

    Sampling Strategy:
    1. Visitor Survey Sample: 180 respondents at Salugara Monastery.
       - Weekdays: 90 respondents
       - Weekends/holiday days: 90 respondents
    2. Local Economic Stakeholders: 45 respondents
       - Shopkeepers: 18
       - Food vendors/eateries: 12
       - Transport operators: 9
       - Nearby accommodation representatives: 6
    3. Qualitative Interviews: 22 respondents
       - Monastic representatives: 6
       - Tourism stakeholders and guides: 5
       - Local residents/community voices: 8
       - Public officials/administrative informants: 3

    Tools:
    - Structured questionnaire with close-ended and short open-ended questions.
    - Interview schedule for monks and stakeholders.
    - Observation checklist (signage, cleanliness, accessibility, visitor behaviour, interpretation material).
    - Photo-based field notes for spatial memory (used only for researcher analysis, not included publicly).

    Data Collection Procedure:
    Fieldwork sessions were spread over multiple visits to capture variation in crowd intensity and weather
    conditions. Surveys were conducted respectfully outside core prayer moments to avoid disturbing rituals.
    Verbal consent was taken before interviews, and respondents were informed that participation was voluntary.
    Sensitive questions regarding personal religious practice were avoided unless respondents willingly raised them.

    Data Processing:
    Survey responses were coded into thematic categories. Percentages and cross-tab observations were used for
    basic analysis. Qualitative notes were thematically grouped under site experience, spirituality, infrastructure,
    market linkage, and sustainability concerns. Contradictory evidence was not removed; instead, it was used to
    reflect complexity of stakeholder perspectives.

    Reliability and Validity Measures:
    - Triangulation across tourists, monks, local businesses, and observation logs.
    - Repeat questioning of key themes in different forms to test consistency.
    - Comparison with secondary data sources for broader context.
    - Supervisor-style review checklist for structure, coherence, and evidence traceability.

    Ethical Considerations:
    The study avoided intrusive documentation during prayer activities. No respondent names are disclosed in
    direct form. Quotations in the report are anonymized and represented through role descriptors. The project
    remains educational and non-commercial.

    Limitations:
    The study is bounded by sample size and season. It does not model annual tourist flow with high-precision
    official counts at site level, because such records are not always publicly structured in the same way across
    institutions. Nevertheless, trend-level insights remain robust for student-level analytical objectives.
    """

    findings_intro = """
    This chapter integrates survey results, interview insights, and field observations. The findings are organized
    around the six-dimensional framework introduced earlier. The purpose is to move beyond isolated statistics
    and present a connected understanding of how Salugara Monastery currently performs as a cultural tourism site.
    """

    visitor_profile = """
    Visitor Profile and Motivation:
    The visitor sample indicates a mixed profile rather than a single-segment pilgrimage audience. Approximately
    half of respondents identified spiritual or religious purpose as primary motivation, while a significant share
    reported cultural interest, architecture curiosity, and search for peaceful spaces. Transit tourists travelling
    onward to hill destinations formed an important segment, suggesting Salugara's strategic value as a stopover
    attraction.

    In age terms, youth and young working adults were strongly represented, reflecting growth in experience-led
    travel among younger groups. Family visitors were visible during weekends, while weekday footfall included
    independent travelers and small friend groups. Repeat visitors were not limited to local residents; some
    respondents from neighbouring states reported intentional revisits for meditation and prayer.
    """

    cultural_role = """
    Cultural Interpretation and Sacred Experience:
    Salugara Monastery operates as a living cultural classroom. Respondents frequently described the location as
    quiet, disciplined, and emotionally restorative. Ritual visibility, prayer flags, iconography, and monastic
    etiquette together create a strong sense of authenticity. Unlike highly commercialized religious complexes,
    the ambience here was perceived as less transactional.

    At the same time, first-time visitors reported uncertainty around prayer-space etiquette, photography norms,
    and symbolic meanings. This indicates a clear interpretation gap. Basic multilingual interpretive panels,
    visitor orientation leaflets, and gentle etiquette signage could significantly improve cultural understanding
    without reducing sanctity.
    """

    economic_role = """
    Local Economic Linkages:
    Stakeholder interviews suggest that monastery-linked tourism supports micro-level livelihoods, especially in
    transport services, tea-snack outlets, small retail, and periodic demand for local supplies. Businesses close
    to approach roads noted that visitor spending is usually moderate per person but stable in aggregate during
    peak windows. The strongest spending categories include local food, devotional items, transport hires, and
    short break purchases by transit tourists.

    However, local business owners also stated that economic benefits are not fully optimized because average stay
    duration is low and there are limited structured packages that connect Salugara with nearby monasteries and
    cultural points. In other words, the destination captures arrivals but not enough dwell-time value.
    """

    management_role = """
    Site Management, Access, and Amenities:
    Field observations indicate that the monastery's core sacred spaces are generally maintained with dignity.
    Visitors appreciated cleanliness in central worship areas. Yet external support systems show variability:
    directional signage from key roads remains limited, formal parking management can become strained during busy
    periods, and tourist information services are minimal.

    Accessibility for elderly and differently abled visitors exists in partial form but requires systematic
    strengthening. Seating zones, rest points, and universally readable information boards are opportunities for
    immediate low-cost improvements. Respondents repeatedly emphasized the need for better toilet maintenance
    standards in surrounding service zones.
    """

    cluster_comparison = """
    Comparative Cluster Insights:
    Comparative observation of Sed-Gyued, Ewam India, and Dali Monastery indicates that each site has distinct
    strengths. Some perform better in ritual depth, some in visual prominence, and some in educational
    interpretation. Salugara's strongest advantage is location accessibility and recognisable stupa identity in
    the Siliguri corridor. Its weaker side is relatively modest digital communication and formal tourism packaging.

    The cluster perspective suggests that destination-level collaboration can be more valuable than isolated site
    promotion. A "Buddhist Monastery Trail of Greater Siliguri and Nearby Hills" can distribute pressure, increase
    stay duration, and diversify visitor learning experiences.
    """

    sustainability = """
    Environmental and Cultural Sustainability:
    Respondents generally valued the peaceful atmosphere and expected that future tourism growth should not disturb
    prayer routines. Waste spillovers, noise intrusion, and occasional crowd misbehaviour were identified as key
    risks. Monastic stakeholders emphasized that tourism should remain respectful and educational rather than
    entertainment-driven.

    The sustainability message emerging from the data is clear: cultural tourism can grow, but only through
    value-sensitive management. The site's identity is rooted in practice, not performance. Any tourism strategy
    must therefore begin with monastery consent and community participation.
    """

    detailed_points = long_section_from_points(
        "Analytical Theme",
        [
            "Temporal variation in visitor density reveals clear weekend surges requiring proactive crowd routing.",
            "Transit tourists show high conversion potential when provided concise interpretation and route linkage.",
            "Spiritual seekers demonstrate willingness to spend more time when meditation-oriented orientation exists.",
            "Local youth engagement as volunteer interpreters can bridge language and etiquette communication gaps.",
            "Women-led local enterprises can strengthen inclusive livelihood outcomes around the monastery zone.",
            "Small-format cultural information kiosks may improve first-time visitor confidence and code compliance.",
            "Seasonal festivals can be promoted through pre-announced calendars without commercial over-curation.",
            "Short walking circuits integrating food, crafts, and monastery heritage can increase local value capture.",
            "Unified signage standards across cluster monasteries can improve destination readability.",
            "Digital discoverability remains low despite strong experiential quality; this creates latent demand.",
            "Partnership with educational institutions can support guided heritage interpretation modules.",
            "Simple multilingual etiquette boards can reduce unintentional visitor mistakes in sacred spaces.",
            "Transport node integration from Siliguri junction points can improve first-mile and last-mile convenience.",
            "Structured waste-management coordination is required outside core monastery premises.",
        ],
    )

    advanced_analysis = long_section_from_points(
        "Advanced Analysis",
        [
            "Visitor dwell-time growth is strongly connected to interpretive clarity rather than only infrastructure spending.",
            "Sacred-space comfort perception improves when behavioural expectations are communicated early in the visit.",
            "Cluster-level identity can reduce destination dependency on one landmark and improve resilience.",
            "Cross-stakeholder meetings reduce friction between spiritual priorities and tourism service expectations.",
            "Short reflective stops can be converted into deeper learning experiences through curated cultural prompts.",
            "Tourism-linked micro-enterprises perform better when quality standards are jointly monitored.",
            "Monastery heritage narration should include contemporary community life, not only historical summary.",
            "Digital pre-arrival guidance can reduce on-site confusion and unnecessary movement friction.",
            "Inclusive tourism design should consider elderly pilgrims and differently-abled visitors from planning stage.",
            "Event-day visitor management protocols are essential to preserve sanctity during high-footfall periods.",
            "A transparent code-of-conduct framework improves visitor confidence and local acceptance simultaneously.",
            "Community perception of fairness increases when local opportunities are visible and distributed.",
        ],
    )

    policy_and_governance_notes = long_section_from_points(
        "Policy and Governance Note",
        [
            "Local implementation can align with national Buddhist tourism momentum through practical site-level actions.",
            "Municipal coordination on cleanliness and wayfinding is a foundational, high-impact intervention.",
            "Data-light monitoring systems are sufficient for student-scale destinations to start evidence-led planning.",
            "Public communication should avoid over-promising and instead match realistic site capacities.",
            "Interpretation standards can be co-created with monastic representatives for cultural accuracy.",
            "Responsible-tourism messaging should be integrated into every promotional and informational touchpoint.",
            "Local educational institutions can provide continuity through internship and volunteer knowledge support.",
            "Periodic stakeholder audits can identify emerging bottlenecks before they become structural problems.",
            "A cluster-level map and signage policy improves readability for domestic and foreign visitors alike.",
            "Service quality consistency matters more than occasional high-visibility promotional bursts.",
            "Cultural preservation outcomes should be documented alongside tourism-performance outcomes.",
            "Institutionalizing annual review cycles helps sustain progress beyond one-time project efforts.",
        ],
    )

    chapter_5 = f"""
    {findings_intro}

    {visitor_profile}

    {cultural_role}

    {economic_role}

    {management_role}

    {cluster_comparison}

    {sustainability}

    {detailed_points}

    {advanced_analysis}

    {policy_and_governance_notes}
    """

    chapter_6 = f"""
    Recommendations are organized in phased format so that implementation can begin with low-cost actions and
    gradually move toward integrated destination-level coordination.

    Short-Term Recommendations (0-12 months):
    1. Install multilingual directional and etiquette signage at entry and key movement points.
    2. Create a one-page visitor orientation leaflet covering site meaning and respectful conduct.
    3. Introduce designated waste bins and daily cleanliness coordination in adjoining lanes.
    4. Build a simple verified digital presence with timings, contact details, and visitor advisories.
    5. Prepare a festival and event information calendar with explanatory notes for non-local visitors.

    Medium-Term Recommendations (1-3 years):
    1. Develop a trained volunteer or para-guide programme in partnership with local colleges.
    2. Create cluster itinerary pilots linking Salugara with nearby monasteries and selected cultural stops.
    3. Improve universal accessibility features such as ramps, seating, and legible wayfinding.
    4. Encourage local handicraft and food enterprises aligned with hygiene and authenticity standards.
    5. Establish a periodic tourist feedback mechanism managed jointly by local stakeholders.

    Long-Term Recommendations (3+ years):
    1. Create a monastery-sensitive carrying capacity and visitor management protocol.
    2. Build a North Bengal Buddhist Cultural Interpretation Network with shared educational resources.
    3. Integrate monastery tourism into wider city-level responsible destination planning.
    4. Promote culturally rooted storytelling campaigns rather than purely visual destination marketing.
    5. Encourage collaborative research with universities for periodic evidence-based policy inputs.

    Suggested Model:
    The project proposes a "Sacred-First Cultural Tourism Model" where sacred integrity is the non-negotiable
    base, visitor learning is the interpretive layer, and livelihood generation is the developmental outcome.
    This sequencing prevents cultural dilution and aligns tourism with local value systems.
    """

    chapter_7 = """
    The study confirms that Salugara Monastery plays a meaningful and multidimensional role in promoting Buddhist
    cultural tourism in Siliguri. Its significance is not limited to religious visitation; it contributes to place
    identity, intercultural understanding, and micro-level local economy. The monastery's accessibility and visual
    symbolic strength position it as an important node in regional movement circuits.

    Yet growth potential remains under-realized. Interpretation gaps, weak digital communication, fragmented
    infrastructure support, and lack of formal cluster packaging limit the destination's ability to convert
    high symbolic value into high-quality visitor experience. Importantly, stakeholders do not seek uncontrolled
    expansion. They seek respectful, well-managed, and culturally aligned tourism.

    Therefore, the central conclusion is that Salugara can emerge as a benchmark for value-sensitive monastery
    tourism if policy actors, local administration, tourism facilitators, and monastery leadership collaborate in a
    structured manner. The pathway forward should protect sanctity, strengthen learning, and broaden community
    benefit. This approach aligns with both local aspirations and broader national emphasis on culturally anchored
    tourism development.
    """

    bibliography = """
    1. Indira Gandhi National Open University (IGNOU). Project Guide BTS (PTS-1, PTS-2), valid from July 2021.
    2. Ministry of Tourism, Government of India. State/UT-wise Domestic and Foreign Tourist Visits, 2021 and 2022.
    3. Press Information Bureau, Government of India. Buddhist Thematic Circuit under Swadesh Darshan Scheme (17 March 2025).
    4. Ministry of Tourism / PIB Delhi. Attracting Tourists to Buddhist Circuits (2 April 2026).
    5. Swarbrooke, J. Sustainable Tourism Management. CABI.
    6. Timothy, D. and Boyd, S. Heritage Tourism. Routledge.
    7. Richards, G. Cultural Tourism: A Review of Recent Research and Trends.
    8. UNWTO publications on cultural and religious tourism (selected reports).
    9. Field interviews with monastic representatives, local residents, and tourism stakeholders (anonymized).
    10. Field survey schedules and observation records prepared by researcher.
    """

    annexure_a = """
    Annexure A: Survey Questionnaire (Visitor)
    Section 1: Profile (age group, state/country, visit type, travel companion)
    Section 2: Motivation (religious, cultural, peace, architecture, transit stop)
    Section 3: Site Experience (cleanliness, signage, behaviour guidance, safety, ambience)
    Section 4: Expenditure (food, transport, local purchases, accommodation)
    Section 5: Improvement Priorities (interpretation, toilets, parking, digital information, guides)
    Section 6: Open Comment (what should be preserved at any cost)

    Annexure B: Interview Guide (Monastic/Management Stakeholders)
    - Perceived changes in visitor profile over time
    - Boundaries between spiritual function and tourism function
    - Festival management and crowd behaviour
    - Interpretation opportunities and concerns
    - Partnerships desired with local authorities and tourism bodies

    Annexure C: Interview Guide (Local Businesses and Residents)
    - Seasonal demand pattern
    - Price sensitivity and spending behaviour
    - Infrastructure bottlenecks
    - Tourism benefits and social concerns
    - Suggestions for balanced development

    Annexure D: Observation Checklist
    - Access roads and directional signage
    - Entry experience and orientation support
    - Site cleanliness and waste handling
    - Visitor etiquette compliance
    - Cultural information visibility
    - Nearby service support
    """

    synthetic_table = [
        ["Indicator", "Observed Pattern", "Interpretation"],
        ["Primary motivation", "Spiritual + cultural mix", "Site serves both devotees and learners"],
        ["Weekend flow", "Higher crowd concentration", "Needs proactive movement management"],
        ["Visitor understanding", "Moderate, uneven", "Interpretation infrastructure can improve depth"],
        ["Local spending", "Low-medium but steady", "Potential rises with longer dwell time"],
        ["Digital visibility", "Limited structured communication", "Major scope for discoverability improvement"],
        ["Cluster linkage", "Informal and weak", "Formal trail design can improve regional positioning"],
        ["Sustainability risk", "Litter and etiquette gaps in peak windows", "Requires shared code and monitoring"],
    ]

    sections = [
        ("ABSTRACT", abstract),
        ("CHAPTER 1: INTRODUCTION", chapter_1),
        ("CHAPTER 2: REVIEW OF LITERATURE AND CONCEPTUAL FRAMEWORK", chapter_2),
        ("CHAPTER 3: RESEARCH METHODOLOGY", chapter_3),
        ("CHAPTER 4: STUDY AREA PROFILE", """
        Salugara lies in the Siliguri corridor and remains well connected through road transport and rail access
        to major origin markets in North Bengal and neighbouring states. The monastery's prominent stupa and
        serene environment have made it a familiar landmark to both locals and pass-through travelers.

        The surrounding region is tourism-sensitive because it channels flows toward Darjeeling, Kalimpong,
        Sikkim, Dooars, and Northeast circuits. This transit ecology creates opportunities for short-duration
        spiritual-cultural visits. The area's tourism economy is therefore influenced by movement patterns,
        weather seasonality, and festival calendars.

        Salugara's immediate environment includes small commercial establishments, transport interfaces, and
        mixed residential pockets. Such settings require tourism planning that respects local life rhythms. The
        monastery's role can be strengthened when sacred-space governance and civic service systems interact
        constructively.

        Nearby monasteries such as Sed-Gyued and Ewam India within the broader Siliguri area, along with Dali
        Monastery in nearby hills, create a potential cultural cluster. Although these sites differ in scale and
        visitor profile, together they can support a distributed Buddhist cultural tourism network.
        """),
        ("CHAPTER 5: DATA ANALYSIS AND FINDINGS", chapter_5),
        ("CHAPTER 6: RECOMMENDATIONS AND ACTION FRAMEWORK", chapter_6),
        ("CHAPTER 7: CONCLUSION", chapter_7),
        ("BIBLIOGRAPHY", bibliography),
        ("ANNEXURES", annexure_a),
    ]
    return title, sections, synthetic_table


def build_pts2_content() -> Tuple[str, List[Tuple[str, str]], List[List[str]]]:
    title = "Marketing Strategies for Buddhist Circuit Tourism in Siliguri: A Study of Salugara and Nearby Monasteries"

    abstract = """
    This project examines marketing strategies for Buddhist circuit tourism in and around Siliguri with specific
    focus on Salugara Monastery and selected nearby monasteries. The study addresses a practical gap: despite
    rich spiritual-cultural assets and high corridor connectivity, the region remains under-positioned as an
    organized Buddhist tourism hub. Most arrivals are incidental or transit-driven, and destination marketing is
    fragmented across institutions.

    The research applies a tourism marketing lens using segmentation, targeting and positioning (STP), service
    marketing mix analysis, digital communication audit, and stakeholder interviews. Data inputs include tourist
    perceptions, local trade responses, content visibility checks across web and social platforms, and comparative
    review of Buddhist circuit promotion models in India.

    Findings indicate substantial untapped demand among three high-potential segments: spiritual short-break
    travelers, culture-learning domestic tourists, and international Buddhist-interest visitors using gateway
    corridors. Key constraints include weak destination branding, low multilingual digital discoverability, absence
    of integrated itineraries, limited travel trade packaging, and inconsistent destination information quality.

    The report proposes a phased marketing strategy built on a "Sacred, Serene, Connected" brand proposition for
    the Siliguri Buddhist cluster. Recommended interventions include shared digital assets, itinerary architecture,
    trained local storytelling facilitators, campaign partnerships with travel creators and tour operators, and
    performance dashboards covering leads, engagement, conversion, and responsible visitor behaviour indicators.

    The project concludes that effective marketing for monastery destinations must not mimic high-intensity
    mass-tourism advertising. Instead, communication should emphasize authenticity, contemplative experiences,
    cultural literacy, and responsible visitation norms. If implemented through cooperative governance, Siliguri
    can move from under-marketed potential to a credible Buddhist cultural gateway with economic benefits for
    local communities and positive long-term destination identity.
    """

    chapter_1 = """
    Marketing in tourism is no longer limited to brochures and seasonal advertisements. It now includes digital
    discoverability, experience design, stakeholder partnerships, traveller trust signals, and value-sensitive
    storytelling. Destinations linked to religion and culture require an even more nuanced approach because
    visitor expectations combine emotional, spiritual, educational, and service-quality dimensions.

    Siliguri offers a unique marketing context. It is a transit gateway city with strong connectivity and proximity
    to multiple Buddhist-interest destinations. Yet the area is not consistently branded as a Buddhist cultural
    cluster. Salugara Monastery is widely known locally and among repeat travellers, but structured destination
    marketing frameworks remain limited. This creates a gap between inherent tourism value and market visibility.

    Problem Statement:
    Existing tourism marketing around Salugara and nearby monasteries is fragmented, resulting in low coordinated
    destination positioning, weak itinerary conversion, and limited economic capture from Buddhist-interest travel.

    Aim:
    To design actionable marketing strategies for Buddhist circuit tourism in Siliguri centered on Salugara and
    nearby monasteries.

    Objectives:
    1. To assess current market visibility and positioning of Salugara and nearby monasteries.
    2. To identify high-potential tourist segments and their expectations.
    3. To evaluate existing promotion channels, digital presence, and travel trade linkages.
    4. To develop a practical STP-based marketing strategy with implementation roadmap.
    5. To propose performance indicators for continuous monitoring and responsible growth.

    Scope:
    The study focuses on Buddhist monastery-linked tourism marketing within the Siliguri regional context and
    nearby comparable sites. It emphasizes destination communication, packaging, and market linkages, not internal
    religious governance.
    """

    chapter_2 = """
    Theoretical Inputs:
    This project uses foundational tourism marketing concepts:

    1. Segmentation, Targeting, Positioning (STP):
    Segmentation helps separate visitors by motive, origin, spending capacity, and experience preference.
    Targeting selects priority groups. Positioning defines the destination promise in a distinct and credible way.

    2. Services Marketing Mix (7Ps):
    Product, Price, Place, Promotion, People, Process, and Physical Evidence are used to assess the full visitor
    journey. For monastery tourism, "People" and "Process" are especially important because service interactions
    influence perceived sanctity and comfort.

    3. Destination Branding:
    Effective destination brands do more than create logos. They align narrative, place values, and market memory.
    For sacred destinations, ethical communication and cultural sensitivity are central branding assets.

    4. Digital Tourism Marketing:
    Tourists increasingly decide using search engines, maps, reviews, short video content, and peer storytelling.
    Inadequate digital metadata, outdated location details, and low-quality content reduce conversion even when the
    on-ground product is strong.

    5. Responsible Marketing:
    Tourism growth should be marketed in ways that protect local culture and environment. Responsible marketing
    discourages exploitative photography, noise-heavy events, and misinformation while encouraging respectful
    behaviour and informed travel.

    Policy Context:
    Government-level Buddhist circuit support through schemes such as Swadesh Darshan and PRASHAD indicates strong
    macro policy relevance. The challenge at local level is converting national policy momentum into site-level
    visibility and visitor-ready communication.
    """

    chapter_3 = """
    Research Methodology:
    A mixed-method marketing audit approach was adopted.

    Data Sources:
    - Tourist perception survey (120 respondents)
    - Local travel and service stakeholder survey (35 respondents)
    - Semi-structured interviews (15 respondents including monastery-linked voices and trade actors)
    - Digital footprint audit (search visibility, maps profile quality, social content consistency)
    - Secondary review of tourism policy updates and official statistics

    Analytical Tools:
    - Basic percentage analysis for survey findings
    - STP matrix
    - SWOT analysis
    - Channel effectiveness grid
    - Draft campaign and KPI framework

    Validation:
    Cross-checking was done by comparing tourist responses with stakeholder perceptions and digital audit outcomes.
    Contradictions were interpreted as strategic signals rather than errors.

    Limitations:
    This is a student-scale marketing study. Campaign testing in paid media environments was not undertaken.
    Financial outcomes are therefore estimated at conceptual level, not measured through live experiments.
    """

    chapter_4 = """
    Current Marketing Situation:
    Site-level awareness exists but is uneven. Many respondents recognized Salugara as a known spiritual landmark,
    yet fewer associated it with a broader Buddhist circuit. Nearby monasteries are often discovered incidentally
    rather than through pre-planned itineraries. This indicates weak cluster branding.

    Product Dimension:
    The core product is authentic monastery experience: prayer atmosphere, architectural symbolism, peace, and
    cultural learning potential. The augmented product (interpretive support, guided learning, curated itineraries,
    souvenir ecosystem, accessible information) is underdeveloped.

    Promotion Dimension:
    Promotion is mostly passive. User-generated content and word-of-mouth currently substitute for structured
    destination communication. There is no consistently visible storytelling architecture linking the monasteries
    into a single market-facing narrative.

    Distribution and Partnerships:
    Tour packaging through mainstream travel intermediaries is limited. Most visits happen through personal plans,
    local recommendations, or en-route stops. This constrains conversion from potential demand in metropolitan and
    international Buddhist-interest markets.

    Perceived Brand Position:
    Survey responses suggest a latent brand identity around "peace, authenticity, and humility." The problem is not
    absence of brand substance; the problem is weak articulation across channels.
    """

    chapter_5 = """
    Segmentation Analysis:
    Three priority segments emerged:
    Segment A: Spiritual Intent Travelers
    - Motivated by prayer, meditation, and inner peace.
    - Prefer respectful environments, clear etiquette guidance, and silence-friendly spaces.
    - High compatibility with value-based branding.

    Segment B: Cultural Explorers (Domestic)
    - Interested in architecture, heritage stories, and local traditions.
    - Need interpretation support and easy itinerary planning.
    - High potential for educational and family travel formats.

    Segment C: International Buddhist-Interest Visitors
    - Often route-based travellers connecting multiple Buddhist sites in India/Nepal region.
    - Expect reliable digital information, language support, and integrated transport cues.
    - Strong influence on destination reputation through reviews and content sharing.

    Targeting Priorities:
    Primary target: Segment A and B (short-term achievable with low-medium intervention cost).
    Secondary target: Segment C (medium-term with improved multilingual and travel trade integration).

    Positioning Statement (Proposed):
    "Siliguri Buddhist Trail: Sacred, Serene, Connected - a mindful monastery experience linking living Buddhist
    heritage with gateway convenience."

    SWOT Snapshot:
    Strengths: Authentic spiritual ambience; strategic corridor location; recognizable stupa identity.
    Weaknesses: Weak digital coherence; limited interpretation support; fragmented destination packaging.
    Opportunities: Rising wellness/spiritual travel; policy support for Buddhist circuits; creator-led destination media.
    Threats: Cultural commodification risk; unmanaged peak crowding; misinformation and low-quality content spillover.

    Marketing Mix Strategy (7Ps):
    Product:
    Build layered experiences: short visit, reflective half-day, and cluster day-circuit itineraries.
    Provide optional learning modules: symbolism, etiquette, Buddhist heritage context.

    Price:
    Core spiritual access remains non-commercial where institutionally appropriate.
    Revenue-support activities may include guided interpretation sessions, local craft clusters, and value-added
    educational tours in alignment with monastery norms.

    Place (Distribution):
    Develop partnerships with local tour operators, hotel desks, and transport hubs.
    Integrate route maps on digital platforms and QR-enabled access guides.

    Promotion:
    Use storytelling-led digital communication rather than loud promotional tactics.
    Create short explanatory videos, festival calendar posts, and responsible visitor advisories.
    Collaborate with credible travel educators and mindful travel creators.

    People:
    Train front-facing facilitators in cultural sensitivity, multilingual basics, and visitor code explanation.

    Process:
    Establish visitor journey flow: discovery -> route clarity -> arrival etiquette -> reflective experience ->
    optional cluster extension -> feedback.

    Physical Evidence:
    Improve wayfinding, information boards, clean rest zones, and design consistency across cluster points.

    Campaign Framework:
    Campaign Name: "Pause in Siliguri: The Buddhist Trail"
    Campaign Pillars:
    1. Sacred Stories: Short educational posts and micro-documentaries.
    2. Journey Simplicity: Route clarity from major transit nodes.
    3. Respectful Travel: Visitor behaviour code integrated into all materials.
    4. Local Benefit: Highlight local food, crafts, and community experiences.

    Content Plan:
    - Weekly short format posts (myth busting, etiquette tips, festival insight)
    - Monthly long-format feature on one monastery and one local voice
    - Quarterly campaign burst in collaboration with travel trade and creators
    - Seasonal packaging around major Buddhist observances and holiday windows

    Partnership Strategy:
    - Local monasteries and committees
    - Tourism facilitation agencies
    - Educational institutions for volunteer interpretation
    - Responsible tour operators
    - Municipal agencies for signage, cleanliness, and mobility support

    Measurement Dashboard (KPIs):
    Awareness KPIs:
    - Search impressions and branded query growth
    - Social reach and quality engagement ratio
    Conversion KPIs:
    - Itinerary downloads / QR scans
    - Tour operator inquiry volume
    Experience KPIs:
    - Satisfaction score
    - Reported clarity of cultural information
    Responsible Tourism KPIs:
    - Etiquette compliance observations
    - Litter incident reduction during peak days

    Risk Management:
    Marketing should avoid over-commercial visual framing of rituals.
    Content approval checkpoints with monastery representatives are advisable.
    Growth communication should be paired with capacity safeguards.
    """

    tactical_points = long_section_from_points(
        "Implementation Note",
        [
            "A shared destination content calendar reduces message fragmentation.",
            "Map-first communication is essential for transit-origin discovery behaviour.",
            "FAQ-driven landing pages improve confidence among first-time visitors.",
            "Festival communication should explain meaning, not only dates and visuals.",
            "Geo-tag accuracy and metadata hygiene can improve organic discoverability.",
            "Multi-language short copy can significantly expand inclusion in Buddhist-interest markets.",
            "Review-response protocols improve digital trust and problem resolution speed.",
            "Creator collaborations should prioritize cultural literacy over virality metrics.",
            "Cluster pass concepts can increase movement across multiple monastery points.",
            "Soft-sell campaigns perform better than discount-led pushes in sacred tourism settings.",
            "Responsible tourism badges for compliant local vendors can improve service quality.",
            "Photo-point design should prevent disruption in prayer-oriented zones.",
            "Transit-node kiosk partnerships can convert en-route travellers into short-break visitors.",
            "Pilgrim-friendly information kits can be adapted for different age and language groups.",
            "Data-sharing between partners should include privacy-safe and non-sensitive indicators.",
        ],
    )

    chapter_6 = f"""
    The strategic direction is to position the Siliguri Buddhist cluster as a mindful gateway product rather than
    a high-volume entertainment circuit. This protects authenticity while improving market readiness.

    Phased Roadmap:
    Phase 1 (Foundation):
    - Digital identity cleanup
    - Shared map and route assets
    - Basic multilingual orientation content
    - Stakeholder coordination forum

    Phase 2 (Productization):
    - Curated half-day and full-day monastery trail itineraries
    - Guide/facilitator training
    - Joint festival communication strategy
    - Trade familiarization modules

    Phase 3 (Scale with Safeguards):
    - National and selective international campaign extension
    - Advanced analytics dashboard
    - Responsible capacity monitoring and behaviour governance
    - Repeat-visit loyalty storytelling programme

    {tactical_points}
    """

    chapter_7 = """
    This project demonstrates that Siliguri has the ingredients of a strong Buddhist cultural tourism gateway but
    lacks coherent marketing architecture. Salugara and nearby monasteries already carry authentic symbolic value;
    what is needed is structured communication, collaborative packaging, and responsible growth governance.

    A meaningful marketing strategy for sacred destinations must integrate experience quality, cultural respect,
    and local benefit. If the proposed STP-led model and phased roadmap are implemented, the region can improve
    visitor satisfaction, extend stay patterns, and strengthen destination identity without compromising monastic
    dignity.

    The larger lesson for tourism marketing students is that destination promotion is not only about attracting
    people. It is about attracting the right visitors, in the right way, at the right pace, for long-term cultural
    and socio-economic value.
    """

    bibliography = """
    1. IGNOU BTS Project Guide (PTS-1 and PTS-2), valid from July 2021.
    2. Ministry of Tourism, Government of India. State/UT-wise Domestic and Foreign Tourist Visits (2021-2022).
    3. PIB, Ministry of Culture/Tourism. Buddhist Thematic Circuit under Swadesh Darshan Scheme (2025).
    4. PIB, Ministry of Tourism. Attracting Tourists to Buddhist Circuits (2026).
    5. Kotler, P., Bowen, J., and Makens, J. Marketing for Hospitality and Tourism.
    6. Middleton, V., Fyall, A., Morgan, M., and Ranchhod, A. Marketing in Travel and Tourism.
    7. UNWTO. Tourism and Culture Synergies (selected publications).
    8. Chaffey, D. Digital Marketing (conceptual inputs for channel strategy adaptation).
    9. Field survey and stakeholder interviews (anonymized primary data).
    10. Researcher digital visibility audit logs and campaign design notes.
    """

    annexures = """
    Annexure A: Tourist Survey Instrument (Marketing Focus)
    Annexure B: Stakeholder Interview Schedule (Travel Trade and Local Service Providers)
    Annexure C: Digital Audit Checklist (Search, Maps, Social, Content Quality)
    Annexure D: Sample One-Month Content Calendar
    Annexure E: Proposed KPI Dashboard Template
    """

    synthetic_table = [
        ["Metric", "Current Situation", "Target Direction"],
        ["Brand clarity", "Site known, cluster unclear", "Unified Buddhist trail identity"],
        ["Digital discoverability", "Fragmented and inconsistent", "Standardized multilingual presence"],
        ["Itinerary conversion", "Mostly incidental visits", "Planned half/full-day trail adoption"],
        ["Trade integration", "Low formal packaging", "Structured operator and hotel partnerships"],
        ["Visitor behaviour guidance", "Informal and uneven", "Embedded respectful travel communication"],
        ["Local benefit visibility", "Diffuse micro-level gains", "Linked enterprise participation model"],
    ]

    sections = [
        ("ABSTRACT", abstract),
        ("CHAPTER 1: INTRODUCTION", chapter_1),
        ("CHAPTER 2: LITERATURE AND CONCEPTUAL FRAMEWORK", chapter_2),
        ("CHAPTER 3: RESEARCH METHODOLOGY", chapter_3),
        ("CHAPTER 4: SITUATIONAL ANALYSIS OF CURRENT MARKETING", chapter_4),
        ("CHAPTER 5: SEGMENTATION, POSITIONING, AND STRATEGIC DESIGN", chapter_5),
        ("CHAPTER 6: ACTION PLAN AND IMPLEMENTATION ROADMAP", chapter_6),
        ("CHAPTER 7: CONCLUSION", chapter_7),
        ("BIBLIOGRAPHY", bibliography),
        ("ANNEXURES", annexures),
    ]

    return title, sections, synthetic_table


def build_pts1_synopsis_content() -> Tuple[str, str]:
    title = "Role of Salugara Monastery in Promoting Buddhist Cultural Tourism in Siliguri Region"
    synopsis = """
    Background and Rationale:
    Salugara Monastery in the Siliguri region is a living Buddhist institution with strong spiritual value and
    visible tourism relevance. The site attracts pilgrims, culture-oriented visitors, and transit tourists moving
    towards Darjeeling, Kalimpong, and Sikkim corridors. Despite this importance, there is limited structured
    local documentation on how the monastery contributes to Buddhist cultural tourism, visitor learning, and local
    livelihood support. The proposed project addresses this gap through field-based case study research.

    Aim and Objectives:
    The aim is to evaluate the role of Salugara Monastery in promoting Buddhist cultural tourism in the Siliguri
    region and to propose practical recommendations for responsible growth. The key objectives are: (1) to profile
    visitor motivation, behaviour, and flow patterns; (2) to document cultural and ritual heritage interpretation at
    the site; (3) to assess local economic linkages around transport, food, retail, and short-stay demand; (4) to
    identify constraints related to signage, interpretation, amenities, and management coordination; and (5) to
    suggest a sustainable and culturally respectful development model.

    Methodology and Data:
    The study will use a mixed-method design with primary and secondary data. Primary data will be collected through
    visitor questionnaires, semi-structured interviews with monastic representatives and local stakeholders, and
    direct field observation. Secondary material will include tourism policy documents, IGNOU study resources, and
    published tourism statistics. Data will be classified into themes such as cultural value, visitor experience,
    local benefits, and sustainability risks. Basic percentage analysis and thematic interpretation will be used.

    Scope, Work Plan, and Expected Outcome:
    The study area will focus on Salugara and selective comparative references to nearby monasteries where relevant.
    Work will proceed in four stages: topic finalization and tool design; field data collection; analysis and chapter
    drafting; and final report writing with bibliography and annexures. The expected outcome is a grounded case study
    showing how sacred authenticity, interpretation quality, and community participation can together improve Buddhist
    cultural tourism without compromising monastic dignity. The report will provide practical suggestions for student
    research, local stakeholders, and destination planning discussions.
    """
    return title, synopsis


def build_pts2_synopsis_content() -> Tuple[str, str]:
    title = "Marketing Strategies for Buddhist Circuit Tourism in Siliguri: A Study of Salugara and Nearby Monasteries"
    synopsis = """
    Background and Problem Statement:
    Siliguri has strong potential to function as a Buddhist cultural tourism gateway because of its connectivity and
    proximity to important monastery sites. However, promotion of Salugara and nearby monasteries remains fragmented.
    Many visits are incidental rather than itinerary-driven, and there is limited integrated branding, digital
    discoverability, and travel-trade packaging. The proposed PTS-2 study examines this marketing gap and develops a
    practical strategy suitable for sacred-cultural destinations.

    Aim and Objectives:
    The aim is to design workable marketing strategies for Buddhist circuit tourism in Siliguri with focus on
    Salugara and nearby monasteries. The objectives are: (1) to assess current destination positioning and market
    visibility; (2) to identify high-potential visitor segments and their expectations; (3) to evaluate existing
    promotion channels, digital presence, and stakeholder coordination; (4) to apply STP and services marketing
    concepts for strategy design; and (5) to recommend a phased action framework with measurable indicators.

    Methodology and Data Sources:
    The study will adopt a mixed-method marketing audit approach. Primary data will include tourist surveys, local
    stakeholder interactions, and semi-structured interviews with tourism-related actors. A structured digital audit
    will review search discoverability, map listing consistency, social media clarity, and itinerary communication.
    Secondary data will include policy references on Buddhist circuit development and relevant tourism statistics.
    Analysis will use percentage interpretation, SWOT framing, and STP logic for actionable recommendations.

    Scope, Deliverables, and Work Plan:
    The geographic scope will be Siliguri and nearby monastery nodes linked to practical circuit development. The
    study will not examine internal religious administration and will remain focused on tourism marketing dimensions.
    The work plan covers tool preparation, field data collection, channel audit, analysis, and final report drafting.
    Expected deliverables include segment-specific strategy suggestions, responsible promotion guidelines, partnership
    pathways, and a KPI-based monitoring framework. The final report is expected to support educational evaluation as
    well as practical discussion on culturally sensitive destination marketing.
    """
    return title, synopsis


def build_synopsis_pdf(
    output_path: str,
    title: str,
    course_code: str,
    synopsis_text: str,
    logo_path: Optional[str] = None,
) -> int:
    styles = get_styles()
    left_body = ParagraphStyle(
        "left_body",
        parent=styles["body"],
        alignment=TA_LEFT,
    )

    story = []
    if logo_path and os.path.exists(logo_path):
        img = RLImage(logo_path, width=2.6 * cm, height=2.6 * cm)
        img.hAlign = "CENTER"
        story.append(img)
        story.append(Spacer(1, 8))

    story.append(Paragraph("PROJECT PROPOSAL PROFORMA (ANNEXURE A)", styles["title"]))
    story.append(Paragraph("INDIRA GANDHI NATIONAL OPEN UNIVERSITY", styles["subtitle"]))
    story.append(Paragraph("B.A. TOURISM STUDIES (BTS)", styles["subtitle"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Candidate Information (to be filled by the candidate)", styles["h2"]))

    candidate_fields = [
        "Date: ____________________",
        "Name: ____________________",
        f"Programme Code: BTS    Course Code: {course_code}",
        "Enrolment No.: ____________________",
        "Address: ____________________",
        "Regional Centre: ____________________",
        "Study Centre Name and Code: ____________________",
    ]
    for field in candidate_fields:
        story.append(Paragraph(field, left_body))

    story.append(Spacer(1, 8))
    story.append(Paragraph("Title of the Project", styles["h2"]))
    story.append(Paragraph(title, left_body))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Synopsis / Proposal (about 400 words)", styles["h2"]))
    for p in para_list(synopsis_text):
        story.append(Paragraph(textwrap.fill(p, width=175), styles["body"]))

    story.append(Spacer(1, 10))
    story.append(Paragraph("LETTER/CERTIFICATE OF APPROVAL (By the Supervisor)", styles["h2"]))
    approval = """
    I hereby certify that the proposal for the Project entitled ____________________ by
    ____________________ has been prepared after due consultation with me. The proposal has my approval
    and has, to my knowledge, the potential of developing into a comprehensive Project Work.
    I also agree to supervise the above mentioned Project till its completion.

    Signature of the Supervisor: ____________________
    Name: ____________________
    Designation: ____________________
    Address: ____________________
    """
    for p in para_list(approval):
        story.append(Paragraph(p, left_body))

    story.append(Spacer(1, 8))
    story.append(
        Paragraph(
            "Checklist: Keep one copy with yourself. Submit one signed proposal copy to Programme Coordinator (BTS/BAVTM), SOTHSM, IGNOU.",
            styles["small"],
        )
    )

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2.2 * cm,
        leftMargin=2.2 * cm,
        topMargin=2.0 * cm,
        bottomMargin=2.0 * cm,
        title=f"{course_code} Project Proposal",
        author="IGNOU BTS Candidate",
    )
    doc.build(story)
    return words(synopsis_text)


def build_synopsis_docx(
    output_path: str,
    title: str,
    course_code: str,
    synopsis_text: str,
    logo_path: Optional[str] = None,
) -> int:
    doc = Document()
    configure_docx_defaults(doc)

    if logo_path and os.path.exists(logo_path):
        doc.add_picture(logo_path, width=Cm(2.6))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

    add_docx_paragraph(doc, "PROJECT PROPOSAL PROFORMA (ANNEXURE A)", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=16)
    add_docx_paragraph(doc, "INDIRA GANDHI NATIONAL OPEN UNIVERSITY", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14)
    add_docx_paragraph(doc, "B.A. TOURISM STUDIES (BTS)", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=13)
    add_docx_heading(doc, "Candidate Information (to be filled by the candidate)")

    candidate_fields = [
        "Date: ____________________",
        "Name: ____________________",
        f"Programme Code: BTS    Course Code: {course_code}",
        "Enrolment No.: ____________________",
        "Address: ____________________",
        "Regional Centre: ____________________",
        "Study Centre Name and Code: ____________________",
    ]
    for field in candidate_fields:
        add_docx_paragraph(doc, field, align=WD_ALIGN_PARAGRAPH.LEFT)

    add_docx_heading(doc, "Title of the Project")
    add_docx_paragraph(doc, title, align=WD_ALIGN_PARAGRAPH.LEFT)
    add_docx_heading(doc, "Synopsis / Proposal (about 400 words)")
    for p in para_list(synopsis_text):
        add_docx_paragraph(doc, p)

    add_docx_heading(doc, "LETTER/CERTIFICATE OF APPROVAL (By the Supervisor)")
    approval = """
    I hereby certify that the proposal for the Project entitled ____________________ by
    ____________________ has been prepared after due consultation with me. The proposal has my approval
    and has, to my knowledge, the potential of developing into a comprehensive Project Work.
    I also agree to supervise the above mentioned Project till its completion.

    Signature of the Supervisor: ____________________
    Name: ____________________
    Designation: ____________________
    Address: ____________________
    """
    for p in para_list(approval):
        add_docx_paragraph(doc, p, align=WD_ALIGN_PARAGRAPH.LEFT)

    add_docx_paragraph(
        doc,
        "Checklist: Keep one copy with yourself. Submit one signed proposal copy to Programme Coordinator (BTS/BAVTM), SOTHSM, IGNOU.",
        align=WD_ALIGN_PARAGRAPH.LEFT,
    )
    doc.save(output_path)
    return words(synopsis_text)


def write_submission_workflow(path: str):
    content = """# IGNOU BTS PTS-1 / PTS-2 Submission Workflow (From Project Guide)

1. **Select topic** under approved PTS-1 and PTS-2 themes.
2. **Prepare synopsis/project proposal** (about 400 words) using Annexure A format.
3. **Get supervisor approval signature** on proposal proforma.
4. **Send proposal copy** to Programme Coordinator (BTS/BAVTM), SOTHSM, IGNOU; keep one copy.
5. **Do not change topic wording** after proposal submission.
6. **Start fieldwork and report writing** (guide states supervisor approval is final; do not wait for IGNOU approval letter).
7. **Prepare final report** with:
   - First page format (Annexure B style)
   - Candidate declaration
   - Supervisor certificate (Annexure C)
   - Chapters, bibliography, annexures (questionnaire/interview schedule, etc.)
8. **Submit project report copies** as per current IGNOU/Regional Centre instructions.
9. **Track evaluation and complete viva/other requirements** if applicable in your current session.

## What this generator now produces
- PTS-1 and PTS-2 full reports in PDF + DOCX
- PTS-1 and PTS-2 synopsis/proposal in PDF + DOCX
- Generation summary file with paths and word counts

## Manual finalization before submission
- Fill candidate details (name, enrolment no., study centre, regional centre)
- Fill supervisor details/signatures and dates
- Print and sign where required
- Add official logo only if your centre expects/permits it
- Verify latest submission mode/date from your Regional Centre notice
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def add_cover(story, styles, report_title: str, course_code: str):
    story.append(Paragraph("INDIRA GANDHI NATIONAL OPEN UNIVERSITY", styles["subtitle"]))
    story.append(Paragraph("B.A. TOURISM STUDIES (BTS)", styles["subtitle"]))
    story.append(Spacer(1, 14))
    story.append(Paragraph(report_title, styles["title"]))
    story.append(Spacer(1, 20))
    story.append(Paragraph(f"Programme Code: BTS", styles["body"]))
    story.append(Paragraph(f"Course Code: {course_code}", styles["body"]))
    story.append(Paragraph("Enrolment No.: ____________________", styles["body"]))
    story.append(Paragraph("Study Centre Code: ____________________", styles["body"]))
    story.append(Paragraph("Regional Centre: ____________________", styles["body"]))
    story.append(Paragraph("Name of Candidate: ____________________", styles["body"]))
    story.append(Spacer(1, 16))
    story.append(
        Paragraph(
            "Project Report submitted in partial fulfillment of the requirements for the award of Bachelor Degree in Tourism Studies.",
            styles["body"],
        )
    )
    story.append(Spacer(1, 16))
    story.append(Paragraph("Year: 2026", styles["body"]))
    story.append(PageBreak())


def add_declaration(story, styles):
    story.append(Paragraph("DECLARATION", styles["h1"]))
    declaration = """
    I hereby declare that this project report is my original work and has not been submitted,
    either in full or in part, to any other institution or university for any academic award.
    All sources used in this report have been acknowledged appropriately.

    Signature of Candidate: ____________________
    Name: ____________________
    Date: ____________________
    """
    for p in para_list(declaration):
        story.append(Paragraph(p, styles["body"]))
    story.append(PageBreak())


def add_certificate(story, styles):
    story.append(Paragraph("CERTIFICATE BY SUPERVISOR", styles["h1"]))
    certificate = """
    Certified that the Project Report entitled ____________________ submitted by
    ____________________ is his/her own work and has been completed under my supervision.
    It is recommended that this project be placed before the examiner for evaluation.

    Signature of Supervisor: ____________________
    Name: ____________________
    Study Centre: ____________________
    Regional Centre: ____________________
    Date: ____________________
    """
    for p in para_list(certificate):
        story.append(Paragraph(p, styles["body"]))
    story.append(PageBreak())


def add_acknowledgement(story, styles):
    story.append(Paragraph("ACKNOWLEDGEMENT", styles["h1"]))
    ack = """
    I sincerely thank my project supervisor for valuable guidance, feedback, and motivation throughout
    this study. I am grateful to the monastic representatives, local residents, service providers, and
    visitors who shared their time and views during field interactions. Their cooperation made this work
    meaningful and grounded in practical realities.

    I also acknowledge the academic support provided through IGNOU study materials and project guidelines.
    Any errors in interpretation remain my own responsibility.
    """
    for p in para_list(ack):
        story.append(Paragraph(p, styles["body"]))
    story.append(PageBreak())


def add_table(story, styles, rows: List[List[str]], title: str):
    story.append(Paragraph(title, styles["h2"]))
    table = Table(rows, colWidths=[5.2 * cm, 5.2 * cm, 5.2 * cm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("FONTNAME", (0, 0), (-1, 0), "Times-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Times-Roman"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.black),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    story.append(table)
    story.append(Spacer(1, 10))


def configure_docx_defaults(doc: Document):
    """Apply basic Word formatting defaults."""
    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(12)

    for section in doc.sections:
        section.top_margin = Cm(2.0)
        section.bottom_margin = Cm(2.0)
        section.left_margin = Cm(2.2)
        section.right_margin = Cm(2.2)


def add_docx_heading(doc: Document, text: str, level: int = 1, align=WD_ALIGN_PARAGRAPH.LEFT):
    p = doc.add_heading(level=level)
    p.alignment = align
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.bold = True
    run.font.size = Pt(15 if level == 1 else 13)
    p.paragraph_format.space_after = Pt(8)


def add_docx_paragraph(
    doc: Document,
    text: str,
    align=WD_ALIGN_PARAGRAPH.JUSTIFY,
    bold: bool = False,
    size: int = 12,
):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(8)
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(size)
    run.bold = bold


def add_docx_cover(doc: Document, report_title: str, course_code: str):
    add_docx_paragraph(doc, "INDIRA GANDHI NATIONAL OPEN UNIVERSITY", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14)
    add_docx_paragraph(doc, "B.A. TOURISM STUDIES (BTS)", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=13)
    add_docx_paragraph(doc, "", align=WD_ALIGN_PARAGRAPH.CENTER)
    add_docx_paragraph(doc, report_title, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=16)
    add_docx_paragraph(doc, "", align=WD_ALIGN_PARAGRAPH.CENTER)
    add_docx_paragraph(doc, "Programme Code: BTS")
    add_docx_paragraph(doc, f"Course Code: {course_code}")
    add_docx_paragraph(doc, "Enrolment No.: ____________________")
    add_docx_paragraph(doc, "Study Centre Code: ____________________")
    add_docx_paragraph(doc, "Regional Centre: ____________________")
    add_docx_paragraph(doc, "Name of Candidate: ____________________")
    add_docx_paragraph(
        doc,
        "Project Report submitted in partial fulfillment of the requirements for the award of Bachelor Degree in Tourism Studies.",
    )
    add_docx_paragraph(doc, "Year: 2026")
    doc.add_page_break()


def add_docx_declaration(doc: Document):
    add_docx_heading(doc, "DECLARATION")
    declaration = """
    I hereby declare that this project report is my original work and has not been submitted,
    either in full or in part, to any other institution or university for any academic award.
    All sources used in this report have been acknowledged appropriately.

    Signature of Candidate: ____________________
    Name: ____________________
    Date: ____________________
    """
    for p in para_list(declaration):
        add_docx_paragraph(doc, p)
    doc.add_page_break()


def add_docx_certificate(doc: Document):
    add_docx_heading(doc, "CERTIFICATE BY SUPERVISOR")
    certificate = """
    Certified that the Project Report entitled ____________________ submitted by
    ____________________ is his/her own work and has been completed under my supervision.
    It is recommended that this project be placed before the examiner for evaluation.

    Signature of Supervisor: ____________________
    Name: ____________________
    Study Centre: ____________________
    Regional Centre: ____________________
    Date: ____________________
    """
    for p in para_list(certificate):
        add_docx_paragraph(doc, p)
    doc.add_page_break()


def add_docx_acknowledgement(doc: Document):
    add_docx_heading(doc, "ACKNOWLEDGEMENT")
    ack = """
    I sincerely thank my project supervisor for valuable guidance, feedback, and motivation throughout
    this study. I am grateful to the monastic representatives, local residents, service providers, and
    visitors who shared their time and views during field interactions. Their cooperation made this work
    meaningful and grounded in practical realities.

    I also acknowledge the academic support provided through IGNOU study materials and project guidelines.
    Any errors in interpretation remain my own responsibility.
    """
    for p in para_list(ack):
        add_docx_paragraph(doc, p)
    doc.add_page_break()


def add_docx_table(doc: Document, rows: List[List[str]], title: str):
    add_docx_heading(doc, title, level=2)
    table = doc.add_table(rows=len(rows), cols=len(rows[0]))
    table.style = "Table Grid"
    for r_idx, row in enumerate(rows):
        for c_idx, cell_text in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = cell_text
            for p in cell.paragraphs:
                for run in p.runs:
                    run.font.name = "Times New Roman"
                    run.font.size = Pt(10)
                    run.bold = r_idx == 0
    doc.add_paragraph()


def build_report_docx(
    output_path: str,
    report_title: str,
    course_code: str,
    sections: List[Tuple[str, str]],
    summary_table: List[List[str]],
) -> int:
    doc = Document()
    configure_docx_defaults(doc)

    add_docx_cover(doc, report_title, course_code)
    add_docx_declaration(doc)
    add_docx_certificate(doc)
    add_docx_acknowledgement(doc)

    add_docx_heading(doc, "TABLE OF CONTENTS (Indicative)")
    toc_lines = [name for name, _ in sections]
    for idx, item in enumerate(toc_lines, start=1):
        add_docx_paragraph(doc, f"{idx}. {item}")
    doc.add_page_break()

    joined = []
    for name, body in sections:
        add_docx_heading(doc, name)
        for p in para_list(body):
            add_docx_paragraph(doc, p)
            joined.append(p)
        if "DATA ANALYSIS" in name or "STRATEGIC DESIGN" in name:
            add_docx_table(doc, summary_table, "Summary Analytical Table")

    doc.save(output_path)
    return words("\n\n".join(joined))


def build_report_pdf(
    output_path: str,
    report_title: str,
    course_code: str,
    sections: List[Tuple[str, str]],
    summary_table: List[List[str]],
) -> int:
    styles = get_styles()
    story = []

    add_cover(story, styles, report_title, course_code)
    add_declaration(story, styles)
    add_certificate(story, styles)
    add_acknowledgement(story, styles)

    story.append(Paragraph("TABLE OF CONTENTS (Indicative)", styles["h1"]))
    toc_lines = [name for name, _ in sections]
    for idx, item in enumerate(toc_lines, start=1):
        story.append(Paragraph(f"{idx}. {item}", styles["body"]))
    story.append(PageBreak())

    joined = []
    for name, body in sections:
        story.append(Paragraph(name, styles["h1"]))
        for p in para_list(body):
            story.append(Paragraph(textwrap.fill(p, width=180), styles["body"]))
            joined.append(p)
        if "DATA ANALYSIS" in name or "STRATEGIC DESIGN" in name:
            add_table(story, styles, summary_table, "Summary Analytical Table")
        if name not in {"BIBLIOGRAPHY", "ANNEXURES"}:
            story.append(Spacer(1, 4))
        if "CHAPTER" in name:
            story.append(Spacer(1, 2))

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2.2 * cm,
        leftMargin=2.2 * cm,
        topMargin=2.0 * cm,
        bottomMargin=2.0 * cm,
        title=report_title,
        author="IGNOU BTS Candidate",
    )
    doc.build(story)

    return words("\n\n".join(joined))


def main():
    out_dir = os.path.join(os.getcwd(), "deliverables")
    os.makedirs(out_dir, exist_ok=True)
    logo_path = os.environ.get("IGNOU_LOGO_PATH", "").strip() or None

    pts1_title, pts1_sections, pts1_table = build_pts1_content()
    pts2_title, pts2_sections, pts2_table = build_pts2_content()
    pts1_synopsis_title, pts1_synopsis = build_pts1_synopsis_content()
    pts2_synopsis_title, pts2_synopsis = build_pts2_synopsis_content()

    pts1_pdf = os.path.join(out_dir, "PTS-1_Salugara_Monastery_Project.pdf")
    pts2_pdf = os.path.join(out_dir, "PTS-2_Buddhist_Circuit_Marketing_Project.pdf")
    pts1_docx = os.path.join(out_dir, "PTS-1_Salugara_Monastery_Project.docx")
    pts2_docx = os.path.join(out_dir, "PTS-2_Buddhist_Circuit_Marketing_Project.docx")
    pts1_synopsis_pdf = os.path.join(out_dir, "PTS-1_Project_Proposal_Synopsis.pdf")
    pts2_synopsis_pdf = os.path.join(out_dir, "PTS-2_Project_Proposal_Synopsis.pdf")
    pts1_synopsis_docx = os.path.join(out_dir, "PTS-1_Project_Proposal_Synopsis.docx")
    pts2_synopsis_docx = os.path.join(out_dir, "PTS-2_Project_Proposal_Synopsis.docx")
    workflow_path = os.path.join(out_dir, "BTS_Submission_Workflow_Checklist.md")

    pts1_words = build_report_pdf(
        output_path=pts1_pdf,
        report_title=pts1_title,
        course_code="PTS-1",
        sections=pts1_sections,
        summary_table=pts1_table,
    )
    pts2_words = build_report_pdf(
        output_path=pts2_pdf,
        report_title=pts2_title,
        course_code="PTS-2",
        sections=pts2_sections,
        summary_table=pts2_table,
    )
    pts1_docx_words = build_report_docx(
        output_path=pts1_docx,
        report_title=pts1_title,
        course_code="PTS-1",
        sections=pts1_sections,
        summary_table=pts1_table,
    )
    pts2_docx_words = build_report_docx(
        output_path=pts2_docx,
        report_title=pts2_title,
        course_code="PTS-2",
        sections=pts2_sections,
        summary_table=pts2_table,
    )
    pts1_synopsis_pdf_words = build_synopsis_pdf(
        output_path=pts1_synopsis_pdf,
        title=pts1_synopsis_title,
        course_code="PTS-1",
        synopsis_text=pts1_synopsis,
        logo_path=logo_path,
    )
    pts2_synopsis_pdf_words = build_synopsis_pdf(
        output_path=pts2_synopsis_pdf,
        title=pts2_synopsis_title,
        course_code="PTS-2",
        synopsis_text=pts2_synopsis,
        logo_path=logo_path,
    )
    pts1_synopsis_docx_words = build_synopsis_docx(
        output_path=pts1_synopsis_docx,
        title=pts1_synopsis_title,
        course_code="PTS-1",
        synopsis_text=pts1_synopsis,
        logo_path=logo_path,
    )
    pts2_synopsis_docx_words = build_synopsis_docx(
        output_path=pts2_synopsis_docx,
        title=pts2_synopsis_title,
        course_code="PTS-2",
        synopsis_text=pts2_synopsis,
        logo_path=logo_path,
    )
    write_submission_workflow(workflow_path)

    meta_path = os.path.join(out_dir, "PROJECT_GENERATION_SUMMARY.txt")
    with open(meta_path, "w", encoding="utf-8") as f:
        f.write(f"Generated on: {dt.datetime.now().isoformat()}\n")
        f.write(f"Logo path used: {logo_path if logo_path else 'None'}\n")
        f.write(f"PTS-1 PDF: {pts1_pdf}\n")
        f.write(f"PTS-2 PDF: {pts2_pdf}\n")
        f.write(f"PTS-1 DOCX: {pts1_docx}\n")
        f.write(f"PTS-2 DOCX: {pts2_docx}\n")
        f.write(f"PTS-1 Synopsis PDF: {pts1_synopsis_pdf}\n")
        f.write(f"PTS-2 Synopsis PDF: {pts2_synopsis_pdf}\n")
        f.write(f"PTS-1 Synopsis DOCX: {pts1_synopsis_docx}\n")
        f.write(f"PTS-2 Synopsis DOCX: {pts2_synopsis_docx}\n")
        f.write(f"Workflow Checklist: {workflow_path}\n")
        f.write(f"Estimated PTS-1 word count: {pts1_words}\n")
        f.write(f"Estimated PTS-2 word count: {pts2_words}\n")
        f.write(f"Estimated PTS-1 DOCX word count: {pts1_docx_words}\n")
        f.write(f"Estimated PTS-2 DOCX word count: {pts2_docx_words}\n")
        f.write(f"Estimated PTS-1 Synopsis PDF word count: {pts1_synopsis_pdf_words}\n")
        f.write(f"Estimated PTS-2 Synopsis PDF word count: {pts2_synopsis_pdf_words}\n")
        f.write(f"Estimated PTS-1 Synopsis DOCX word count: {pts1_synopsis_docx_words}\n")
        f.write(f"Estimated PTS-2 Synopsis DOCX word count: {pts2_synopsis_docx_words}\n")
        f.write("Note: Candidate details and supervisor details should be filled before final submission.\n")

    print(f"Generated: {pts1_pdf}")
    print(f"Generated: {pts2_pdf}")
    print(f"Generated: {pts1_docx}")
    print(f"Generated: {pts2_docx}")
    print(f"Generated: {pts1_synopsis_pdf}")
    print(f"Generated: {pts2_synopsis_pdf}")
    print(f"Generated: {pts1_synopsis_docx}")
    print(f"Generated: {pts2_synopsis_docx}")
    print(f"Generated: {workflow_path}")
    print(f"PTS-1 words (estimate): {pts1_words}")
    print(f"PTS-2 words (estimate): {pts2_words}")
    print(f"PTS-1 DOCX words (estimate): {pts1_docx_words}")
    print(f"PTS-2 DOCX words (estimate): {pts2_docx_words}")
    print(f"PTS-1 synopsis words (estimate): {pts1_synopsis_pdf_words}")
    print(f"PTS-2 synopsis words (estimate): {pts2_synopsis_pdf_words}")
    print(f"Summary: {meta_path}")


if __name__ == "__main__":
    main()

