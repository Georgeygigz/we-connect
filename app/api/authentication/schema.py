from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
import graphene
import graphql_jwt
from .models import User
from django.contrib.auth import authenticate
from ..helpers.constants import SIGNUP_SUCCESS_MESSAGE

class UserType(DjangoObjectType):
    class Meta:
        model = User

class Query(graphene.ObjectType):
    users = graphene.List(UserType)

    def resolve_users(self, info):
        return User.objects.all()

class UserInput(graphene.InputObjectType):
    id = graphene.ID()
    username = graphene.String(required=True)
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    surname = graphene.String(required=True)
    email = graphene.String(required=True)
    password = graphene.String(required=True)
    id_number = graphene.Int(required=True)
    phone_number = graphene.String(required=True)

class CreateUser(graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)
    ok = graphene.Boolean()
    user = graphene.Field(UserType)
    message = graphene.String()
    token = graphene.String()

    def mutate(self, info, input=None):
        message = SIGNUP_SUCCESS_MESSAGE
        ok = True
        user = User(
            username=input.username,
            first_name=input.first_name,
            last_name=input.last_name,
            surname=input.surname,
            id_number=input.id_number,
            phone_number=input.phone_number,
            email=input.email
        )
        user.set_password(input.password)
        user.save()
        token = user.token
        return CreateUser(message=message, ok=ok, user=user,token=token)


class UserLogin(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
    ok = graphene.Boolean()
    user = graphene.Field(UserType)
    message = "User logedin successfully"
    def mutate (self, info, email, password):
        user = authenticate(email=email, password=password)
        if user is None:
            message = "User does not exist"
            return User(ok=ok, user=user, message=message)
        ok = True
        email = user.email
        token = user.token
        import pdb; pdb.set_trace()
        return User(ok=ok, email=email, token=token)


class Mutation(graphene.ObjectType):
    createUser = CreateUser.Field()
    userLogin = UserLogin.Field()
    # token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    # verify_token = graphql_jwt.Verify.Field()
    # refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
