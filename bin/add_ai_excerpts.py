import os
import csv
import traceback
import argparse
from dotenv import load_dotenv
from atlassian import Confluence
import re
import requests

# Load environment variables
load_dotenv()
confluence_username = os.getenv('CONFLUENCE_USERNAME')
confluence_token = os.getenv('ATLASSIAN_TOKEN')

if not confluence_username:
    raise ValueError("CONFLUENCE_USERNAME environment variable is not set")
if not confluence_token:
    raise ValueError("ATLASSIAN_TOKEN environment variable is not set")

# Initialize Confluence client
confluence = Confluence(
    url='https://schrodinger-sandbox.atlassian.net',
    username=confluence_username,
    password=confluence_token
)

def extract_page_id_from_url(url):
    """Extract page ID from Confluence URL."""
    # First try to get it from the URL path
    match = re.search(r'/pages/(\d+)/', url)
    if match:
        return match.group(1)
    
    # If not found in URL, might be an overview page
    # Get space key from URL
    space_match = re.search(r'/spaces/([^/]+)/', url)
    if not space_match:
        raise ValueError(f"Could not extract space key from URL: {url}")
    
    space_key = space_match.group(1)
    # Get the space's overview page
    overview_page = confluence.get_space(space_key).get('homepage')
    if not overview_page:
        raise ValueError(f"Could not find overview page for space: {space_key}")
    
    return overview_page['id']

def has_excerpt_section(content):
    """Check if the content already has an excerpt section."""
    return bool(re.search(r'<ac:structured-macro ac:name="excerpt"', content, re.IGNORECASE))

def extract_excerpt_content(content):
    """Extract the content from an existing excerpt section."""
    match = re.search(r'<ac:structured-macro ac:name="excerpt".*?>(.*?)</ac:structured-macro>', content, re.DOTALL | re.IGNORECASE)
    if match:
        # Clean up any nested HTML/XML tags to get plain text
        excerpt = re.sub(r'<[^>]+>', '', match.group(1))
        return excerpt.strip()
    return None

def create_excerpt_macro(summary):
    """Create a Confluence excerpt macro with the given summary."""
    return f'''<ac:structured-macro ac:name="excerpt">
<ac:rich-text-body>
<p>{summary}</p>
</ac:rich-text-body>
</ac:structured-macro>

'''

def validate_excerpt_content(excerpt):
    """
    Validate if the existing excerpt meets our criteria:
    - Is accurate (assumed from AI summary)
    - Is precise
    - Less than 3 sentences
    """
    if not excerpt:
        return False
    
    # Count sentences (basic implementation)
    sentences = len(re.split(r'[.!?]+', excerpt.strip()))
    return sentences < 3

def create_ai_summary_macro():
    """Create a Confluence Summarize Writing macro."""
    return '<ac:structured-macro ac:name="Summarize writing" />'

def process_page(url, dry_run=False):
    """Process a single Confluence page."""
    try:
        if not confluence_token:
            raise ValueError("ATLASSIAN_TOKEN environment variable is not set")
        page_id = extract_page_id_from_url(url)
        page = confluence.get_page_by_id(page_id, expand='body.storage,version')
        content = page['body']['storage']['value']
        
        if has_excerpt_section(content):
            # Extract and validate existing excerpt
            existing_excerpt = extract_excerpt_content(content)
            if validate_excerpt_content(existing_excerpt):
                print(f"Page {url} has a valid excerpt. Skipping.")
                return
            
            # Remove existing excerpt if it's not valid
            content = re.sub(
                r'<ac:structured-macro ac:name="excerpt".*?</ac:structured-macro>\s*',
                '',
                content,
                flags=re.DOTALL | re.IGNORECASE
            )
            print(f"Removed invalid excerpt from page: {url}")
        
        # Add AI Summary macro at the top
        updated_content = create_ai_summary_macro() + '\n\n' + content
        
        # Update the page
        if dry_run:
            print(f"[DRY RUN] Would update page: {url}")
            print(f"[DRY RUN] Changes to be made:")
            print(f"  - {'Remove invalid excerpt and ' if has_excerpt_section(content) else ''}Add AI Summary macro")
        else:
            confluence.update_page(
                page_id=page_id,
                title=page['title'],
                body=updated_content,
                type='page',
                version_comment='Updated with Confluence AI Summary'
            )
            print(f"Successfully added/updated AI Summary for page: {url}")
        
    except requests.exceptions.HTTPError as e:
        print(f"\nAPI Permission Error for page {url}:")
        print("The Confluence API token lacks required permissions. The token needs:")
        print("- Read and write access to pages")
        print("- Space permissions for the target Confluence spaces")
        print("\nFull error details:")
        traceback.print_exc()
    except Exception as e:
        print(f"\nError processing page {url}:")
        traceback.print_exc()

def main():
    """Main function to process all pages."""
    parser = argparse.ArgumentParser(description='Add AI excerpts to Confluence pages')
    parser.add_argument('--dry-run', action='store_true', help='Simulate changes without making actual updates')
    args = parser.parse_args()

    if args.dry_run:
        print("\n=== DRY RUN MODE - No changes will be made ===\n")

    try:
        with open('configs/pages.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                url = row['url'].strip()
                if url:
                    print(f"\nProcessing: {url}")
                    process_page(url, dry_run=args.dry_run)
    except Exception as e:
        print("Error in main function:")
        traceback.print_exc()

if __name__ == "__main__":
    main()
