# GROUP-NAME - DOBBY - lab 4 - variant 4

This is the Lab4 of Computational Process Organization in ITMO, 2022 spring.

## Project structure

- `future.py` -- includes done, progress, cancel, result
- `future_test.py` -- unit and PBT tests for `future`.

## Features

- IsDone() return True if future evaluation is complete;
- InProgress() return True if future evaluated right now;
- Result(timeout=None) return the future execution result (if the future is done);
- raise the exception (if the future is done and raise an exception);
- block until the future is done (if the timeout is None and future is not done);
- raise TimeoutError after timeout (if the timeout is not None and the future is not done).
- Cancel() cancel a future (if the future not executed).

## Contribution

- Du,Mei(212320038@hdu.edu.cn) -- Implement `future.py`.
- zhuhaonan(921057454@qq.com) -- Implement `future_test.py`.

## Changelog

- 20.06.2022 - 3
  - update README
- 20.03.2022 - 1
  - update future.py and futurs_test.py.
- 20.06.2022 - 0
  - Initial

## Design notes

- we practiced a thread pool.  
- Our library thread pool can do some simple work and can set priorities 
- so that higher-priority tasks are executed first.  
- for some abnormal cases our library also has some processing, 
- to ensure the stability of the program
