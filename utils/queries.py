from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


class Subgraph:
    def __init__(self, network="Ethereum"):
        if network=="Ethereum":
            url_extension = "-"
        else:
            url_extension = "-"+network.lower()+"-"
        subgraph_url = f"https://api.thegraph.com/subgraphs/name/balancer-labs/balancer{url_extension}v2"
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
                poolType
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
