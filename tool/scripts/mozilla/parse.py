from datetime import datetime

def parse_date(date: str):
    if date == "null":
        return None
    try:
        datetime_object = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        return datetime_object
    except ValueError as e:
        print(e)
        return None


def parse_classification(classification: str):
    # clsfs = []
    bracket_pattern = 'previewer\(([a-zA-Z\&\/\- ]+)\)'
    btacket_gle_pattern = '>(.+)<'
    match = re.search(bracket_pattern, classification)

    if match is not None:
        clsf = match.group(1)
        # clsf = re.sub(r'\/', ' ', clsf)
        # clsf = clsf.strip()
        # splitted = clsf.split('&')
        # clsfs.extend(splitted)
        return clsf
    else:
        match = re.search(btacket_gle_pattern, classification)

        if match is not None:
            clsf = match.group(1)
            # splitted = clsf.split('<>')
            # clsfs.extend(splitted)
            return clsf
        else:
            # clsfs.append(classification)
            return classification