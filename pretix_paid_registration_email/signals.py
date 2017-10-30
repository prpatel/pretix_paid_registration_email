from pretix.base.signals import order_paid
from pretix.base.services.mail import mail
from pprint import pprint
from pretix.multidomain.urlreverse import build_absolute_uri
from pretix.control.signals import nav_event_settings
from django.dispatch import receiver
from django.core.urlresolvers import resolve, reverse
# Register your receivers here

# @receiver(nav_event_settings, dispatch_uid='pretix_paid_registration_email_nav_settings')
# def navbar_settings(sender, request, **kwargs):
#     url = resolve(request.path_info)
#     return [{
#         'label': 'Auto email',
#         'url': reverse('pretix_paid_registration_email:settings', kwargs={
#             'event': request.event.slug,
#             'organizer': request.organizer.slug,
#         }),
#         'active': url.namespace == 'pretix_paid_registration_email' and url.url_name == 'settings',
#     }]

@receiver(order_paid, dispatch_uid='newsletter_ml_nav')
def receiver(sender, order, **kwargs):
    for position in order.positions.all():
        if not position.attendee_email:
            continue

        # print("order object")
        # pprint(vars(order))
        # print("event object")
        # pprint(vars(order.event))
        # print("order.position")
        # pprint(vars(position.item))
        mail_subject = 'Your Ticket for %s' % (order.event.name)
        mail_subject2 = 'Audit: ticket sold for %s' % (order.event.name)
        template_name = '%s.txt' % (order.event.slug)
        print('template name')
        pprint(template_name)
        # {expire_date}, {event}, {code}, {date}, {url}, {invoice_name}, {invoice_company}

        email_context = {
            'event': order.event.name,
            'ordered_by': order.email,
            'url': order.event.settings.imprint_url,
            'contact_mail': order.event.settings.contact_mail,
            'code': order.code,
            'attendee_email': position.attendee_email,
            'attendee_name': position.attendee_name,
            'date_from': order.event.date_from,
            'date_to': order.event.date_to,
            'location': order.event.location,
            'item_purchased': position.item
        }
        # order.event.settings.mail_text_order_paid
        mail(position.attendee_email, mail_subject, template_name , email_context, order.event)
        mail('audit@connectevents.io', mail_subject2, template_name , email_context, order.event)

