from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

subgraph_url = "https://api.thegraph.com/subgraphs/name/balancer-labs/balancer-v2"
balancer_transport=RequestsHTTPTransport(
    url=subgraph_url,
    verify=True,
    retries=3
)
client = Client(transport=balancer_transport)

def query_pool_data(pool_id):
  query = '''
  query {{
      pools(where: {{ id: "{pool_id}" }}) {{
          amp
          name
      }}
      poolTokens( where: {{ poolId: "{pool_id}" }}) {{
          id
              name
              balance
      }}
  }}
  '''
  return client.execute(gql(query.format(pool_id=pool_id)))