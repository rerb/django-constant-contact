import json

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_delete, pre_save
import jsonfield
import mailchimp
import nap

from utils import (
    CONSTANT_CONTACT_COUNTRIES,
    ConstantContactAPIError,
    ConstantContact)


class ConstantContactAPIError(Exception):
    """An exception that passes error info from response to exception catcher.
    """

    def __init__(self, response, *args, **kwargs):
        super(ConstantContactAPIError, self).__init__(*args, **kwargs)
        self.message = str(response.status_code) + ': ' + response.reason
        self.errors = json.loads(response.content)

    def __str__(self):
        s = '<ConstantContactAPIError ' + self.message + ' '
        for error in self.errors:
            s += str(error)
        s += '>'
        return s


class ConstantContact(object):

    API_URL = 'https://api.constantcontact.com/v2/'
    EMAIL_MARKETING_CAMPAIGN_URL = 'emailmarketing/campaigns'

    def __init__(self):
        self.api = nap.url.Url(
            self.API_URL,
            params={'api_key': settings.CONSTANT_CONTACT_API_KEY,
                    'access_token': settings.CONSTANT_CONTACT_ACCESS_TOKEN})

    def handle_response_status(self, response):
        """Raise an exception for response errors.

        Constant Contact returns some nice error info that we lose if
        we only response.raise_for_status(). So we trap most errors
        and raise exceptions that preserve the error info.

        Calling raise_for_status() catches any other errors.
        """
        if 400 <= response.status_code <= 599:
            raise ConstantContactAPIError(response)

        response.raise_for_status()

    def new_email_marketing_campaign(self, name, email_content, from_email,
                                     from_name, reply_to_email, subject,
                                     text_content, address):
        """Create a Constant Contact email marketing campaign.
        Returns an EmailMarketingCampaign object.
        """
        url = self.api.join(self.EMAIL_MARKETING_CAMPAIGN_URL)

        inlined_email_content = self.inline_css(email_content)

        data = {
            'name': name,
            'subject': subject,
            'from_name': from_name,
            'from_email': from_email,
            'reply_to_email': reply_to_email,
            'email_content': inlined_email_content,
            'email_content_format': 'HTML',
            'text_content': text_content,
            'message_footer': {
                'organization_name': address['organization_name'],
                'address_line_1': address['address_line_1'],
                'address_line_2': address['address_line_2'],
                'address_line_3': address['address_line_3'],
                'city': address['city'],
                'state': address['state'],
                'international_state': address['international_state'],
                'postal_code': address['postal_code'],
                'country': address['country']
            }
        }
        response = url.post(data=json.dumps(data),
                            headers={'content-type': 'application/json'})

        self.handle_response_status(response)

        return EmailMarketingCampaign.objects.create(data=response.json())

    def update_email_marketing_campaign(self, email_marketing_campaign,
                                        name, email_content, from_email,
                                        from_name, reply_to_email, subject,
                                        text_content, address):
        """Update a Constant Contact email marketing campaign.
        Returns the updated EmailMarketingCampaign object.
        """
        url = self.api.join(
            '/'.join([self.EMAIL_MARKETING_CAMPAIGN_URL,
                      str(email_marketing_campaign.constant_contact_id)]))

        inlined_email_content = self.inline_css(email_content)

        data = {
            'name': name,
            'subject': subject,
            'from_name': from_name,
            'from_email': from_email,
            'reply_to_email': reply_to_email,
            'email_content': inlined_email_content,
            'email_content_format': 'HTML',
            'text_content': text_content,
            'message_footer': {
                'organization_name': address['organization_name'],
                'address_line_1': address['address_line_1'],
                'address_line_2': address['address_line_2'],
                'address_line_3': address['address_line_3'],
                'city': address['city'],
                'state': address['state'],
                'international_state': address['international_state'],
                'postal_code': address['postal_code'],
                'country': address['country']
            }
        }
        response = url.put(data=json.dumps(data),
                           headers={'content-type': 'application/json'})

        self.handle_response_status(response)

        email_marketing_campaign.data = response.json()
        email_marketing_campaign.save()

        return email_marketing_campaign

    def delete_email_marketing_campaign(self, email_marketing_campaign):
        """Deletes a Constant Contact email marketing campaign.
        """
        url = self.api.join('/'.join([
            self.EMAIL_MARKETING_CAMPAIGN_URL,
            str(email_marketing_campaign.constant_contact_id)]))
        response = url.delete()
        self.handle_response_status(response)
        return response

    def inline_css(self, html):
        """Inlines CSS defined in external style sheets.

        This implementation requires a Mailchimp account.
        """
        mailchimp_api = mailchimp.Mailchimp(settings.MAILCHIMP_API_KEY)
        response = mailchimp_api.helper.inline_css(html)
        return response['html']

    def preview_email_marketing_campaign(self, email_marketing_campaign):
        """Returns HTML and text previews of an EmailMarketingCampaign.
        """
        url = self.api.join('/'.join([
            self.EMAIL_MARKETING_CAMPAIGN_URL,
            str(email_marketing_campaign.constant_contact_id),
            'preview']))
        response = url.get()
        self.handle_response_status(response)
        return (response.json()['preview_email_content'],
                response.json()['preview_text_content'])


class EmailMarketingCampaign(models.Model):
    """A Constant Contact email marketing campaign.

    "Email marketing campaign" is the Constant Contact term analogous
    to our "Issue".

    WARNING! Deleting an EmailMarketingCampaign will also delete
             the corresponding email marketing campaign at
             Constant Contact.

    The `data` field should be JSON from Constant Contact, describing
    the "real" email marketing campaign that lives on their server.
    (Constant Contact supplies this when an email marketing campaign
    is created or modified.)

    There should be a one-to-one relationship between each
    EmailMarketingCampaign and an email marketing campaign
    living on a Constant Contact server.  To enforce this, the
    ID Constant Contact uses to identify an email marketing campaign
    is stored here as constant_contact_id, with a uniqueness constraint.

    It's a pretty sparse class -- no instance methods at all.  Shouldn't
    these fields just be absorbed into Issue?  I concluded not, since
    there's some processing done here, pulling `constant_contact_id`
    out of `data` in pre_save, cascading a delete into Constant
    Contact in pre_delete, then wiring those up to signals.  Seems
    like I'd just be cluttering up Issue with this stuff.
    """
    constant_contact_id = models.BigIntegerField(unique=True)
    data = jsonfield.JSONField()

    @classmethod
    def pre_save(cls, sender, instance, *args, **kwargs):
        """Pull constant_contact_id out of data.
        """
        instance.constant_contact_id = str(instance.data['id'])

    @classmethod
    def pre_delete(cls, sender, instance, *args, **kwargs):
        """Deletes the CC email marketing campaign associated with me.
        """
        cc = ConstantContact()
        response = cc.delete_email_marketing_campaign(instance)
        response.raise_for_status()

pre_save.connect(EmailMarketingCampaign.pre_save,
                 sender=EmailMarketingCampaign)

pre_delete.connect(EmailMarketingCampaign.pre_delete,
                   sender=EmailMarketingCampaign)
