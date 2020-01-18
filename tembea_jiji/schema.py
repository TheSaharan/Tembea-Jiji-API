import graphene
import routes.schema

class Query(routes.schema.Query, graphene.ObjectType):
    # This class will inherit from multiple queries
    # as we begin to add more apps to our project
    pass


class Mutation(routes.schema.Mutation, graphene.ObjectType):
    # This class will inherit from multiple queries
    # as we begin to add more apps to our project
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
