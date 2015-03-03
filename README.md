[![Build Status](https://drone.io/github.com/AASHE/django-constant-contact/status.png)](https://drone.io/github.com/AASHE/django-constant-contact/latest)

# django-constant-contact

Django package for creating email marketing campaigns in Constant Contact

## Installation

Using pip:

    pip install django-constant-contact

## Settings

The following variables should be set in your settings.py:

    CONSTANT_CONTACT_API_KEY
    CONSTANT_CONTACT_ACCESS_TOKEN
    CONSTANT_CONTACT_FROM_EMAIL
    CONSTANT_CONTACT_REPLY_TO_EMAIL
    CONSTANT_CONTACT_USERNAME
    CONSTANT_CONTACT_PASSWORD

`CONSTANT_CONTACT_API_KEY` is assigned by Constant Contact when
you register your application. (You need to register as a
Constant Contact developer.)

`CONSTANT_CONTACT_ACCESS_TOKEN` is the access token granted to
your application by a Constant Contact user. This is the User
who will own all Constant Contact versions of uploaded Issues.

## Usage Examples

Create a new marketing campaign:

    email_content = "<html>....</html>"
    text_content = "blah blah blah"
    constant_contact = ConstantContact()

    options = {name: , from_email: , email_content: , text_content:, ....}

    try:
      campaign = constant_contact.new_email_marketing_campaign(options)
    except ConstantContactAPIError as exc:
      print exc.errors

Update an existing campaign (stored in a model):

    options['email_marketing_campaign'] = campaign
    options['name'] = "new name"

    try:
      constant_contact.update_email_marketing_campaign(options)
    except ConstantContactAPIError as exc:
      print exc.errors
