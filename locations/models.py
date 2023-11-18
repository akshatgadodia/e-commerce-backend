from django.db import models


class Country(models.Model):
    # Name of the country, with a maximum length of 255 characters
    country_name = models.CharField(max_length=255, unique=True)
    # Currency symbol of the country
    currency = models.CharField(max_length=10)
    # Currency name of the country
    currency_name = models.CharField(max_length=255)
    # Phone code of the country
    phone_code = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
        ordering = ('country_name',)

    def __str__(self):
        return self.country_name


class State(models.Model):
    # Name of the state, with a maximum length of 255 characters
    state_name = models.CharField(max_length=255)
    # Foreign key relationship with the Country table, specifying that if a referenced country is deleted,
    # also delete the states associated with it
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    # Name of the country (for fast access)
    country_name = models.CharField(max_length=255)

    class Meta:
        ordering = ('state_name',)

    def __str__(self):
        return f"{self.state_name}, {self.country_name}"


class City(models.Model):
    # Name of the city, with a maximum length of 255 characters
    city_name = models.CharField(max_length=255)
    # Foreign key relationship with the State table, specifying that if a referenced state is deleted,
    # also delete the cities associated with it
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    # Name of the state (for fast access)
    state_name = models.CharField(max_length=255)
    # ID of the country (for fast access)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    # Name of country (for fast access)
    country_name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'
        ordering = ('city_name',)

    def __str__(self):
        return f"{self.city_name}, {self.state_name}, {self.country_name}"
