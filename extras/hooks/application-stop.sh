#!/usr/bin/env bash

if ( sudo initctl status puppet | grep start ); then sudo initctl stop puppet; fi