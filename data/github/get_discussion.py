from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import os

"""
{
  "Authorization": f'Bearer {os.getenv("GITHUB_ACCESS_TOKEN")}',
  "Content-Type": "application/json"
}
"""


headers = {
  "Authorization": f'Bearer {os.getenv("GITHUB_ACCESS_TOKEN")}',
  "Content-Type": "application/json"
}

# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(url="https://api.github.com/graphql", headers=headers)

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)

# Provide a GraphQL query
query = gql(
    """
    query {
    repository(owner:"flyteorg", name:"flyte") {
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
