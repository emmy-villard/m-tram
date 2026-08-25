# Challenges
This file lists the main challenges I encountered while working on this project

## Understanding How APIs Work
The Grenoble traffic API is particularly poorly documented, and I had to do a bit of simple reverse engineering to figure out what data I needed and how to get it.

## Managing Installations
I had to ensure that the installations were reproducible—whether they were Python packages or Docker images—so that I could easily deploy my application and run automated tests via GitHub Actions.

## Docker Compose
I had to adapt the .yaml template provided by Airflow by defining variables that I generate automatically (in .env). I also had to make sure that all volumes were properly mounted and secure the installations to prevent losing my database during application updates.
