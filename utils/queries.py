from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


class Subgraph:
    def __init__(self, network="balancer-v2"):
        subgraph_url = f"https://api.thegraph.com/subgraphs/name/balancer-labs/{network}"
        balancer_transport=RequestsHTTPTransport(
            url=subgraph_url,
            verify=True,
            retries=3
        )
        self.client = Client(transport=balancer_transport)

    def query_pool_by_id(self, pool_id):
        query = '''
        query {{
            pool(id:"{pool_id}") {{
                amp
                name
                tokens {{
                    id
                        symbol
                        name
                        balance

                }}
            }}
        }}
        '''
        return self.client.execute(gql(query.format(pool_id=pool_id)))
