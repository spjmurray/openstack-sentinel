# OpenStack Sentinel

## Description

Sits in front of your federated cloud allowing admin level access to trusted parties,
with collections scoped to their specific domain.

## Contents

1. [Detailed Description](#detailed-description)
    1. [Organization](#organization)
    2. [Technical Details](#technical-details)
2. [Installation](#installation)
    1. [pip](#pip)
    2. [dpkg](#dpkg)
3. [Configuration](#configuration)
    1. [PKI](#pki)
    2. [Apache](#apache)
    3. [Sentinel](#sentinel)
4. [IdP Onboarding](#idp-onboarding)
    1. [Connecting to Sentinel](#connecting-to-sentinel)
        1. [Python](#python)
        2. [Ruby](#ruby-fog-openstack)
5. [Testing](#testing)

## Detailed Description

Although Keystone has come along leaps and bounds as regards domain admins the rest
of openstack has been slow to catch up.  Granting admin rights to a user means that
when lisitng resource types they get everything; there is no domain scoping.

This is a bigger issue for federated public clouds in that data sovereignty must be
preserved across international boundaries for customers on a multi-tenant cloud who
have not opted into federated cloud services.  Administrative access to all virtual
machines may reveal sensitive information about customers, their products etc.

This is where sentinel comes in.  It acts as a middle-man between a federated IdP
and administrative functions of the SP cloud.  Crucially we never give out
administrative cloud access to a 3rd party, and only return collections of resources
scoped to projects within their domain.

### Organisation

When onboarding a new IdP, the SP will create a domain for the IdP's users and projects.
A role is surfaced within the domain to be applied to users and groups.  This role
is used to infer a SP specific role in the default domain, and thus acts as an
abstraction layer, so if IdP wants to use `User` and the SP still uses `_member_` this
can be facilitated easily.

The IdP is free to create users, projects, groups within their domain and assign
role associations which allows users to operate on the SP cloud via standard K2K
federation mechanisms.  The IdP is also granted access to modify project and user
quotas within their domain, based on a trust model.  The IdP also has access to
retrieve scoped event data for billing and scoped resource collections for any
necessary sanity checks.

### Technical Details

Sentinel is a simple REST application that imitates an OpenStack cloud, implementing
an identity service to issue tokens and return a service catalog.  Various
service endpoints are surfaced to allow IdP management applications to handle their
user's needs and collect billing information.

The SP maintains PKI which authorizes an SP to interact with Sentinel, this is
supported by all major clients.  The certificate CN maps to the IdP domain
within the SP cloud, and is used to override all explicit domain references within
the identity service.  It is also used to generate a collection of projects
within that domain which is then used to scope even and collection data.  All
tainted resource IDs are also checked for ownership by that domain.

The subject access tokens passed around are simple json strings, and are only
used to scope operations to a specific project.

The entire system is stateless, so there is no reliance on any external components
e.g. databases, memcache.

## Installation

### pip

For basic hacking you can probably just get away with installing it into one of
python's global search paths.

    sudo -H pip install --upgrade --prefix /usr/local/ .

### dpkg

Production deployments will want to have native packages available.  We use FPM
to streamline the process.

    apt-get -y install python-setuptools gcc make ruby-dev libffi-dev
    gem install fpm
    fpm -f -s python -t deb \
      --depends apache2 \
      --depends python-pecan \
      --depends python-keystoneclient \
      --depends python-novaclient \
      --depends python-neutronclient \
      --depends python-cinderclient \
      --depends python-ceilometerclient \
      --depends python-oslo.config \
      --depends python-stevedore \
      .

## Configuration

### PKI

We need to create a secure CA to authenticate clients and encrypt traffic across
the internet.  Typically easyrsa is a good and simple option.

    git clone https://github.com/OpenVPN/easy-rsa
    cd easy-rsa/easyrsa3
    ./easyrsa init-pki

First create the CA:

    ./easyrsa build-ca

Also create a CRL so we can stop revoked certificates from gaining access:

    ./easyrsa gen-crl

Next generate the server certificate.  Ensure you set the SAN as learning the
client hostname from the CN field has been deprecated for a long time and will
result in client warnings:

    ./easyrsa --subject-alt-name=DNS:sentinel.example.com build-server-full sentinel.example.com nopass

And finally to issue certificates to IdPs:

    ./easyrsa build-client-full my.trusted.idp.com nopass

Remember to keep your CA private key physically locked away.  It's also far
more secure for the IdP to create their key and certificate signing request
locally, then have the CA sign the CSR.

### Apache

Sentinel is a WSGI python application and needs to sit behind a web server.
This is a typical apache configuration which requires TLSv2 or higher and
high security ciphers.  The important lines are the fact that client
verification is required as this replaces keystone's username/password
functionality, and also we need to export TLS variables to the WSGI environment
in order to get access to the client identity.

    <VirtualHost *:4567>
        SSLEngine on
        SSLProtocol ALL -SSLv2 -SSLv3 -TLSv1

        SSLCipherSuite EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH
        SSLCertificateFile /etc/sentinel/ssl/easy-rsa/easyrsa3/pki/issued/sentinel.example.com.crt
        SSLCertificateKeyFile /etc/sentinel/ssl/easy-rsa/easyrsa3/pki/private/sentinel.example.com.key

        SSLCACertificateFile /etc/sentinel/ssl/easy-rsa/easyrsa3/pki/ca.crt
        SSLCARevocationFile /etc/sentinel/ssl/easy-rsa/easyrsa3/pki/crl.pem
        SSLVerifyClient require
        SSLOptions +StdEnvVars

        WSGIDaemonProcess sentinel processes=1 user=www-data group=www-data threads=1 display-name=(wsgi:sentinel)
        WSGIScriptAlias / /usr/local/lib/python2.7/dist-packages/sentinel/api/wsgi_app.py
        WSGIProcessGroup sentinel
        WSGIScriptReloading On

        <IfVersion >= 2.4>
          ErrorLogFormat "%{cu}t %M"
        </IfVersion>

        ErrorLog /var/log/apache2/sentinel.log
        CustomLog /var/log/apache2/sentinel_access.log combined

        <Directory /usr/local/lib/python2.7/dist-packages/sentinel/api>
    	    Require all granted
        </Directory>
    </VirtualHost>

### Sentinel

Sentinel's main configuration file is a simple ini based affair with many similarities
to standard OpenStack components.  You should only need to modify the `identity`
section which identifies the SP cloud identity endpoint and administrative access
credentials.

To automatically generate the configuration template:

    oslo-config-generator --namespace sentinel > /etc/sentinel/sentinel.conf

The whitelist section selects which fields are not filtered out of queries that
return resources or collections.  This is purely illustrative, however it gives us
a mechanism to remove fields which are unnecessary e.g. an IdP doesn't need to know
about hypervisors servers are resident on, and my leak information about the SP
cloud architecture.

The other important configuration is the domain mapping.  When an IdP is onboarded
the SP will create a domain for them to create users, groups and projects in etc.
This is simply a JSON dictionary which maps the certificate CN which you specified
when creating a client certificate, to their domain ID.

    {
      "my.trusted.idp.com": "4ca11fb8c4f943d4b69c0205dcb74603"
    }


## IdP Onboarding

First thing you need to do is create the IdP's domain:

    openstack domain create my.trusted.idp.com

Then we create a role in the domain to be associated by the IdP to their users,
groups and projects.  The IdP may ask for a specific role name to ease integration
with their management application.

    openstack role create --domain my.trusted.idp.com user

Finally we need to apply inference rules so that the domain role maps onto a
SP cloud role.  At present this functionality isn't available via the openstack
client, so we have to add this in manually.  A simple script may look like the
following.

    #!/usr/bin/python
    import os
    import sys
    
    from keystoneauth1 import session
    from keystoneauth1.identity import v3
    from keystoneclient.v3 import client
    
    auth = v3.Password(auth_url='https://cloud.example.com:5000/v3',
                       username='admin',
                       password='password',
                       user_domain_name='default',
                       project_name='admin',
                       project_domain_name='default')
    session = session.Session(auth=auth)
    keystone = client.Client(session=session)
    keystone.inference_rules.create(sys.argv[1], sys.argv[2])

This consumes UUIDs which map a prior role to an inferred role.  You can infer
multiple roles if the underlying SP cloud requires multiple roles in order to
provide full functionality.

    ./inference.py c06c73240ff44190a8644b1d626510c3 a6a386defcb0438fa013dbe038562c39

Now you know the IdP's certificate CN and their domain you can add the domain
mapping into Sentinel's main configuration and reload the WSGI application.

### Connecting to Sentinel

The IdP should be in possession now of the SP's Sentinel identity endpoint,
their private and public keys and can now start performing administrative
operations.  The following section shows how to interact via popular libraries.

#### Python

    #!/usr/bin/python
    
    from keystoneauth1 import session
    from keystoneauth1.identity import v3
    from keystoneclient.v3 import client
    
    auth = v3.Password(auth_url='https://sentinel.example.com:4567/identity/v3')
    session = session.Session(auth=auth,
                              verify='ca.crt',
                              cert=('my.trusted.idp.com.crt', 'my.trusted.idp.com.key'))
    identity = client.Client(session=session)

#### Ruby (Fog OpenStack)

    #!/usr/bin/ruby
    
    require 'fog/openstack'
    require 'openssl'
    
    options = {
      :openstack_auth_url => 'https://sentinel.example.com:4567/identity/v3/auth/tokens',
      :openstack_username => 'required-by-library',
      :openstack_api_key  => 'required-by-library',
      :connection_options => {
        :ssl_verify_peer => true,
        :ssl_ca_file     => 'ca.crt',
        :client_cert     => 'my.trusted.idp.com.crt',
        :client_key      => 'my.trusted.idp.com.key',
      },
    }
    
    compute = Fog::Compute::OpenStack.new(options)

## Testing

This shouldn't get any lower without good reason.

    pylint sentinel

This will always work.

    python -m testtools.run discover sentinel.tests.functional
