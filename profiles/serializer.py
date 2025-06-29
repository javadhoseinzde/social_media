from rest_framework import serializers


# phone_number = serializers.CharField(
#     validators=[
#         number_validator,
#         letter_validator,
#         special_char_validator,
#         MinLengthValidator(limit_value=11),
#     ],
#     max_length=11,
#     required=False,
# )
# email = serializers.EmailField(required=False)