#!/bin/bash
env $(cat .env | xargs) $@
