# Internship Application Tracker
This project is a python application that connects to a Yahoo Mail acccount, reads recent emails, identifies emails that may be related to internship applications, and stores information about processed emails in a local SQLite database.

The project is being developed in stages. The initial version does **NOT** use the OpenAI API. Instead, it uses a simple keyword-based filter. OpenAi will be added later to provide intelligent email classification, information extraction, and application matching.

## Table of Contents
* [Overview](#overview)
* [Current Features](#current-features)
* [Planned Features](#planned-features)
* [How It Works](#how-it-works)
* [Project Architecture](#project-architecture)
* [Project Structure](#project-structure)
* [Requirements](#requirements)
* [Installation](#installation)
* [Yahoo Mail Setup](#yahoo-mail-setup)
* [Environment Variables](#environment-variables)
* [Running the Application](#running-the-application)
* [How Each File Works](#how-each-file-works)
* [Database](#database)
* [Email Processing Pipeline](#email-processing-pipeline)
* [Internship Detection](#internship-detection)
* [Current Limitations](#current-limitations)
* [Development Roadmap](#development-roadmap)
* [Security](#security)
* [Troubleshooting](#troubleshooting)
* [Future OpenAI Integration](#future-openai-integration)

## Overview
My Internship Application Tracker is designed to automatically monitor my Yahoo Mail inbox for emails related to internship applications. 

The long term goal is to turn the application into a personal internship application management system.

For example, the system should eventually be able to recognize that these emails all belong to the same application:

```bash
Company: Acme

Title: Software Engineer Intern

1. Application recieved 

Next

2. Online Assessment

Next

3. Interview Invitation

Next

4. Interview Confirmation

Next

5. Offer or Rejection

```

This project will eventually track:
* Company
* Position
* Location
* Application Date
* Application Status
* Interview Dates
* Deadlines
* Recruiter Information
* Next Actions
* Related Emails
* Application History


## Current Features 
The current version focuses on building the foundation of the project wiithout using Open AI

## Planned Features

## How It Works

## Project Architecture

## Project Structure

## Requirements

## Installation

## Yahoo Mail Setup

## Environment Variables

## Running the Application

## How Each File Works

## Database 

## Email Processing Pipeline

## Internship Detection 

## Current Limitations

## Development Roadmap

## Security

## Troubleshooting 

## Future OpenAI Integration