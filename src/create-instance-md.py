"""Extremely quick and dirty module for creating a markdown file from the instances.yaml file"""
from urllib.parse import urlparse

import yaml
from mdutils.mdutils import MdUtils


def create_table(table_data, instance_data):
    rows = []
    for field, value in instance_data.items():
        if value is None:
            rows.append("")
        
        # Use markdown links for Addresses
        elif field in ["url", "associated_clearnet_instance"]:
            url = urlparse(value).hostname
            rows.append(f"[{url}]({value})")

        elif field == "status" and value is not None:
            if value.get("display_content_is_image"):
                rows.append(f"[![{value['display_content_image_fallback']}]({value['display_content']})]({value['url']})")
            else:
                rows.append(f"[{value['display_content']}]({value['url']})")
        
        elif field == "country" and value:
            rows.append(f"{value['flag']} {value['name']}")

        elif field == "modified":
            if value.get("is_modified"):
                rows.append(f"[Yes]({value['source_url']})")
            else:
                rows.append("No")

        # We're going to use a markdown link here
        elif field == "privacy_policy":
            rows.append(f"[Here]({value})")

        # Handle author name
        elif field == "owner":
            # Assuming github url
            author_name = value.split("/")
            rows.append(f"[@{author_name[-1]}]({value})")
        else:
            rows.append(value)

    table_data.extend(rows)


with open("instances.yaml") as configuration_yaml:
    data = yaml.safe_load(configuration_yaml)

instance_list = data["instances"]

# Initial information
md_instance_list = MdUtils(file_name='Invidious-Instances.md')
md_instance_list.new_header(level=1, title='Public Instances')
md_instance_list.new_paragraph("Uptime History: [uptime.invidious.io](https://uptime.invidious.io)")
md_instance_list.new_paragraph("Instances API: [api.invidious.io](api.invidious.io)")


# Clearnet instances
md_instance_list.new_header(level=1, title='Instances list')
table_data = ["Address", "Country", "Status", "Privacy policy", "DDos Protection / MITM", "Owner", "Modified"]
for instance_data in instance_list["https"]:
    create_table(table_data, instance_data)

md_instance_list.new_line()
md_instance_list.new_table(columns=7, rows=len(instance_list["https"]) + 1, text=table_data, text_align='center')


# Onion instances
md_instance_list.new_header(level=1, title='Tor onion instances list')
table_data = ["Address", "Country", "Associated clearnet instance", "Privacy policy", "Owner", "Modified"]
for instance_data in instance_list["onion"]:
    create_table(table_data, instance_data) 

md_instance_list.new_line()
md_instance_list.new_table(columns=6, rows=len(instance_list["onion"]) + 1, text=table_data, text_align='center')


# Instance adding directions and prerequisites
md_instance_list.new_header(level=1, title='Adding your instance')

# Prerequisites
md_instance_list.new_header(level=2, title='Prerequisites')
md_instance_list.new_list(data["adding_instance"]["prerequisites"])
md_instance_list.new_line()

# Directions
md_instance_list.new_header(level=2, title='Directions')
md_instance_list.new_list(data["adding_instance"]["directions"], marked_with="1")
md_instance_list.create_md_file()
