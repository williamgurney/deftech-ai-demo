"""
Creates sample defense documents for the demo
Generates realistic PDF files with defense content
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
import os


def create_header(text, classification="UNCLASSIFIED"):
    """Create a document header with classification marking"""
    return f"""
    <para align=center>
    <b>{classification}</b><br/>
    <font size=16><b>{text}</b></font><br/>
    {classification}
    </para>
    """


def create_equipment_maintenance_manual():
    """Create Equipment Maintenance Manual v3.2"""
    filename = "./sample_docs/equipment_maintenance_manual.pdf"
    os.makedirs("./sample_docs", exist_ok=True)

    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()

    # Title page
    story.append(Spacer(1, 2*inch))
    title = Paragraph(create_header(
        "Equipment Maintenance Manual v3.2",
        "UNCLASSIFIED"
    ), styles['Title'])
    story.append(title)
    story.append(Spacer(1, 0.5*inch))

    subtitle = Paragraph(
        "<para align=center>Standard Operating Procedures<br/>Effective Date: January 2024</para>",
        styles['Normal']
    )
    story.append(subtitle)
    story.append(PageBreak())

    # Section 1: Daily Inspection Procedures
    story.append(Paragraph("<b>1. Daily Equipment Inspection Procedures</b>", styles['Heading1']))
    story.append(Spacer(1, 0.2*inch))

    content1 = """
    All operational equipment must undergo daily inspection before use. Personnel are required
    to follow these standardized procedures to ensure equipment reliability and safety.
    """
    story.append(Paragraph(content1, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("<b>1.1 Visual Inspection Protocol</b>", styles['Heading2']))
    content1_1 = """
    Begin with a comprehensive visual inspection of all equipment components. Check for:
    <br/><br/>
    • Physical damage including cracks, dents, or deformation<br/>
    • Corrosion or rust on metal components<br/>
    • Fluid leaks from hydraulic or fuel systems<br/>
    • Worn or frayed electrical cables<br/>
    • Missing or loose fasteners, bolts, or securing mechanisms<br/>
    <br/>
    Any defects identified during visual inspection must be documented in the maintenance log
    with specific location and severity assessment.
    """
    story.append(Paragraph(content1_1, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("<b>1.2 Functional Testing Requirements</b>", styles['Heading2']))
    content1_2 = """
    After visual inspection, conduct functional tests on all critical systems:
    <br/><br/>
    • Power systems: Verify proper startup sequence and voltage levels<br/>
    • Emergency shutdown systems: Test activation and response time<br/>
    • Communication systems: Confirm clear signal transmission<br/>
    • Safety interlocks: Validate proper engagement and disengagement<br/>
    • Calibration instruments: Check against known reference standards<br/>
    <br/>
    Record all test results with timestamp and operator identification. Any system failing
    functional tests must be tagged out-of-service immediately.
    """
    story.append(Paragraph(content1_2, styles['BodyText']))
    story.append(PageBreak())

    # Section 2: Preventive Maintenance
    story.append(Paragraph("<b>2. Preventive Maintenance Schedule</b>", styles['Heading1']))
    story.append(Spacer(1, 0.2*inch))

    content2 = """
    Preventive maintenance is conducted on a tiered schedule based on equipment criticality
    and manufacturer specifications. All maintenance activities must be logged in the digital
    maintenance management system.
    """
    story.append(Paragraph(content2, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("<b>2.1 Weekly Maintenance Tasks</b>", styles['Heading2']))
    content2_1 = """
    Weekly maintenance includes:<br/><br/>
    • Lubrication of all moving parts per specification chart<br/>
    • Filter inspection and replacement if pressure differential exceeds threshold<br/>
    • Battery voltage and electrolyte level checks<br/>
    • Tire pressure verification for wheeled equipment<br/>
    • Torque verification on critical fasteners<br/>
    <br/>
    Use only approved lubricants and replacement parts as specified in Appendix C.
    """
    story.append(Paragraph(content2_1, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("<b>2.2 Monthly Calibration Procedures</b>", styles['Heading2']))
    content2_2 = """
    All precision instruments require monthly calibration against NIST-traceable standards.
    Calibration procedures must be performed by certified technicians and include:
    <br/><br/>
    • Zero-point adjustment verification<br/>
    • Full-scale accuracy testing at minimum 5 reference points<br/>
    • Linearity assessment across operational range<br/>
    • Environmental compensation factor validation<br/>
    • Calibration certificate generation with serial number tracking<br/>
    <br/>
    Instruments failing calibration must be immediately removed from service and sent
    to depot-level maintenance facility for repair.
    """
    story.append(Paragraph(content2_2, styles['BodyText']))
    story.append(PageBreak())

    # Section 3: Troubleshooting
    story.append(Paragraph("<b>3. Troubleshooting Common Issues</b>", styles['Heading1']))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("<b>3.1 Equipment Type A - Failure to Start</b>", styles['Heading2']))
    content3_1 = """
    If Equipment Type A fails to start, follow this diagnostic sequence:<br/><br/>
    1. Verify main power supply voltage (should be 24-28 VDC)<br/>
    2. Check emergency stop button is in reset position<br/>
    3. Inspect control panel for fault indicator lights<br/>
    4. Test ignition circuit continuity with multimeter<br/>
    5. Examine fuel supply line for blockages or leaks<br/>
    6. Review system logs for error codes<br/>
    <br/>
    If issue persists after these checks, escalate to senior maintenance technician.
    Do not attempt to bypass safety interlocks.
    """
    story.append(Paragraph(content3_1, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("<b>3.2 Equipment Type B - Hydraulic System Issues</b>", styles['Heading2']))
    content3_2 = """
    Hydraulic system problems in Equipment Type B typically manifest as:<br/><br/>
    • Sluggish or unresponsive controls<br/>
    • Unusual noise during operation<br/>
    • Visible fluid leakage<br/>
    • Inconsistent pressure readings<br/>
    <br/>
    Troubleshooting steps:<br/><br/>
    1. Check hydraulic fluid level in reservoir - maintain between MIN and MAX marks<br/>
    2. Inspect all hoses and fittings for damage or loose connections<br/>
    3. Verify pump pressure against specification (2000-2200 PSI nominal)<br/>
    4. Test relief valve operation and setpoint<br/>
    5. Examine filters for contamination or bypass indicator<br/>
    6. Check for air in system - bleed if necessary per Section 4.3<br/>
    <br/>
    Use only approved MIL-PRF-83282 hydraulic fluid for replenishment.
    """
    story.append(Paragraph(content3_2, styles['BodyText']))

    # Build PDF
    doc.build(story)
    print(f"✓ Created: {filename}")


def create_safety_guidelines():
    """Create Safety Guidelines 2024"""
    filename = "./sample_docs/safety_guidelines.pdf"

    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()

    # Title page
    story.append(Spacer(1, 2*inch))
    title = Paragraph(create_header(
        "Safety Guidelines 2024",
        "UNCLASSIFIED"
    ), styles['Title'])
    story.append(title)
    story.append(Spacer(1, 0.5*inch))

    subtitle = Paragraph(
        "<para align=center>Personnel Safety and Operational Security<br/>Effective Date: March 2024</para>",
        styles['Normal']
    )
    story.append(subtitle)
    story.append(PageBreak())

    # Content
    story.append(Paragraph("<b>1. Personal Protective Equipment (PPE) Requirements</b>", styles['Heading1']))
    story.append(Spacer(1, 0.2*inch))

    content1 = """
    All personnel operating or maintaining equipment must wear appropriate personal protective
    equipment. Minimum PPE requirements vary by operation type and environmental conditions.
    """
    story.append(Paragraph(content1, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("<b>1.1 Standard PPE for Maintenance Operations</b>", styles['Heading2']))
    content1_1 = """
    When performing maintenance tasks, the following PPE is mandatory:<br/><br/>
    • Safety glasses with side shields (ANSI Z87.1 certified)<br/>
    • Steel-toed boots (ASTM F2413 compliant)<br/>
    • Hearing protection when noise levels exceed 85 dBA<br/>
    • Cut-resistant gloves (ANSI Level A4 minimum) when handling sharp components<br/>
    • High-visibility vest in areas with vehicle traffic<br/>
    <br/>
    Additional PPE may be required based on specific task hazards identified in job safety analysis.
    """
    story.append(Paragraph(content1_1, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("<b>1.2 Cold Weather Operations PPE</b>", styles['Heading2']))
    content1_2 = """
    During winter operations or in cold environments (below 32°F/0°C), additional protection is required:<br/><br/>
    • Insulated gloves that maintain dexterity (do not compromise safety)<br/>
    • Cold weather headwear that fits under hard hat<br/>
    • Layered clothing system to prevent hypothermia<br/>
    • Anti-slip boot traction devices in icy conditions<br/>
    • Face protection if wind chill is below -20°F<br/>
    <br/>
    See Winter Operations Procedures manual for complete cold weather safety protocols.
    """
    story.append(Paragraph(content1_2, styles['BodyText']))
    story.append(PageBreak())

    # Section 2
    story.append(Paragraph("<b>2. Hazardous Material Handling</b>", styles['Heading1']))
    story.append(Spacer(1, 0.2*inch))

    content2 = """
    Many maintenance procedures involve hazardous materials including fuels, solvents,
    and chemical agents. Proper handling procedures must be followed to prevent exposure
    and environmental contamination.
    """
    story.append(Paragraph(content2, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("<b>2.1 Fuel Handling Safety</b>", styles['Heading2']))
    content2_1 = """
    When working with fuels and petroleum products:<br/><br/>
    • Ensure adequate ventilation to prevent vapor accumulation<br/>
    • Eliminate all ignition sources within 50 feet of fueling operations<br/>
    • Use proper grounding to prevent static discharge<br/>
    • Have appropriate fire extinguisher (Class B) readily available<br/>
    • Wear chemical-resistant gloves and eye protection<br/>
    • Use drip pans to capture spills - do not allow ground contamination<br/>
    <br/>
    In case of fuel spill exceeding 1 gallon, immediately notify environmental compliance officer
    and initiate spill response procedures per Section 2.4.
    """
    story.append(Paragraph(content2_1, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("<b>2.2 Battery Maintenance Safety</b>", styles['Heading2']))
    content2_2 = """
    Lead-acid batteries present both chemical and electrical hazards:<br/><br/>
    • Wear face shield and acid-resistant apron when servicing batteries<br/>
    • Remove all jewelry and metal objects before working near batteries<br/>
    • Use insulated tools to prevent short circuits<br/>
    • Ensure proper ventilation - hydrogen gas accumulation is explosive<br/>
    • Neutralize acid spills immediately with sodium bicarbonate solution<br/>
    • Never check charge by shorting terminals - use proper voltmeter<br/>
    <br/>
    Battery charging areas must have emergency eyewash station within 25 feet.
    """
    story.append(Paragraph(content2_2, styles['BodyText']))
    story.append(PageBreak())

    # Section 3
    story.append(Paragraph("<b>3. Lockout/Tagout Procedures</b>", styles['Heading1']))
    story.append(Spacer(1, 0.2*inch))

    content3 = """
    All equipment maintenance requires proper energy isolation using lockout/tagout (LOTO)
    procedures to prevent accidental startup or energy release.
    """
    story.append(Paragraph(content3, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("<b>3.1 LOTO Implementation Steps</b>", styles['Heading2']))
    content3_1 = """
    Mandatory lockout/tagout sequence:<br/><br/>
    1. Notify all affected personnel of impending shutdown<br/>
    2. Identify all energy sources (electrical, hydraulic, pneumatic, thermal)<br/>
    3. Shut down equipment using normal stop procedures<br/>
    4. Isolate each energy source using approved disconnect method<br/>
    5. Apply individual padlock and danger tag to each isolation point<br/>
    6. Attempt to start equipment to verify effective isolation<br/>
    7. Dissipate or restrain residual energy (bleed pressure, discharge capacitors, block suspended loads)<br/>
    <br/>
    Only the person who applied the lock may remove it. Group lockout requires coordinator
    assignment per Section 3.3.
    """
    story.append(Paragraph(content3_1, styles['BodyText']))

    doc.build(story)
    print(f"✓ Created: {filename}")


def create_tactical_doctrine():
    """Create Tactical Doctrine TD-2023-04"""
    filename = "./sample_docs/tactical_doctrine.pdf"

    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()

    # Title page
    story.append(Spacer(1, 2*inch))
    title = Paragraph(create_header(
        "Tactical Doctrine TD-2023-04",
        "SECRET"
    ), styles['Title'])
    story.append(title)
    story.append(Spacer(1, 0.5*inch))

    subtitle = Paragraph(
        "<para align=center><b>SIMULATED FOR DEMO PURPOSES</b><br/>Urban Operations Tactical Guidelines<br/>Publication Date: April 2023</para>",
        styles['Normal']
    )
    story.append(subtitle)
    story.append(PageBreak())

    # Content
    story.append(Paragraph("<b>1. Urban Operations Overview</b>", styles['Heading1']))
    story.append(Spacer(1, 0.2*inch))

    content1 = """
    Urban operations present unique challenges requiring specialized tactics and coordination.
    This doctrine establishes standardized procedures for operations in built-up areas.
    <br/><br/>
    <i>Note: This is a simulated document for demonstration purposes only.</i>
    """
    story.append(Paragraph(content1, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("<b>1.1 Urban Terrain Characteristics</b>", styles['Heading2']))
    content1_1 = """
    Urban environments are characterized by:<br/><br/>
    • Three-dimensional battlespace with vertical engagement zones<br/>
    • Limited fields of fire and observation<br/>
    • Complex navigation with multiple routing options<br/>
    • Civilian presence requiring positive identification<br/>
    • Infrastructure that can provide cover and concealment<br/>
    <br/>
    Commanders must account for these factors in mission planning and execution.
    """
    story.append(Paragraph(content1_1, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("<b>1.2 Tactical Movement in Urban Areas</b>", styles['Heading2']))
    content1_2 = """
    Movement techniques in urban terrain prioritize security and stealth:<br/><br/>
    • Utilize covered routes parallel to main avenues<br/>
    • Establish overwatch positions before movement<br/>
    • Clear potential danger areas systematically<br/>
    • Maintain communications at all times<br/>
    • Mark cleared structures with standardized symbols<br/>
    <br/>
    Units should avoid predictable patterns and vary routes when conducting repeated operations
    in the same area.
    """
    story.append(Paragraph(content1_2, styles['BodyText']))
    story.append(PageBreak())

    # Section 2
    story.append(Paragraph("<b>2. Building Entry and Clearance</b>", styles['Heading1']))
    story.append(Spacer(1, 0.2*inch))

    content2 = """
    Systematic building clearance is fundamental to urban operations success. All personnel
    must be proficient in standard entry and clearance techniques.
    """
    story.append(Paragraph(content2, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("<b>2.1 Pre-Entry Procedures</b>", styles['Heading2']))
    content2_1 = """
    Before entering any structure:<br/><br/>
    1. Conduct external reconnaissance to identify entry points and potential threats<br/>
    2. Establish security perimeter to prevent egress<br/>
    3. Brief team on building layout if available<br/>
    4. Assign individual responsibilities and sectors<br/>
    5. Coordinate with support elements (overwatch, QRF)<br/>
    6. Confirm communications and emergency signals<br/>
    <br/>
    Consider use of technical surveillance assets prior to entry when available and time permits.
    """
    story.append(Paragraph(content2_1, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("<b>2.2 Room Clearing Techniques</b>", styles['Heading2']))
    content2_2 = """
    Standard room clearing follows this sequence:<br/><br/>
    • Entry team positions at doorway maintaining cover<br/>
    • First operator enters rapidly, moving to designated corner<br/>
    • Subsequent operators flow in, taking assigned sectors<br/>
    • Methodically clear all areas including behind doors and furniture<br/>
    • Secure any occupants and search for threats<br/>
    • Mark room as clear and move to next objective<br/>
    <br/>
    Maintain 360-degree security at all times. Do not silhouette in doorways or windows.
    Use mirrors or cameras to preview rooms when tactical situation permits.
    """
    story.append(Paragraph(content2_2, styles['BodyText']))
    story.append(PageBreak())

    # Section 3
    story.append(Paragraph("<b>3. Communications in Urban Environment</b>", styles['Heading1']))
    story.append(Spacer(1, 0.2*inch))

    content3 = """
    Effective communications are critical in urban operations where visual contact may be
    limited and operations tempo is high.
    """
    story.append(Paragraph(content3, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("<b>3.1 Radio Communications Challenges</b>", styles['Heading2']))
    content3_1 = """
    Urban terrain degrades radio communications through:<br/><br/>
    • Signal absorption by concrete and steel structures<br/>
    • Multi-path interference from reflected signals<br/>
    • Dead zones in basements and interior rooms<br/>
    • Electronic interference from civilian infrastructure<br/>
    <br/>
    Mitigation strategies:<br/><br/>
    • Position relay stations at elevated locations<br/>
    • Use hand-held radios with fresh batteries<br/>
    • Establish alternate communications means (visual signals, runners)<br/>
    • Pre-position external antennas when establishing static positions<br/>
    • Monitor multiple frequencies for redundancy<br/>
    """
    story.append(Paragraph(content3_1, styles['BodyText']))

    doc.build(story)
    print(f"✓ Created: {filename}")


def create_winter_operations():
    """Create Winter Operations Procedures"""
    filename = "./sample_docs/winter_operations.pdf"

    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()

    # Title page
    story.append(Spacer(1, 2*inch))
    title = Paragraph(create_header(
        "Winter Operations Procedures v2.1",
        "UNCLASSIFIED"
    ), styles['Title'])
    story.append(title)
    story.append(Spacer(1, 0.5*inch))

    subtitle = Paragraph(
        "<para align=center>Cold Weather Equipment and Personnel Guidelines<br/>Effective Date: February 2024</para>",
        styles['Normal']
    )
    story.append(subtitle)
    story.append(PageBreak())

    # Content
    story.append(Paragraph("<b>1. Cold Weather Equipment Preparation</b>", styles['Heading1']))
    story.append(Spacer(1, 0.2*inch))

    content1 = """
    Operations in cold weather (below 32°F/0°C) require special equipment preparation to
    ensure reliability and prevent cold-related failures.
    """
    story.append(Paragraph(content1, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("<b>1.1 Winterization Checklist</b>", styles['Heading2']))
    content1_1 = """
    Complete the following winterization tasks before cold weather operations:<br/><br/>
    • Replace fluids with cold-weather grades (engine oil, transmission fluid, hydraulic fluid)<br/>
    • Install engine block heaters and connect to power source when parked<br/>
    • Test battery capacity - must maintain 80% minimum charge<br/>
    • Inspect and replace coolant - verify antifreeze protection to expected minimum temperature<br/>
    • Check tire pressure - cold air causes pressure drop<br/>
    • Verify operation of heating systems for operator compartments<br/>
    • Install winter air intake filters to prevent ice formation<br/>
    <br/>
    Reference Equipment Maintenance Manual Section 2 for detailed fluid specifications and capacities.
    """
    story.append(Paragraph(content1_1, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("<b>1.2 Cold Weather Starting Procedures</b>", styles['Heading2']))
    content1_2 = """
    When starting equipment in cold weather (below 0°F):<br/><br/>
    1. Connect to shore power for block heater minimum 2 hours before start<br/>
    2. Check that all fluids are appropriate cold-weather grades<br/>
    3. Ensure battery is fully charged and terminals are clean<br/>
    4. Glow plugs (diesel engines): activate for full cycle before cranking<br/>
    5. Do not exceed 15 seconds of continuous cranking - allow 2 minute rest between attempts<br/>
    6. After start, allow engine to warm to operating temperature before loading<br/>
    7. Monitor gauges for abnormal pressure or temperature readings<br/>
    <br/>
    If equipment fails to start after 3 attempts, investigate cause before continuing.
    Excessive cranking can damage starter motors and drain batteries.
    """
    story.append(Paragraph(content1_2, styles['BodyText']))
    story.append(PageBreak())

    # Section 2
    story.append(Paragraph("<b>2. Personnel Safety in Cold Weather</b>", styles['Heading1']))
    story.append(Spacer(1, 0.2*inch))

    content2 = """
    Cold weather poses significant risks to personnel including frostbite, hypothermia,
    and reduced dexterity. Proper procedures and PPE are essential.
    """
    story.append(Paragraph(content2, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("<b>2.1 Work/Rest Cycles in Extreme Cold</b>", styles['Heading2']))
    content2_1 = """
    When operating in extreme cold (wind chill below 0°F), implement work/rest cycles:<br/><br/>
    • 0°F to -10°F: 50 minutes work, 10 minutes warm-up break<br/>
    • -10°F to -20°F: 40 minutes work, 20 minutes warm-up break<br/>
    • -20°F to -30°F: 30 minutes work, 30 minutes warm-up break<br/>
    • Below -30°F: Suspend non-essential outdoor operations<br/>
    <br/>
    Warm-up breaks must be in heated shelter. Supervisors must monitor personnel for
    signs of cold stress. See Safety Guidelines 2024 Section 1.2 for cold weather PPE requirements.
    """
    story.append(Paragraph(content2_1, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("<b>2.2 Frostbite Recognition and Response</b>", styles['Heading2']))
    content2_2 = """
    Frostbite symptoms include:<br/><br/>
    • Numbness or tingling in extremities<br/>
    • Skin appears white, waxy, or grayish<br/>
    • Skin feels hard or unusually firm<br/>
    • Loss of dexterity in fingers or toes<br/>
    <br/>
    Immediate response:<br/><br/>
    1. Move person to warm environment<br/>
    2. Remove wet clothing and replace with dry garments<br/>
    3. Warm affected area gradually with body heat or warm water (98-105°F)<br/>
    4. Do NOT rub frozen tissue - can cause permanent damage<br/>
    5. Seek medical attention immediately for anything beyond superficial frostbite<br/>
    6. Do NOT allow refreezing of thawed tissue<br/>
    <br/>
    Prevention is critical - ensure all personnel have proper cold weather gear and monitor
    buddy system for early warning signs.
    """
    story.append(Paragraph(content2_2, styles['BodyText']))
    story.append(PageBreak())

    # Section 3
    story.append(Paragraph("<b>3. Winter Maintenance Considerations</b>", styles['Heading1']))
    story.append(Spacer(1, 0.2*inch))

    content3 = """
    Maintenance activities in cold weather require modified procedures and additional precautions.
    """
    story.append(Paragraph(content3, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("<b>3.1 Cold Weather Maintenance Safety</b>", styles['Heading2']))
    content3_1 = """
    Special considerations for winter maintenance:<br/><br/>
    • Metal tools and parts can cause instant frostbite - wear appropriate gloves<br/>
    • Fluids are more viscous - allow extra time for draining operations<br/>
    • Use heated workspace when possible for detailed repairs<br/>
    • Warm metal parts before torque application to avoid stress fractures<br/>
    • Keep replacement parts at room temperature before installation<br/>
    • Clean ice and snow from work area to prevent slips and falls<br/>
    • Ensure adequate lighting - winter days have reduced daylight hours<br/>
    <br/>
    When maintenance must be performed outdoors, establish windbreaks and use portable
    heaters to create acceptable working environment. Monitor personnel closely for
    cold stress symptoms.
    """
    story.append(Paragraph(content3_1, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("<b>3.2 Inspection Intervals in Cold Weather</b>", styles['Heading2']))
    content3_2 = """
    Increase inspection frequency during winter operations:<br/><br/>
    • Daily fluid level checks - consumption may increase<br/>
    • Battery condition check every 3 days minimum<br/>
    • Tire pressure verification weekly (pressure fluctuates with temperature)<br/>
    • Heating system function test before each use<br/>
    • Ice accumulation inspection on cooling systems and air intakes<br/>
    <br/>
    Refer to Equipment Maintenance Manual Section 1 for complete daily inspection procedures.
    Winter conditions may reveal latent defects not apparent in warmer weather.
    """
    story.append(Paragraph(content3_2, styles['BodyText']))

    doc.build(story)
    print(f"✓ Created: {filename}")


def main():
    """Create all sample documents"""
    print("\n=== Creating Sample Defense Documents ===\n")

    try:
        # Import required library
        from reportlab.lib.pagesizes import letter
        print("✓ ReportLab library found")
    except ImportError:
        print("✗ ReportLab library not found")
        print("\nPlease install it with: pip install reportlab")
        return

    create_equipment_maintenance_manual()
    create_safety_guidelines()
    create_tactical_doctrine()
    create_winter_operations()

    print("\n" + "=" * 50)
    print("Sample documents created successfully!")
    print("=" * 50)
    print("\nDocuments ready for ingestion:")
    print("  1. Equipment Maintenance Manual v3.2 (UNCLASSIFIED)")
    print("  2. Safety Guidelines 2024 (UNCLASSIFIED)")
    print("  3. Tactical Doctrine TD-2023-04 (SECRET - simulated)")
    print("  4. Winter Operations Procedures (UNCLASSIFIED)")
    print("\nNext step: Run 'python ingest_documents.py' to index documents\n")


if __name__ == "__main__":
    main()
