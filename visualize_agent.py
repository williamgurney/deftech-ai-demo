"""
Agent Visualization for DefTech AI Document Assistant
Creates a graphical representation of the agent architecture and workflow
"""
from graphviz import Digraph
import os


def create_agent_architecture():
    """Create high-level agent architecture diagram"""
    dot = Digraph('DefTech_Agent_Architecture', comment='DefTech AI Agent Architecture')
    dot.attr(rankdir='TB', size='12,16')
    dot.attr('node', shape='box', style='rounded,filled', fontname='Arial')

    # Define color scheme
    colors = {
        'user': '#E3F2FD',
        'agent': '#BBDEFB',
        'tool': '#90CAF9',
        'data': '#64B5F6',
        'output': '#42A5F5'
    }

    # User layer
    with dot.subgraph(name='cluster_user') as c:
        c.attr(style='filled', color='lightgrey', label='User Interface Layer')
        c.node('user_query', 'User Query\n"What is the equipment\ninspection procedure?"',
               fillcolor=colors['user'])

    # Agent layer
    with dot.subgraph(name='cluster_agent') as c:
        c.attr(style='filled', color='lightblue', label='Agent Layer (Cohere Command-R+)')
        c.node('agent_init', 'Initialize Agent\n(Load tools & context)', fillcolor=colors['agent'])
        c.node('agent_plan', 'Plan Action\n(Decide which tools to use)', fillcolor=colors['agent'])
        c.node('agent_execute', 'Execute Tools\n(Call selected tools)', fillcolor=colors['agent'])
        c.node('agent_synthesize', 'Synthesize Answer\n(Combine results)', fillcolor=colors['agent'])
        c.node('agent_cite', 'Add Citations\n(Link to sources)', fillcolor=colors['agent'])

    # Tools layer
    with dot.subgraph(name='cluster_tools') as c:
        c.attr(style='filled', color='lightgreen', label='Tools Layer')
        c.node('tool_search_manuals', 'search_manuals\n(Query, Manual Type)',
               fillcolor=colors['tool'], shape='component')
        c.node('tool_search_doctrine', 'search_doctrine\n(Query, Doctrine Area)',
               fillcolor=colors['tool'], shape='component')
        c.node('tool_log_access', 'log_access\n(Doc ID, User, Classification)',
               fillcolor=colors['tool'], shape='component')

    # Data layer
    with dot.subgraph(name='cluster_data') as c:
        c.attr(style='filled', color='lightyellow', label='Data Layer')
        c.node('embed', 'Cohere Embed v3\n(Generate embeddings)',
               fillcolor=colors['data'], shape='cylinder')
        c.node('qdrant', 'Qdrant Vector DB\n(16 document chunks)',
               fillcolor=colors['data'], shape='cylinder')
        c.node('audit_log', 'Audit Logs\n(JSON files)',
               fillcolor=colors['data'], shape='cylinder')

    # Output layer
    with dot.subgraph(name='cluster_output') as c:
        c.attr(style='filled', color='lightgrey', label='Output Layer')
        c.node('result', 'Answer with Citations\n+ Audit Logs', fillcolor=colors['output'])

    # Flow connections
    dot.edge('user_query', 'agent_init', label='1')
    dot.edge('agent_init', 'agent_plan', label='2')
    dot.edge('agent_plan', 'agent_execute', label='3')

    # Tool execution branches
    dot.edge('agent_execute', 'tool_search_manuals', label='3a')
    dot.edge('agent_execute', 'tool_search_doctrine', label='3b')
    dot.edge('agent_execute', 'tool_log_access', label='3c')

    # Tool to data connections
    dot.edge('tool_search_manuals', 'embed', label='Embed query')
    dot.edge('tool_search_doctrine', 'embed', label='Embed query')
    dot.edge('embed', 'qdrant', label='Search')
    dot.edge('tool_log_access', 'audit_log', label='Write')

    # Data to agent
    dot.edge('qdrant', 'agent_synthesize', label='Results')
    dot.edge('audit_log', 'agent_synthesize', label='Logs')

    # Final steps
    dot.edge('agent_synthesize', 'agent_cite', label='4')
    dot.edge('agent_cite', 'result', label='5')

    return dot


def create_tool_workflow():
    """Create detailed tool workflow diagram"""
    dot = Digraph('DefTech_Tool_Workflow', comment='Tool Workflow')
    dot.attr(rankdir='LR', size='14,8')
    dot.attr('node', shape='box', style='rounded,filled', fontname='Arial')

    # Search Manuals workflow
    with dot.subgraph(name='cluster_search_manuals') as c:
        c.attr(style='filled', color='#E8F5E9', label='search_manuals Workflow')
        c.node('sm_input', 'Input:\n- query\n- manual_type', fillcolor='#C8E6C9')
        c.node('sm_embed', 'Embed Query\n(Cohere v3)', fillcolor='#A5D6A7')
        c.node('sm_filter', 'Filter:\ndocument_type="manual"\nmanual_type=?', fillcolor='#81C784')
        c.node('sm_search', 'Vector Search\n(Top 5 results)', fillcolor='#66BB6A')
        c.node('sm_output', 'Output:\n- manual_name\n- page\n- text\n- classification', fillcolor='#4CAF50')

    dot.edge('sm_input', 'sm_embed')
    dot.edge('sm_embed', 'sm_filter')
    dot.edge('sm_filter', 'sm_search')
    dot.edge('sm_search', 'sm_output')

    # Search Doctrine workflow
    with dot.subgraph(name='cluster_search_doctrine') as c:
        c.attr(style='filled', color='#E3F2FD', label='search_doctrine Workflow')
        c.node('sd_input', 'Input:\n- query\n- doctrine_area', fillcolor='#BBDEFB')
        c.node('sd_embed', 'Embed Query\n(Cohere v3)', fillcolor='#90CAF9')
        c.node('sd_filter', 'Filter:\ndocument_type="doctrine"\ndoctrine_area=?', fillcolor='#64B5F6')
        c.node('sd_search', 'Vector Search\n(Top 5 results)', fillcolor='#42A5F5')
        c.node('sd_output', 'Output:\n- manual_name\n- page\n- text\n- classification', fillcolor='#2196F3')

    dot.edge('sd_input', 'sd_embed')
    dot.edge('sd_embed', 'sd_filter')
    dot.edge('sd_filter', 'sd_search')
    dot.edge('sd_search', 'sd_output')

    # Log Access workflow
    with dot.subgraph(name='cluster_log_access') as c:
        c.attr(style='filled', color='#FFF3E0', label='log_access Workflow')
        c.node('la_input', 'Input:\n- document_id\n- user_id\n- classification', fillcolor='#FFE0B2')
        c.node('la_validate', 'Validate\nClassification', fillcolor='#FFCC80')
        c.node('la_generate', 'Generate\nAudit ID', fillcolor='#FFB74D')
        c.node('la_write', 'Write to\nAudit Log', fillcolor='#FFA726')
        c.node('la_output', 'Output:\n- audit_id\n- timestamp\n- success', fillcolor='#FF9800')

    dot.edge('la_input', 'la_validate')
    dot.edge('la_validate', 'la_generate')
    dot.edge('la_generate', 'la_write')
    dot.edge('la_write', 'la_output')

    return dot


def create_multi_step_example():
    """Create example of multi-step agent execution"""
    dot = Digraph('DefTech_MultiStep_Example', comment='Multi-Step Agent Example')
    dot.attr(rankdir='TB', size='10,14')
    dot.attr('node', shape='box', style='rounded,filled', fontname='Arial')

    # Query
    dot.node('query', 'User Query:\n"What are safety protocols for\nwinter maintenance?"',
             fillcolor='#FFF9C4', shape='note')

    # Step 1
    with dot.subgraph(name='cluster_step1') as c:
        c.attr(style='filled', color='#E8F5E9', label='Step 1: Plan')
        c.node('s1_analyze', 'Agent Analyzes Query\n- Identifies "safety"\n- Identifies "winter"',
               fillcolor='#C8E6C9')
        c.node('s1_decide', 'Decides: Need to search\nsafety AND winter docs', fillcolor='#A5D6A7')

    dot.edge('query', 's1_analyze')
    dot.edge('s1_analyze', 's1_decide')

    # Step 2
    with dot.subgraph(name='cluster_step2') as c:
        c.attr(style='filled', color='#E3F2FD', label='Step 2: Execute Tools')
        c.node('s2_tool1', 'Call: search_manuals\n(query="safety", type="safety")',
               fillcolor='#BBDEFB')
        c.node('s2_tool2', 'Call: search_manuals\n(query="winter", type="operations")',
               fillcolor='#90CAF9')

    dot.edge('s1_decide', 's2_tool1')
    dot.edge('s1_decide', 's2_tool2')

    # Step 3
    with dot.subgraph(name='cluster_step3') as c:
        c.attr(style='filled', color='#F3E5F5', label='Step 3: Process Results')
        c.node('s3_results', 'Received:\n- 5 safety doc chunks\n- 5 winter ops chunks',
               fillcolor='#E1BEE7')
        c.node('s3_analyze', 'Analyze Overlap\n& Relevance', fillcolor='#CE93D8')

    dot.edge('s2_tool1', 's3_results')
    dot.edge('s2_tool2', 's3_results')
    dot.edge('s3_results', 's3_analyze')

    # Step 4
    with dot.subgraph(name='cluster_step4') as c:
        c.attr(style='filled', color='#FFF3E0', label='Step 4: Synthesize')
        c.node('s4_combine', 'Combine Information\nfrom Both Sources', fillcolor='#FFE0B2')
        c.node('s4_cite', 'Add Citations:\n- Safety Guidelines p.2\n- Winter Ops p.4',
               fillcolor='#FFCC80')

    dot.edge('s3_analyze', 's4_combine')
    dot.edge('s4_combine', 's4_cite')

    # Final answer
    dot.node('answer', 'Final Answer:\n"For winter maintenance:\n1. Wear insulated PPE\n2. Work/rest cycles\n3. Monitor for frostbite\n\n[Citations included]"',
             fillcolor='#C8E6C9', shape='note')

    dot.edge('s4_cite', 'answer')

    return dot


def create_data_flow():
    """Create data flow diagram"""
    dot = Digraph('DefTech_Data_Flow', comment='Data Flow')
    dot.attr(rankdir='LR', size='14,10')
    dot.attr('node', fontname='Arial')

    # Input
    dot.node('pdf_docs', 'PDF Documents\n(4 manuals)', shape='folder', fillcolor='#FFECB3', style='filled')

    # Processing
    dot.node('extract', 'Extract Text\n(PyPDF2)', shape='box', fillcolor='#E1F5FE', style='filled')
    dot.node('chunk', 'Chunk Text\n(~500 tokens)', shape='box', fillcolor='#B3E5FC', style='filled')
    dot.node('embed', 'Generate Embeddings\n(Cohere Embed v3)', shape='box', fillcolor='#81D4FA', style='filled')

    # Storage
    dot.node('qdrant', 'Qdrant Vector DB\n(16 chunks)\n1024 dimensions',
             shape='cylinder', fillcolor='#4FC3F7', style='filled')

    # Query time
    dot.node('user_q', 'User Query', shape='note', fillcolor='#FFF59D', style='filled')
    dot.node('q_embed', 'Embed Query\n(Cohere Embed v3)', shape='box', fillcolor='#81D4FA', style='filled')
    dot.node('search', 'Similarity Search\n(Cosine distance)', shape='box', fillcolor='#4FC3F7', style='filled')
    dot.node('results', 'Top 5 Results', shape='box', fillcolor='#C8E6C9', style='filled')
    dot.node('agent', 'Agent Synthesis', shape='box', fillcolor='#A5D6A7', style='filled')
    dot.node('answer', 'Final Answer', shape='note', fillcolor='#81C784', style='filled')

    # Ingestion flow
    dot.edge('pdf_docs', 'extract', label='Load')
    dot.edge('extract', 'chunk', label='Split')
    dot.edge('chunk', 'embed', label='Vectorize')
    dot.edge('embed', 'qdrant', label='Store')

    # Query flow
    dot.edge('user_q', 'q_embed', label='1')
    dot.edge('q_embed', 'search', label='2')
    dot.edge('qdrant', 'search', label='Search in', style='dashed')
    dot.edge('search', 'results', label='3')
    dot.edge('results', 'agent', label='4')
    dot.edge('agent', 'answer', label='5')

    return dot


def main():
    """Generate all visualizations"""
    output_dir = './visualizations'
    os.makedirs(output_dir, exist_ok=True)

    print("Generating Agent Visualizations...")
    print("=" * 60)

    # Generate architecture diagram
    print("\n1. Agent Architecture Diagram...")
    arch = create_agent_architecture()
    arch.render(f'{output_dir}/01_agent_architecture', format='png', cleanup=True)
    print(f"   ✓ Saved: {output_dir}/01_agent_architecture.png")

    # Generate tool workflow
    print("\n2. Tool Workflow Diagram...")
    tools = create_tool_workflow()
    tools.render(f'{output_dir}/02_tool_workflow', format='png', cleanup=True)
    print(f"   ✓ Saved: {output_dir}/02_tool_workflow.png")

    # Generate multi-step example
    print("\n3. Multi-Step Example Diagram...")
    multi = create_multi_step_example()
    multi.render(f'{output_dir}/03_multistep_example', format='png', cleanup=True)
    print(f"   ✓ Saved: {output_dir}/03_multistep_example.png")

    # Generate data flow
    print("\n4. Data Flow Diagram...")
    data = create_data_flow()
    data.render(f'{output_dir}/04_data_flow', format='png', cleanup=True)
    print(f"   ✓ Saved: {output_dir}/04_data_flow.png")

    print("\n" + "=" * 60)
    print("✓ All visualizations generated successfully!")
    print(f"\nView them in: {output_dir}/")
    print("\nGenerated files:")
    print("  1. 01_agent_architecture.png - High-level agent architecture")
    print("  2. 02_tool_workflow.png - Detailed tool workflows")
    print("  3. 03_multistep_example.png - Example of multi-step reasoning")
    print("  4. 04_data_flow.png - Document ingestion and query flow")

    # Also generate SVG for better quality
    print("\nGenerating SVG versions (scalable)...")
    arch.render(f'{output_dir}/01_agent_architecture', format='svg', cleanup=True)
    tools.render(f'{output_dir}/02_tool_workflow', format='svg', cleanup=True)
    multi.render(f'{output_dir}/03_multistep_example', format='svg', cleanup=True)
    data.render(f'{output_dir}/04_data_flow', format='svg', cleanup=True)
    print("✓ SVG versions saved (better for presentations)")


if __name__ == "__main__":
    main()
