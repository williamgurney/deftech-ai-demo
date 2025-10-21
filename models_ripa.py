"""
RIPA-Compliant Data Models for DDO Intelligence System
Regulation of Investigatory Powers Act compliance for Russian subject tracking
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict
from enum import Enum


class ClassificationLevel(Enum):
    """Security classification levels"""
    UNCLASSIFIED = "UNCLASSIFIED"
    CONFIDENTIAL = "CONFIDENTIAL"
    SECRET = "SECRET"
    TOP_SECRET = "TOP SECRET"


class InterceptType(Enum):
    """Types of RIPA-authorized intercepts"""
    PHONE_CALL = "phone_call"
    TEXT_MESSAGE = "text_message"
    EMAIL = "email"
    SOCIAL_MEDIA = "social_media"
    PHYSICAL_SURVEILLANCE = "physical_surveillance"
    LOCATION_TRACKING = "location_tracking"


class ThreatLevel(Enum):
    """Subject threat assessment levels"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class CustodyEvent:
    """Chain of custody tracking event"""
    timestamp: datetime
    action: str  # collected, accessed, analyzed, exported, disclosed
    actor_id: str  # Analyst/officer ID
    actor_name: str
    purpose: str  # investigation, briefing, court_disclosure
    system_used: str  # which agent/tool was used
    ip_address: Optional[str] = None
    notes: Optional[str] = None


@dataclass
class RIPAIntercept:
    """RIPA-compliant intercept record"""
    # Unique identifiers
    intercept_id: str
    subject_id: str

    # RIPA authorization details
    authorization_ref: str  # e.g., "RIPA/2025/DDO/0423"
    authorized_by: str  # Authorizing officer name/ID
    authorization_date: datetime
    expiry_date: datetime

    # Intercept metadata
    intercept_type: InterceptType
    collection_timestamp: datetime
    collection_method: str  # telecom_tap, social_scrape, physical_obs

    # Content (multilingual support)
    content_language: str  # Russian, English, mixed
    raw_content: str  # Original content with Cyrillic preserved
    platform: Optional[str] = None  # VKontakte, Telegram, WhatsApp, etc.

    # Classification and handling
    handling_classification: ClassificationLevel = ClassificationLevel.SECRET
    disclosed_to_defense: bool = False
    redaction_required: bool = False

    # Chain of custody
    chain_of_custody: List[CustodyEvent] = field(default_factory=list)

    # Analysis flags
    contains_operational_language: bool = False
    tradecraft_indicators: List[str] = field(default_factory=list)
    threat_level: Optional[ThreatLevel] = None

    def add_custody_event(self, action: str, actor_id: str, actor_name: str,
                         purpose: str, system: str):
        """Add chain of custody event"""
        event = CustodyEvent(
            timestamp=datetime.now(),
            action=action,
            actor_id=actor_id,
            actor_name=actor_name,
            purpose=purpose,
            system_used=system
        )
        self.chain_of_custody.append(event)


@dataclass
class RussianNameVariation:
    """Russian name variations (patronymics, diminutives, etc.)"""
    formal_full: str  # Иван Петрович Сидоров
    given_name: str  # Иван
    patronymic: str  # Петрович
    surname: str  # Сидоров
    diminutives: List[str]  # Ваня, Ванечка, Иванушка
    transliterations: List[str]  # Ivan, Iwan, Evan
    aliases: List[str]  # Known aliases
    nicknames: List[str]  # Criminal/operational nicknames


@dataclass
class RussianSubjectProfile:
    """Comprehensive Russian subject profile"""
    subject_id: str

    # Identity
    primary_name: str
    name_variations: RussianNameVariation
    nationality: str = "Russian"
    date_of_birth: Optional[datetime] = None
    passport_numbers: List[str] = field(default_factory=list)

    # Threat assessment
    threat_level: ThreatLevel = ThreatLevel.MEDIUM
    suspected_activity: str = ""  # "FSB officer", "GRU operative", "Criminal associate"
    organizational_affiliations: List[str] = field(default_factory=list)

    # Intelligence analysis
    intercepts_analyzed: int = 0
    native_processing: bool = True  # No translation used
    language: str = "Russian"
    dialect_markers: List[str] = field(default_factory=list)  # Moscow, Petersburg, regional
    education_indicators: str = ""
    military_background: bool = False
    intelligence_background: bool = False

    # Network
    known_associates: List[str] = field(default_factory=list)
    handler_identified: bool = False
    network_role: str = ""  # handler, agent, courier, facilitator

    # Behavioral assessment
    operational_security_level: str = "UNKNOWN"  # LOW, MEDIUM, HIGH, PROFESSIONAL
    violence_potential: int = 0  # 0-10 scale
    cooperation_likelihood: int = 5  # 0-10 scale (post-arrest)
    flight_risk: int = 5  # 0-10 scale
    evidence_destruction_risk: int = 5  # 0-10 scale

    # RIPA compliance
    ripa_authorization: str = ""
    surveillance_authorized: bool = False
    intercept_authorized: bool = False

    # Metadata
    profile_generated_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)
    comprehensive_analysis: str = ""  # Full analysis text from Cohere


@dataclass
class DetentionLocation:
    """Potential detention location"""
    location_id: str
    description: str
    location_type: str  # home, vehicle, public_place, workplace
    address: str
    latitude: float
    longitude: float

    # Operational factors
    public_exposure_level: str  # LOW, MEDIUM, HIGH
    crowd_level: str  # NONE, LOW, MEDIUM, HIGH
    access_difficulty: str  # EASY, MODERATE, DIFFICULT
    escape_routes_count: int

    # Evidence factors
    evidence_likely_present: bool = False
    evidence_description: str = ""

    # Timing factors
    subject_typically_present: List[str] = field(default_factory=list)  # time windows
    alone_probability: float = 0.5  # 0.0 to 1.0
    pattern_confidence: float = 0.5  # How predictable

    # Planet Labs satellite data
    satellite_coverage: str = ""
    last_satellite_update: Optional[datetime] = None
    geospatial_confidence: float = 0.0


@dataclass
class DetentionWindow:
    """Optimal detention time/location opportunity"""
    window_id: str
    location: DetentionLocation
    datetime_start: datetime
    datetime_end: datetime

    # Scoring
    officer_safety_score: int = 0  # 0-100
    public_safety_score: int = 0  # 0-100
    evidence_preservation_score: int = 0  # 0-100
    success_probability_score: int = 0  # 0-100
    overall_score: int = 0  # Weighted total

    # Rationale
    recommendation: str = ""
    risks: List[str] = field(default_factory=list)
    mitigation_strategies: List[str] = field(default_factory=list)

    # Confidence
    confidence_level: float = 0.0  # 0.0 to 1.0


@dataclass
class AssetRequirements:
    """Required assets for DDO"""
    arrest_team_size: int
    armed_support_required: bool
    armed_officers_count: int = 0
    search_team_size: int = 0
    surveillance_team_size: int = 0
    russian_interpreter_required: bool = True
    technical_support_required: bool = True

    # Specialist requirements
    digital_forensics: bool = False
    explosives_disposal: bool = False
    medical_support: bool = False

    # Equipment
    cell_phone_faraday_bags: int = 0  # Prevent remote wipe
    recording_equipment: bool = True
    translation_equipment: bool = True


@dataclass
class RiskAssessment:
    """DDO risk assessment"""
    violence_potential: int  # 0-10
    escape_risk: int  # 0-10
    evidence_destruction_risk: int  # 0-10
    counter_surveillance_awareness: int  # 0-10
    public_safety_risk: int  # 0-10
    officer_safety_risk: int  # 0-10

    overall_risk_level: str = "MEDIUM"  # LOW, MEDIUM, HIGH, CRITICAL
    risk_summary: str = ""
    recommended_precautions: List[str] = field(default_factory=list)


@dataclass
class DDOPlan:
    """Deliberate Detention Operation Plan"""
    plan_id: str
    subject_id: str
    subject_name: str

    # Timing
    recommended_window: DetentionWindow
    alternative_windows: List[DetentionWindow] = field(default_factory=list)

    # Assets
    asset_requirements: AssetRequirements = None

    # Risk
    risk_assessment: RiskAssessment = None

    # Operational details
    operational_summary: str = ""
    arrest_strategy: str = ""
    search_strategy: str = ""
    interview_strategy: str = ""

    # Legal compliance
    ripa_authorization: str = ""
    arrest_authority: str = ""
    search_warrant_required: bool = True
    search_warrant_ref: Optional[str] = None
    consular_notification_required: bool = True
    consular_notification_timing: str = "POST_ARREST"

    # Evidence
    expected_evidence_types: List[str] = field(default_factory=list)
    evidence_preservation_plan: str = ""

    # Contingencies
    contingency_plans: Dict[str, str] = field(default_factory=dict)

    # Metadata
    generated_at: datetime = field(default_factory=datetime.now)
    generated_by: str = "DDO Planning Agent"
    briefing_ready: bool = False


@dataclass
class EvidencePackage:
    """Prosecution-ready evidence package"""
    package_id: str
    subject_id: str
    subject_name: str

    # Content
    executive_summary: str
    detailed_chronology: str
    network_analysis: str
    interview_strategy: str

    # Evidence items
    intercepts_included: int
    russian_content_preserved: bool = True
    surveillance_logs_included: int = 0
    osint_items_included: int = 0

    # Legal compliance
    ripa_compliant: bool = True
    court_ready: bool = True
    disclosure_package_prepared: bool = False
    redactions_applied: List[str] = field(default_factory=list)

    # Metadata
    detention_date: Optional[datetime] = None
    generated_at: datetime = field(default_factory=datetime.now)
    generated_by: str = "Evidence Package Generator"


@dataclass
class LiveLocationData:
    """Real-time location intelligence"""
    subject_id: str
    timestamp: datetime
    latitude: float
    longitude: float
    accuracy_meters: float

    # Context
    location_description: str = ""
    address: str = ""
    location_type: str = ""  # residence, commercial, transport, public

    # Operational status
    moving: bool = False
    speed_kph: float = 0.0
    heading_degrees: Optional[float] = None

    # Source
    collection_method: str = ""  # gps_track, cell_tower, wifi, manual_obs, planet_satellite
    ripa_authorized: bool = True
    authorization_ref: str = ""

    # Planet Labs satellite data
    satellite_images_available: int = 0
    last_satellite_image: Optional[datetime] = None
    area_assessment: Optional[Dict] = None


# Demo data constants
DEMO_RUSSIAN_INTERCEPTS = [
    {
        'content': 'Встреча состоится завтра в старом месте. Принеси материалы. Окно с 15:00 до 16:00. Убедись что чистый.',
        'translation_note': 'Meeting tomorrow at old place. Bring materials. Window 15:00-16:00. Make sure clean (counter-surveillance clear)',
        'indicators': ['старое место (dead drop)', 'материалы (materials/intelligence)', 'окно (time window)', 'чистый (counter-surveillance term)']
    },
    {
        'content': 'Брат готов. Объект наблюдается. Передача завтра.',
        'translation_note': 'Brother ready. Object under observation. Handover tomorrow.',
        'indicators': ['объект (target/object - FSB term)', 'передача (handover - operational)', 'брат (operative/contact)']
    },
    {
        'content': 'Сегодня встречаюсь со старым другом. Давно не виделись!',
        'translation_note': 'Meeting an old friend today. Haven\'t seen each other in a long time!',
        'indicators': ['Possible cover story for operational meeting']
    }
]
