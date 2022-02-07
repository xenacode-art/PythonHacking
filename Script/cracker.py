# import my_cracker_functions as m
# import shadow as shadow
#
# filename = shadow
# (usernames, salt, hashes) = m.extract_info(filename)
# (username, password) = m.find_password(usernames, salt, hashes)
# m.print_password(username, password)
# Content of my_cracker_functions.py is shown below:
# We define a function that reads lines in the shadow file into a list of Strings
def extract_info(shadow):
    f = open(shadow, "r")
    lines = f.read().split()
    f.close()

    # extract username, salts, hashes into lists
    usernames = []
    salts = []
    hashes = []
    for line in lines:
        if "$6" in line:
            sections = line.split("$")  # clean out the entries into expected part
            usernames.append(sections[0].split(":")[0])  # clean out the entries into expected part
            salts.append(sections[2])  # clean out the entries into expected part
            hashes.append(sections[3].split(":")[0])  # clean out the entries into expected part
            return usernames, salts, hashes


# find a good package to create hashes
# crypt, hash, hashlib, passlib are examples of libraries in python for data dictionaries
# by default, Kali linux uses sha512 encryption and goes 5000 rounds and also uses salt to defeat rainbow attack
# We define a function that finds the passwords, if any can be found
def find_password(usernames, salts, hashes):
    # import and test our hash function
    from passlib.hash import sha512_crypt
    # We call in the special characters from the string library
    import string
    special_char = string.punctuations
    # May 28 Jax
    # policy: uppercase, lowercase, digit

    decodedusernames = []  # a variable to store usernames with broken password
    decodedpasswords = []  # a variable to store passwords that have been broken
    names = []  # a variable to hold all possible name combinations
    list1 = ["j", "J"]
    list2 = ["@", "a", "A"]
    list3 = ["X", "x"]
    # iterate through and append all possibilities
    for l1 in list1:
        for l2 in list2:
            for l3 in list3:
                names.append(l1 + l2 + l3)
                # Next, we check for probable permutations
    from itertools import permutations
    for n in names:
        for c in special_char:
            permu = permutations([n, c, '05', '28'], 4)
    for p in list(permu):
        newpass = ''.join(p)
        # Finally, we iterate through our hashes in the shadow file and check for comparisons
    for i in range(len(hashes)):
        if hashes[i] == sha512_crypt.using(rounds=5000, salt=salts[i]).hash(newpass).split("$")[-1]:
            decodedusernames.append(usernames[i])
            decodedpasswords.append(newpass)
        else:
            print("Password for " + usernames[i] + " is not: " + newpass)
    return decodedusernames, decodedpasswords


# Finally, we print out the decoded logon details using function print_password
def print_password(decodedusernames, decodedpasswords):
    for p in range(len(decodedusernames)):
        print("Decoded logon:");
        print("############################################################")
        print("Username is: " + decodedusernames[p] + " while Password is: " + decodedpasswords[p])
        print("############################################################")
    import sys
    sys.exit()
