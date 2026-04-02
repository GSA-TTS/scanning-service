---
status: "accepted"
date: 2026-02-27
decision-makers: []
---

# Adopt MADR as the decision record framework

## Context and Problem Statement

As agile projects age, it is sometimes hard to keep track of the reasoning behind the decisions made. This is especially true as new people join the projects when those involved in the early stages are no longer around. How do we help posterity understand why we did or do things a certain way?

## Decision Drivers

- We want future people (including us) to understand "load-bearing" decisions we made along the way so they can consider the impact of changing them, and to avoid religitating decisions in a vaccuum.
- We want to follow a fairly well-known practice for doing this

## Considered Options

We're not trying to invent the wheel here, we know ADRs are a good idea. So start from there:

- [Nygard's template](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [MADR](https://adr.github.io/madr/)

## Decision Outcome

Chosen option: "MADR", because it's straightforward without being overbearing, and has a simple website.

### Consequences

- Good, because we can get going with _some_ standard
- Good, because that standard has social proof
- Neutral, because there may be something better suited

### Confirmation

Look for docs/decisions and find this document there
