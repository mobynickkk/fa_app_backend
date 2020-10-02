import graphene
import graphqlapi.schema


class Query(graphqlapi.schema.Query, graphene.ObjectType):
    pass


class Mutation(graphqlapi.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
