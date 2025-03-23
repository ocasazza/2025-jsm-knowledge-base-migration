# Confluence Page Splitting Template

This template describes the process of splitting a Confluence page into multiple subpages with proper formatting and organization. It can be used with Cline to automate the process of creating structured documentation from a single FAQ page.

## Overview

The process involves:
1. Identifying the sections/questions in the source page
2. Creating individual subpages for each section/question
3. Adding user story excerpts to each subpage
4. Organizing the main page with a table of contents and links to subpages

## Required Parameters

To use this template, you'll need to provide:

- `source_page_id`: The ID of the source Confluence page to split
- `space_key`: The Confluence space key (e.g., "ITLC")

## Process Steps

### 1. Create Individual Subpages

For each category in the main page, create a subpage with the following structure:

```
<use_mcp_tool>
<server_name>mcp-atlassian</server_name>
<tool_name>confluence_create_page</tool_name>
<arguments>
{
  "space_key": "[SPACE_KEY]",
  "title": "[CATEGORY_TITLE]",
  "content": "[CATEGORY_CONTENT]\n\nstory\n\n[USER_STORY]",
  "parent_id": "[SOURCE_PAGE_ID]"
}
</arguments>
</use_mcp_tool>
```

### 2. Update the Main Page

After creating all subpages, update the main page with a table of contents and organized links to the subpages:

```
<use_mcp_tool>
<server_name>mcp-atlassian</server_name>
<tool_name>confluence_update_page</tool_name>
<arguments>
{
  "page_id": "[SOURCE_PAGE_ID]",
  "title": "[MAIN_PAGE_TITLE]",
  "content": "# [MAIN_PAGE_TITLE]\n\n[INTRODUCTION_TEXT]\n\n## Table of Contents\n\n| Category | Description |\n|----------|-------------|\n[TABLE_OF_CONTENTS_ROWS]\n\n[CATEGORY_SECTIONS]",
  "is_minor_edit": false
}
</arguments>
</use_mcp_tool>
```

## Formatting Guidelines

### User Story Format

The user story should follow this format:
```
<actor role type: (e.g. user or administrator or researcher)> Story

As a [role], I need to [action/capability] so I can [benefit/outcome].
```

This format will be rendered as an excerpt macro in Confluence.

It is critical that this is added to the bottom most part of the page as a confluence macro. The MCP can only add the macro by editing the page via storage xml format and add the excerpt macro. The macro should have both the "hidden" and "name" paramaters 

### Table of Contents Format

Each row in the table of contents should link to the corresponding section:
```
| [Category Name](https://[CONFLUENCE_URL]/wiki/spaces/[SPACE_KEY]/pages/[SOURCE_PAGE_ID]#[category-anchor]) | [Category Description] |
```

### Category Sections Format

Each category section should include:
```
## [Category Name]

- [Question 1 Title](https://[CONFLUENCE_URL]/wiki/spaces/[SPACE_KEY]/pages/[SUBPAGE_ID_1])
- [Question 2 Title](https://[CONFLUENCE_URL]/wiki/spaces/[SPACE_KEY]/pages/[SUBPAGE_ID_2])
- ...
```

## Example Implementation

Here's an example of how to implement this template:

### 1. Create a Subpage

```
<use_mcp_tool>
<server_name>mcp-atlassian</server_name>
<tool_name>confluence_create_page</tool_name>
<arguments>
{
  "space_key": "ITLC",
  "title": "How do I check the load on a cluster?",
  "content": "Run \"/nfs/working/sysmgr/sysmgr-repo/scripts/clustutil.pl -u -a\". It will display the current usage of the cluster like this:\n\n```\nOpen GPUs  / Queue\n--------------------\n28    admin.q\n20    cuda.q\n8    small.q\n388 / 416 physical GPUs (93.3%) in use\n32 GPUs currently offline:\n<cluster node>-0-25 <cluster node>-1-1 <cluster node>-1-8 <cluster node>-1-13 \n\nUser      Run GPUs   Pend GPUs\n----------------------------------\nharder      1 4  0 0\njshelley    2 2  0 0\nkim         2 8  0 0\nknight     25 100   54 216\nlebard     25 100  485 1895\nlupyan      4 4  0 0\nlwang      18 72    0 0\nmaier       1 1  0 0\nmondal     12 48    0 0\nmshelley    5 5  0 0\nmurdock     1 4  0 0\nsanders    11 44  129 513\nwarshavi    1 4  0 0\nTOTAL     108 396    668 2624\n```\n\nstory\n\nAs a researcher, I need to know how to check the current load on the cluster so I can understand resource availability and estimate when my jobs might run.",
  "parent_id": "210894876"
}
</arguments>
</use_mcp_tool>
```

### 2. Update the Main Page

```
<use_mcp_tool>
<server_name>mcp-atlassian</server_name>
<tool_name>confluence_update_page</tool_name>
<arguments>
{
  "page_id": "210894876",
  "title": "High Performance Computing FAQ(s)",
  "content": "# FAQ\n\nPlease send your questions to [sysmgr@schrodinger.com](mailto:sysmgr@schrodinger.com).\n\n## Table of Contents\n\n| Category | Description |\n|----------|-------------|\n| [Cluster Information](https://schrodinger-sandbox.atlassian.net/wiki/spaces/ITLC/pages/210894876#cluster-information) | Information about the clusters |\n| [Queue and Job Management](https://schrodinger-sandbox.atlassian.net/wiki/spaces/ITLC/pages/210894876#queue-and-job-management) | Managing jobs and queues |\n| [Cluster Usage and Commands](https://schrodinger-sandbox.atlassian.net/wiki/spaces/ITLC/pages/210894876#cluster-usage-and-commands) | How to use the clusters |\n\n## Cluster Information\n\n- [Where did the cluster names come from?](https://schrodinger-sandbox.atlassian.net/wiki/spaces/ITLC/pages/210993365)\n- [Where are the clusters physically located?](https://schrodinger-sandbox.atlassian.net/wiki/spaces/ITLC/pages/210895069)\n\n## Queue and Job Management\n\n- [What about the urgent queue?](https://schrodinger-sandbox.atlassian.net/wiki/spaces/ITLC/pages/210895094)\n- [My project isn't listed and my jobs aren't running](https://schrodinger-sandbox.atlassian.net/wiki/spaces/ITLC/pages/210993410)\n\n## Cluster Usage and Commands\n\n- [How do I check the load on a cluster?](https://schrodinger-sandbox.atlassian.net/wiki/spaces/ITLC/pages/210927718)",
  "is_minor_edit": false
}
</arguments>
</use_mcp_tool>
```

## Script Example

Here's a pseudocode example of how you might implement this as a script:

```python
def split_confluence_page(source_page_id, space_key, categories, questions):
    # 1. Create subpages for each question
    subpage_ids = {}
    for question in questions:
        subpage_id = create_subpage(
            space_key=space_key,
            title=question['title'],
            content=question['content'],
            user_story=question['user_story'],
            parent_id=source_page_id
        )
        
        category = question['category']
        if category not in subpage_ids:
            subpage_ids[category] = []
        
        subpage_ids[category].append({
            'id': subpage_id,
            'title': question['title']
        })
    
    # 2. Update the main page with TOC and links
    update_main_page(
        page_id=source_page_id,
        space_key=space_key,
        categories=categories,
        subpage_ids=subpage_ids
    )

def create_subpage(space_key, title, content, user_story, parent_id):
    # Format the content with the user story
    formatted_content = f"{content}\n\nstory\n\n{user_story}"
    
    # Call the Confluence API to create the page
    # Return the new page ID
    
def update_main_page(page_id, space_key, categories, subpage_ids):
    # Generate table of contents
    toc_rows = []
    for category in categories:
        toc_rows.append(f"| [{category['name']}](https://.../wiki/spaces/{space_key}/pages/{page_id}#{category['anchor']}) | {category['description']} |")
    
    # Generate category sections with links to subpages
    category_sections = []
    for category in categories:
        section = f"## {category['name']}\n\n"
        for subpage in subpage_ids.get(category['name'], []):
            section += f"- [{subpage['title']}](https://.../wiki/spaces/{space_key}/pages/{subpage['id']})\n"
        category_sections.append(section)
    
    # Format the main page content
    # Call the Confluence API to update the page
```

## Notes

- The `story` format is important for the excerpt macro to work correctly in Confluence
- When creating links to sections within the main page, use the format `#section-name` with lowercase and hyphens
- The Confluence API may handle formatting differently than expected, so test the template with a small set of questions first
- The page IDs returned by the Confluence API are needed to create the links to subpages

By following this template, you can automate the process of splitting a Confluence page into multiple subpages with proper formatting and organization.
