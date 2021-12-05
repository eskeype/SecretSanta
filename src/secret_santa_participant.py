import random


def is_derangement(cand):
    if len(cand) < 2:
        return False

    for i, v in enumerate(cand):
        if i == v:
            return False
    return True


def get_random_derangement(n):
    if n < 2:
        raise Exception(
            "Can't have derangement of length < 2. Length is {}".format(n))

    nums = list(range(n))

    while True:
        random.shuffle(nums)
        if is_derangement(nums):
            return nums


class Participant:
    def __init__(self, name, email, address):
        self.name = name
        self.email = email
        self.address = address

    def get_name(self):
        return self.name

    def get_email(self):
        return self.email

    def get_address(self):
        return self.address

    def _members(self):
        return (self.name, self.email, self.address)

    def __eq__(self, other):
        if (type(self) == type(other)):
            return self._members() == other._members()
        else:
            return False

    def __hash__(self):
        return hash(self._members())


def is_valid_matching(matching):
    for sender, receiver in matching.items():
        if sender.get_address() == receiver.get_address():
            return False
    return True


def get_matching(participants):
    while True:
        derangement = get_random_derangement(len(participants))
        matching = {}

        for sender, receiver in enumerate(derangement):
            matching[participants[sender]] = participants[receiver]

        if is_valid_matching(matching):
            return matching
