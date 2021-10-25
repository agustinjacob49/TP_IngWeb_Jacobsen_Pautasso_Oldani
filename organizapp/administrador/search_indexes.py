from haystack import indexes
from .models import Event

class EventIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    description = indexes.CharField(model_attr='description')

    def get_model(self):
        return Event

    def index_queryset(self, using=None):
        """Queremos que se indexen solo los eventos publicos"""
        return self.get_model().objects.filter(visibility="publico")