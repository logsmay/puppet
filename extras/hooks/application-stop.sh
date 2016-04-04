#!/usr/bin/env bash

if ( initctl status puppet | grep start ); then
  initctl stop puppet
fi