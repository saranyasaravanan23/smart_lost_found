
def find_matching_items(lost_item, found_items):

    matches = []

    for item in found_items:

        name_match = (
            lost_item["item_name"].strip().lower()
            == item["item_name"].strip().lower()
        )

        category_match = (
            lost_item["category"].strip().lower()
            == item["category"].strip().lower()
        )

        location_match = (
            lost_item["location"].strip().lower()
            == item["location"].strip().lower()
        )

        if name_match and category_match and location_match:
            matches.append(item)

    return matches
