"""Extremely quick and dirty module for creating a markdown file from the instances.yaml file"""
from urllib.parse import urlparse

import pycountry
import yaml
from mdutils.mdutils import MdUtils


class ColumnBuilder:
    def route(self, name):
        router = {
            "url": self._create_url_column,
            "associated_clearnet_instance": self._create_url_column,
            "country": self._create_country_column,
            "status": self._create_status_column,
            "is_modified": self._create_modified_column,
            "privacy_policy": self._create_privacy_policy_column,
            "ddos_mitm_protection": self.ddos_protection,
            "owner": self._create_owner_column,
            "notes": self._create_notes_column,
            "mirrors": self._create_mirror_column
        }

        return router[name]

    @staticmethod
    def get_country_name_and_flag_from_code(code):
        name = pycountry.countries.get(alpha_2=code).name
        # https://stackoverflow.com/a/42235254
        flag = (lambda s, e: chr(ord(s.upper()) - 0x41 + 0x1F1E6) +
                            chr(ord(e.upper()) - 0x41 + 0x1F1E6))(*list(code))

        return name, flag


    @staticmethod
    def _create_url_column(url):
        if not url:
            return ""

        hostname = urlparse(url).hostname
        return f"[{hostname[:35] + (hostname[35:] and '...')}]({url})"

    def _create_country_column(self, country_code):
        main_name, main_flag = self.get_country_name_and_flag_from_code(country_code)
        return f"{main_name} {main_flag}"

    @staticmethod
    def _create_status_column(status_dict):
        if not status_dict:
            return ""

        status_url = status_dict["url"]
        image = status_dict.get("image")
        text = status_dict.get("text", "Status Page")

        if image:
            return f"[![{text}]({image})]({status_url})"
        else:
            return f"[{text}]({status_url})"

    @staticmethod
    def _create_modified_column(is_modified, source):
        if is_modified:
            return f"[Yes]({source})"
        return f"No"

    @staticmethod
    def _create_privacy_policy_column(privacy):
        if not privacy:
            return ""

        return f"[Here]({privacy})"

    @staticmethod
    def ddos_protection(ddos):
        if not ddos:
            return ""
        return f"{ddos}"

    @staticmethod
    def _create_owner_column(owner):
        author_name = owner.split("/")
        return f"[@{author_name[-1]}]({owner})"

    @staticmethod
    def _create_notes_column(notes, is_modified, source):
        # It is possible for both the notes and is_modified data to be falsey
        if not notes and not is_modified:
            return ""

        notes_list = []
        if is_modified:
            notes_list.append(f" - [Modified source code]({source})")
        if notes:
            [notes_list.append(f" - {note}") for note in notes]
        
        return '<br/>'.join(notes_list)

    def _create_mirror_column(self, mirrors):
        if not mirrors:
            return ""

        country_column = []

        for mirror in mirrors:
            name, flag = self.get_country_name_and_flag_from_code(mirror["country"])
            country_column.append(f"[{name} {flag}]({mirror['url']})")

        return "<br/>".join(country_column)


class MDInstanceListBuilder:
    def __init__(self, instance_list_config):
        self.config = instance_list_config
        self.md = MdUtils(file_name='Invidious-Instances.md')
        self.builder = ColumnBuilder()

    def _generate_heading(self):
        self.md.new_header(level=1, title='Public Instances')
        self.md.new_paragraph("Uptime History: [uptime.invidious.io](https://uptime.invidious.io)")
        self.md.new_paragraph("Instances API: [api.invidious.io](api.invidious.io)")

    def _create_instance_tables(self):
        # HTTPS
        self.md.new_header(level=1, title='Instances list')
        rows = ["Address", "Country", "Mirrors", "Status", "Privacy policy", "DDos Protection / MITM", "Owner", "Notes"]
        for instance in self.config["instances"]["https"]:
            rows.extend(self._create_http_row(instance))

        self.md.new_table(columns=8, rows=len(self.config["instances"]["https"]) + 1, text=rows, text_align='center')

        self.md.new_line()

        # Onion
        self.md.new_header(level=1, title='Onion instances list')
        rows = ["Address", "Country", "Mirrors", "Associated clearnet instance", "Privacy policy", "Owner", "Notes"]
        for instance in self.config["instances"]["onion"]:
            rows.extend(self._create_onion_row(instance))
        self.md.new_table(columns=7, rows=len(self.config["instances"]["onion"]) + 1, text=rows, text_align='center')

    def _create_prerequisite_list(self):
        self.md.new_header(level=2, title='Prerequisites')
        self.md.new_list(self.config["adding_instance"]["prerequisites"])
        self.md.new_line()

    def _create_direction_list(self):
        self.md.new_header(level=2, title='Directions')
        self.md.new_list(self.config["adding_instance"]["directions"], marked_with="1")
        self.md.create_md_file()

    def _create_http_row(self, instance):
        return [
            self.builder.route("url")(instance["url"]),
            self.builder.route("country")(instance["country"]),
            self.builder.route("mirrors")(instance["mirrors"]),
            self.builder.route("status")(instance["status"]),
            self.builder.route("privacy_policy")(instance["privacy_policy"]),
            self.builder.route("ddos_mitm_protection")(instance["ddos_mitm_protection"]),
            self.builder.route("owner")(instance["owner"]),
            self.builder.route("notes")(instance["notes"], instance["is_modified"], instance["source"]),
        ]

    def _create_onion_row(self, instance):
        return [
            self.builder.route("url")(instance["url"]),
            self.builder.route("country")(instance["country"]),
            self.builder.route("mirrors")(instance["mirrors"]),
            self.builder.route("associated_clearnet_instance")(instance["associated_clearnet_instance"]),
            self.builder.route("privacy_policy")(instance["privacy_policy"]),
            self.builder.route("owner")(instance["owner"]),
            self.builder.route("notes")(instance["notes"], instance["is_modified"], instance["source"]),
        ]

    def create(self):
        self._generate_heading()
        self.md.new_line()

        self._create_instance_tables()
        self.md.new_line()

        # Instance adding directions and prerequisites
        self.md.new_header(level=1, title='Adding your instance')
        self._create_prerequisite_list()
        self.md.new_line()
        self._create_direction_list()

        self.md.create_md_file()


with open("instances.yaml") as configuration_yaml:
    data = yaml.safe_load(configuration_yaml)

md_builder = MDInstanceListBuilder(data)
md_builder.create()