from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Article, Rating, User
from .utils import update_rating_cache


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class ArticleSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    ratings_count = serializers.IntegerField(read_only=True)
    user_rating = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "content",
            "ratings_count",
            "average_rating",
            "user_rating",
        ]

    def get_average_rating(self, obj):
        return obj.average_rating

    def get_user_rating(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            rating = obj.ratings.filter(user=request.user).first()
            if rating:
                return rating.score
        return None


class RatingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    article = ArticleSerializer(read_only=True)
    article_id = serializers.PrimaryKeyRelatedField(
        queryset=Article.objects.all(), write_only=True, source="article"
    )

    class Meta:
        model = Rating
        fields = ["id", "user", "article", "article_id", "score"]

    def validate_score(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Score must be between 1 and 5.")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        article = validated_data['article']
        score = validated_data['score']

        rating, created = Rating.objects.update_or_create(user=user, article=article, score=score)

        old_score = rating.score if not created else None
        update_rating_cache(article.id, old_score, score)

        return rating


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Password fields didn’t match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"],
        )
        return user
