from rest_framework import serializers
from .models import Photo, Post, Profile
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    '''Serializer for creating a new User with a password.'''
    # write_only=True so the password is never returned in API responses
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        # Use create_user so the password is hashed before saving
        user = User.objects.create_user(
            username=validated_data['username'], password=validated_data['password'], email=validated_data.get('email')
        )
        return user

class ProfileSerializer(serializers.ModelSerializer):
    '''Serializer for reading Profile data.'''

    class Meta:
        model = Profile
        # expose only the fields the API client needs
        fields = ["id", "username", "display_name", "bio_text", "join_date", "profile_image_url",]


class PhotoSerializer(serializers.ModelSerializer):
    '''Serializer for reading Photo data.'''

    # SerializerMethodField lets us call get_image() to compute the value
    image = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ["id", "timestamp", "image"]

    def get_image(self, obj):
        '''Return an absolute URL for whichever image source this photo stores.'''
        # get_image_url() returns image_url string or image_file.url (relative path)
        url = obj.get_image_url()
        if not url:
            return ''
        # build_absolute_uri converts a relative /media/... path to a full http://... URL
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(url)
        # fall back to relative path if no request in context (e.g. shell/tests)
        return url


class PostSerializer(serializers.ModelSerializer):
    '''Serializer for reading Post data with photos.'''

    # nest the full profile object instead of just its id
    profile = ProfileSerializer(read_only=True)
    # SerializerMethodField lets us attach photos from the related Photo model
    photos = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "profile", "timestamp", "caption", "photos"]

    def get_photos(self, obj):
        '''Return photos attached to this post in timestamp order.'''
        photos = obj.get_all_photos()
        # pass context so PhotoSerializer can build absolute image URLs
        return PhotoSerializer(photos, many=True, context=self.context).data


class PostCreateSerializer(serializers.ModelSerializer):
    '''Serializer for creating a Post without authentication.'''

    # accept profile_id in the request body, map it to the profile FK internally
    profile_id = serializers.PrimaryKeyRelatedField(
        queryset=Profile.objects.all(), source="profile", write_only=True
    )
    # optional image fields — only one will be used per post
    image_url = serializers.URLField(required=False, allow_blank=True, write_only=True)
    image_file = serializers.ImageField(required=False, write_only=True)

    class Meta:
        model = Post
        fields = ["id", "profile_id", "caption", "image_url", "image_file"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        '''Create a post and optionally create one attached photo.'''
        # pop image fields before creating the Post; Post has no image columns
        image_url = validated_data.pop("image_url", "").strip()
        image_file = validated_data.pop("image_file", None)

        post = Post.objects.create(**validated_data)

        # create a Photo attached to the new post; file takes priority over URL
        if image_file:
            Photo.objects.create(post=post, image_file=image_file)
        elif image_url:
            Photo.objects.create(post=post, image_url=image_url)

        return post
