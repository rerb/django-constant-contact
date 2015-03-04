import uuid
import unittest

from django.conf import settings
import django.test

from .models import (ConstantContact,
                     ConstantContactAPIError,
                     EmailMarketingCampaign)


ORG_ADDRESS = {
        'organization_name': 'My Organization',
        'address_line_1': '123 Maple Street',
        'address_line_2': 'Suite 1',
        'address_line_3': '',
        'city': 'Anytown',
        'state': 'MA',
        'international_state': '',
        'postal_code': '01444',
        'country': 'US'
}


class ConstantContactTests(unittest.TestCase):

    def setUp(self):
        self.cc = ConstantContact()
        self.email_marketing_campaign = None
        self.email_marketing_campaign_kwargs = {
            'name': 'Test Campaign {0}'.format(uuid.uuid4()),
            'email_content': '<html><body>Test Email Content</body></html>',
            'from_email': settings.CONSTANT_CONTACT_FROM_EMAIL,
            'from_name': 'Test Sender',
            'reply_to_email': settings.CONSTANT_CONTACT_REPLY_TO_EMAIL,
            'subject': 'Test Subject',
            'text_content': '<text>Test Text Content</text>',
            'address': ORG_ADDRESS}

    def tearDown(self):
        if self.email_marketing_campaign:
            # Call delete on any email marketing campaign
            # we created, which should also delete it up
            # on Constant Contact's servers.
            self.email_marketing_campaign.delete()

    def test_connect(self):
        response = self.cc.api.get('/account/info')
        self.assertEqual(200, response.status_code)

    def test_create_email_marketing_campaign(self):
        self.email_marketing_campaign = self.cc.new_email_marketing_campaign(
            **self.email_marketing_campaign_kwargs)
        self.assertIsInstance(self.email_marketing_campaign,
                              EmailMarketingCampaign)

    def test_update_email_marketing_campaign(self):
        """Can we update an Email Marketing Campaign?
        Will fail if test_create_email_marketing_campaign fails.
        """
        self.email_marketing_campaign = self.cc.new_email_marketing_campaign(
            **self.email_marketing_campaign_kwargs)

        update_kwargs = self.email_marketing_campaign_kwargs
        updated_subject = (
            self.email_marketing_campaign.data['subject'] + 'Tom Brady')
        update_kwargs['subject'] = updated_subject
        update_kwargs['email_marketing_campaign'] = (
            self.email_marketing_campaign)

        self.email_marketing_campaign = (
            self.cc.update_email_marketing_campaign(**update_kwargs))

        self.assertEqual(updated_subject,
                         self.email_marketing_campaign.data['subject'])

    def test_delete_email_marketing_campaign(self):
        """Can we delete an email marketing campaign?
        """
        email_marketing_campaign = self.cc.new_email_marketing_campaign(
            **self.email_marketing_campaign_kwargs)
        self.cc.delete_email_marketing_campaign(
            email_marketing_campaign)

    def test_failed_delete_email_marketing_campaign_raises_exception(self):
        """When a delete fails, is an exception raised?
        """
        # Try to delete a bogus ID:
        email_marketing_campaign = EmailMarketingCampaign.objects.create(
            data={'id': 1})
        self.assertRaises(ConstantContactAPIError,
                          self.cc.delete_email_marketing_campaign,
                          email_marketing_campaign)

    def test_server_version_is_removed_upon_delete_of_email_marketing_campaign(
            self):
        """When EmailMarketingCampaign deleted, is the CC version deleted?
        """
        email_marketing_campaign = self.cc.new_email_marketing_campaign(
            **self.email_marketing_campaign_kwargs)
        # GET the email marketing campaign:
        cc = ConstantContact()
        url = cc.api.join('/'.join([
            cc.EMAIL_MARKETING_CAMPAIGN_URL,
            str(email_marketing_campaign.data['id'])]))
        response = url.get()
        self.assertEqual(200, response.status_code)
        # Delete the EmailMarketingCampaign:
        email_marketing_campaign.delete()
        # Same GET should 404 now:
        response = url.get()
        self.assertEqual(404, response.status_code)

    def test_inline_css(self):
        """Can we inline CSS?

        Needs better test HTML to actually test output of inline_css.
        Since we're using MailChimp's API to do the inlining, we don't
        have to unit test their service, so we'll assume it works.  If
        we switch ConstantContact.inline_css() to a different implementation,
        we might need more rigorous tests.  For now, if we can call into
        inline_css() without an Exception, that's good enough.
        """
        html = '<html><head></head><body></body></html>'
        inlined_html = self.cc.inline_css(html)

        self.assertEqual(html, inlined_html)

    def test_preview_email_marketing_campaign(self):
        """Can we preview an Email Marketing Campaign?

        Pretty weak test.  Makes no assertions.
        """
        self.email_marketing_campaign = self.cc.new_email_marketing_campaign(
            **self.email_marketing_campaign_kwargs)
        html, text = self.cc.preview_email_marketing_campaign(
            self.email_marketing_campaign)


class EmailMarketingCampaignTests(django.test.TestCase):

    def test_pre_save_works(self):
        """Does pre_save set constant_contact_id?
        """
        data = {'id': 1}
        emc = EmailMarketingCampaign(data=data)
        emc.save()
        self.assertEqual(emc.constant_contact_id, '1')

    def test_pre_delete_fires(self):
        """Is pre_delete wired up correctly?

        If yes, it should raise an exception when we try to delete
        an EmailMarketingCampaign with a bogus constant_contact_id.
        """
        data = {'id': 1}
        emc = EmailMarketingCampaign(data=data)
        emc.save()

        self.assertRaises(ConstantContactAPIError, emc.delete)
