import sys
from pathlib import Path
from bs4 import BeautifulSoup

def find_note_panel(soup):
    """Find and validate a note panel in the soup."""
    adf_ext = soup.find('ac:adf-extension')
    if not adf_ext:
        return None
    
    panel_node = adf_ext.find('ac:adf-node', {'type': 'panel'})
    if not panel_node:
        return None
    
    panel_type = panel_node.find('ac:adf-attribute', {'key': 'panel-type'})
    if not panel_type:
        return None
    
    panel_type_text = panel_type.get_text().strip()
    if panel_type_text != 'note':
        return None
    
    return panel_node

def extract_summary(soup):
    """Extract summary text from ADF panel if it exists."""
    panel_node = find_note_panel(soup)
    if not panel_node:
        return None
        
    # Get the content text
    content = panel_node.find('ac:adf-content')
    if content:
        return ' '.join(content.get_text().strip().split())
    
    # Fallback to panel content if ADF content not found
    fallback = panel_node.find('div', class_='panelContent')
    if fallback:
        return ' '.join(fallback.get_text().strip().split())
        
    return None

def get_page_content(soup):
    """Get the main content of the page excluding the summary."""
    # Remove the summary panel if it exists
    summary = soup.find('ac:adf-extension')
    if summary:
        summary.decompose()
    
    # Get remaining text content
    return ' '.join(soup.get_text().strip().split())

def get_page_structure(soup):
    """Extract page structure information."""
    # Get children macro details
    children_macro = soup.find('ac:structured-macro', {'ac:name': 'children'})
    depth_param = None
    if children_macro:
        depth_elem = children_macro.find('ac:parameter', {'ac:name': 'depth'})
        if depth_elem:
            depth_param = depth_elem.get_text().strip()
    
    # Check for note panel
    panel_node = find_note_panel(soup)
    
    structure = {
        'has_summary': bool(panel_node),
        'has_children_macro': bool(children_macro),
        'children_depth': depth_param,
        'headers': [],
        'macros': []
    }
    
    # Find standard HTML headers
    for header in soup.find_all(['h1', 'h2', 'h3']):
        header_text = header.get_text().strip()
        if header_text:
            structure['headers'].append(header_text)
    
    # Find Confluence macros
    for macro in soup.find_all('ac:structured-macro'):
        macro_name = macro.get('ac:name', '')
        if macro_name and macro_name not in ['children']:  # Exclude children macro as it's tracked separately
            structure['macros'].append(macro_name)
            
    return structure

def extract_key_topics(text):
    """Extract key topics from text using basic NLP-like techniques."""
    # Convert to lowercase and split into words
    words = text.lower().split()
    
    # Remove common stop words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    words = [w for w in words if w not in stop_words]
    
    # Find noun phrases (simplified approach)
    topics = set()
    for i in range(len(words)):
        # Single word topics
        if words[i] not in stop_words and len(words[i]) > 3:
            topics.add(words[i])
        
        # Two word phrases
        if i < len(words) - 1:
            phrase = f"{words[i]} {words[i+1]}"
            if len(phrase) > 7:  # Avoid very short phrases
                topics.add(phrase)
    
    return topics

def analyze_summary(summary, content, soup):
    """
    Analyze if summary accurately reflects content.
    Returns tuple of (is_accurate, list of issues)
    """
    issues = []
    
    # Basic length checks
    if len(summary) < 50:
        issues.append("Summary seems too short to be comprehensive")
    elif len(summary) > 1000:
        issues.append("Summary seems too long - should be more concise")
    
    # Get page structure
    structure = get_page_structure(soup)
    
    # Extract key topics from summary and content
    summary_topics = extract_key_topics(summary)
    content_topics = extract_key_topics(content)
    
    # Check if key topics from summary exist in content
    missing_topics = [topic for topic in summary_topics if not any(topic in c_topic for c_topic in content_topics)]
    if missing_topics:
        issues.append(f"Summary mentions topics not found in content: {', '.join(missing_topics)}")
    
    # Check if major content topics are mentioned in summary
    major_content_topics = set(topic for topic in content_topics 
                             if sum(topic in c for c in content.lower().split('\n')) > 2)
    missing_major_topics = [topic for topic in major_content_topics 
                          if not any(topic in s_topic for s_topic in summary_topics)]
    if missing_major_topics:
        issues.append(f"Content contains major topics not mentioned in summary: {', '.join(missing_major_topics[:3])}")
    
    # For pages using children macro, verify summary reflects page structure
    if structure['has_children_macro']:
        overview_terms = {'overview', 'guide', 'section', 'category', 'topics'}
        has_overview_term = any(term in summary.lower() for term in overview_terms)
        if not has_overview_term:
            issues.append("Summary should indicate this is a parent/overview page with subsections")
        
        # Check if summary mentions depth of content
        depth = structure.get('children_depth')
        if depth and depth != '1':
            depth_terms = {'subsections', 'subtopics', 'subcategories', 'detailed'}
            has_depth_term = any(term in summary.lower() for term in depth_terms)
            if not has_depth_term:
                issues.append(f"Summary should indicate page contains nested content ({depth} levels deep)")
    
    # Check if summary matches page headers
    if structure['headers']:
        header_topics = extract_key_topics(' '.join(structure['headers']))
        missing_headers = [topic for topic in header_topics 
                         if not any(topic in s_topic for s_topic in summary_topics)]
        if missing_headers:
            issues.append(f"Summary doesn't mention major sections: {', '.join(missing_headers)}")
    
    return not bool(issues), issues if issues else ["Summary appears to accurately reflect the page content"]

def check_page_summary(html_path):
    """Check if page has a summary and analyze its accuracy."""
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Create two copies of the soup - one for structure analysis and one for content
        soup_structure = BeautifulSoup(content, 'html.parser')
        soup_content = BeautifulSoup(content, 'html.parser')
            
        # Extract summary if it exists
        summary = extract_summary(soup_structure)
        if not summary:
            print("❌ No summary found at top of page")
            print("\nSuggested summary structure:")
            print("-" * 80)
            print("<ac:adf-extension>")
            print("  <ac:adf-node type=\"panel\">")
            print("    <ac:adf-attribute key=\"panel-type\">note</ac:adf-attribute>")
            print("    <ac:adf-content>")
            print("      <p>Add a comprehensive summary here that describes the purpose and content of this page...</p>")
            print("    </ac:adf-content>")
            print("  </ac:adf-node>")
            print("</ac:adf-extension>")
            return
            
        print("\n📝 Found summary:")
        print("-" * 80)
        print(summary)
        print("-" * 80)
        
        # Get main content (using separate soup)
        content = get_page_content(soup_content)
        
        # Analyze summary (using structure soup)
        is_accurate, messages = analyze_summary(summary, content, soup_structure)
        print("\n🔍 Analysis:")
        for msg in messages:
            print(f"{'✅' if is_accurate else '❌'} {msg}")
        
        # Print page structure (using structure soup)
        structure = get_page_structure(soup_structure)
        print("\n📋 Page structure:")
        print(f"{'✅' if structure['has_summary'] else '❌'} Has summary")
        print(f"{'📚' if structure['has_children_macro'] else '📄'} {'Parent page with children' if structure['has_children_macro'] else 'Content page'}")
        if structure['children_depth']:
            print(f"  ↳ Children macro depth: {structure['children_depth']}")
        if structure['headers']:
            print("\n📑 Page headers:")
            for header in structure['headers']:
                print(f"  • {header}")
        if structure['macros']:
            print("\n🔧 Confluence macros used:")
            for macro in structure['macros']:
                print(f"  • {macro}")
        
    except Exception as e:
        print(f"Error processing {html_path}: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_summary.py <path/to/content.html>")
        sys.exit(1)
        
    html_path = Path(sys.argv[1])
    if not html_path.exists():
        print(f"File not found: {html_path}")
        sys.exit(1)
        
    check_page_summary(html_path)
