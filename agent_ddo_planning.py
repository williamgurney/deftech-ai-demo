"""
DDO Planning Agent - Deliberate Detention Operation Planning
Generates comprehensive arrest plans with timing, location, assets, and risk assessment
"""
import cohere
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import random
from models_ripa import (
    RussianSubjectProfile, DDOPlan, DetentionWindow, DetentionLocation,
    AssetRequirements, RiskAssessment, ThreatLevel, LiveLocationData
)


class DDOPlanningAgent:
    """
    Generates detention operation plans for Russian subjects
    Combines intelligence analysis with operational planning
    """

    def __init__(self, cohere_client: cohere.ClientV2):
        self.co = cohere_client

    async def generate_detention_plan(
        self,
        subject_profile: RussianSubjectProfile,
        intelligence_summary: str,
        ripa_authorization: str
    ) -> DDOPlan:
        """
        Generate comprehensive DDO plan
        """

        # Predict detention windows
        detention_windows = await self.predict_detention_windows(
            subject_profile,
            intelligence_summary
        )

        if not detention_windows:
            # Create fallback window
            detention_windows = [self._create_fallback_window(subject_profile)]

        recommended_window = detention_windows[0]

        # Generate operational plan using Cohere
        plan_prompt = f"""
Generate a Deliberate Detention Operation (DDO) Plan:

SUBJECT INFORMATION:
- Name: {subject_profile.primary_name}
- ID: {subject_profile.subject_id}
- Nationality: Russian
- Threat Level: {subject_profile.threat_level.value}
- Suspected Activity: {subject_profile.suspected_activity}

RIPA AUTHORIZATION: {ripa_authorization}

INTELLIGENCE SUMMARY:
{intelligence_summary}

RECOMMENDED DETENTION WINDOW:
- Location: {recommended_window.location.description}
- Date/Time: {recommended_window.datetime_start} to {recommended_window.datetime_end}
- Overall Score: {recommended_window.overall_score}/100
- Rationale: {recommended_window.recommendation}

SUBJECT RISK FACTORS:
- Violence potential: {subject_profile.violence_potential}/10
- Flight risk: {subject_profile.flight_risk}/10
- Evidence destruction risk: {subject_profile.evidence_destruction_risk}/10
- Operational security level: {subject_profile.operational_security_level}

GENERATE COMPREHENSIVE DDO OPERATIONAL ORDER:

1. EXECUTIVE SUMMARY (2-3 paragraphs)
   - Who is being detained and why
   - Key intelligence supporting detention
   - Recommended approach and timing

2. ARREST STRATEGY
   - Approach method (covert vs. overt)
   - Team positioning
   - Subject containment plan
   - Backup plan if subject deviates from pattern

3. SEARCH STRATEGY
   - Areas to search (person, vehicle, residence)
   - Evidence likely to be found
   - Digital evidence handling (phones, computers)
   - Russian-language document preservation

4. INTERVIEW STRATEGY
   - Key questions based on intelligence
   - Russian language interpreter requirements
   - Evidence to confront subject with
   - Anticipated defense arguments
   - Cooperation assessment strategy

5. ASSET COORDINATION
   - Arrest team positioning
   - Surveillance team placement
   - Search team readiness
   - Technical support requirements
   - Russian interpreter availability

6. CONTINGENCY PLANS
   - If subject attempts to flee
   - If subject destroys evidence
   - If subject becomes violent
   - If additional subjects are present
   - If subject location changes

7. LEGAL COMPLIANCE CHECKLIST
   - RIPA authorization confirmed
   - Arrest authority verified
   - Search warrant status
   - Consular notification (Russian Embassy)
   - Interview under caution requirements
   - Detention time limits

8. POST-ARREST ACTIONS
   - Evidence preservation protocol
   - Phone seizure (Faraday bag to prevent remote wipe)
   - Russian consular notification timing
   - Interview scheduling
   - Evidence processing priorities

FORMAT: Professional operational order suitable for briefing arrest teams.
BE SPECIFIC with times, locations, and procedures.
"""

        try:
            response = self.co.chat(
                model='command-r-plus-08-2024',
                messages=[
                    {
                        "role": "user",
                        "content": plan_prompt
                    }
                ]
            )

            operational_summary = response.message.content[0].text

            # Generate risk assessment
            risk_assessment = self._calculate_risk_assessment(subject_profile)

            # Generate asset requirements
            asset_requirements = self._calculate_asset_requirements(
                subject_profile,
                recommended_window
            )

            # Create DDO plan
            plan = DDOPlan(
                plan_id=f"DDO_{subject_profile.subject_id}_{datetime.now().strftime('%Y%m%d_%H%M')}",
                subject_id=subject_profile.subject_id,
                subject_name=subject_profile.primary_name,
                recommended_window=recommended_window,
                alternative_windows=detention_windows[1:4] if len(detention_windows) > 1 else [],
                asset_requirements=asset_requirements,
                risk_assessment=risk_assessment,
                operational_summary=operational_summary,
                ripa_authorization=ripa_authorization,
                arrest_authority="Police and Criminal Evidence Act 1984",
                search_warrant_required=True,
                consular_notification_required=True,
                consular_notification_timing="POST_ARREST",
                expected_evidence_types=[
                    "Mobile phones (Russian language content)",
                    "Computers/tablets",
                    "Russian language documents",
                    "SIM cards",
                    "USB drives",
                    "Notebooks/written materials"
                ],
                evidence_preservation_plan="All devices in Faraday bags immediately. Russian language materials photographed in situ before seizure.",
                contingency_plans={
                    "subject_flees": "Surveillance team trails, backup arrest team intercepts",
                    "subject_violent": "Armed support deploys, tactical containment",
                    "evidence_destruction": "Immediate intervention, technical support recovers data",
                    "location_change": "Mobile surveillance maintains contact, adjust arrest location"
                },
                generated_at=datetime.now(),
                generated_by="DDO Planning Agent",
                briefing_ready=True
            )

            return plan

        except Exception as e:
            # Return minimal plan on error
            return DDOPlan(
                plan_id=f"DDO_{subject_profile.subject_id}_ERROR",
                subject_id=subject_profile.subject_id,
                subject_name=subject_profile.primary_name,
                recommended_window=recommended_window,
                operational_summary=f"Error generating plan: {str(e)}",
                ripa_authorization=ripa_authorization
            )

    async def predict_detention_windows(
        self,
        subject_profile: RussianSubjectProfile,
        intelligence_summary: str
    ) -> List[DetentionWindow]:
        """
        Identify optimal detention opportunities
        Uses Cohere to analyze patterns and predict best arrest times/locations
        """

        analysis_prompt = f"""
Analyze subject intelligence to predict optimal detention opportunities:

SUBJECT: {subject_profile.primary_name}
THREAT LEVEL: {subject_profile.threat_level.value}
INTELLIGENCE SUMMARY:
{intelligence_summary}

KNOWN BEHAVIORS:
- Operational security level: {subject_profile.operational_security_level}
- Flight risk: {subject_profile.flight_risk}/10
- Violence potential: {subject_profile.violence_potential}/10

TASK: Identify 3-5 OPTIMAL DETENTION OPPORTUNITIES

For each opportunity, consider:

1. LOCATION FACTORS:
   - Subject's routine locations (home, work, regular stops)
   - Public vs. private spaces
   - Escape route availability
   - Officer access and positioning
   - Evidence likely present
   - Public safety considerations

2. TIMING FACTORS:
   - When subject is predictably present
   - Times when subject is likely alone
   - Low public exposure periods
   - Evidence destruction opportunity
   - Subject's state (alert vs. tired)

3. OPERATIONAL FACTORS:
   - Officer safety
   - Success probability
   - Evidence preservation
   - Public safety
   - Resource requirements

DETENTION LOCATION TYPES to consider:
- HOME: Subject's residence (early morning often optimal)
- VEHICLE: Subject's car (traffic stop or while parked)
- WORKPLACE: Subject's place of employment
- ROUTINE STOP: Regular location subject visits
- PUBLIC TRANSPORT: Train/bus station (if regular commuter)

For each opportunity, provide:
- Location description
- Date/time window
- Rationale (why this is a good opportunity)
- Risks
- Mitigation strategies

Return 3-5 ranked opportunities from BEST to acceptable.

FORMAT:

**OPPORTUNITY 1 (RECOMMENDED):**
Location: [specific location and type]
Date/Time: [specific window]
Rationale: [why this is optimal]
Risks: [list risks]
Mitigation: [how to address risks]
Scores: Officer Safety [0-100], Public Safety [0-100], Evidence Preservation [0-100], Success Probability [0-100]

**OPPORTUNITY 2:**
[same format]

**OPPORTUNITY 3:**
[same format]
"""

        try:
            response = self.co.chat(
                model='command-r-plus-08-2024',
                messages=[
                    {
                        "role": "user",
                        "content": analysis_prompt
                    }
                ],
                temperature=0.3
            )

            analysis = response.message.content[0].text

            # Parse opportunities (simplified - would use structured output in production)
            windows = self._parse_detention_windows(analysis, subject_profile)

            return windows if windows else [self._create_fallback_window(subject_profile)]

        except Exception as e:
            # Return fallback window on error
            return [self._create_fallback_window(subject_profile)]

    def _parse_detention_windows(
        self,
        analysis: str,
        subject_profile: RussianSubjectProfile
    ) -> List[DetentionWindow]:
        """
        Parse Cohere's analysis into structured detention windows
        Simplified version - production would use structured output
        """

        windows = []

        # Create sample windows based on common patterns
        # In production, would parse from Cohere response

        # Window 1: Early morning at residence
        home_location = DetentionLocation(
            location_id="LOC_001",
            description="Subject's residence - early morning arrest",
            location_type="home",
            address="Manchester city centre (specific address redacted)",
            latitude=53.4808,
            longitude=-2.2426,
            public_exposure_level="LOW",
            crowd_level="NONE",
            access_difficulty="MODERATE",
            escape_routes_count=2,
            evidence_likely_present=True,
            evidence_description="Phones, computers, documents",
            subject_typically_present=["06:00-09:00", "18:00-08:00"],
            alone_probability=0.8,
            pattern_confidence=0.85
        )

        window1 = DetentionWindow(
            window_id="WIN_001",
            location=home_location,
            datetime_start=datetime.now() + timedelta(hours=12),
            datetime_end=datetime.now() + timedelta(hours=15),
            officer_safety_score=85,
            public_safety_score=95,
            evidence_preservation_score=90,
            success_probability_score=88,
            overall_score=88,
            recommendation="Early morning residence arrest. Subject typically alone, low public exposure, high evidence recovery probability.",
            risks=["Subject may have security measures", "Multiple exits from building"],
            mitigation_strategies=["Position teams at all exits", "Use of element of surprise", "Early entry before subject fully alert"],
            confidence_level=0.85
        )

        windows.append(window1)

        # Window 2: Vehicle stop
        vehicle_location = DetentionLocation(
            location_id="LOC_002",
            description="Subject's vehicle - traffic stop or at destination",
            location_type="vehicle",
            address="Subject's known vehicle (registration plate on file)",
            latitude=53.4808,
            longitude=-2.2426,
            public_exposure_level="MEDIUM",
            crowd_level="LOW",
            access_difficulty="EASY",
            escape_routes_count=1,
            evidence_likely_present=True,
            evidence_description="Phone, documents in vehicle",
            subject_typically_present=["08:00-09:00", "17:00-18:00"],
            alone_probability=0.9,
            pattern_confidence=0.75
        )

        window2 = DetentionWindow(
            window_id="WIN_002",
            location=vehicle_location,
            datetime_start=datetime.now() + timedelta(hours=24),
            datetime_end=datetime.now() + timedelta(hours=26),
            officer_safety_score=75,
            public_safety_score=80,
            evidence_preservation_score=70,
            success_probability_score=82,
            overall_score=78,
            recommendation="Vehicle stop during routine journey. Subject contained in vehicle, limited escape options.",
            risks=["Public location", "Vehicle pursuit if subject attempts to flee"],
            mitigation_strategies=["Multiple vehicles for stop", "Block escape routes", "Quick extraction from vehicle"],
            confidence_level=0.75
        )

        windows.append(window2)

        return windows

    def _create_fallback_window(self, subject_profile: RussianSubjectProfile) -> DetentionWindow:
        """Create a default detention window if analysis fails"""

        fallback_location = DetentionLocation(
            location_id="LOC_FALLBACK",
            description="Subject's last known location",
            location_type="public_place",
            address="Manchester city centre",
            latitude=53.4808,
            longitude=-2.2426,
            public_exposure_level="MEDIUM",
            crowd_level="MEDIUM",
            access_difficulty="MODERATE",
            escape_routes_count=3,
            evidence_likely_present=False,
            alone_probability=0.5,
            pattern_confidence=0.5
        )

        return DetentionWindow(
            window_id="WIN_FALLBACK",
            location=fallback_location,
            datetime_start=datetime.now() + timedelta(hours=24),
            datetime_end=datetime.now() + timedelta(hours=48),
            officer_safety_score=60,
            public_safety_score=60,
            evidence_preservation_score=50,
            success_probability_score=65,
            overall_score=60,
            recommendation="Fallback detention plan - requires further intelligence gathering",
            risks=["Limited intelligence", "Unpredictable conditions"],
            mitigation_strategies=["Enhanced surveillance", "Flexible team positioning"],
            confidence_level=0.5
        )

    def _calculate_risk_assessment(self, subject_profile: RussianSubjectProfile) -> RiskAssessment:
        """Calculate comprehensive risk assessment"""

        violence_potential = subject_profile.violence_potential
        escape_risk = subject_profile.flight_risk
        evidence_destruction = subject_profile.evidence_destruction_risk

        # Calculate additional risk factors
        counter_surveillance = 7 if subject_profile.operational_security_level == "PROFESSIONAL" else 4
        public_safety = max(3, violence_potential - 2)
        officer_safety = max(5, violence_potential)

        # Overall risk level
        avg_risk = (violence_potential + escape_risk + evidence_destruction + counter_surveillance) / 4

        if avg_risk >= 8:
            overall_level = "CRITICAL"
        elif avg_risk >= 6:
            overall_level = "HIGH"
        elif avg_risk >= 4:
            overall_level = "MEDIUM"
        else:
            overall_level = "LOW"

        precautions = []
        if violence_potential >= 6:
            precautions.append("Armed support required")
            precautions.append("Body armor for all officers")
        if escape_risk >= 7:
            precautions.append("Multiple containment teams")
            precautions.append("Vehicle blocking positions")
        if evidence_destruction >= 6:
            precautions.append("Immediate phone seizure and Faraday bag")
            precautions.append("Technical support on scene")
        if counter_surveillance >= 6:
            precautions.append("Covert approach until last moment")
            precautions.append("Counter-surveillance detection")

        return RiskAssessment(
            violence_potential=violence_potential,
            escape_risk=escape_risk,
            evidence_destruction_risk=evidence_destruction,
            counter_surveillance_awareness=counter_surveillance,
            public_safety_risk=public_safety,
            officer_safety_risk=officer_safety,
            overall_risk_level=overall_level,
            risk_summary=f"Overall risk: {overall_level}. Primary concerns: violence potential ({violence_potential}/10), flight risk ({escape_risk}/10), evidence destruction ({evidence_destruction}/10).",
            recommended_precautions=precautions
        )

    def _calculate_asset_requirements(
        self,
        subject_profile: RussianSubjectProfile,
        detention_window: DetentionWindow
    ) -> AssetRequirements:
        """Calculate required assets for DDO"""

        # Base team sizes
        arrest_team_size = 4

        # Adjust based on risk
        if subject_profile.violence_potential >= 7:
            arrest_team_size = 8
            armed_support = True
            armed_officers = 2
        elif subject_profile.violence_potential >= 5:
            arrest_team_size = 6
            armed_support = True
            armed_officers = 1
        else:
            armed_support = False
            armed_officers = 0

        # Search team
        if detention_window.location.evidence_likely_present:
            search_team_size = 4
        else:
            search_team_size = 0

        # Surveillance team
        if subject_profile.operational_security_level == "PROFESSIONAL":
            surveillance_team_size = 6
        else:
            surveillance_team_size = 3

        return AssetRequirements(
            arrest_team_size=arrest_team_size,
            armed_support_required=armed_support,
            armed_officers_count=armed_officers,
            search_team_size=search_team_size,
            surveillance_team_size=surveillance_team_size,
            russian_interpreter_required=True,
            technical_support_required=True,
            digital_forensics=True,
            recording_equipment=True,
            translation_equipment=True,
            cell_phone_faraday_bags=5
        )
