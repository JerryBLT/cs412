from rest_framework import serializers

from .models import Photo, Post, Profile


class ProfileSerializer(serializers.ModelSerializer):
    '''Serializer for reading Profile data.'''

    class Meta:
        model = Profile
        fields = ["id", "username", "display_name", "bio_text", "join_date", "profile_image_url",]


class PhotoSerializer(serializers.ModelSerializer):
    '''Serializer for reading Photo data.'''

    image = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ["id", "timestamp", "image"]

    def get_image(self, obj):
        '''Return whichever image source this photo stores.'''
        return obj.get_image_url()


class PostSerializer(serializers.ModelSerializer):
    '''Serializer for reading Post data with photos.'''

    profile = ProfileSerializer(read_only=True)
    photos = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "profile", "timestamp", "caption", "photos"]

    def get_photos(self, obj):
        '''Return photos attached to this post in timestamp order.'''
        photos = obj.get_all_photos()
        return PhotoSerializer(photos, many=True).data


class PostCreateSerializer(serializers.ModelSerializer):
    '''Serializer for creating a Post without authentication.'''

    profile_id = serializers.PrimaryKeyRelatedField(
        queryset=Profile.objects.all(), source="profile", write_only=True
    )
    image_url = serializers.URLField(required=False, allow_blank=True, write_only=True)
    image_file = serializers.ImageField(required=False, write_only=True)

    class Meta:
        model = Post
        fields = ["id", "profile_id", "caption", "image_url", "image_file"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        '''Create a post and optionally create one attached photo.'''
        image_url = validated_data.pop("image_url", "").strip()
        image_file = validated_data.pop("image_file", None)

        post = Post.objects.create(**validated_data)

        if image_file:
            Photo.objects.create(post=post, image_file=image_file)
        elif image_url:
            Photo.objects.create(post=post, image_url=image_url)

        return post
