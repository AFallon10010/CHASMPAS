# CHASMPAS ETL

CHASMPAS ETL is a script for parsing through the .json test results from the CHASMPAS protocol.

## Overview

There are several test types associated with the CHASMPAS protocol. Each test has different outputs. The tests are
comprised of audiometric tests, questionnaires, triple-digit testing, MLD and dosimetry results.

The tests do not follow a strict format and can be repeated, omitted or sustitutded for different variants (audiometry).
The script takes all possible entries within each test type and parses the test to find if a value exists. Keys that
are not represented within the json branches are skipped (returns a NONE or Not Found).