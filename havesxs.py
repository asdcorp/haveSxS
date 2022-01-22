import re

def hash_data(data):
    hashes = [0, 0, 0, 0]

    for i, x in enumerate(data.lower()):
        i = i % 4
        hashes[i] *= 0x1003F
        hashes[i] += ord(x)
        hashes[i] &= 0xFFFFFFFF

    hashed = hashes[0] * 0x1E5FFFFFD27
    hashed += hashes[1] * 0xFFFFFFDC00000051
    hashed += hashes[2] * 0x1FFFFFFF7
    hashed += hashes[3]

    return hashed & 0xFFFFFFFFFFFFFFFF

def generate_pseudo_key(pkg, *, winners = False):
    order = [
        'name',
        'culture',
        'type',
        'version',
        'publicKeyToken',
        'processorArchitecture',
        'versionScope'
    ]

    data = []
    for x in order:
        if x not in pkg:
            continue

        data.append([x, pkg[x]])

    key = 0
    for x in data:
        if winners == True and x[0] == "version":
            continue

        if x[1] == "none":
            continue

        hash_attr = hash_data(x[0])
        hash_val = hash_data(x[1])

        both_hashes = hash_val + 0x1FFFFFFF7 * hash_attr
        key = both_hashes + 0x1FFFFFFF7 * key

    key &= 0xFFFFFFFFFFFFFFFF
    return '{:016x}'.format(key)

def generate_sxs_name(pkg, *, winners = False):
    pseudo_key = generate_pseudo_key(pkg, winners=winners)
    sxs_name = []

    name = re.sub(r'[^A-z0-9\-\._]', '', pkg['name'])

    if len(name) > 40:
        name = name[:19] + '..' + name[-19:]

    if len(pkg['culture']) > 8:
        culture = pkg['culture'][:3] + '..' + pkg['culture'][-3:]
    else:
        culture = pkg['culture']

    sxs_name.append(pkg['processorArchitecture'])
    sxs_name.append(name)
    sxs_name.append(pkg['publicKeyToken'])

    if winners == False:
        sxs_name.append(pkg['version'])

    sxs_name.append(culture)
    sxs_name.append(pseudo_key)

    return '_'.join(sxs_name).lower()
