# api/graphql/schema.py
# Strawberry GraphQL schema setup

import strawberry
from strawberry.fastapi import GraphQLRouter

from api.graphql.queries import Query
from api.graphql.mutations import Mutation
from api.graphql.subscriptions import Subscription


# Create schema with queries, mutations, and subscriptions
schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription
)


# Create GraphQL router for FastAPI
# WebSocket support enabled for subscriptions
graphql_router = GraphQLRouter(
    schema,
    subscription_protocols=[
        "graphql-transport-ws",  # newer protocol
        "graphql-ws",            # legacy protocol (Node-RED uses this)
    ]
)
