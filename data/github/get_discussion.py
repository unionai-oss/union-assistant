from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import os

headers = {
        'Authorization': f'token {os.getenv("GITHUB_ACCESS_TOKEN")}'
    }

# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(url="https://api.github.com/graphql", headers=headers)

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)

# Provide a GraphQL query
query = gql(
    """
    query {
    repository(owner:"octocat", name:"Hello-World") {
      issues(last:20, states:CLOSED) {
        edges {
          node {
            title
            url
            labels(first:5) {
              edges {
                node {
                  name
                }
              }
            }
          }
        }
      }
    }
  }
"""
)

# Execute the query on the transport
result = client.execute(query)
print(result)
