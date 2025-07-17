-- من قام بالسحب من الصراف في Leggett Street يوم الجريمة؟
SELECT name
FROM people
JOIN bank_accounts ON people.id = bank_accounts.person_id
JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
WHERE atm_location = 'Leggett Street'
AND day = 28 AND month = 7 AND year = 2021;

-- أول رحلة غادرت بعد الجريمة من Fiftyville
SELECT id, hour, minute, city
FROM flights
JOIN airports ON flights.destination_airport_id = airports.id
WHERE origin_airport_id = (
    SELECT id FROM airports WHERE city = 'Fiftyville'
)
AND day = 29 AND month = 7 AND year = 2021
ORDER BY hour, minute;

-- من كان على متن الرحلة 36
SELECT name
FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
WHERE flight_id = 36;

-- المكالمات التي حصلت يوم الجريمة ومدتها أقل من دقيقة
SELECT caller.name AS caller, receiver.name AS receiver
FROM phone_calls
JOIN people AS caller ON caller.phone_number = phone_calls.caller
JOIN people AS receiver ON receiver.phone_number = phone_calls.receiver
WHERE day = 28 AND duration < 60;

-- من اشترى تذكرة في نفس اليوم للرحلة رقم 36
SELECT name
FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
WHERE flight_id = 36;

-- المدينة التي سافر إليها السارق
SELECT city
FROM flights
JOIN airports ON flights.destination_airport_id = airports.id
WHERE flights.id = 36;
