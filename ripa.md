# Project: RIPA DDO Intelligence System - Russian Subject Tracking with Native Multilingual Processing

## Mission Context

Build an intelligence system to support a **Deliberate Detention Operation (DDO)** under RIPA (Regulation of Investigatory Powers Act) targeting a Russian subject. The system must process Russian-language intelligence WITHOUT translation, using Cohere's Command-R multilingual capabilities to understand and analyze content in native Russian while providing English operational outputs.

## Critical Legal/Operational Requirements

### RIPA Compliance
- All intercepts must be logged with RIPA authorization details
- Maintain chain of custody for all intelligence
- Timestamp and attribute every data collection action
- Generate audit trail for legal review
- Support necessity/proportionality assessments
- Enable redaction for court disclosure

### DDO Operational Requirements
- **Pre-detention intelligence**: Build comprehensive subject profile
- **Timing intelligence**: Predict optimal detention window
- **Location intelligence**: Identify best detention location (minimal public exposure)
- **Asset coordination**: Position arrest teams, surveillance, support units
- **Evidence package**: Generate prosecution-ready intelligence brief
- **Risk assessment**: Threat to officers, escape risk, evidence destruction risk

## Enhanced Architecture: Multilingual-First Design

### Key Difference from Previous Design

**OLD APPROACH** (Don't do this):
```
Russian text → Translation API → English text → Analysis
PROBLEMS: 
- Loses nuance and context
- Misses cultural references
- Mistranslates idioms/code words
- Adds latency
```

**NEW APPROACH** (Do this):
```
Russian text → Cohere Command-R (multilingual) → Analysis in Russian context → English operational output
BENEFITS:
- Preserves original meaning
- Understands Russian cultural context
- Detects Russian-specific patterns
- Identifies Cyrillic variations
- Maintains operational speed
```

## Core Components

### 1. RIPA-Compliant Data Layer

#### Intercept Management System
```python
class RIPAIntercept:
    intercept_id: str              # Unique identifier
    authorization_ref: str         # RIPA warrant reference
    authorized_by: str             # Authorizing officer
    authorization_date: datetime   # Warrant issue date
    expiry_date: datetime         # Warrant expiry
    target_subject: str           # Subject ID
    intercept_type: str           # phone, email, social_media, physical
    content_language: str         # Russian, English, mixed
    raw_content: str              # Original content (Cyrillic preserved)
    collection_timestamp: datetime
    collection_method: str        # telecom_tap, social_scrape, etc.
    handling_classification: str  # SECRET, TOP SECRET
    disclosed_to_defense: bool    # For court proceedings
    redaction_required: bool
    chain_of_custody: List[CustodyEvent]
    
class CustodyEvent:
    timestamp: datetime
    action: str                   # collected, accessed, analyzed, exported
    actor_id: str                # analyst ID
    purpose: str                 # investigation, briefing, court
    system_used: str             # which agent/tool
```

#### Russian Language Intelligence Store
- Separate indexes for Russian vs English documents
- Preserve Cyrillic characters throughout pipeline
- Metadata includes: language, dialect detection, cultural context flags
- Special handling for:
  - Mixed Russian/English communications
  - Transliterated Russian (Latin alphabet)
  - Russian abbreviations and slang
  - Code words in Russian intelligence tradecraft

### 2. Cohere Multilingual Integration

#### Command-R Multilingual Setup
```python
class MultilingualIntelligenceEngine:
    """
    Uses Cohere Command-R for native Russian understanding
    NO translation layer
    """
    
    def __init__(self):
        self.co = cohere.Client(api_key=COHERE_API_KEY)
        
    async def analyze_russian_intercept(self, intercept: RIPAIntercept):
        """
        Analyze Russian content directly without translation
        """
        
        prompt = f"""
        Ты работаешь как аналитик разведки, анализирующий перехваченное сообщение.
        (You are working as an intelligence analyst analyzing an intercepted communication.)
        
        ПЕРЕХВАЧЕННОЕ СООБЩЕНИЕ / INTERCEPTED MESSAGE:
        {intercept.raw_content}
        
        ЗАДАЧИ АНАЛИЗА / ANALYSIS TASKS:
        1. Определить тип сообщения (operational, personal, business)
        2. Извлечь ключевую информацию: места, времена, люди, планы
        3. Оценить оперативную значимость (LOW/MEDIUM/HIGH/CRITICAL)
        4. Выявить кодовые слова или эвфемизмы
        5. Определить эмоциональное состояние отправителя
        6. Оценить связь с известными преступными/разведывательными сетями
        
        IMPORTANT: 
        - Analyze in Russian context (understand cultural references)
        - Identify Russian intelligence tradecraft indicators
        - Flag Russian state actor language patterns
        - Detect Russian criminal argot (блатная музыка)
        
        Provide analysis in ENGLISH for operational use, but preserve Russian 
        phrases where culturally significant. Include confidence scores.
        """
        
        response = await self.co.chat(
            message=prompt,
            model='command-r-plus',  # Multilingual model
            temperature=0.3
        )
        
        return {
            'original_russian': intercept.raw_content,
            'analysis': response.text,
            'language': 'Russian',
            'cultural_context_preserved': True,
            'requires_translation': False
        }
    
    async def cross_reference_russian_names(self, name: str):
        """
        Handle Russian name variations WITHOUT translation
        Understands: patronymics, diminutives, formal/informal
        """
        
        prompt = f"""
        Russian Name Analysis Task:
        
        Given name: {name}
        
        Identify all possible variations:
        1. Formal full name (Иван Петрович Сидоров)
        2. Informal variations (Ваня, Ванечка, Иванушка)
        3. Patronymic forms
        4. Common transliterations (Ivan, Iwan, Evan)
        5. Nickname possibilities
        6. Surname variations (different endings)
        
        Consider:
        - Regional variations (Moscow vs. regions)
        - Historical Soviet naming patterns
        - Criminal underworld nicknames
        - Intelligence officer aliases
        
        Return ALL possible variations this person might use or be known by.
        """
        
        response = await self.co.chat(
            message=prompt,
            model='command-r-plus'
        )
        
        return response.text
    
    async def detect_russian_tradecraft(self, content: str):
        """
        Identify Russian intelligence/criminal tradecraft patterns
        """
        
        prompt = f"""
        Russian Intelligence Tradecraft Analysis:
        
        Content: {content}
        
        Analyze for indicators of:
        1. FSB/GRU operational language patterns
        2. Russian criminal organization communication styles
        3. Dead drop arrangements (Russian style)
        4. Surveillance detection route descriptions
        5. Handler/agent communication protocols
        6. Russian counter-intelligence awareness
        7. Use of Soviet-era intelligence terminology
        
        Known Russian intelligence indicators:
        - Time/location specification patterns
        - Meeting arrangement euphemisms
        - Document exchange terminology
        - Emergency protocol language
        - Exfiltration planning phrases
        
        Provide threat assessment and operational recommendations.
        """
        
        response = await self.co.chat(
            message=prompt,
            model='command-r-plus',
            temperature=0.2  # Lower temp for pattern recognition
        )
        
        return response.text
```

### 3. DDO-Specific Agents

#### DDO Planning Agent
```python
class DDOPlanningAgent:
    """
    Generates detention operation plans
    """
    
    async def generate_detention_plan(
        self, 
        subject_profile: SubjectProfile,
        intelligence_package: IntelligencePackage
    ):
        """
        Create comprehensive DDO plan
        """
        
        # Analyze subject's current pattern of life
        current_pattern = await self.temporal_agent.analyze_current_pattern(
            subject_profile.id
        )
        
        # Predict optimal detention windows
        detention_opportunities = await self.predict_detention_windows(
            current_pattern,
            intelligence_package
        )
        
        # Generate operational plan
        plan_prompt = f"""
        Deliberate Detention Operation Planning:
        
        SUBJECT: {subject_profile.name}
        NATIONALITY: Russian
        THREAT LEVEL: {subject_profile.threat_level}
        RIPA AUTHORIZATION: {intelligence_package.ripa_ref}
        
        INTELLIGENCE SUMMARY:
        {intelligence_package.summary}
        
        CURRENT PATTERN OF LIFE:
        {current_pattern}
        
        PREDICTED DETENTION OPPORTUNITIES:
        {detention_opportunities}
        
        GENERATE DDO PLAN INCLUDING:
        
        1. RECOMMENDED DETENTION WINDOW
           - Date/time with rationale
           - Confidence level
           - Alternative windows (backup plans)
        
        2. OPTIMAL DETENTION LOCATION
           - Minimize public exposure
           - Maximize officer safety
           - Prevent evidence destruction
           - Consider: home, vehicle, public location
        
        3. ASSET REQUIREMENTS
           - Arrest team size
           - Armed support (threat-dependent)
           - Search team (evidence seizure)
           - Surveillance (approach monitoring)
           - Interview team (Russian speakers)
           - Technical support (phone/computer seizure)
        
        4. RISK ASSESSMENT
           - Subject violence potential: [score]
           - Escape risk: [score]
           - Evidence destruction risk: [score]
           - Counter-surveillance awareness: [score]
           - Public safety risk: [score]
        
        5. CONTINGENCY PLANS
           - If subject deviates from pattern
           - If subject attempts escape
           - If subject destroys evidence
           - If additional subjects present
        
        6. LEGAL REQUIREMENTS
           - RIPA compliance checklist
           - Arrest authority
           - Search warrant requirements
           - Interview under caution
           - Consular notification (Russian embassy)
        
        7. EVIDENCE PRESERVATION
           - Phone seizure protocol (prevent remote wipe)
           - Document handling
           - Digital evidence chain of custody
           - Russian language material handling
        
        Generate detailed operational order suitable for briefing arrest teams.
        """
        
        response = await self.co.chat(
            message=plan_prompt,
            model='command-r-plus'
        )
        
        return DDOPlan(
            subject_id=subject_profile.id,
            plan_text=response.text,
            recommended_window=detention_opportunities[0],
            risk_score=self.calculate_overall_risk(intelligence_package),
            ripa_compliant=True,
            generated_at=datetime.now()
        )
    
    async def predict_detention_windows(
        self,
        current_pattern: PatternAnalysis,
        intelligence: IntelligencePackage
    ) -> List[DetentionWindow]:
        """
        Identify optimal times/locations for detention
        """
        
        # Analyze subject's routine
        routine_locations = current_pattern.frequent_locations
        routine_times = current_pattern.typical_schedule
        
        # Score each opportunity
        opportunities = []
        
        for location in routine_locations:
            for time_window in routine_times:
                score = self.score_detention_opportunity(
                    location=location,
                    time=time_window,
                    intelligence=intelligence
                )
                
                opportunities.append(DetentionWindow(
                    location=location,
                    time_window=time_window,
                    score=score,
                    rationale=score.reasoning
                ))
        
        # Sort by score, return top 5
        return sorted(opportunities, key=lambda x: x.score.total, reverse=True)[:5]
    
    def score_detention_opportunity(
        self,
        location: Location,
        time: TimeWindow,
        intelligence: IntelligencePackage
    ) -> OpportunityScore:
        """
        Score detention opportunity on multiple factors
        """
        
        scoring_prompt = f"""
        Score this detention opportunity:
        
        LOCATION: {location.description}
        - Type: {location.type}  # home, vehicle, public_place, workplace
        - Public exposure: {location.crowd_level}
        - Officer access: {location.access_difficulty}
        - Escape routes: {location.escape_routes}
        
        TIME: {time.start} - {time.end}
        - Subject typically: {time.subject_activity}
        - Likelihood of being alone: {time.alone_probability}
        - Predictability: {time.pattern_confidence}
        
        INTELLIGENCE FACTORS:
        - Subject awareness of surveillance: {intelligence.counter_surveillance_score}
        - Evidence at location: {intelligence.evidence_likely}
        - Associated subjects: {intelligence.associates_present}
        
        Score 0-100 on:
        1. Officer safety (weight: 40%)
        2. Public safety (weight: 25%)
        3. Evidence preservation (weight: 20%)
        4. Operational success probability (weight: 15%)
        
        Provide: Overall score, breakdown, and operational recommendation.
        """
        
        # Use Cohere to generate sophisticated scoring
        response = self.co.chat(
            message=scoring_prompt,
            model='command-r-plus'
        )
        
        return OpportunityScore.from_analysis(response.text)
```

#### Russian Intelligence Analysis Agent
```python
class RussianIntelAgent(LanguageIntelAgent):
    """
    Specialized for Russian subject analysis
    NO TRANSLATION - Native Russian processing
    """
    
    async def analyze_russian_subject_profile(
        self,
        subject_id: str,
        intercepts: List[RIPAIntercept]
    ):
        """
        Build comprehensive profile from Russian-language intelligence
        """
        
        # Collect all Russian content
        russian_content = [
            i.raw_content for i in intercepts 
            if i.content_language == 'Russian'
        ]
        
        analysis_prompt = f"""
        Comprehensive Russian Subject Analysis:
        
        SUBJECT ID: {subject_id}
        INTERCEPTS ANALYZED: {len(russian_content)}
        
        RUSSIAN LANGUAGE INTERCEPTS:
        {chr(10).join(russian_content)}
        
        ANALYZE FOR:
        
        1. IDENTITY INDICATORS
           - Full name variations used
           - Patronymic (отчество)
           - Nicknames and informal names
           - Surnames and aliases
           - Document names vs. street names
        
        2. ORIGIN AND BACKGROUND
           - Regional dialect markers (Moscow, Petersburg, regional)
           - Education level (vocabulary sophistication)
           - Military/intelligence background indicators
           - Soviet-era terminology usage
           - Social class indicators
        
        3. NETWORK AND RELATIONSHIPS
           - Associates mentioned by name
           - Nature of relationships (handler, accomplice, contact)
           - Organizational affiliations (FSB, GRU, criminal groups)
           - Family connections
           - Operational relationships
        
        4. OPERATIONAL INDICATORS
           - Intelligence tradecraft language
           - Operational security awareness
           - Communication patterns (when, how often, with whom)
           - Stress or urgency indicators
           - Deception indicators
        
        5. BEHAVIORAL ASSESSMENT
           - Personality traits from language use
           - Emotional state
           - Risk tolerance
           - Professionalism level
           - Likelihood of violence
           - Cooperation potential (post-arrest)
        
        6. THREAT ASSESSMENT
           - Espionage indicators
           - Criminal activity indicators
           - Violence potential
           - Network danger level
           - State actor connections
        
        7. DETENTION CONSIDERATIONS
           - Flight risk assessment
           - Evidence destruction risk
           - Resistance likelihood
           - Interview strategy recommendations
           - Russian consular notification requirements
        
        Provide comprehensive intelligence brief in ENGLISH for operational use.
        Include Russian phrases only where culturally/operationally significant.
        Flag HIGH PRIORITY items for immediate operational attention.
        """
        
        response = await self.co.chat(
            message=analysis_prompt,
            model='command-r-plus',
            temperature=0.3
        )
        
        return RussianSubjectProfile(
            subject_id=subject_id,
            comprehensive_analysis=response.text,
            language='Russian',
            intercepts_analyzed=len(russian_content),
            native_processing=True,  # No translation used
            generated_at=datetime.now()
        )
    
    async def detect_russian_operational_language(self, text: str):
        """
        Identify if Russian text contains intelligence operational language
        """
        
        prompt = f"""
        Russian Operational Language Detection:
        
        Text: {text}
        
        Analyze for Russian intelligence/security service terminology:
        
        FSB/GRU INDICATORS:
        - "встреча" (meeting) in operational context
        - "объект" (object/target)
        - "контакт" (contact/agent)
        - "материал" (material/intelligence)
        - "передача" (handover/transmission)
        - "точка" (point/location)
        - "окно" (window - time window)
        - "чистый" (clean - counter-surveillance clear)
        
        CRIMINAL/MAFIA INDICATORS:
        - "братва" (brotherhood/gang)
        - "решать вопросы" (solve problems - code for violence)
        - "крыша" (roof - protection)
        - "наезд" (pressure/intimidation)
        - "откат" (kickback)
        
        TEMPORAL INDICATORS:
        - Unusual time specifications
        - Countdown language
        - Deadline urgency
        
        LOCATION INDICATORS:
        - "старое место" (old place - dead drop)
        - "наше место" (our place)
        - Numbered locations
        
        Return:
        - Operational language: YES/NO
        - Confidence: 0-100
        - Specific indicators found
        - Context interpretation
        - Threat level: LOW/MEDIUM/HIGH/CRITICAL
        """
        
        response = await self.co.chat(
            message=prompt,
            model='command-r-plus'
        )
        
        return response.text
```

### 4. DDO Evidence Package Generator
```python
class DDOEvidencePackage:
    """
    Generates prosecution-ready intelligence packages
    RIPA-compliant, court-disclosable
    """
    
    async def generate_evidence_package(
        self,
        subject_id: str,
        detention_date: datetime
    ):
        """
        Create comprehensive evidence package for prosecution
        """
        
        # Gather all RIPA-authorized intelligence
        intercepts = await self.get_ripa_intercepts(subject_id)
        surveillance_logs = await self.get_surveillance_logs(subject_id)
        osint = await self.get_osint_package(subject_id)
        
        # Timeline of subject's activities
        timeline = await self.temporal_agent.build_evidence_timeline(
            subject_id=subject_id,
            end_date=detention_date
        )
        
        # Russian language analysis (preserve originals)
        russian_analysis = await self.russian_intel_agent.analyze_all_intercepts(
            intercepts=intercepts
        )
        
        package_prompt = f"""
        Generate PROSECUTION EVIDENCE PACKAGE:
        
        SUBJECT: [Subject details]
        DETENTION DATE: {detention_date}
        INVESTIGATION PERIOD: [Start] to {detention_date}
        
        RIPA AUTHORIZATIONS:
        {[i.authorization_ref for i in intercepts]}
        
        EVIDENCE CATEGORIES:
        
        1. INTERCEPT EVIDENCE (RIPA-compliant)
           {len(intercepts)} intercepts
           - Russian language communications (originals preserved)
           - English operational summaries
           - Chain of custody documentation
           - RIPA necessity/proportionality justification
        
        2. SURVEILLANCE EVIDENCE
           {len(surveillance_logs)} surveillance logs
           - Physical surveillance observations
           - CCTV captures
           - Location tracking (RIPA-authorized)
        
        3. OPEN SOURCE INTELLIGENCE
           - Social media activity
           - Public records
           - Travel records
        
        4. TIMELINE OF ACTIVITIES
           {timeline}
        
        5. RUSSIAN INTELLIGENCE ANALYSIS
           {russian_analysis}
        
        GENERATE:
        
        A. EXECUTIVE SUMMARY
           - Threat posed by subject
           - Key evidence highlights
           - Recommended charges
        
        B. DETAILED CHRONOLOGY
           - Date/time stamped activities
           - Source attribution for each item
           - Russian communications with translations (where provided)
        
        C. NETWORK ANALYSIS
           - Associates identified
           - Organizational connections
           - Russian state actor links (if any)
        
        D. LEGAL COMPLIANCE
           - RIPA authorization for each intercept
           - Necessity/proportionality assessment
           - Disclosure requirements
           - Defense disclosure package
        
        E. INTERVIEW STRATEGY
           - Key questions based on intelligence
           - Evidence to confront subject with
           - Russian language requirements (interpreter)
           - Anticipated defense arguments
        
        F. APPENDICES
           - Original Russian intercepts (Cyrillic)
           - English translations (where applicable)
           - Surveillance photos
           - Maps and timelines
           - Technical analysis reports
        
        Format: Prosecution-ready, court-disclosable, RIPA-compliant.
        """
        
        response = await self.co.chat(
            message=package_prompt,
            model='command-r-plus'
        )
        
        return EvidencePackage(
            subject_id=subject_id,
            generated_at=datetime.now(),
            detention_date=detention_date,
            content=response.text,
            intercepts_included=len(intercepts),
            ripa_compliant=True,
            court_ready=True,
            russian_content_preserved=True
        )
```

### 5. Demo Scenario: Russian Subject DDO
```python
# Complete demo scenario showing multilingual capabilities

DEMO_SUBJECT = {
    'id': 'RUS_001',
    'name': 'Dmitry Alexandrovich Sokolov',
    'aliases': ['Дмитрий Соколов', 'Dima', 'Митя', 'D. Sokolov'],
    'nationality': 'Russian',
    'threat_level': 'HIGH',
    'suspected_activity': 'Intelligence officer, FSB',
    'ripa_authorization': 'RIPA/2025/DDO/0423'
}

DEMO_INTERCEPTS = [
    {
        'timestamp': '2025-10-20 14:23:00',
        'type': 'phone_call',
        'language': 'Russian',
        'content': '''
        Встреча состоится завтра в старом месте. Принеси материалы.
        Окно с 15:00 до 16:00. Убедись что чистый.
        ''',
        'translation_note': 'Operational language detected'
    },
    {
        'timestamp': '2025-10-20 18:45:00',
        'type': 'text_message',
        'language': 'Russian',
        'content': '''
        Брат готов. Объект наблюдается. Передача завтра.
        ''',
        'translation_note': 'FSB tradecraft indicators'
    },
    {
        'timestamp': '2025-10-21 09:15:00',
        'type': 'social_media',
        'platform': 'VKontakte',
        'language': 'Russian',
        'content': '''
        Сегодня встречаюсь со старым другом. Давно не виделись!
        ''',
        'translation_note': 'Possible cover story'
    }
]

async def run_ddo_demo():
    """
    Complete DDO scenario from intelligence to arrest plan
    """
    
    print("="*60)
    print("DDO INTELLIGENCE SYSTEM DEMO")
    print("Target: Russian Intelligence Officer")
    print("="*60)
    
    # Initialize system
    system = PatternOfLifeRAGSystem(cohere_api_key=COHERE_API_KEY)
    russian_agent = RussianIntelAgent()
    ddo_planner = DDOPlanningAgent()
    
    # Step 1: Ingest Russian intercepts (NO TRANSLATION)
    print("\n[1] INGESTING RUSSIAN INTERCEPTS...")
    for intercept in DEMO_INTERCEPTS:
        await system.ingest_ripa_intercept(intercept)
    print(f"✓ {len(DEMO_INTERCEPTS)} intercepts processed in native Russian")
    
    # Step 2: Analyze Russian content directly
    print("\n[2] ANALYZING RUSSIAN CONTENT (No translation)...")
    russian_analysis = await russian_agent.analyze_russian_subject_profile(
        subject_id=DEMO_SUBJECT['id'],
        intercepts=DEMO_INTERCEPTS
    )
    print("✓ Russian analysis complete")
    print("\nKEY FINDINGS:")
    print(russian_analysis.summary)
    
    # Step 3: Detect operational language
    print("\n[3] DETECTING RUSSIAN TRADECRAFT...")
    for intercept in DEMO_INTERCEPTS:
        tradecraft = await russian_agent.detect_russian_operational_language(
            intercept['content']
        )
        print(f"Intercept {intercept['timestamp']}: {tradecraft.threat_level}")
    
    # Step 4: Build subject profile with name variations
    print("\n[4] BUILDING SUBJECT PROFILE...")
    name_variations = await russian_agent.cross_reference_russian_names(
        DEMO_SUBJECT['name']
    )
    print(f"✓ Identified {len(name_variations)} name variations")
    print(f"Variations: {name_variations}")
    
    # Step 5: Get live location data
    print("\n[5] GATHERING REAL-TIME INTELLIGENCE...")
    live_location = await system.fusion.live_streams.get_live_location(
        DEMO_SUBJECT['id']
    )
    print(f"✓ Subject located: {live_location['latitude']}, {live_location['longitude']}")
    print(f"  Location: Manchester city centre")
    print(f"  Accuracy: {live_location['accuracy_meters']}m")
    
    # Step 6: Generate DDO plan
    print("\n[6] GENERATING DETENTION OPERATION PLAN...")
    ddo_plan = await ddo_planner.generate_detention_plan(
        subject_profile=DEMO_SUBJECT,
        intelligence_package=russian_analysis
    )
    
    print("\n" + "="*60)
    print("DDO OPERATIONAL PLAN")
    print("="*60)
    print(ddo_plan.summary)
    
    print("\n[RECOMMENDED DETENTION WINDOW]")
    print(f"Date/Time: {ddo_plan.recommended_window.datetime}")
    print(f"Location: {ddo_plan.recommended_window.location}")
    print(f"Rationale: {ddo_plan.recommended_window.rationale}")
    print(f"Confidence: {ddo_plan.recommended_window.confidence}%")
    
    print("\n[RISK ASSESSMENT]")
    print(f"Violence potential: {ddo_plan.risk_assessment.violence}/10")
    print(f"Escape risk: {ddo_plan.risk_assessment.escape}/10")
    print(f"Evidence destruction: {ddo_plan.risk_assessment.evidence_destruction}/10")
    print(f"Counter-surveillance: {ddo_plan.risk_assessment.counter_surveillance}/10")
    
    print("\n[ASSET REQUIREMENTS]")
    print(f"Arrest team: {ddo_plan.assets.arrest_team_size} officers")
    print(f"Armed support: {'YES' if ddo_plan.assets.armed_support else 'NO'}")
    print(f"Russian interpreter: REQUIRED")
    print(f"Search team: {ddo_plan.assets.search_team_size} officers")
    print(f"Tech support: Digital forensics unit")
    
    print("\n[LEGAL COMPLIANCE]")
    print(f"RIPA Authorization: {DEMO_SUBJECT['ripa_authorization']}")
    print(f"Arrest authority: Confirmed")
    print(f"Search warrant: Required (obtaining)")
    print(f"Consular notification: Russian Embassy (post-arrest)")
    
    # Step 7: Generate evidence package
    print("\n[7] GENERATING EVIDENCE PACKAGE...")
    evidence = await system.generate_evidence_package(
        subject_id=DEMO_SUBJECT['id'],
        detention_date=ddo_plan.recommended_window.datetime
    )
    
    print(f"✓ Evidence package complete")
    print(f"  Intercepts: {evidence.intercept_count}")
    print(f"  Russian content: Preserved in original Cyrillic")
    print(f"  RIPA compliant: YES")
    print(f"  Court ready: YES")
    
    print("\n" + "="*60)
    print("OPERATIONAL STATUS: READY FOR BRIEFING")
    print("="*60)
    
    return ddo_plan, evidence
```

## Updated File Structure
```
ddo-intelligence-system/
├── backend/
│   ├── models/
│   │   ├── ripa_intercept.py        # RIPA-compliant intercept model
│   │   ├── ddo_plan.py              # DDO operation plan model
│   │   └── russian_subject.py       # Russian subject profile
│   ├── agents/
│   │   ├── russian_intel.py         # Russian language specialist
│   │   ├── ddo_planning.py          # DDO operation planner
│   │   └── evidence_generator.py    # Court-ready packages
│   ├── compliance/
│   │   ├── ripa_handler.py          # RIPA compliance checks
│   │   ├── chain_of_custody.py      # Evidence tracking
│   │   └── audit_logger.py          # Legal audit trail
│   ├── demo/
│   │   ├── russian_subject_scenario.py  # Full DDO demo
│   │   └── generate_russian_intercepts.py  # Test data
```

## Key Demo Features to Showcase

1. **Russian Text Displayed**: Show Cyrillic in UI alongside English analysis
2. **No Translation Layer**: Demonstrate direct Russian→Analysis→English output
3. **Cultural Context**: Show how system understands Russian idioms/patterns
4. **Name Variations**: Display all Russian name forms automatically detected
5. **Tradecraft Detection**: Highlight FSB/GRU operational language in red
6. **DDO Plan Generation**: Show comprehensive operation plan with timings/assets
7. **RIPA Compliance**: Display authorization details, audit trail
8. **Evidence Package**: Show court-ready document with Russian originals preserved

## Success Criteria for Demo

✅ Russian intercepts processed WITHOUT translation
✅ Cyrillic text preserved and displayed correctly
✅ System detects Russian intelligence tradecraft
✅ Generates comprehensive DDO operation plan
✅ Risk assessment for Russian intelligence officer
✅ Asset positioning recommendations
✅ RIPA-compliant evidence package generated
✅ All sources attributed with chain of custody
✅ UI shows both Russian original and English analysis
✅ Detention window predicted with >80% confidence
✅ Complete demo runs in <60 seconds

## Environment Variables
```bash
COHERE_API_KEY=your_key_here
DEMO_MODE=true
SUBJECT_NATIONALITY=Russian
RIPA_AUTHORIZATION_REF=RIPA/2025/DDO/0423
LOG_RUSSIAN_CONTENT=true
ENABLE_CYRILLIC_DISPLAY=true
```

This updated prompt focuses on the **operational reality of a DDO against a Russian subject**, showcasing Cohere's multilingual capabilities by processing Russian intelligence WITHOUT translation, while maintaining RIPA compliance and generating actionable detention plans.