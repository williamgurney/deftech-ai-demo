"""
RIPA DDO Intelligence System - Streamlit Frontend
Russian Subject Tracking with Native Multilingual Processing
"""
import streamlit as st
import asyncio
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import cohere

from models_ripa import (
    RIPAIntercept, InterceptType, ClassificationLevel, ThreatLevel,
    RussianSubjectProfile, RussianNameVariation
)
from agent_russian_intel import RussianIntelAgent
from agent_ddo_planning import DDOPlanningAgent
from planet_geolocation import PlanetGeolocationService

# Load environment
load_dotenv()

# Page config
st.set_page_config(
    page_title="RIPA DDO Intelligence System",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .classification-banner {
        background-color: #dc2626;
        color: white;
        padding: 0.5rem;
        text-align: center;
        font-weight: bold;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    .russian-content {
        background-color: #f3f4f6;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #3b82f6;
        font-family: 'Courier New', monospace;
        direction: ltr;
    }
    .tradecraft-indicator {
        background-color: #fef3c7;
        padding: 0.5rem;
        border-radius: 5px;
        border-left: 3px solid #f59e0b;
        margin: 0.5rem 0;
    }
    .threat-high {
        color: #dc2626;
        font-weight: bold;
    }
    .threat-medium {
        color: #f59e0b;
        font-weight: bold;
    }
    .threat-low {
        color: #10b981;
        font-weight: bold;
    }
    .ddo-plan {
        background-color: #ecfdf5;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #10b981;
        margin: 1rem 0;
    }
    .risk-metric {
        background-color: #fee2e2;
        padding: 1rem;
        border-radius: 5px;
        text-align: center;
        margin: 0.5rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #3b82f6;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'cohere_client' not in st.session_state:
    api_key = os.getenv("COHERE_API_KEY")
    if api_key:
        st.session_state.cohere_client = cohere.ClientV2(api_key=api_key)
        st.session_state.russian_agent = RussianIntelAgent(st.session_state.cohere_client)
        st.session_state.ddo_planner = DDOPlanningAgent(st.session_state.cohere_client)
    else:
        st.session_state.cohere_client = None

if 'planet_service' not in st.session_state:
    st.session_state.planet_service = PlanetGeolocationService()

if 'intercepts' not in st.session_state:
    st.session_state.intercepts = []

if 'subject_profile' not in st.session_state:
    st.session_state.subject_profile = None

if 'ddo_plan' not in st.session_state:
    st.session_state.ddo_plan = None

if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = []

if 'geolocation_data' not in st.session_state:
    st.session_state.geolocation_data = None

if 'satellite_images' not in st.session_state:
    st.session_state.satellite_images = []

# Header
st.markdown("""
<div class="main-header">
    <h1>🔒 RIPA DDO Intelligence System</h1>
    <p>Russian Subject Tracking with Native Multilingual Processing</p>
    <p style="font-size: 0.9rem; opacity: 0.9;">Cohere Command-R+ | No Translation Layer</p>
</div>
""", unsafe_allow_html=True)

# Classification banner
st.markdown("""
<div class="classification-banner">
    ⚠️ CLASSIFICATION: SECRET | RIPA AUTHORIZED INTERCEPTS ONLY | OPERATIONAL SECURITY REQUIRED
</div>
""", unsafe_allow_html=True)

# Check API key
if not st.session_state.cohere_client:
    st.error("❌ COHERE_API_KEY not found. Please add it to your .env file.")
    st.stop()

# Sidebar
with st.sidebar:
    st.header("📋 System Controls")

    # Demo subject selector
    st.subheader("Demo Subject")
    demo_subject = st.selectbox(
        "Select Subject",
        ["Dmitry Alexandrovich Sokolov (FSB)", "Custom Subject"]
    )

    if demo_subject.startswith("Dmitry"):
        subject_id = "RUS_001"
        subject_name = "Dmitry Alexandrovich Sokolov"
        subject_aliases = ["Дмитрий Соколов", "Dima", "Митя", "D. Sokolov"]
        suspected_activity = "FSB intelligence officer"
        threat_level = ThreatLevel.HIGH
        ripa_auth = "RIPA/2025/DDO/0423"
    else:
        st.text_input("Subject ID", key="custom_id")
        st.text_input("Subject Name", key="custom_name")
        st.text_area("Aliases (one per line)", key="custom_aliases")
        subject_id = st.session_state.get("custom_id", "CUSTOM_001")
        subject_name = st.session_state.get("custom_name", "Unknown")
        subject_aliases = st.session_state.get("custom_aliases", "").split("\n")
        suspected_activity = st.text_input("Suspected Activity", "Unknown")
        threat_level = st.selectbox("Threat Level", [ThreatLevel.LOW, ThreatLevel.MEDIUM, ThreatLevel.HIGH, ThreatLevel.CRITICAL])
        ripa_auth = st.text_input("RIPA Authorization", "RIPA/2025/XXX/XXXX")

    st.divider()

    # Quick actions
    st.subheader("🚀 Quick Actions")

    if st.button("📥 Load Demo Intercepts"):
        # Load demo Russian intercepts
        demo_intercepts = [
            {
                'intercept_id': 'INT_001',
                'timestamp': datetime.now() - timedelta(days=1, hours=10),
                'type': InterceptType.PHONE_CALL,
                'platform': 'Mobile phone tap',
                'content': 'Встреча состоится завтра в старом месте. Принеси материалы. Окно с 15:00 до 16:00. Убедись что чистый.',
            },
            {
                'intercept_id': 'INT_002',
                'timestamp': datetime.now() - timedelta(hours=6),
                'type': InterceptType.TEXT_MESSAGE,
                'platform': 'WhatsApp',
                'content': 'Брат готов. Объект наблюдается. Передача завтра.',
            },
            {
                'intercept_id': 'INT_003',
                'timestamp': datetime.now() - timedelta(hours=2),
                'type': InterceptType.SOCIAL_MEDIA,
                'platform': 'VKontakte',
                'content': 'Сегодня встречаюсь со старым другом. Давно не виделись!',
            },
            {
                'intercept_id': 'INT_004',
                'timestamp': datetime.now() - timedelta(minutes=30),
                'type': InterceptType.PHONE_CALL,
                'platform': 'Mobile phone tap',
                'content': 'Точка чистая. Контакт подтверждён. Время не изменилось.',
            }
        ]

        st.session_state.intercepts = []
        for demo_int in demo_intercepts:
            intercept = RIPAIntercept(
                intercept_id=demo_int['intercept_id'],
                subject_id=subject_id,
                authorization_ref=ripa_auth,
                authorized_by="DCI Williams",
                authorization_date=datetime.now() - timedelta(days=30),
                expiry_date=datetime.now() + timedelta(days=60),
                intercept_type=demo_int['type'],
                collection_timestamp=demo_int['timestamp'],
                collection_method="lawful_intercept",
                content_language="Russian",
                raw_content=demo_int['content'],
                platform=demo_int['platform'],
                handling_classification=ClassificationLevel.SECRET
            )
            intercept.add_custody_event(
                action="collected",
                actor_id="SYS_001",
                actor_name="Intercept System",
                purpose="intelligence_collection",
                system="RIPA Intercept Platform"
            )
            st.session_state.intercepts.append(intercept)

        st.success(f"✅ Loaded {len(demo_intercepts)} Russian intercepts")

    if st.button("🔄 Clear All Data"):
        st.session_state.intercepts = []
        st.session_state.subject_profile = None
        st.session_state.ddo_plan = None
        st.session_state.analysis_results = []
        st.success("✅ All data cleared")

    st.divider()

    # System status
    st.subheader("📊 System Status")
    st.metric("Intercepts", len(st.session_state.intercepts))
    st.metric("Analyses", len(st.session_state.analysis_results))
    if st.session_state.subject_profile:
        st.success("✅ Profile Generated")
    if st.session_state.ddo_plan:
        st.success("✅ DDO Plan Ready")

# Main content tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📥 Intercepts",
    "🔍 Analysis",
    "👤 Subject Profile",
    "🎯 DDO Planning",
    "🛰️ Geolocation",
    "📚 Reference"
])

# Tab 1: Intercepts
with tab1:
    st.header("📥 RIPA-Authorized Intercepts")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Add New Intercept")

        with st.form("new_intercept"):
            int_id = st.text_input("Intercept ID", value=f"INT_{len(st.session_state.intercepts)+1:03d}")
            int_type = st.selectbox("Type", [InterceptType.PHONE_CALL, InterceptType.TEXT_MESSAGE, InterceptType.EMAIL, InterceptType.SOCIAL_MEDIA])
            platform = st.text_input("Platform", "Mobile phone tap")
            russian_content = st.text_area("Russian Content (Cyrillic)", placeholder="Введите русский текст здесь...")

            submitted = st.form_submit_button("Add Intercept")

            if submitted and russian_content:
                intercept = RIPAIntercept(
                    intercept_id=int_id,
                    subject_id=subject_id,
                    authorization_ref=ripa_auth,
                    authorized_by="DCI Williams",
                    authorization_date=datetime.now() - timedelta(days=30),
                    expiry_date=datetime.now() + timedelta(days=60),
                    intercept_type=int_type,
                    collection_timestamp=datetime.now(),
                    collection_method="lawful_intercept",
                    content_language="Russian",
                    raw_content=russian_content,
                    platform=platform,
                    handling_classification=ClassificationLevel.SECRET
                )
                intercept.add_custody_event(
                    action="collected",
                    actor_id="USER_001",
                    actor_name="Analyst",
                    purpose="intelligence_collection",
                    system="RIPA Web Interface"
                )
                st.session_state.intercepts.append(intercept)
                st.success(f"✅ Intercept {int_id} added")
                st.rerun()

    with col2:
        st.subheader("Quick Stats")
        st.metric("Total Intercepts", len(st.session_state.intercepts))
        if st.session_state.intercepts:
            types = [i.intercept_type.value for i in st.session_state.intercepts]
            st.write("**By Type:**")
            for t in set(types):
                st.write(f"- {t}: {types.count(t)}")

    # Display intercepts
    if st.session_state.intercepts:
        st.divider()
        st.subheader("📋 Collected Intercepts")

        for idx, intercept in enumerate(st.session_state.intercepts):
            with st.expander(f"{intercept.intercept_id} - {intercept.intercept_type.value} ({intercept.collection_timestamp.strftime('%Y-%m-%d %H:%M')})"):
                col1, col2 = st.columns([2, 1])

                with col1:
                    st.markdown(f"""
                    <div class="russian-content">
                    <strong>Russian Content:</strong><br>
                    {intercept.raw_content}
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    st.write(f"**Platform:** {intercept.platform}")
                    st.write(f"**Time:** {intercept.collection_timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
                    st.write(f"**Classification:** {intercept.handling_classification.value}")
                    st.write(f"**RIPA Auth:** {intercept.authorization_ref}")

                if st.button(f"🔍 Analyze {intercept.intercept_id}", key=f"analyze_{idx}"):
                    with st.spinner("Analyzing Russian intercept..."):
                        async def analyze():
                            return await st.session_state.russian_agent.analyze_russian_intercept(intercept)
                        result = asyncio.run(analyze())
                        st.session_state.analysis_results.append({
                            'intercept_id': intercept.intercept_id,
                            'result': result
                        })
                        st.success("✅ Analysis complete!")
                        st.rerun()

# Tab 2: Analysis
with tab2:
    st.header("🔍 Russian Intelligence Analysis")

    if not st.session_state.intercepts:
        st.info("📥 No intercepts to analyze. Load demo intercepts or add new ones in the Intercepts tab.")
    else:
        col1, col2 = st.columns([1, 1])

        with col1:
            if st.button("🔍 Analyze All Intercepts", type="primary"):
                with st.spinner("Analyzing Russian intercepts with Cohere Command-R+..."):
                    st.session_state.analysis_results = []
                    progress_bar = st.progress(0)

                    async def analyze_all():
                        results = []
                        for idx, intercept in enumerate(st.session_state.intercepts):
                            result = await st.session_state.russian_agent.analyze_russian_intercept(intercept)
                            results.append({
                                'intercept_id': intercept.intercept_id,
                                'result': result
                            })
                            progress_bar.progress((idx + 1) / len(st.session_state.intercepts))
                        return results

                    st.session_state.analysis_results = asyncio.run(analyze_all())
                    st.success(f"✅ Analyzed {len(st.session_state.analysis_results)} intercepts!")
                    st.rerun()

        with col2:
            if st.session_state.analysis_results and st.button("🕵️ Detect FSB Tradecraft"):
                with st.spinner("Detecting Russian tradecraft patterns..."):
                    progress_bar = st.progress(0)

                    async def detect_all():
                        for idx, intercept in enumerate(st.session_state.intercepts):
                            tradecraft = await st.session_state.russian_agent.detect_russian_tradecraft(
                                intercept.raw_content
                            )
                            # Add tradecraft to analysis results
                            for analysis in st.session_state.analysis_results:
                                if analysis['intercept_id'] == intercept.intercept_id:
                                    analysis['tradecraft'] = tradecraft
                            progress_bar.progress((idx + 1) / len(st.session_state.intercepts))

                    asyncio.run(detect_all())
                    st.success("✅ Tradecraft detection complete!")
                    st.rerun()

    # Display analysis results
    if st.session_state.analysis_results:
        st.divider()
        st.subheader("📊 Analysis Results")

        for analysis in st.session_state.analysis_results:
            with st.expander(f"📄 {analysis['intercept_id']} - Analysis", expanded=True):
                st.markdown(f"""
                <div class="russian-content">
                <strong>Original Russian:</strong><br>
                {analysis['result']['original_russian']}
                </div>
                """, unsafe_allow_html=True)

                st.markdown("---")
                st.markdown("**🔍 Intelligence Analysis:**")
                st.markdown(analysis['result']['analysis'])

                if 'tradecraft' in analysis:
                    st.markdown("---")
                    st.markdown("**🕵️ FSB/GRU Tradecraft Detection:**")
                    st.markdown(f"""
                    <div class="tradecraft-indicator">
                    {analysis['tradecraft']['tradecraft_analysis']}
                    </div>
                    """, unsafe_allow_html=True)

# Tab 3: Subject Profile
with tab3:
    st.header("👤 Russian Subject Profile")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader(f"Subject: {subject_name}")
        st.write(f"**Subject ID:** {subject_id}")
        st.write(f"**Aliases:** {', '.join(subject_aliases)}")
        st.write(f"**Suspected Activity:** {suspected_activity}")
        st.write(f"**Threat Level:** {threat_level.value}")
        st.write(f"**RIPA Authorization:** {ripa_auth}")

    with col2:
        if st.session_state.intercepts and st.button("🔨 Generate Profile", type="primary"):
            with st.spinner("Building comprehensive subject profile from Russian intercepts..."):
                async def build_profile():
                    return await st.session_state.russian_agent.analyze_russian_subject_profile(
                        subject_id=subject_id,
                        intercepts=st.session_state.intercepts
                    )

                profile = asyncio.run(build_profile())

                # Enhance with demo data
                profile.primary_name = subject_name
                profile.threat_level = threat_level
                profile.suspected_activity = suspected_activity
                profile.ripa_authorization = ripa_auth
                profile.violence_potential = 6
                profile.flight_risk = 7
                profile.evidence_destruction_risk = 8
                profile.operational_security_level = "PROFESSIONAL"
                profile.intelligence_background = True
                profile.organizational_affiliations = ["FSB"]

                st.session_state.subject_profile = profile
                st.success("✅ Profile generated!")
                st.rerun()

    if st.session_state.subject_profile:
        st.divider()

        # Risk metrics
        st.subheader("⚠️ Risk Assessment")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="risk-metric">
            <h3>{st.session_state.subject_profile.violence_potential}/10</h3>
            <p>Violence Potential</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="risk-metric">
            <h3>{st.session_state.subject_profile.flight_risk}/10</h3>
            <p>Flight Risk</p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="risk-metric">
            <h3>{st.session_state.subject_profile.evidence_destruction_risk}/10</h3>
            <p>Evidence Destruction</p>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="risk-metric">
            <h3>{st.session_state.subject_profile.operational_security_level}</h3>
            <p>OpSec Level</p>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # Comprehensive analysis
        st.subheader("📋 Comprehensive Intelligence Assessment")
        st.markdown(st.session_state.subject_profile.comprehensive_analysis)

        # Russian name variations
        if st.button("🔤 Generate Russian Name Variations"):
            with st.spinner("Generating all name variations..."):
                async def get_names():
                    return await st.session_state.russian_agent.cross_reference_russian_names(subject_name)

                name_vars = asyncio.run(get_names())
                st.markdown("**Russian Name Variations:**")
                st.write(f"- **Formal Full:** {name_vars.formal_full}")
                st.write(f"- **Given Name:** {name_vars.given_name}")
                st.write(f"- **Patronymic:** {name_vars.patronymic}")
                st.write(f"- **Surname:** {name_vars.surname}")

# Tab 4: DDO Planning
with tab4:
    st.header("🎯 Deliberate Detention Operation Planning")

    if not st.session_state.subject_profile:
        st.info("👤 Generate a subject profile first in the Subject Profile tab.")
    else:
        if st.button("⚡ Generate DDO Plan", type="primary"):
            with st.spinner("Generating comprehensive DDO operation plan..."):
                intelligence_summary = f"""
Russian intelligence officer {subject_name} under RIPA surveillance.

KEY INTELLIGENCE from {len(st.session_state.intercepts)} intercepts:
- Confirmed FSB operational language in communications
- High counter-surveillance awareness
- Contact with handler confirmed
- Intelligence handover activity detected

THREAT ASSESSMENT:
- Professional FSB officer
- High operational security
- Likely to destroy evidence if alerted
- Flight risk to Russia
- May be armed

IMMEDIATE OPERATIONAL REQUIREMENT:
Detention required for intelligence gathering and prosecution.
"""

                async def generate_plan():
                    return await st.session_state.ddo_planner.generate_detention_plan(
                        subject_profile=st.session_state.subject_profile,
                        intelligence_summary=intelligence_summary,
                        ripa_authorization=ripa_auth
                    )

                st.session_state.ddo_plan = asyncio.run(generate_plan())
                st.success("✅ DDO Plan generated!")
                st.rerun()

    if st.session_state.ddo_plan:
        plan = st.session_state.ddo_plan

        st.markdown(f"""
        <div class="ddo-plan">
        <h2>📋 DDO Plan: {plan.plan_id}</h2>
        <p><strong>Subject:</strong> {plan.subject_name}</p>
        <p><strong>Generated:</strong> {plan.generated_at.strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>Status:</strong> {'✅ READY FOR BRIEFING' if plan.briefing_ready else '⏳ In Progress'}</p>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # Detention Window
        st.subheader("🎯 Recommended Detention Window")
        window = plan.recommended_window

        col1, col2 = st.columns([2, 1])

        with col1:
            st.write(f"**Location:** {window.location.description}")
            st.write(f"**Location Type:** {window.location.location_type}")
            st.write(f"**Date/Time:** {window.datetime_start.strftime('%Y-%m-%d %H:%M')} to {window.datetime_end.strftime('%H:%M')}")
            st.write(f"**Rationale:** {window.recommendation}")

        with col2:
            st.metric("Overall Score", f"{window.overall_score}/100")
            st.metric("Confidence", f"{window.confidence_level*100:.0f}%")

        # Opportunity Scoring
        st.markdown("**📊 Opportunity Scoring:**")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Officer Safety", f"{window.officer_safety_score}/100")
        with col2:
            st.metric("Public Safety", f"{window.public_safety_score}/100")
        with col3:
            st.metric("Evidence Preservation", f"{window.evidence_preservation_score}/100")
        with col4:
            st.metric("Success Probability", f"{window.success_probability_score}/100")

        # Risks and Mitigation
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**⚠️ Risks:**")
            for risk in window.risks:
                st.write(f"- {risk}")

        with col2:
            st.markdown("**✓ Mitigation Strategies:**")
            for mitigation in window.mitigation_strategies:
                st.write(f"- {mitigation}")

        st.divider()

        # Risk Assessment
        st.subheader("⚠️ Risk Assessment")
        risk = plan.risk_assessment

        st.write(f"**Overall Risk Level:** {risk.overall_risk_level}")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Violence Potential", f"{risk.violence_potential}/10")
            st.metric("Escape Risk", f"{risk.escape_risk}/10")
        with col2:
            st.metric("Evidence Destruction", f"{risk.evidence_destruction_risk}/10")
            st.metric("Counter-Surveillance", f"{risk.counter_surveillance_awareness}/10")
        with col3:
            st.metric("Public Safety Risk", f"{risk.public_safety_risk}/10")
            st.metric("Officer Safety Risk", f"{risk.officer_safety_risk}/10")

        st.markdown("**⚡ Recommended Precautions:**")
        for precaution in risk.recommended_precautions:
            st.write(f"- {precaution}")

        st.divider()

        # Asset Requirements
        st.subheader("👮 Asset Requirements")
        assets = plan.asset_requirements

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Arrest Team", f"{assets.arrest_team_size} officers")
            st.metric("Search Team", f"{assets.search_team_size} officers")
        with col2:
            st.metric("Surveillance Team", f"{assets.surveillance_team_size} officers")
            st.write(f"**Armed Support:** {'✅ YES' if assets.armed_support_required else '❌ NO'}")
            if assets.armed_support_required:
                st.write(f"Armed Officers: {assets.armed_officers_count}")
        with col3:
            st.write(f"**Russian Interpreter:** {'✅ REQUIRED' if assets.russian_interpreter_required else '❌ Not required'}")
            st.write(f"**Digital Forensics:** {'✅ YES' if assets.digital_forensics else '❌ NO'}")
            st.write(f"**Faraday Bags:** {assets.cell_phone_faraday_bags}")

        st.divider()

        # Legal Compliance
        st.subheader("⚖️ Legal Compliance")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**RIPA Authorization:** {plan.ripa_authorization}")
            st.write(f"**Arrest Authority:** {plan.arrest_authority}")
            st.write(f"**Search Warrant:** {'✅ REQUIRED' if plan.search_warrant_required else '❌ Not required'}")
        with col2:
            st.write(f"**Consular Notification:** {'✅ REQUIRED - Russian Embassy' if plan.consular_notification_required else '❌ Not required'}")
            if plan.consular_notification_required:
                st.write(f"**Timing:** {plan.consular_notification_timing}")

        st.divider()

        # Operational Summary
        st.subheader("📄 Operational Order")
        with st.expander("View Full Operational Summary", expanded=False):
            st.markdown(plan.operational_summary)

        # Expected Evidence
        st.subheader("🔍 Expected Evidence")
        for evidence in plan.expected_evidence_types:
            st.write(f"- {evidence}")

        st.write(f"**Evidence Preservation Plan:** {plan.evidence_preservation_plan}")

# Tab 5: Geolocation
with tab5:
    st.header("🛰️ Planet Labs Satellite Geolocation")

    st.markdown("""
    **Satellite Intelligence for DDO Operations**

    Integration with Planet Labs provides:
    - Satellite imagery search and analysis
    - DDO area suitability assessment
    - Subject movement tracking
    - Points of interest identification
    """)

    # API Key status
    planet_api_key = os.getenv("PLANET_API_KEY")
    if planet_api_key:
        st.success("✅ Planet API Key configured - Real satellite data available")
    else:
        st.info("ℹ️ Running in Demo Mode - No Planet API key detected. Generating simulated satellite data.")

    st.divider()

    # Location input
    st.subheader("📍 Location Intelligence")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.write("**Enter target location:**")

        use_demo = st.checkbox("Use demo location (Manchester)", value=True)

        if use_demo:
            latitude = 53.4808
            longitude = -2.2426
            location_name = "Subject residence - Manchester"
        else:
            latitude = st.number_input("Latitude", value=53.4808, format="%.6f")
            longitude = st.number_input("Longitude", value=-2.2426, format="%.6f")
            location_name = st.text_input("Location Name", "Target location")

    with col2:
        st.write("**Quick Stats:**")
        if st.session_state.geolocation_data:
            st.metric("Confidence", f"{st.session_state.geolocation_data.confidence*100:.0f}%")
            st.metric("Satellite Images", len(st.session_state.geolocation_data.satellite_images))

    # Get satellite intelligence
    if st.button("🛰️ Get Satellite Intelligence", type="primary"):
        with st.spinner("Searching Planet Labs satellite imagery..."):
            intel = st.session_state.planet_service.get_location_intelligence(
                latitude=latitude,
                longitude=longitude,
                location_name=location_name,
                subject_id="TARGET"
            )
            st.session_state.geolocation_data = intel
            st.session_state.satellite_images = intel.satellite_images
            st.success(f"✅ Found {len(intel.satellite_images)} satellite images!")
            st.rerun()

    # Display satellite imagery results
    if st.session_state.satellite_images:
        st.divider()
        st.subheader("🛰️ Satellite Imagery")

        for img in st.session_state.satellite_images:
            with st.expander(f"📷 {img.image_id} - {img.acquisition_time.strftime('%Y-%m-%d %H:%M')}"):
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Acquisition Date", img.acquisition_time.strftime('%Y-%m-%d'))
                    st.metric("Cloud Cover", f"{img.cloud_cover*100:.1f}%")

                with col2:
                    st.metric("Resolution (GSD)", f"{img.ground_sample_distance}m")
                    st.metric("Satellite", img.satellite)

                with col3:
                    if img.thumbnail_url:
                        st.write(f"[View Thumbnail]({img.thumbnail_url})")
                    st.write(f"**BBox:** {img.bbox[:2]}")

    # Display geolocation intelligence
    if st.session_state.geolocation_data:
        intel = st.session_state.geolocation_data

        st.divider()
        st.subheader("📊 Geolocation Intelligence Package")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.write(f"**Location:** {intel.latitude:.6f}, {intel.longitude:.6f}")
            st.write(f"**Timestamp:** {intel.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            st.write(f"**Source:** {intel.source}")

        with col2:
            st.metric("Intelligence Confidence", f"{intel.confidence*100:.0f}%")

        # Points of Interest
        if intel.points_of_interest:
            st.divider()
            st.subheader("📍 Points of Interest")

            for poi in intel.points_of_interest:
                with st.expander(f"🎯 {poi['type'].upper()} - {poi['distance_meters']}m"):
                    st.write(f"**Description:** {poi['description']}")
                    st.write(f"**Visibility:** {poi['visibility']}")
                    st.write(f"**Access Points:** {poi['access_points']}")
                    st.progress(poi['confidence'], text=f"Confidence: {poi['confidence']*100:.0f}%")

        # DDO Area Assessment
        if intel.area_assessment:
            st.divider()
            st.subheader("🎯 DDO Area Assessment")

            assessment = intel.area_assessment

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("**Exposure & Density:**")
                st.write(f"- Public Exposure: **{assessment.get('public_exposure_level', 'N/A').upper()}**")
                st.write(f"- Crowd Density: **{assessment.get('crowd_density', 'N/A').upper()}**")
                st.write(f"- Visibility: **{assessment.get('visibility_from_main_road', 'N/A')}**")

            with col2:
                st.markdown("**Operational Factors:**")
                st.write(f"- Officer Approach: **{assessment.get('officer_approach_difficulty', 'N/A')}**")
                st.write(f"- Subject Escape: **{assessment.get('subject_escape_difficulty', 'N/A')}**")
                st.write(f"- Evidence Environment: **{assessment.get('evidence_preservation_environment', 'N/A')}**")

            with col3:
                st.markdown("**Intelligence Quality:**")
                st.write(f"- Satellite Coverage: **{assessment.get('satellite_coverage', 'N/A')}**")
                st.write(f"- Imagery Quality: **{assessment.get('imagery_quality', 'N/A')}**")

            st.markdown("---")

            st.markdown("**🎯 Operational Recommendation:**")
            st.info(assessment.get('operational_recommendation', 'N/A'))

            st.markdown("**⏰ Best Time Window:**")
            st.success(assessment.get('best_time_window', 'N/A'))

            # Officer Positioning
            if 'officer_positioning' in assessment:
                st.markdown("**👮 Officer Positioning:**")
                for position in assessment['officer_positioning']:
                    st.write(f"- {position}")

        # Route Analysis
        if intel.route_analysis:
            st.divider()
            st.subheader("🛣️ Route Analysis")

            routes = intel.route_analysis

            st.write(f"**Primary Access:** {routes.get('primary_access', 'N/A')}")

            if 'escape_routes' in routes:
                st.markdown("**Escape Routes:**")
                for route in routes['escape_routes']:
                    st.write(f"- {route['direction'].upper()}: {route['distance_km']}km ({route['type']})")

            if 'chokepoints' in routes:
                st.markdown("**Chokepoints:**")
                for cp in routes['chokepoints']:
                    controllable = "✅ Controllable" if cp['controllable'] else "⚠️ Not controllable"
                    st.write(f"- {cp['location']}: {controllable}")

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Nearest Police Station", f"{routes.get('nearest_police_station_km', 'N/A')} km")
            with col2:
                st.metric("Nearest Hospital", f"{routes.get('nearest_hospital_km', 'N/A')} km")

    # Live Location Data
    st.divider()
    st.subheader("📡 Create Live Location Data")

    if st.button("📡 Generate RIPA Live Location"):
        if st.session_state.geolocation_data:
            live_data = st.session_state.planet_service.create_live_location_data(
                latitude=latitude,
                longitude=longitude,
                location_name=location_name,
                location_type="residence"
            )

            st.success("✅ Live location data created with satellite intelligence!")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Accuracy", f"{live_data.accuracy_meters}m")
            with col2:
                st.metric("Collection Method", live_data.collection_method)
            with col3:
                st.metric("Satellite Images", live_data.satellite_images_available)

            st.write(f"**Location:** {live_data.location_description}")
            st.write(f"**Address:** {live_data.address}")
            st.write(f"**RIPA Authorized:** {'✅ Yes' if live_data.ripa_authorized else '❌ No'}")
            st.write(f"**Authorization Ref:** {live_data.authorization_ref}")
        else:
            st.warning("⚠️ Please get satellite intelligence first!")

# Tab 6: Reference
with tab6:
    st.header("📚 Russian Tradecraft Reference")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🕵️ FSB/GRU Operational Terms")
        terms = {
            "встреча": "meeting - Operational meeting",
            "объект": "object - Surveillance target",
            "материалы": "materials - Intelligence documents",
            "передача": "handover - Intelligence transmission",
            "точка": "point - Location/dead drop",
            "окно": "window - Operational time window",
            "чистый": "clean - Counter-surveillance clear",
            "хвост": "tail - Surveillance detection",
            "контакт": "contact - Agent contact",
            "брат": "brother - Operative/contact"
        }

        for russian, english in terms.items():
            st.markdown(f"**{russian}** - {english}")

    with col2:
        st.subheader("🔴 Criminal Organization Terms")
        criminal_terms = {
            "братва": "brotherhood - Gang/organization",
            "решать вопросы": "solve problems - Violence euphemism",
            "крыша": "roof - Protection/extortion",
            "наезд": "pressure - Intimidation",
            "откат": "kickback - Bribe",
            "разборка": "showdown - Confrontation"
        }

        for russian, english in criminal_terms.items():
            st.markdown(f"**{russian}** - {english}")

    st.divider()

    st.subheader("📖 About This System")
    st.markdown("""
    ### Key Innovation: No Translation Layer

    Unlike traditional systems that translate Russian → English → Analysis, this system
    analyzes Russian content **directly** using Cohere's Command-R+ multilingual capabilities.

    **Benefits:**
    - Preserves cultural context and nuance
    - Detects FSB/GRU tradecraft patterns
    - Understands Russian idioms and code words
    - Maintains operational accuracy
    - Faster processing (no translation step)

    ### RIPA Compliance

    All intercepts are processed under the Regulation of Investigatory Powers Act 2000:
    - Full chain of custody tracking
    - RIPA authorization on every intercept
    - Audit trail for all actions
    - Court-ready evidence packages
    - Defense disclosure support

    ### Technical Stack

    - **LLM:** Cohere Command-R+ (multilingual)
    - **Embeddings:** Cohere Embed v3 (1024 dimensions)
    - **Framework:** Python 3.9+, Streamlit
    - **Language Processing:** Native Russian (no translation)
    """)

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #6b7280; font-size: 0.875rem; padding: 1rem;">
    <p>RIPA DDO Intelligence System | Powered by Cohere Command-R+ | Classification: SECRET</p>
    <p>🤖 Built with Claude Code | For authorized law enforcement use only</p>
</div>
""", unsafe_allow_html=True)
