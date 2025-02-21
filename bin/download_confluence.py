import os
import re
import html
import time
from pathlib import Path
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from atlassian import Confluence
from requests.exceptions import RequestException

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

def sanitize_filename(title):
    """Convert a title to a valid filename."""
    # Replace invalid filename characters with underscores
    filename = re.sub(r'[<>:"/\\|?*]', '_', title)
    # Remove leading/trailing spaces and dots
    filename = filename.strip('. ')
    return filename

def extract_page_id_from_url(url):
    """Extract page ID from Confluence URL."""
    match = re.search(r'/pages/(\d+)/', url)
    if match:
        return match.group(1)
    return None

def clean_html_content(html_content):
    """Clean and format HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove any script tags
    for script in soup.find_all('script'):
        script.decompose()
        
    # Remove any style tags
    for style in soup.find_all('style'):
        style.decompose()
    
    # Format the HTML with proper indentation
    return soup.prettify()

def download_attachments(page_id, save_dir):
    """Download all attachments for a page."""
    try:
        attachments_dir = save_dir / 'attachments'
        attachments_dir.mkdir(exist_ok=True)
        
        attachments = confluence.get_attachments_from_content(page_id)
        
        # Save attachment metadata
        with open(attachments_dir / 'attachments.txt', 'w', encoding='utf-8') as f:
            for attachment in attachments.get('results', []):
                f.write(f"Title: {attachment['title']}\n")
                f.write(f"ID: {attachment['id']}\n")
                f.write(f"MediaType: {attachment.get('metadata', {}).get('mediaType', 'unknown')}\n")
                f.write(f"Comment: {attachment.get('comment', '')}\n")
                f.write(f"Created: {attachment.get('created', '')}\n")
                f.write("-" * 80 + "\n")
                
    except Exception as e:
        print(f"Error processing attachments: {str(e)}")

def load_progress(progress_file):
    """Load previously processed page IDs from progress file."""
    processed = set()
    if progress_file.exists():
        with open(progress_file, 'r') as f:
            processed = set(line.strip() for line in f)
    return processed

def save_progress(progress_file, page_id):
    """Save processed page ID to progress file."""
    with open(progress_file, 'a') as f:
        f.write(f"{page_id}\n")

def get_local_version(page_dir):
    """Get the version number from local metadata file."""
    try:
        metadata_file = page_dir / 'metadata.txt'
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                for line in f:
                    if line.startswith('version:'):
                        return int(line.split(':')[1].strip())
    except Exception:
        pass
    return None

def needs_update(page_id, page_dir):
    """Check if a page needs to be updated based on version."""
    try:
        # If directory doesn't exist, needs update
        if not page_dir.exists():
            return True, None
            
        # Get local version
        local_version = get_local_version(page_dir)
        if local_version is None:
            return True, None
            
        # Get current version from Confluence
        page = confluence.get_page_by_id(page_id, expand='version')
        current_version = page['version']['number']
        
        return current_version != local_version, current_version
        
    except Exception as e:
        print(f"Error checking version for {page_id}: {str(e)}")
        return True, None

def save_page_content(page_id, base_dir, progress_file, current_depth=0, max_depth=10, processed_ids=None):
    """
    Recursively save page content and its children.
    Returns a tuple of (success, title)
    """
    if processed_ids is None:
        processed_ids = set()
    
    if current_depth > max_depth:
        print(f"Maximum depth {max_depth} reached")
        return False, None
    
    try:
        if page_id in processed_ids:
            # Get page to process children even if parent is already processed
            page = confluence.get_page_by_id(
                page_id, 
                expand='body.storage,children.page,version,space'
            )
            
            print(f"{'  ' * current_depth}Skipping already processed page: {page_id}")
            
            # Process children before returning
            children = page.get('children', {}).get('page', {}).get('results', [])
            total_children = len(children)
            for i, child in enumerate(children, 1):
                print(f"{'  ' * (current_depth + 1)}Processing child {i}/{total_children}")
                save_page_content(
                    child['id'], 
                    base_dir,
                    progress_file,
                    current_depth + 1, 
                    max_depth,
                    processed_ids
                )
            return True, None
        # Add rate limiting
        time.sleep(1)  # Wait 1 second between API calls
        
        # Get page content
        page = confluence.get_page_by_id(
            page_id, 
            expand='body.storage,children.page,version,space'
        )
        
        title = page['title']
        page_dir = base_dir / sanitize_filename(title)
        
        # Check if page needs updating
        should_update, current_version = needs_update(page_id, page_dir)
        
        if not should_update:
            print(f"{'  ' * current_depth}Skipping up-to-date page: {title}")
            processed_ids.add(page_id)
            
            # Still process children even if parent is up to date
            children = page.get('children', {}).get('page', {}).get('results', [])
            total_children = len(children)
            for i, child in enumerate(children, 1):
                print(f"{'  ' * (current_depth + 1)}Processing child {i}/{total_children}")
                save_page_content(
                    child['id'], 
                    page_dir,
                    progress_file,
                    current_depth + 1, 
                    max_depth,
                    processed_ids
                )
            return True, title
        
        print(f"{'  ' * current_depth}Processing: {title}")
        
        # Create directory for this page
        page_dir.mkdir(parents=True, exist_ok=True)
        
        # Save page metadata
        metadata = {
            'id': page['id'],
            'title': title,
            'version': page['version']['number'],
            'space_key': page['space']['key']
        }
        
        with open(page_dir / 'metadata.txt', 'w', encoding='utf-8') as f:
            for key, value in metadata.items():
                f.write(f"{key}: {value}\n")
        
        # Save page content
        content = page['body']['storage']['value']
        cleaned_content = clean_html_content(content)
        
        with open(page_dir / 'content.html', 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        
        # Download attachments
        download_attachments(page_id, page_dir)
        
        # Save progress
        save_progress(progress_file, page_id)
        processed_ids.add(page_id)
        
        # Process child pages
        children = page.get('children', {}).get('page', {}).get('results', [])
        total_children = len(children)
        for i, child in enumerate(children, 1):
            print(f"{'  ' * (current_depth + 1)}Processing child {i}/{total_children}")
            save_page_content(
                child['id'], 
                page_dir,
                progress_file,
                current_depth + 1, 
                max_depth,
                processed_ids
            )
        
        return True, title
        
    except RequestException as e:
        print(f"Network error processing page {page_id}: {str(e)}")
        print("Retrying in 5 seconds...")
        time.sleep(5)
        return save_page_content(page_id, base_dir, progress_file, current_depth, max_depth, processed_ids)
    except Exception as e:
        print(f"Error processing page {page_id}: {str(e)}")
        return False, None

def main():
    try:
        # Create base directory for all content
        base_dir = Path('../confluence_content')
        base_dir.mkdir(exist_ok=True)
        
        # Create progress file
        progress_file = base_dir / 'progress.txt'
        
        print("Starting Confluence content download...")
        print("Base directory:", base_dir.absolute())
        print("Progress file:", progress_file)
        
        # Start URL
        start_url = "https://schrodinger-sandbox.atlassian.net/wiki/spaces/ITLC/pages/196542469/IT+Knowledge+Base"
        
        # Extract and process the root page
        root_page_id = extract_page_id_from_url(start_url)
        if not root_page_id:
            print("Could not extract page ID from URL")
            return
        
        print(f"Root page ID: {root_page_id}")
        
        # Load progress
        processed_ids = load_progress(progress_file)
        if processed_ids:
            print(f"Resuming from previous run ({len(processed_ids)} pages already processed)")
        
        print("Beginning content download...")
        success, title = save_page_content(root_page_id, base_dir, progress_file, processed_ids=processed_ids)
        
        if success:
            print(f"\nSuccessfully downloaded content to: {base_dir}")
        else:
            print("\nErrors occurred during download")
            
    except Exception as e:
        print(f"\nError in main: {str(e)}")

if __name__ == "__main__":
    main()
