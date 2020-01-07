def get_channel_name(party_pk: str) -> str:
    """
    All party models need to send pusher signals
    to this channel name specific for this party
    """
    return 'party-{pk}'.format(pk=party_pk)
