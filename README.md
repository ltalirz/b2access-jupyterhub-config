# B2ACCESS JupyterHub configuration

This repo contains a [documented JupyterHub configuration](jupyterhub_config.py) for
use with the [B2ACCESS](https://b2access.eudat.eu) Authentication and Authorization infrastructure.

It assumes you have entered the following information in the B2ACCESS client registration form:

 * User name: `aiidalab-demo`
 * Password credential: `afakepw`
 * OAuth client return URL (1): `https://aiidalab-demo.materialscloud.org/hub/oauth_callback`

Note: Start by registering with the [B2ACCESS staging instance](https://unity.eudat-aai.fz-juelich.de/home/) before moving to the B2ACCESS production instance.
