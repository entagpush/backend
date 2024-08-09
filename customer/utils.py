from accounts.models import User
from customer.models import Message


def create_message(
    sender: User,
    receiver: User,
    content: str,
    is_counter_offer=False,
    gig=None,
):
    Message.objects.create(
        sender=sender,
        receiver=receiver,
        content=content,
        is_counter_offer=is_counter_offer,
        gig=gig,
    )
