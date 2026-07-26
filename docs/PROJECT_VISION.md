# Project Vision

## What is Movie Excluder?

Movie Excluder is a personal desktop application that helps me discover better movies by permanently excluding the ones I never want to see.

Unlike traditional movie recommendation apps that try to suggest more content, this project focuses on removing unwanted content first. The goal is to reduce noise so that only movies worth considering remain.

## Why am I building it?

Existing movie platforms recommend too many irrelevant movies and give limited control over filtering. I want a system that learns what I never want to watch and remembers those decisions permanently.

## Core Philosophy

- Exclusion comes before recommendation.
- My negative preferences are more important than my positive preferences.
- The app should become cleaner over time as I exclude more content.
- I own the filtering rules.
- The project will be built incrementally, with simple, modular components from the beginning.
- Every major decision should be documented so both humans and AI can easily understand and continue the project.

## Designed for presonal preferences (useful to others as well)

Movie Excluder should be usable by different people, while keeping every user's preferences and movie history private and independent.

## Version 1 Goal

Build a simple desktop application that can:

- Fetch movies.
- Display them.
- Let me exclude unwanted movies.
- Save those exclusions locally.

## Movie Data Source

Movie Excluder will use TMDB to fetch movie information such as titles, posters, genres, ratings, cast and release dates.

TMDB provides the movie data, but it does not control personal preferences. Exclusions, watch history, notes and filtering choices will be stored in the user's own local database.

TMDB Movie ID will be used as the permanent identifier for each movie.

TMDB = movie information
SQLite = user preferences and history

## Completed

- Project foundation
- SQLite database
- TMDB integration
- Search V1
- User state merging

## Current Focus

Movie Details

Build a complete movie details workflow that combines TMDB metadata with the user's local movie state and prepares movies for classification.