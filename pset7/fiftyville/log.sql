-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Investigate the crime scene report on July 28, 2020 on Chamberlin Street
-- Result: Theft took place at 10:15am, there are some witness inteviews on the incident
SELECT description FROM crime_scene_reports
WHERE year = 2020 AND month = 7 AND day = 28 and street = "Chamberlin Street";

-- Check out the interviews of witnesses who were present there at the time
-- Result: 3 witnesses mention the courthouse
SELECT name, transcript FROM interviews
WHERE year = 2020 AND month = 7 AND day = 28;

-- Investigate the leads from the witnesses' statements
-- No.1: Ruth saw the thief get into a car and leave from the courthouse within 10 minutes of the theft
-- Result: All activities are 'exit' and a bunch of license numbers
SELECT activity, license_plate FROM courthouse_security_logs
WHERE year = 2020 AND month = 7 AND day = 28 AND
      hour = 10 and minute >= 15 AND minute <= 30;

-- No.2: Eugene recognized the thief but not their name. Earlier she saw the thief withrawing money from an ATM on Fifer Street
-- Result: A bunch of info about ATM transactions (account numbers)
SELECT account_number, transaction_type, amount FROM atm_transactions
WHERE year = 2020 AND month = 7 AND day = 28 and atm_location = "Fifer Street";

-- No.3: Raymond said as the thief leaving the courthouse, they were talking to someone on the phone for less than a minute
--       The thief planned to take the earliest flight out of Fiftyvill and asked the person on the phone to purchase flight ticket
-- Result: Info about callers and receivers (phone numbers)
SELECT caller, receiver FROM phone_calls
WHERE year = 2020 AND month = 7 AND day = 28 AND duration < 60;

-- Search for people with info matched the results returned from No.1, No.2 and No.3 investigations
-- Note: The thief is among these people
-- Results (Primary Suspects - Thief):
--          Ernest | 94KL13X | 49610011 | (367) 555-5533
--          Russell | 322W7JE | 26013199 | (770) 555-1861
SELECT people.name, people.license_plate, bank_accounts.account_number, people.phone_number FROM people
JOIN bank_accounts ON people.id = bank_accounts.person_id
WHERE
    people.license_plate IN (
        SELECT license_plate FROM courthouse_security_logs
        WHERE year = 2020 AND month = 7 AND day = 28 AND
              hour = 10 and minute >= 15 AND minute <= 30) AND
    bank_accounts.account_number IN (
        SELECT account_number FROM atm_transactions
        WHERE year = 2020 AND month = 7 AND day = 28 and atm_location = "Fifer Street") AND
    people.phone_number IN (
        SELECT caller FROM phone_calls
        WHERE year = 2020 AND month = 7 AND day = 28 AND duration < 60)
ORDER BY people.name;

-- Search for receiver of the phone call from Earnest in No.3 investitation
-- Result (Primary Suspect 1 - Accomplice):
--          Berthold | 4V16VO0 | 94751264 | (375) 555-8161
SELECT people.name, people.license_plate, bank_accounts.account_number, people.phone_number FROM people
JOIN bank_accounts ON people.id = bank_accounts.person_id
WHERE people.phone_number IN (
    SELECT receiver FROM phone_calls
    WHERE
        (year = 2020 AND month = 7 AND day = 28 AND duration < 60) AND
        caller IN (
            SELECT phone_number FROM people
            WHERE name = "Ernest"));

-- Search for receiver of the phone call from Russell in No.3 investitation
-- Result (Primary Suspect 2 - Accomplice):
--          Philip | GW362R6 | 47746428 | (725) 555-3243
SELECT people.name, people.license_plate, bank_accounts.account_number, people.phone_number FROM people
JOIN bank_accounts ON people.id = bank_accounts.person_id
WHERE people.phone_number IN (
    SELECT receiver FROM phone_calls
    WHERE
        (year = 2020 AND month = 7 AND day = 28 AND duration < 60) AND
        caller IN (
            SELECT phone_number FROM people
            WHERE name = "Russell"));

-- Based on clue from No.3 investigation, check out the earliest flight out of Fiftyvill on July 29, 2020
-- Result: Flight No.36 at 8:20
SELECT id, hour, minute FROM flights
WHERE
    (year = 2020 AND month = 7 AND day = 29) AND
    origin_airport_id IN (
        SELECT id FROM airports
        WHERE city = "Fiftyville")
ORDER BY hour, minute;

-- Check the passengers on that flight
-- If Ernest or Russell is on the list, we will have got our thief and accomplice
-- Result:
--          Ernest is the thief
--          Therefore, the accomplice is Berthold
SELECT name FROM people
WHERE passport_number IN (
    SELECT passengers.passport_number FROM passengers
    JOIN flights ON flights.id = passengers.flight_id
    WHERE
        (flights.year = 2020 AND flights.month = 7 AND flights.day = 29) AND
        flights.id = 36)
ORDER BY name;

-- Final investigation: The destination of that flight
-- Result: London
SELECT city FROM airports
WHERE id IN (
    SELECT destination_airport_id FROM flights
    WHERE
        (flights.year = 2020 AND flights.month = 7 AND flights.day = 29) AND
        flights.id = 36);