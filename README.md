Microservice architecture application for ACIT-3855 - Service Based Architectures.

This is an application for reporting and analyzing users' sleep patterns and daily moods to provide information to the users and staff.

The events are sleep stats reported every morning and day stats reported every night. The sleep stats are expected to be very high in the mornings with as many as 100 requests per second. The day stats are expected to be very high at nights with as many as 100 requests per second.

The requests are stored to allow the following:
- Users to view history of their sleep and corresponding feelings.
- Users to receive automatic suggestions regarding their sleep.
- Analysis of the data to study effects of sleep lengths and patterns and how they affect different demographics of users.

Users of the system are customers (ie., those tracking sleep) and sleep scientists.