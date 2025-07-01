import sys
from typing import Dict, List, Optional
import cartopy.crs as ccrs
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from reagentpy.ReagentClient import ReagentClient
from reagentpy.clients.repo import RepoClient
from reagentpy.clients.composite_scores import CompositeClient


class TimezoneVisClient(ReagentClient):
    def __init__(self):
        super().__init__()
        # The file that contains timezone boundaries; will be downloaded if needed
        self.local_geojson_path = "combined-now.json"


    def get_tz_ids(self, offset: float) -> List[str]:
        """Return all of the timezone known areas for the given offset"""

        try:
            tz_dict = {
                -12.0: ["Etc/GMT+12"],
                -11.0: [
                    "Etc/GMT+11",
                    "Pacific/Midway",
                    "Pacific/Niue",
                    "Pacific/Pago_Pago",
                    "Pacific/Samoa",
                    "US/Samoa",
                ],
                -10.0: [
                    "America/Adak",
                    "America/Atka",
                    "Etc/GMT+10",
                    "HST",
                    "Pacific/Honolulu",
                    "Pacific/Johnston",
                    "Pacific/Rarotonga",
                    "Pacific/Tahiti",
                    "US/Aleutian",
                    "US/Hawaii",
                ],
                -9.0: [
                    "America/Anchorage",
                    "America/Juneau",
                    "America/Metlakatla",
                    "America/Nome",
                    "America/Sitka",
                    "America/Yakutat",
                    "Etc/GMT+9",
                    "Pacific/Gambier",
                    "US/Alaska",
                ],
                -8.5: ["Pacific/Marquesas"],
                -8.0: [
                    "America/Ensenada",
                    "America/Los_Angeles",
                    "America/Santa_Isabel",
                    "America/Tijuana",
                    "America/Vancouver",
                    "Canada/Pacific",
                    "Etc/GMT+8",
                    "Mexico/BajaNorte",
                    "PST8PDT",
                    "Pacific/Pitcairn",
                    "US/Pacific",
                ],
                -7.0: [
                    "America/Boise",
                    "America/Cambridge_Bay",
                    "America/Ciudad_Juarez",
                    "America/Creston",
                    "America/Dawson",
                    "America/Dawson_Creek",
                    "America/Denver",
                    "America/Edmonton",
                    "America/Fort_Nelson",
                    "America/Hermosillo",
                    "America/Inuvik",
                    "America/Mazatlan",
                    "America/Phoenix",
                    "America/Shiprock",
                    "America/Whitehorse",
                    "America/Yellowknife",
                    "Canada/Mountain",
                    "Canada/Yukon",
                    "Etc/GMT+7",
                    "MST",
                    "MST7MDT",
                    "Mexico/BajaSur",
                    "Navajo",
                    "US/Arizona",
                    "US/Mountain",
                ],
                -6.0: [
                    "America/Bahia_Banderas",
                    "America/Belize",
                    "America/Chicago",
                    "America/Chihuahua",
                    "America/Costa_Rica",
                    "America/El_Salvador",
                    "America/Guatemala",
                    "America/Indiana/Knox",
                    "America/Indiana/Tell_City",
                    "America/Knox_IN",
                    "America/Managua",
                    "America/Matamoros",
                    "America/Menominee",
                    "America/Merida",
                    "America/Mexico_City",
                    "America/Monterrey",
                    "America/North_Dakota/Beulah",
                    "America/North_Dakota/Center",
                    "America/North_Dakota/New_Salem",
                    "America/Ojinaga",
                    "America/Rainy_River",
                    "America/Rankin_Inlet",
                    "America/Regina",
                    "America/Resolute",
                    "America/Swift_Current",
                    "America/Tegucigalpa",
                    "America/Winnipeg",
                    "CST6CDT",
                    "Canada/Central",
                    "Canada/Saskatchewan",
                    "Etc/GMT+6",
                    "Mexico/General",
                    "Pacific/Galapagos",
                    "US/Central",
                    "US/Indiana-Starke",
                ],
                -5.0: [
                    "America/Atikokan",
                    "America/Bogota",
                    "America/Cancun",
                    "America/Cayman",
                    "America/Coral_Harbour",
                    "America/Detroit",
                    "America/Eirunepe",
                    "America/Fort_Wayne",
                    "America/Grand_Turk",
                    "America/Guayaquil",
                    "America/Havana",
                    "America/Indiana/Indianapolis",
                    "America/Indiana/Marengo",
                    "America/Indiana/Petersburg",
                    "America/Indiana/Vevay",
                    "America/Indiana/Vincennes",
                    "America/Indiana/Winamac",
                    "America/Indianapolis",
                    "America/Iqaluit",
                    "America/Jamaica",
                    "America/Kentucky/Louisville",
                    "America/Kentucky/Monticello",
                    "America/Lima",
                    "America/Louisville",
                    "America/Montreal",
                    "America/Nassau",
                    "America/New_York",
                    "America/Nipigon",
                    "America/Panama",
                    "America/Pangnirtung",
                    "America/Port-au-Prince",
                    "America/Porto_Acre",
                    "America/Rio_Branco",
                    "America/Thunder_Bay",
                    "America/Toronto",
                    "Brazil/Acre",
                    "Canada/Eastern",
                    "Chile/EasterIsland",
                    "Cuba",
                    "EST",
                    "EST5EDT",
                    "Etc/GMT+5",
                    "Jamaica",
                    "Pacific/Easter",
                    "US/East-Indiana",
                    "US/Eastern",
                    "US/Michigan",
                ],
                -4.5: ["Error/Timezone"],
                -4.0: [
                    "America/Anguilla",
                    "America/Antigua",
                    "America/Aruba",
                    "America/Barbados",
                    "America/Blanc-Sablon",
                    "America/Boa_Vista",
                    "America/Campo_Grande",
                    "America/Caracas",
                    "America/Cuiaba",
                    "America/Curacao",
                    "America/Dominica",
                    "America/Glace_Bay",
                    "America/Goose_Bay",
                    "America/Grenada",
                    "America/Guadeloupe",
                    "America/Guyana",
                    "America/Halifax",
                    "America/Kralendijk",
                    "America/La_Paz",
                    "America/Lower_Princes",
                    "America/Manaus",
                    "America/Marigot",
                    "America/Martinique",
                    "America/Moncton",
                    "America/Montserrat",
                    "America/Port_of_Spain",
                    "America/Porto_Velho",
                    "America/Puerto_Rico",
                    "America/Santo_Domingo",
                    "America/St_Barthelemy",
                    "America/St_Kitts",
                    "America/St_Lucia",
                    "America/St_Thomas",
                    "America/St_Vincent",
                    "America/Thule",
                    "America/Tortola",
                    "America/Virgin",
                    "Atlantic/Bermuda",
                    "Brazil/West",
                    "Canada/Atlantic",
                    "Etc/GMT+4",
                ],
                -3.0: [
                    "America/Araguaina",
                    "America/Argentina/Buenos_Aires",
                    "America/Argentina/Catamarca",
                    "America/Argentina/ComodRivadavia",
                    "America/Argentina/Cordoba",
                    "America/Argentina/Jujuy",
                    "America/Argentina/La_Rioja",
                    "America/Argentina/Mendoza",
                    "America/Argentina/Rio_Gallegos",
                    "America/Argentina/Salta",
                    "America/Argentina/San_Juan",
                    "America/Argentina/San_Luis",
                    "America/Argentina/Tucuman",
                    "America/Argentina/Ushuaia",
                    "America/Asuncion",
                    "America/Bahia",
                    "America/Belem",
                    "America/Buenos_Aires",
                    "America/Catamarca",
                    "America/Cayenne",
                    "America/Cordoba",
                    "America/Fortaleza",
                    "America/Jujuy",
                    "America/Maceio",
                    "America/Mendoza",
                    "America/Miquelon",
                    "America/Montevideo",
                    "America/Paramaribo",
                    "America/Punta_Arenas",
                    "America/Recife",
                    "America/Rosario",
                    "America/Santarem",
                    "America/Santiago",
                    "America/Sao_Paulo",
                    "Atlantic/Stanley",
                    "Brazil/East",
                    "Chile/Continental",
                    "Etc/GMT+3",
                ],
                -2.5: ["America/St_Johns", "Canada/Newfoundland"],
                -2.0: [
                    "America/Godthab",
                    "America/Noronha",
                    "America/Nuuk",
                    "Atlantic/South_Georgia",
                    "Brazil/DeNoronha",
                    "Etc/GMT+2",
                ],
                -1.0: [
                    "America/Scoresbysund",
                    "Atlantic/Azores",
                    "Atlantic/Cape_Verde",
                    "Etc/GMT+1",
                ],
                0.0: [
                    "Africa/Abidjan",
                    "Africa/Accra",
                    "Africa/Bamako",
                    "Africa/Banjul",
                    "Africa/Bissau",
                    "Africa/Conakry",
                    "Africa/Dakar",
                    "Africa/Freetown",
                    "Africa/Lome",
                    "Africa/Monrovia",
                    "Africa/Nouakchott",
                    "Africa/Ouagadougou",
                    "Africa/Sao_Tome",
                    "Africa/Timbuktu",
                    "America/Danmarkshavn",
                    "Atlantic/Canary",
                    "Atlantic/Faeroe",
                    "Atlantic/Faroe",
                    "Atlantic/Madeira",
                    "Atlantic/Reykjavik",
                    "Atlantic/St_Helena",
                    "Eire",
                    "Etc/GMT",
                    "Etc/GMT+0",
                    "Etc/GMT-0",
                    "Etc/GMT0",
                    "Etc/Greenwich",
                    "Etc/UCT",
                    "Etc/UTC",
                    "Etc/Universal",
                    "Etc/Zulu",
                    "Europe/Belfast",
                    "Europe/Dublin",
                    "Europe/Guernsey",
                    "Europe/Isle_of_Man",
                    "Europe/Jersey",
                    "Europe/Lisbon",
                    "Europe/London",
                    "GB",
                    "GB-Eire",
                    "GMT",
                    "GMT+0",
                    "GMT-0",
                    "GMT0",
                    "Greenwich",
                    "Iceland",
                    "Portugal",
                    "UCT",
                    "UTC",
                    "Universal",
                    "WET",
                    "Zulu",
                ],
                1.0: [
                    "Africa/Algiers",
                    "Africa/Bangui",
                    "Africa/Brazzaville",
                    "Africa/Casablanca",
                    "Africa/Ceuta",
                    "Africa/Douala",
                    "Africa/El_Aaiun",
                    "Africa/Kinshasa",
                    "Africa/Lagos",
                    "Africa/Libreville",
                    "Africa/Luanda",
                    "Africa/Malabo",
                    "Africa/Ndjamena",
                    "Africa/Niamey",
                    "Africa/Porto-Novo",
                    "Africa/Tunis",
                    "Arctic/Longyearbyen",
                    "Atlantic/Jan_Mayen",
                    "CET",
                    "Etc/GMT-1",
                    "Europe/Amsterdam",
                    "Europe/Andorra",
                    "Europe/Belgrade",
                    "Europe/Berlin",
                    "Europe/Bratislava",
                    "Europe/Brussels",
                    "Europe/Budapest",
                    "Europe/Busingen",
                    "Europe/Copenhagen",
                    "Europe/Gibraltar",
                    "Europe/Ljubljana",
                    "Europe/Luxembourg",
                    "Europe/Madrid",
                    "Europe/Malta",
                    "Europe/Monaco",
                    "Europe/Oslo",
                    "Europe/Paris",
                    "Europe/Podgorica",
                    "Europe/Prague",
                    "Europe/Rome",
                    "Europe/San_Marino",
                    "Europe/Sarajevo",
                    "Europe/Skopje",
                    "Europe/Stockholm",
                    "Europe/Tirane",
                    "Europe/Vaduz",
                    "Europe/Vatican",
                    "Europe/Vienna",
                    "Europe/Warsaw",
                    "Europe/Zagreb",
                    "Europe/Zurich",
                    "MET",
                    "Poland",
                ],
                2.0: [
                    "Africa/Blantyre",
                    "Africa/Bujumbura",
                    "Africa/Cairo",
                    "Africa/Gaborone",
                    "Africa/Harare",
                    "Africa/Johannesburg",
                    "Africa/Juba",
                    "Africa/Khartoum",
                    "Africa/Kigali",
                    "Africa/Lubumbashi",
                    "Africa/Lusaka",
                    "Africa/Maputo",
                    "Africa/Maseru",
                    "Africa/Mbabane",
                    "Africa/Tripoli",
                    "Africa/Windhoek",
                    "Asia/Beirut",
                    "Asia/Famagusta",
                    "Asia/Gaza",
                    "Asia/Hebron",
                    "Asia/Jerusalem",
                    "Asia/Nicosia",
                    "Asia/Tel_Aviv",
                    "EET",
                    "Egypt",
                    "Etc/GMT-2",
                    "Europe/Athens",
                    "Europe/Bucharest",
                    "Europe/Chisinau",
                    "Europe/Helsinki",
                    "Europe/Kaliningrad",
                    "Europe/Kiev",
                    "Europe/Kyiv",
                    "Europe/Mariehamn",
                    "Europe/Nicosia",
                    "Europe/Riga",
                    "Europe/Sofia",
                    "Europe/Tallinn",
                    "Europe/Tiraspol",
                    "Europe/Uzhgorod",
                    "Europe/Vilnius",
                    "Europe/Zaporozhye",
                    "Israel",
                    "Libya",
                ],
                3.0: [
                    "Africa/Addis_Ababa",
                    "Africa/Asmara",
                    "Africa/Asmera",
                    "Africa/Dar_es_Salaam",
                    "Africa/Djibouti",
                    "Africa/Kampala",
                    "Africa/Mogadishu",
                    "Africa/Nairobi",
                    "Asia/Aden",
                    "Asia/Amman",
                    "Asia/Baghdad",
                    "Asia/Bahrain",
                    "Asia/Damascus",
                    "Asia/Istanbul",
                    "Asia/Kuwait",
                    "Asia/Qatar",
                    "Asia/Riyadh",
                    "Etc/GMT-3",
                    "Europe/Istanbul",
                    "Europe/Kirov",
                    "Europe/Minsk",
                    "Europe/Moscow",
                    "Europe/Simferopol",
                    "Europe/Volgograd",
                    "Indian/Antananarivo",
                    "Indian/Comoro",
                    "Indian/Mayotte",
                    "Turkey",
                    "W-SU",
                ],
                3.5: ["Asia/Tehran", "Iran"],
                4.0: [
                    "Asia/Baku",
                    "Asia/Dubai",
                    "Asia/Muscat",
                    "Asia/Tbilisi",
                    "Asia/Yerevan",
                    "Etc/GMT-4",
                    "Europe/Astrakhan",
                    "Europe/Samara",
                    "Europe/Saratov",
                    "Europe/Ulyanovsk",
                    "Indian/Mahe",
                    "Indian/Mauritius",
                    "Indian/Reunion",
                ],
                4.5: ["Asia/Kabul"],
                5.0: [
                    "Asia/Almaty",
                    "Asia/Aqtau",
                    "Asia/Aqtobe",
                    "Asia/Ashgabat",
                    "Asia/Ashkhabad",
                    "Asia/Atyrau",
                    "Asia/Dushanbe",
                    "Asia/Karachi",
                    "Asia/Oral",
                    "Asia/Qostanay",
                    "Asia/Qyzylorda",
                    "Asia/Samarkand",
                    "Asia/Tashkent",
                    "Asia/Yekaterinburg",
                    "Etc/GMT-5",
                    "Indian/Kerguelen",
                    "Indian/Maldives",
                ],
                5.5: ["Asia/Calcutta", "Asia/Colombo", "Asia/Kolkata"],
                5.75: ["Asia/Kathmandu", "Asia/Katmandu"],
                6.0: [
                    "Asia/Bishkek",
                    "Asia/Dacca",
                    "Asia/Dhaka",
                    "Asia/Kashgar",
                    "Asia/Omsk",
                    "Asia/Thimbu",
                    "Asia/Thimphu",
                    "Asia/Urumqi",
                    "Etc/GMT-6",
                    "Indian/Chagos",
                ],
                6.5: ["Asia/Rangoon", "Asia/Yangon", "Indian/Cocos"],
                7.0: [
                    "Asia/Bangkok",
                    "Asia/Barnaul",
                    "Asia/Ho_Chi_Minh",
                    "Asia/Hovd",
                    "Asia/Jakarta",
                    "Asia/Krasnoyarsk",
                    "Asia/Novokuznetsk",
                    "Asia/Novosibirsk",
                    "Asia/Phnom_Penh",
                    "Asia/Pontianak",
                    "Asia/Saigon",
                    "Asia/Tomsk",
                    "Asia/Vientiane",
                    "Etc/GMT-7",
                    "Indian/Christmas",
                ],
                8.0: [
                    "Asia/Brunei",
                    "Asia/Choibalsan",
                    "Asia/Chongqing",
                    "Asia/Chungking",
                    "Asia/Harbin",
                    "Asia/Hong_Kong",
                    "Asia/Irkutsk",
                    "Asia/Kuala_Lumpur",
                    "Asia/Kuching",
                    "Asia/Macao",
                    "Asia/Macau",
                    "Asia/Makassar",
                    "Asia/Manila",
                    "Asia/Shanghai",
                    "Asia/Singapore",
                    "Asia/Taipei",
                    "Asia/Ujung_Pandang",
                    "Asia/Ulaanbaatar",
                    "Asia/Ulan_Bator",
                    "Australia/Perth",
                    "Australia/West",
                    "Etc/GMT-8",
                    "Hongkong",
                    "PRC",
                    "ROC",
                    "Singapore",
                ],
                8.75: ["Australia/Eucla"],
                9.0: [
                    "Asia/Chita",
                    "Asia/Dili",
                    "Asia/Jayapura",
                    "Asia/Khandyga",
                    "Asia/Pyongyang",
                    "Asia/Seoul",
                    "Asia/Tokyo",
                    "Asia/Yakutsk",
                    "Etc/GMT-9",
                    "Japan",
                    "Pacific/Palau",
                    "ROK",
                ],
                9.5: ["Australia/Darwin", "Australia/North"],
                10.0: [
                    "Asia/Ust-Nera",
                    "Asia/Vladivostok",
                    "Australia/Brisbane",
                    "Australia/Lindeman",
                    "Australia/Queensland",
                    "Etc/GMT-10",
                    "Pacific/Chuuk",
                    "Pacific/Guam",
                    "Pacific/Port_Moresby",
                    "Pacific/Saipan",
                    "Pacific/Truk",
                    "Pacific/Yap",
                ],
                10.5: [
                    "Australia/Adelaide",
                    "Australia/Broken_Hill",
                    "Australia/South",
                    "Australia/Yancowinna",
                ],
                11.0: [
                    "Asia/Magadan",
                    "Asia/Sakhalin",
                    "Asia/Srednekolymsk",
                    "Australia/ACT",
                    "Australia/Canberra",
                    "Australia/Currie",
                    "Australia/Hobart",
                    "Australia/LHI",
                    "Australia/Lord_Howe",
                    "Australia/Melbourne",
                    "Australia/NSW",
                    "Australia/Sydney",
                    "Australia/Tasmania",
                    "Australia/Victoria",
                    "Etc/GMT-11",
                    "Pacific/Bougainville",
                    "Pacific/Efate",
                    "Pacific/Guadalcanal",
                    "Pacific/Kosrae",
                    "Pacific/Noumea",
                    "Pacific/Pohnpei",
                    "Pacific/Ponape",
                ],
                12.0: [
                    "Asia/Anadyr",
                    "Asia/Kamchatka",
                    "Etc/GMT-12",
                    "Kwajalein",
                    "Pacific/Fiji",
                    "Pacific/Funafuti",
                    "Pacific/Kwajalein",
                    "Pacific/Majuro",
                    "Pacific/Nauru",
                    "Pacific/Norfolk",
                    "Pacific/Tarawa",
                    "Pacific/Wake",
                    "Pacific/Wallis",
                ],
                13.0: [
                    "Etc/GMT-13",
                    "NZ",
                    "Pacific/Apia",
                    "Pacific/Auckland",
                    "Pacific/Enderbury",
                    "Pacific/Fakaofo",
                    "Pacific/Kanton",
                    "Pacific/Tongatapu",
                ],
                13.75: ["NZ-CHAT", "Pacific/Chatham"],
                14.0: ["Etc/GMT-14", "Pacific/Kiritimati"],
            }
            return tz_dict[offset]
        except KeyError:
            # If the offset is not found, return an empty list
            return []


    # Use a file-level var to avoid re-reading into memory
    geojson_data: Optional[dict] = None


    def read_timezone_geojson(self) -> Optional[dict]:
        """Read the large (~70MB) geojson file into an object in memory"""

        geojson_path = "combined-now.json"

        # print(f"  Reading timezones from {geojson_path}...", end="")
        sys.stdout.flush()

        # start = time.time()
        geojson_data = gpd.read_file(geojson_path)
        bounds = geojson_data.crs.area_of_use.bounds
        # print(f"bounds: {str(bounds)}")
        # duration = time.time() - start
        # print(f"  Finished in {duration:.2f} seconds.")

        return geojson_data


    def plot_timezone_distribution_map(self, timezone_boundaries, timezone_dict_list):
        """Show a map of the world with timezone boundaries colored by commit count"""

        # Sort timezone_dict_list by total_commits in descending order
        timezone_dict_list = sorted(
            timezone_dict_list,
            key=lambda x: x['total_commits'],
            reverse=True
        )

        commit_count = [d["total_commits"] for d in timezone_dict_list]

        # Select the 'cool' colormap for cold-to-hot mapping
        normalized_values = (commit_count - np.min(commit_count)) / (
            np.max(commit_count) - np.min(commit_count)
        )
        colormap = plt.get_cmap("gist_heat_r")
        bar_colors = colormap(normalized_values)

        # Set up the plot with Cartopy
        fig, ax = plt.subplots(
            1, 1, figsize=(15, 10), subplot_kw={"projection": ccrs.PlateCarree()}
        )

        # Create colorbar
        sm = plt.cm.ScalarMappable(
            cmap=colormap, norm=plt.Normalize(np.min(commit_count), np.max(commit_count))
        )
        sm.set_array([])
        cbar = plt.colorbar(sm, ax=ax)
        cbar.set_label("Number of Commits")

        # Create a list to store legend handles and labels
        legend_handles = []
        legend_labels = []

        # Draw shapes for each timezone
        for i in range(0, len(timezone_dict_list)):
            small_dict = timezone_dict_list[i]
            tz_names = self.get_tz_ids(small_dict["timezone"])
            
            # Create a patch for the legend
            legend_patch = plt.Rectangle(
                (0, 0), 1, 1, 
                facecolor=bar_colors[i], 
                edgecolor="black", 
                alpha=0.8
            )
            legend_handles.append(legend_patch)
            if small_dict["total_commits"] > 1:
                legend_labels.append(f"{small_dict['timezone']} ({small_dict['total_commits']} commits)")
            
            for tz_name in tz_names:
                specific_tz = timezone_boundaries[timezone_boundaries["tzid"] == tz_name]
                color = bar_colors[i]
                ax.add_geometries(
                    specific_tz.geometry,
                    crs=ccrs.PlateCarree(),
                    facecolor=color,
                    edgecolor="black",
                    alpha=0.8,
                )

        # Add the legend
        legend = ax.legend(
            legend_handles,
            legend_labels,
            loc='lower left',
            title="Timezones",
            framealpha=1.0,  # Make legend background fully opaque
            facecolor='white'  # Set legend background color to white
        )
        # Make the legend title bold
        legend.get_title().set_fontweight('bold')

        ax.set_global()
        ax.coastlines()

        plt.title("Number of Commits by Timezone")
        
        # Adjust layout to prevent legend from being cut off
        plt.tight_layout()
        plt.show()


    def build_and_show_timezone_map(self, repo: str):
        """Pull in all the geojson data and plot the commits onto the map"""

        data = RepoClient().timezones(repo)
        values = data.dict()[0]["timezone_commit_totals"]

        # print("Reading timezone geo data...")
        timezone_boundaries = self.read_timezone_geojson()
        if timezone_boundaries is None:
            return

        # print("Plotting timezone map...")
        self.plot_timezone_distribution_map(timezone_boundaries, values)


    def show_logarithmic_bar_chart(self, repo: str):
        """Show a bar chart of commits with log scale"""

        data = RepoClient().timezones(repo)
        values = data.dict()[0]["timezone_commit_totals"]

        # Create DataFrame
        df = pd.DataFrame(values)

        # Sort by timezones
        df = df.sort_values(by="timezone", ascending=True)

        # Convert timezone from seconds to "UTC±" format
        df["timezone"] = df["timezone"].apply(lambda x: f"UTC{x:+.0f}")

        # Convert 'timezone' back to numerical offset for sorting
        df["timezone_numeric"] = df["timezone"].apply(
            lambda x: float(x[3:]) if x[3:] != "" else 0
        )

        # Plot chart
        plt.figure(figsize=(10, 6))
        plt.bar(x=df["timezone"], height=df["total_commits"], color="c")

        # Setting y-axis to logarithmic scale
        plt.yscale("log")

        # Setting labels and title
        plt.xlabel("Timezone (UTC±)", fontsize=16)
        plt.ylabel("Commit Count (log scale)", fontsize=16)
        plt.title("Commit Counts by Timezone Around the World (Log Scale)", fontsize=18)
        plt.xticks(rotation=45)  # Rotate the x-axis labels to avoid overlapping
        plt.grid(
            axis="y", linestyle="--", which="both"
        )  # Grid lines for both major and minor ticks

        plt.tight_layout()  # Adjust the layout
        plt.show()


    def plot_timezone_distribution(self, repo: str):
        """Simple showing distribution across all timezones"""

        data = RepoClient().timezones(repo)
        timezone_commit_data = data.dict()[0]["timezone_commit_totals"]

        timezone_dict = {t: 0 for t in range(-12, 15)}
        for d in timezone_commit_data:
            normalized_timezone = d["timezone"]
            timezone_dict[normalized_timezone] = d["total_commits"]

        timezones = list(timezone_dict.keys())
        commit_count = list(timezone_dict.values())

        # Plotting
        plt.figure(figsize=(10, 6))
        plt.bar(timezones, commit_count, width=0.4, zorder=3)

        plt.xticks(range(-12, 15))
        plt.xlabel("Time Zone (GMT Offset)")
        plt.ylabel("Number of Commits")
        plt.title("Commit Distribution Across Time Zones")

        plt.grid(axis="y", zorder=0)
        plt.gca().set_axisbelow(True)
        plt.tight_layout()
        plt.show()


    def plot_timezone_distribution_color(self, repo: str):
        """Shows distribution across all timezones, coloring bars based on count"""

        data = RepoClient().timezones(repo)
        timezone_commit_data = data.dict()[0]["timezone_commit_totals"]

        timezone_dict = {t: 0 for t in range(-12, 15)}
        for d in timezone_commit_data:
            normalized_timezone = d["timezone"]
            timezone_dict[normalized_timezone] = d["total_commits"]

        timezones = list(timezone_dict.keys())
        commit_count = list(timezone_dict.values())

        # Select a colormap for cold-to-hot mapping
        colormap = plt.get_cmap("gist_heat_r")
        normalized_values = (commit_count - np.min(commit_count)) / (
            np.max(commit_count) - np.min(commit_count)
        )
        bar_colors = colormap(normalized_values)

        # Plotting
        plt.figure(figsize=(10, 6))
        plt.bar(timezones, commit_count, color=bar_colors, width=0.4, zorder=3)

        plt.xticks(range(-12, 15))
        plt.xlabel("Time Zone (GMT Offset)")
        plt.ylabel("Number of Commits")
        plt.title("Commit Distribution Across Time Zones")

        plt.grid(axis="y", zorder=0)
        plt.gca().set_axisbelow(True)
        plt.tight_layout()
        plt.show()


    def map_timezone_to_city(self, timezone: float) -> Optional[str]:
        """Get ONE city by timezone, returns None if offset not found"""
        tz_to_city = {
            -12.0: ["Etc/GMT+12"],
            -11.0: ["Pacific/Midway", "Pacific/Samoa"],
            -10.0: ["Pacific/Honolulu"],
            -9.0: ["America/Anchorage"],
            -8.5: ["Pacific/Marquesas"],
            -8.0: ["America/Los_Angeles", "America/Vancouver"],
            -7.0: ["America/Denver", "America/Edmonton"],
            -6.0: ["America/Chicago", "America/Mexico_City", "America/Winnipeg"],
            -5.0: ["America/New_York", "America/Toronto", "Brazil/Acre"],
            -4.0: ["America/Caracas", "America/Puerto_Rico", "America/Thule"],
            -3.0: ["America/Buenos_Aires", "America/Santiago", "America/Sao_Paulo"],
            -2.5: ["Canada/Newfoundland"],
            -2.0: ["Brazil/DeNoronha"],
            -1.0: ["Atlantic/Azores"],
            0.0: ["Europe/London", "Africa/Ouagadougou", "Atlantic/Reykjavik"],
            1.0: ["Europe/Rome", "Africa/Lagos", "Europe/Berlin", "Europe/Madrid"],
            2.0: ["Europe/Kiev", "Africa/Cairo", "Africa/Johannesburg", "Asia/Tel_Aviv"],
            3.0: ["Europe/Moscow", "Africa/Nairobi", "Asia/Baghdad", "Europe/Istanbul"],
            3.5: ["Asia/Tehran"],
            4.0: ["Asia/Dubai", "Europe/Samara"],
            4.5: ["Asia/Kabul"],
            5.0: ["Asia/Karachi", "Asia/Tashkent", "Asia/Yekaterinburg", "Indian/Maldives"],
            5.5: ["Asia/Kolkata"],
            5.75: [
                "Asia/Kathmandu",
            ],
            6.0: ["Asia/Dhaka"],
            6.5: ["Asia/Rangoon"],
            7.0: ["Asia/Bangkok", "Asia/Jakarta", "Asia/Saigon"],
            8.0: ["Asia/Shanghai", "Asia/Kuala_Lumpur", "Australia/Perth"],
            8.75: ["Australia/Eucla"],
            9.0: ["Asia/Tokyo"],
            9.5: ["Australia/Darwin"],
            10.0: ["Australia/Queensland", "Pacific/Guam"],
            10.5: ["Australia/Adelaide"],
            11.0: ["Australia/Sydney"],
            12.0: ["Asia/Kamchatka", "Pacific/Fiji"],
            13.0: ["Pacific/Auckland"],
            13.75: ["Pacific/Chatham"],
            14.0: ["Pacific/Kiritimati"],
        }
        return tz_to_city.get(timezone, [None])[0]


    def offset_to_gmt_plus(self, offset: float) -> str:
        '''Given a number, get string like "GMT+5.5"'''
        if offset < 0:
            return f"GMT{offset}"
        elif offset == 0:
            return "GMT+0.0"
        else:
            return f"GMT+{offset}"


    def get_top_n_timezones(self, repo: str, N=10) -> str:

        data = RepoClient().timezones(repo)
        list_of_dicts = data.dict()[0]["timezone_commit_totals"]
        sorted_list = sorted(list_of_dicts, key=lambda x: x["total_commits"], reverse=True)
        top_n = sorted_list[:N]

        cities: Dict[float, Optional[str]] = {}
        for cur_dict in top_n:
            cur_tz = cur_dict["timezone"]
            cities[cur_tz] = str(self.map_timezone_to_city(cur_tz))
        max_city_len = max(len(v) for v in cities.values())

        output = ""
        for i, entry_dict in enumerate(top_n):
            timezone = entry_dict["timezone"]
            commit_count = entry_dict["total_commits"]

            cur_city = cities[timezone]
            city_and_offset = f"{cur_city} ({self.offset_to_gmt_plus(timezone)})".rjust(
                max_city_len + 10
            )

            output += f"{i+1:-2}. {city_and_offset}: {commit_count}\n"

        return output
