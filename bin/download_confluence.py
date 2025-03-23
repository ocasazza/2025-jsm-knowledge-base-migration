#!/usr/bin/env python3
import os
import re
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
confluence_url = os.getenv('CONFLUENCE_URL')

print(f"Username: {confluence_username}")
print(f"Token: {'*' * (len(confluence_token) if confluence_token else 0)}")
print(f"URL: {confluence_url}")

if not confluence_username:
    raise ValueError("CONFLUENCE_USERNAME environment variable is not set")
if not confluence_token:
    raise ValueError("ATLASSIAN_TOKEN environment variable is not set")

# Initialize Confluence client
confluence = Confluence(
    url=confluence_url,
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

def build_path_from_ancestors(base_dir, ancestors):
    """Build a path from the base directory and ancestors."""
    if not ancestors:
        return base_dir
    
    path = base_dir
    for ancestor in ancestors:
        ancestor_title = ancestor.get('title', 'Unknown')
        path = path / sanitize_filename(ancestor_title)
    
    return path

def save_page_content(page_id, base_dir, progress_file, current_depth=0, max_depth=10, processed_ids=None, parent_dir=None):
    """
    Recursively save page content and its children.
    Returns a tuple of (success, title)
    
    Parameters:
    - page_id: ID of the page to process
    - base_dir: Base directory for all content
    - progress_file: File to track processed pages
    - current_depth: Current recursion depth
    - max_depth: Maximum recursion depth
    - processed_ids: Set of already processed page IDs
    - parent_dir: Directory of the parent page (used for proper nesting)
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
                expand='body.storage,children.page,version,space,ancestors'
            )
            
            print(f"{'  ' * current_depth}Skipping already processed page: {page_id} - Title: {page.get('title', 'Unknown')}")
            
            # Process children before returning
            children = page.get('children', {}).get('page', {}).get('results', [])
            total_children = len(children)
            
            # Use the correct parent directory for children
            if parent_dir:
                current_page_dir = parent_dir / sanitize_filename(page.get('title', 'Unknown'))
            else:
                # If no parent_dir is provided, check if we have ancestors to determine the path
                ancestors = page.get('ancestors', [])
                if ancestors:
                    # Build the path based on ancestors
                    parent_path = build_path_from_ancestors(base_dir, ancestors)
                    current_page_dir = parent_path / sanitize_filename(page.get('title', 'Unknown'))
                else:
                    # If no ancestors, use base_dir (root level page)
                    current_page_dir = base_dir / sanitize_filename(page.get('title', 'Unknown'))
            
            for i, child in enumerate(children, 1):
                print(f"{'  ' * (current_depth + 1)}Processing child {i}/{total_children} - ID: {child['id']} - Title: {child.get('title', 'Unknown')}")
                save_page_content(
                    child['id'], 
                    base_dir,
                    progress_file,
                    current_depth + 1, 
                    max_depth,
                    processed_ids,
                    current_page_dir  # Pass the current page directory as parent_dir for children
                )
            return True, None
        
        # Add rate limiting
        time.sleep(1)  # Wait 1 second between API calls
        
        # Get page content with ancestors
        page = confluence.get_page_by_id(
            page_id, 
            expand='body.storage,children.page,version,space,ancestors'
        )
        
        title = page['title']
        
        # Get ancestors information
        ancestors = page.get('ancestors', [])
        
        # Determine the correct directory for this page
        if parent_dir is not None:
            # If parent_dir is provided, use it as the base for this page's directory
            page_dir = parent_dir / sanitize_filename(title)
        else:
            # If no parent_dir is provided, check if we have ancestors to determine the path
            if ancestors:
                # Build the path based on ancestors
                parent_path = build_path_from_ancestors(base_dir, ancestors)
                
                # Add the current page to the path
                page_dir = parent_path / sanitize_filename(title)
            else:
                # If no ancestors, use base_dir (root level page)
                page_dir = base_dir / sanitize_filename(title)
        
        # Debug: Print the path that will be used for this page
        print(f"{'  ' * current_depth}Page path: {page_dir}")
        
        # Check if page needs updating
        should_update, current_version = needs_update(page_id, page_dir)
        
        if not should_update:
            print(f"{'  ' * current_depth}Skipping up-to-date page: {title}")
            processed_ids.add(page_id)
            
            # Still process children even if parent is up to date
            children = page.get('children', {}).get('page', {}).get('results', [])
            total_children = len(children)
            for i, child in enumerate(children, 1):
                print(f"{'  ' * (current_depth + 1)}Processing child {i}/{total_children} - ID: {child['id']} - Title: {child.get('title', 'Unknown')}")
                
                save_page_content(
                    child['id'], 
                    base_dir,
                    progress_file,
                    current_depth + 1, 
                    max_depth,
                    processed_ids,
                    page_dir  # Pass the current page directory as parent_dir for children
                )
            return True, title
        
        print(f"{'  ' * current_depth}Processing: {title}")
        
        # Create directory for this page
        try:
            page_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"{'  ' * current_depth}ERROR: Failed to create directory {page_dir}: {str(e)}")
            return False, None
        
        # Save page metadata
        metadata = {
            'id': page['id'],
            'title': title,
            'version': page['version']['number'],
            'space_key': page['space']['key']
        }
        
        # Add parent ID to metadata if available
        if ancestors and len(ancestors) > 0:
            parent = ancestors[-1]  # Last ancestor is the immediate parent
            metadata['parent_id'] = parent.get('id', 'Unknown')
            metadata['parent_title'] = parent.get('title', 'Unknown')
        
        try:
            with open(page_dir / 'metadata.txt', 'w', encoding='utf-8') as f:
                for key, value in metadata.items():
                    f.write(f"{key}: {value}\n")
        except Exception as e:
            print(f"{'  ' * current_depth}ERROR: Failed to save metadata: {str(e)}")
        
        # Save page content
        try:
            content = page['body']['storage']['value']
            cleaned_content = clean_html_content(content)
            
            with open(page_dir / 'content.html', 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
        except Exception as e:
            print(f"{'  ' * current_depth}ERROR: Failed to save content: {str(e)}")
        
        # Download attachments
        try:
            download_attachments(page_id, page_dir)
        except Exception as e:
            print(f"{'  ' * current_depth}ERROR: Failed to download attachments: {str(e)}")
        
        # Save progress
        save_progress(progress_file, page_id)
        processed_ids.add(page_id)
        
        # Process child pages
        children = page.get('children', {}).get('page', {}).get('results', [])
        total_children = len(children)
        
        for i, child in enumerate(children, 1):
            child_title = child.get('title', 'Unknown')
            child_id = child['id']
            print(f"{'  ' * (current_depth + 1)}Processing child {i}/{total_children} - ID: {child_id} - Title: {child_title}")
            
            save_page_content(
                child_id, 
                base_dir,
                progress_file,
                current_depth + 1, 
                max_depth,
                processed_ids,
                page_dir  # Pass the current page directory as parent_dir for children
            )
        
        return True, title
        
    except RequestException as e:
        print(f"Network error processing page {page_id}: {str(e)}")
        print("Retrying in 5 seconds...")
        time.sleep(5)
        return save_page_content(page_id, base_dir, progress_file, current_depth, max_depth, processed_ids, parent_dir)
    except Exception as e:
        print(f"Error processing page {page_id}: {str(e)}")
        return False, None

def get_all_page_ids(page_id, collected_ids=None):
    """
    Recursively get all page IDs under a given page.
    Returns a set of page IDs.
    """
    if collected_ids is None:
        collected_ids = set()
    
    # Add the current page ID
    collected_ids.add(page_id)
    
    try:
        # Get the page with its children
        page = confluence.get_page_by_id(
            page_id, 
            expand='children.page'
        )
        
        # Process children
        children = page.get('children', {}).get('page', {}).get('results', [])
        for child in children:
            child_id = child['id']
            # Recursively get all page IDs under this child
            get_all_page_ids(child_id, collected_ids)
    except Exception as e:
        print(f"Error getting page IDs for {page_id}: {str(e)}")
    
    return collected_ids

def get_all_space_page_ids(space_key):
    """
    Get all page IDs in a space, including orphaned pages.
    Returns a set of page IDs.
    """
    all_page_ids = set()
    start = 0
    limit = 100
    
    while True:
        try:
            # Get a batch of pages from the space
            pages = confluence.get_all_pages_from_space(space_key, start=start, limit=limit)
            
            if not pages:
                break
                
            # Add page IDs to the set
            for page in pages:
                all_page_ids.add(page['id'])
                
            # If we got fewer pages than the limit, we've reached the end
            if len(pages) < limit:
                break
                
            # Move to the next batch
            start += limit
            
        except Exception as e:
            print(f"Error getting all pages from space {space_key}: {str(e)}")
            break
    
    return all_page_ids

def get_local_page_ids(base_dir):
    """
    Get all page IDs from local metadata files.
    Returns a dictionary mapping page IDs to their local directory paths.
    """
    local_pages = {}
    
    # Walk through all directories under base_dir
    for root, dirs, files in os.walk(base_dir):
        root_path = Path(root)
        
        # Check if this directory has a metadata file
        metadata_file = root_path / 'metadata.txt'
        if metadata_file.exists():
            try:
                with open(metadata_file, 'r') as f:
                    for line in f:
                        if line.startswith('id:'):
                            page_id = line.split(':')[1].strip()
                            local_pages[page_id] = root_path
                            break
            except Exception as e:
                print(f"Error reading metadata file {metadata_file}: {str(e)}")
    
    return local_pages

def main():
    try:
        # Create base directory for all content
        base_dir = Path('./confluence_content')
        base_dir.mkdir(exist_ok=True)
        
        # Create progress file
        progress_file = base_dir / 'progress.txt'
        
        print("Starting Confluence content download...")
        print(f"Base directory: {base_dir.absolute()}")
        print(f"Progress file: {progress_file}")
        
        # Start URL
        start_url = "https://schrodinger-sandbox.atlassian.net/wiki/spaces/ITLC/pages/196542469/IT+Knowledge+Base"
        
        # Extract and process the root page
        root_page_id = extract_page_id_from_url(start_url)
        if not root_page_id:
            print("Could not extract page ID from URL")
            return
        
        print(f"Root page ID: {root_page_id}")
        
        # Get space key from the root page
        root_page = confluence.get_page_by_id(root_page_id, expand='space')
        space_key = root_page['space']['key']
        print(f"Space key: {space_key}")
        
        # Get all page IDs in the space
        print("Getting all page IDs in the space...")
        all_space_page_ids = get_all_space_page_ids(space_key)
        print(f"Found {len(all_space_page_ids)} pages in space {space_key}")
        
        # Get all page IDs under the root page
        print("Getting all page IDs under the root page...")
        root_tree_page_ids = get_all_page_ids(root_page_id)
        print(f"Found {len(root_tree_page_ids)} pages under the root page")
        
        # Find orphaned pages (pages in the space but not under the root page)
        orphaned_page_ids = all_space_page_ids - root_tree_page_ids
        print(f"Found {len(orphaned_page_ids)} orphaned pages")
        
        # Load progress
        processed_ids = load_progress(progress_file)
        if processed_ids:
            print(f"Resuming from previous run ({len(processed_ids)} pages already processed)")
        
        # Process the root page and its children
        print("Beginning content download...")
        success, title = save_page_content(root_page_id, base_dir, progress_file, processed_ids=processed_ids)
        
        # Process orphaned pages
        if orphaned_page_ids:
            print("\nProcessing orphaned pages...")
            orphaned_dir = base_dir / "Orphaned_Pages"
            orphaned_dir.mkdir(exist_ok=True)
            
            for i, page_id in enumerate(orphaned_page_ids, 1):
                if page_id in processed_ids:
                    continue
                    
                print(f"Processing orphaned page {i}/{len(orphaned_page_ids)} - ID: {page_id}")
                save_page_content(page_id, orphaned_dir, progress_file, processed_ids=processed_ids)
        
        print(f"\nSuccessfully downloaded content to: {base_dir}")
        
    except Exception as e:
        print(f"\nError in main: {str(e)}")

if __name__ == "__main__":
    main()
