"""Create Linear project and link issues to it."""
import sys
sys.path.insert(0, '.agent/core')
from linear_client import LinearClient

client = LinearClient()
team_id = client.get_team_id()

# Create project using GraphQL
create_project_mutation = """
mutation CreateProject($name: String!, $teamIds: [String!]!, $description: String) {
    projectCreate(input: {
        name: $name
        teamIds: $teamIds
        description: $description
    }) {
        success
        project {
            id
            name
            url
        }
    }
}
"""

result = client._execute_query(create_project_mutation, {
    "name": "Altery Tools",
    "teamIds": [team_id],
    "description": "Coverage & Rails Finder MVP - SEO tool for organic traffic to altery.com"
})

project_data = result.get("projectCreate", {})
if project_data.get("success"):
    project = project_data.get("project", {})
    project_id = project.get("id")
    print(f"✅ Created project: {project.get('name')}")
    print(f"   URL: {project.get('url')}")
    
    # Now link existing issues to the project
    issue_ids = ["LIN-38", "LIN-39", "LIN-40", "LIN-41", "LIN-42", "LIN-43", "LIN-44", "LIN-45", "LIN-46", "LIN-47"]
    
    for issue_id in issue_ids:
        # Get issue internal ID
        parts = issue_id.split("-")
        team_key = parts[0]
        issue_number = int(parts[1])
        
        query = """
        query GetIssueId($teamKey: String!, $number: Float!) {
            issues(filter: { team: { key: { eq: $teamKey } }, number: { eq: $number } }, first: 1) {
                nodes { id identifier }
            }
        }
        """
        data = client._execute_query(query, {"teamKey": team_key, "number": issue_number})
        nodes = data.get("issues", {}).get("nodes", [])
        
        if nodes:
            issue_uuid = nodes[0].get("id")
            
            # Update issue to link to project
            update_mutation = """
            mutation LinkToProject($id: String!, $projectId: String!) {
                issueUpdate(id: $id, input: { projectId: $projectId }) {
                    success
                    issue { identifier project { name } }
                }
            }
            """
            update_result = client._execute_query(update_mutation, {"id": issue_uuid, "projectId": project_id})
            if update_result.get("issueUpdate", {}).get("success"):
                print(f"   ✓ Linked {issue_id} to project")
            else:
                print(f"   ✗ Failed to link {issue_id}")
else:
    print(f"❌ Failed to create project: {result}")
