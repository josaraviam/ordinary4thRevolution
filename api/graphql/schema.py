import strawberry
from strawberry.fastapi import GraphQLRouter

from api.graphql.queries import Query         
from api.graphql.mutations import Mutation     
from api.graphql.subscriptions import Subscription  


# Create the main GraphQL schema - this is the "brain" of our GraphQL API
# Combines all three operation types into one schema
schema = strawberry.Schema(
    query=Query,         
    mutation=Mutation,   
    subscription=Subscription  
)

graphql_router = GraphQLRouter(
    schema,
    subscription_protocols=[
        "graphql-transport-ws",  # Modern protocol
        "graphql-ws",            # Legacy protocol just in case
    ]
)
