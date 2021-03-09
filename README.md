# Raspberry-Python-MeteoStation

This is my side project which helped me learn how to use Raspberry Pi. I used it to create some kind of meteo station with two sensors connected via I2C interface. With Python scripts Raspberry execute measurements and save them to the PostgreSQL database. All data are presented by Django application. This project was also a good opportunity to remaind how write Ansible playbooks for automatic deployment.

## Stack

* Ubuntu
* Python
* Django
* HTML
* Ansible
* Raspberry Pi with I2C interface

## Requirements

* Raspberry Pi 4 model B with Ubuntu server 20.04
* GY-68 BMP180 sensor
* GY-30 H1750 sensor
* 1 Host with SSH access to Raspberry for Ansible (pref. Linux)

