class AllFieldsListDisplayMixin:
    """
    A mixin for adding all fields of a model to list_display in the admin.
    """

    def get_list_display(self, request):
        # Retrieve the model's fields and convert them to a list of field names
        model_fields = [field.name for field in self.model._meta.fields]

        # Add the fields to list_display
        list_display = list(model_fields)
        list_display.extend(super().get_list_display(request))
        return list_display
