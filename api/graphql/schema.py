# api/graphql/schema.py
# GraphQL schema setup using Strawberry - because GraphQL is pretty awesome
# This is where we wire up all our queries, mutations, and subscriptions

import strawberry
from strawberry.fastapi import GraphQLRouter

from api.graphql.queries import Query          # Read operations (GET-like)
from api.graphql.mutations import Mutation     # Write operations (POST/PUT-like)
from api.graphql.subscriptions import Subscription  # Real-time streams (WebSocket magic)


# Create the main GraphQL schema - this is the "brain" of our GraphQL API
# Combines all three operation types into one schema
schema = strawberry.Schema(
    query=Query,         # For fetching data
    mutation=Mutation,   # For modifying data  
    subscription=Subscription  # For real-time updates
)


# Create GraphQL router that integrates with FastAPI
# WebSocket support for subscriptions included
graphql_router = GraphQLRouter(
    schema,
    subscription_protocols=[
        "graphql-transport-ws",  # Modern protocol (recommended)
        "graphql-ws",            # Legacy protocol (Node-RED still uses this)
    ]
)
