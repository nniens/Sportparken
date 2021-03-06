from django.contrib.auth import get_user_model
from rest_framework import serializers

from sportparken.dataset.models import (
        Huurder,
        HuurderObjectRelation,
        Sportpark,
        SportparkObjectGeometry,
        SportparkObject,
        SportparkGeometry,
        Ondergrond
        )

User = get_user_model()

class HuurderListSerializer(serializers.ModelSerializer):
	url = serializers.HyperlinkedIdentityField( view_name = 'api:huurder-detail')

	objecten = serializers.SerializerMethodField()

	def get_objecten(self, obj):
		request = self.context.get('request')
		spi = request.query_params.get('sp', None)
		return SportparkObjectDetailSerializer(obj.get_sp_objecten(spi), many=True, context={'request':request}).data

	class Meta:
		model = Huurder
		fields = [
			'url',
			'tid',
			'kvk',
			'name',
			'sport',
			'objecten',
			'bezoek_adres',
			'post_adres'
		]


class HuurderDetailSerializer(serializers.ModelSerializer):

	objecten = serializers.SerializerMethodField()

	def get_objecten(self, obj):
		request = self.context.get('request')
		spi = request.query_params.get('sp', None)
		return SportparkObjectDetailSerializer(obj.get_sp_objecten(spi), many=True, context={'request':request}).data

	class Meta:
		model = Huurder
		fields = [
			'tid',
			'name',
			'sport',
			'kvk',
			'objecten',
			'bezoek_adres',
			'post_adres'
		]


class SportparkListSerializer(serializers.ModelSerializer):
	url = serializers.HyperlinkedIdentityField( view_name = 'api:sportpark-detail')
	class Meta:
		model = Sportpark
		fields = [
			'url',
			'tid',
			'name'
		]


class SportparkDetailSerializer(serializers.ModelSerializer):
	geometry = serializers.SerializerMethodField()

	def get_geometry(self, obj):
		request = self.context.get('request')
		qs = obj.object_geometry_set
		return SportparkGeomListSerializer(qs, many=True, context={'request':request}).data

	class Meta:
		model = Sportpark
		fields = [
			'tid',
			'name',
			'geometry'
		]


class SportparkObjectListSerializer(serializers.ModelSerializer):
	url = serializers.HyperlinkedIdentityField( view_name = 'api:sportparkObject-detail')

	geometry = serializers.SerializerMethodField()

	huurders = serializers.SerializerMethodField()

	def get_huurders(self, obj):
		request = self.context.get('request')
		qs = obj.get_huurder_set()
		return HuurderListSerializer(qs, many=True, context={'request':request}).data

	def get_geometry(self, obj):
		request = self.context.get('request')
		qs = obj.object_geometry_set
		return SportparkObjectGeomListSerializer(qs, many=True, context={'request':request}).data

	class Meta:
		model = SportparkObject
		fields = [
			'uid',
			'url',
			'tid',
			'name',
			'objectType',
			'ondergrond_type',
			'verhuurprijs',
			'geometry',
			'huurders',
		]


class SportparkObjectDetailSerializer(serializers.ModelSerializer):
	geometry = serializers.SerializerMethodField()

	def get_geometry(self, obj):
		request = self.context.get('request')
		qs = obj.object_geometry_set
		return SportparkObjectGeomListSerializer(qs, many=True, context={'request':request}).data

	class Meta:
		model = SportparkObject
		fields = [
			'tid',
			'name',
			'objectType',
			'ondergrond_type',
			'verhuurprijs',
			'geometry',
		]


class SportparkGeomListSerializer(serializers.ModelSerializer):
	url = serializers.HyperlinkedIdentityField( view_name = 'api:sportparkGeom-detail')

	class Meta:
		model = SportparkGeometry
		fields = [ 
			'tid',
			'url'
			]


class SportparkGeomDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = SportparkGeometry
		fields = '__all__'


class SportparkObjectGeomListSerializer(serializers.ModelSerializer):
	url = serializers.HyperlinkedIdentityField( view_name = 'api:sportparkObjectGeom-detail')

	class Meta:
		model = SportparkObjectGeometry
		fields = [ 
			'tid',
			'url',
			]


class SportparkObjectGeomDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = SportparkObjectGeometry
		# fields = '__all__'
		fields = [
			'tid',
			'ondergrond',
			'sportpark_object_id',
			'sportpark_object_name',
			'sportpark_object_type',
			'ondergrond_type',
			'lokaalid',
			'bagpndid',
			'bron',
			'geometry',
		]


class SportparkObjectGeomDetailEditSerializer(serializers.ModelSerializer):
	class Meta:
		model = SportparkObjectGeometry
		# fields = '__all__'
		fields = [
			'tid',
			'ondergrond'
		]


class RelationListSerializer(serializers.ModelSerializer):
	sportparkObject = serializers.SerializerMethodField()
	huurder = serializers.SerializerMethodField()


	def get_sportparkObject(self, obj):
		vo = obj.sportpark_object
		request = self.context.get('request')
		return SportparkObjectDetailSerializer(vo, many=False, context={'request':request}).data

	def get_huurder(self, obj):
		vo = obj.huurder
		request = self.context.get('request')
		return HuurderDetailSerializer(vo, many=False, context={'request':request}).data


	class Meta:
		model = HuurderObjectRelation
		fields = [
			'tid',
			'sportparkObject',
			'huurder',
			]


class RelationPostRemoveSerializer(serializers.ModelSerializer):
	class Meta:
		model = HuurderObjectRelation
		fields = '__all__'

class OndergrondListSerializer(serializers.ModelSerializer):
	url = serializers.HyperlinkedIdentityField( view_name = 'api:ondergrond-detail')

	def get_ondergrond(self, obj):
		vo = obj.ondergrond_type
		request = self.context.get('request')
		return OndergrondDetailSerializer(vo, many=False, context={'request':request}).data


	def get_ondergronden(self, obj):
		request = self.context.get('request')
		qs = obj.get_ondergrond_set()
		return OndergrondListSerializer(qs, many=True, context={'request':request}).data


	class Meta:
		model = Ondergrond
		fields = [
			'tid',
			'name',
			'url'
		]


class UserLoginSerializer(serializers.ModelSerializer):
	token = serializers.CharField(allow_blank=True, read_only=True)
	username = serializers.CharField()

	class Meta:
		model = User
		fields  =[
		        'username',
		        'password',
		        'token',
		    ]
		extra_kwargs = {'password':
		                        {'write_only': True}
		                    }
	def validate(self, data):
		username = data.get('username', None)
		password = data['password']

		if not username:
			raise serializers.ValidationError('Username is verplicht')

		user = User.objects.filter(username=username).distinct()

		if user.exists() and user.count() == 1:
			user_obj = user.first()
		else:
			raise serializers.ValidationError('Username is niet correct')

		if user_obj:
			if not user_obj.check_password(password):
				raise serializers.ValidationError('Password niet correct')
			data['token'] = "SOME TOKEN"
		return data




