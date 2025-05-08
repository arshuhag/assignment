import requests
from django.core.management.base import BaseCommand
from countries.models import Country

class Command(BaseCommand):
    help = 'Fetch country data from restcountries.com and save to database'

    def handle(self, *args, **kwargs):
        url = "https://restcountries.com/v3.1/all"
        response = requests.get(url)

        if response.status_code != 200:
            self.stdout.write(self.style.ERROR('Failed to fetch data from API'))
            return

        countries = response.json()
        count = 0

        for country in countries:
            try:
                Country.objects.update_or_create(
                    cca2=country.get("cca2", ""),
                    defaults={
                        "name_common": country["name"]["common"],
                        "name_official": country["name"]["official"],
                        "name_native": country["name"].get("nativeName"),
                        "tld": country.get("tld"),
                        "ccn3": country.get("ccn3", ""),
                        "cioc": country.get("cioc"),
                        "independent": country.get("independent", False),
                        "status": country.get("status", ""),
                        "un_member": country.get("unMember", False),
                        "currencies": country.get("currencies"),
                        "idd": country.get("idd"),
                        "capital": country.get("capital"),
                        "alt_spellings": country.get("altSpellings"),
                        "region": country.get("region", ""),
                        "subregion": country.get("subregion", ""),
                        "languages": country.get("languages"),
                        "latlng": country.get("latlng"),
                        "landlocked": country.get("landlocked", False),
                        "borders": country.get("borders"),
                        "area": country.get("area"),
                        "demonyms": country.get("demonyms"),
                        "cca3": country.get("cca3", ""),
                        "translations": country.get("translations"),
                        "flag": country.get("flag"),
                        "maps": country.get("maps"),
                        "population": country.get("population"),
                        "gini": country.get("gini"),
                        "fifa": country.get("fifa", ""),
                        "car": country.get("car"),
                        "timezones": country.get("timezones"),
                        "continents": country.get("continents"),
                        "flags": country.get("flags"),
                        "coat_of_arms": country.get("coatOfArms"),
                        "startOfWeek": country.get("startOfWeek", ""),
                        "capitalInfo": country.get("capitalInfo"),
                        "postalCode": country.get("postalCode"),
                    }
                )
                count += 1
            except Exception as e:
                self.stderr.write(f"❌ Error processing {country.get('name', {}).get('common', 'Unknown')}: {e}")

        self.stdout.write(self.style.SUCCESS(f"✅ Successfully saved {count} countries"))