# OpenStack Sentinel

## Description

Sits in front of your federated cloud allowing admin level access scoped to trusted
parties.

## Installation

### pip

For basic hacking you can probably just get away with installing it into one of
python's global search paths.

    sudo pip install --prefix /usr/local/ .

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
      .

## Testing

python -m testtools.run discover sentinel.tests.functional
