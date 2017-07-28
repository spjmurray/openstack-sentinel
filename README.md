# OpenStack Sentinel

## Description

Sits in front of your federated cloud allowing admin level access scoped to trusted
parties.

### Detail

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

## dpkg

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
      .

If you are hacking and don't want to build release packages then you can simply
use PIP:

    sudo -H pip install --upgrade --prefix /usr/local/ .

## Configuration

### PKI

We need to create a secure CA to authenticate clients and encrypt traffic across
the internet.  Typically easyrsa is a good and simple option.  First create the
CA:

    ./easyrsa build-ca

Also create a CRL so we can stop revoked certificates from gaining access:

    ./easyrsa gen-crl

Next generate the server certificate.  Ensure you set the SAN as learning the
client hostname from the CN field has been deprecated for a long time and will
result in client warnings:

    ./easyrsa --subject-alt-name DNS:sentinel.example.com build-server-full sentinel.example.com nopass

And finally to issue certificates to IdPs:

    ./easyrsa build-client-full my.trusted.idp.com nopass

Remember to keep your CA private key physically locked away.

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

TODO

## IdP Onboarding

TODO

## Testing

This shouldn't get any lower without good reason.

    pylint sentinel

This will always work.

    python -m testtools.run discover sentinel.tests.functional
