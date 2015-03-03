import mailchimp


CONSTANT_CONTACT_COUNTRIES = [
    'AF', 'AX', 'AL', 'DZ', 'AS', 'AD', 'AO', 'AI', 'AQ', 'AG', 'AR', 'AM',
    'AW', 'AU', 'AT', 'AZ', 'BS', 'BH', 'BD', 'BB', 'BY', 'BE', 'BZ', 'BJ',
    'BM', 'BT', 'BO', 'BA', 'BW', 'BV', 'BR', 'IO', 'BN', 'BG', 'BF', 'BI',
    'KH', 'CM', 'CA', 'CV', 'KY', 'CF', 'TD', 'CL', 'CN', 'CX', 'CC', 'CO',
    'KM', 'CG', 'CD', 'CK', 'CR', 'CI', 'HR', 'CY', 'CZ', 'DK', 'DJ', 'DM',
    'DO', 'TL', 'EC', 'EG', 'SV', 'U1', 'GQ', 'ER', 'EE', 'ET', 'FO', 'FK',
    'FJ', 'FI', 'FR', 'GF', 'PF', 'TF', 'GA', 'GM', 'GE', 'DE', 'GH', 'GI',
    'GR', 'GL', 'GD', 'GP', 'GU', 'GT', 'GG', 'GN', 'GW', 'GY', 'HT', 'HM',
    'HN', 'HK', 'HU', 'IS', 'IN', 'ID', 'IQ', 'IE', 'IM', 'IL', 'IT', 'JM',
    'JP', 'JE', 'JO', 'KZ', 'KE', 'KI', 'KW', 'KG', 'LA', 'LV', 'LB', 'LS',
    'LR', 'LY', 'LI', 'LT', 'LU', 'MO', 'MK', 'MG', 'MW', 'MY', 'MV', 'ML',
    'MT', 'MH', 'MQ', 'MR', 'MU', 'YT', 'MX', 'FM', 'MD', 'MC', 'MN', 'ME',
    'MS', 'MA', 'MZ', 'MM', 'NA', 'NR', 'NP', 'NL', 'AN', 'NT', 'NC', 'NZ',
    'NI', 'NE', 'NG', 'NU', 'NF', 'U4', 'MP', 'NO', 'OM', 'PK', 'PW', 'PS',
    'PA', 'PG', 'PY', 'PE', 'PH', 'PN', 'PL', 'PT', 'PR', 'QA', 'RE', 'RO',
    'RU', 'RW', 'BL', 'SH', 'KN', 'LC', 'MF', 'PM', 'VC', 'WS', 'SM', 'ST',
    'SA', 'U3', 'SN', 'RS', 'SC', 'SL', 'SG', 'SK', 'SI', 'SB', 'SO', 'ZA',
    'GS', 'KR', 'ES', 'LK', 'SR', 'SJ', 'SZ', 'SE', 'CH', 'TW', 'TJ', 'TZ',
    'TH', 'TG', 'TK', 'TO', 'TT', 'TN', 'TR', 'TM', 'TC', 'TV', 'UG', 'UA',
    'AE', 'GB', 'US', 'USA', 'UM', 'UY', 'UZ', 'VU', 'VA', 'VE', 'VN', 'VG',
    'VI', 'U2', 'WF', 'EH', 'YE', 'ZM', 'ZW']


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
