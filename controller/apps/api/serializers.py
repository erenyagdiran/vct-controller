import ast

from rest_framework import serializers

# Haking rest_framework in order to meet our crazy design specifications


class RelHyperlinkedRelatedField(serializers.HyperlinkedRelatedField):
    """ 
    HyperlinkedRelatedField field providing a relation object rather than flat URL 
    """
    def to_native(self, obj):
        # FIXME this doesn't work when posting
        url = super(RelHyperlinkedRelatedField, self).to_native(obj)
        if url is None:
             return None
        return {'uri': url}

    def from_native(self, value):
        value = ast.literal_eval(str(value)).pop('uri')
        return super(RelHyperlinkedRelatedField, self).from_native(value)


class RelManyHyperlinkedRelatedField(serializers.ManyRelatedMixin, RelHyperlinkedRelatedField):
    """
    Represents a to-many relationship, using hyperlinking inside a relation object
    """
    pass


class UriHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
    """ 
    Like HyperlinkedModelSerializer but renaming url field to uri 
    """
    uri = serializers.HyperlinkedIdentityField()
    
    def __init__(self, *args, **kwargs):
        super(UriHyperlinkedModelSerializer, self).__init__(*args, **kwargs)
        self.fields.pop('url', None)
    
    def get_related_field(self, model_field, to_many):
        """
        Same as DRF2 but returning RelXxxxXxxx
        """
        rel = model_field.rel.to
        kwargs = {
            'null': model_field.null,
            'queryset': rel._default_manager,
            'view_name': self._get_default_view_name(rel)
        }
        if to_many:
            return RelManyHyperlinkedRelatedField(**kwargs)
        return RelHyperlinkedRelatedField(**kwargs)


class HyperlinkedFileField(serializers.FileField):
    def to_native(self, value):
        if value:
            request = self.context.get('request', None)
            return request.build_absolute_uri(value.url)


class PropertyField(serializers.WritableField):
    """
    Dict-like representation of a Property Model
    A bit hacky, objects get deleted on from_native method and Serializer will
    need a custom override of restore_object method.
    """
    def to_native(self, value):
        """ Dict-like representation of a Property Model"""
        return dict([ (prop.name, prop.value) for prop in value.all() ])
    
    def from_native(self, value):
        """ Convert a dict-like representation back to a Property Model """
        parent = self.parent
        related_manager = getattr(parent.object, self.source or field_name, False)
        properties = []
        if value:
            model = getattr(parent.opts.model, self.source).related.model
            dict_value = ast.literal_eval(str(value))
            if not related_manager:
                # POST (new parent object)
                return [ model(name=n, value=v) for n,v in dict_value.iteritems() ]
            # PUT
            for (name, value) in dict_value.iteritems():
                try:
                    # Update existing property
                    prop = related_manager.get(name=name)
                except model.DoesNotExist:
                    # Create a new one
                    prop = model(name=name, value=value)
                else:
                    prop.value = value
                properties.append(prop)
        # Discart old values
        if related_manager:
            related_manager.all().delete()
        return properties