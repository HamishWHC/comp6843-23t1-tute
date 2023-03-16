# Week 4
- SQL
  - `SELECT _ FROM table_name ...`
  - `INSERT INTO table (col1, col2, ..., colN) VALUES (val1, val2, ..., valN)`
  - `UPDATE _ SET _ = _ ...`
  - `DELETE FROM _ ...`
  - `... -- this is a comment`
  - WHERE:
    - LIKE
      - % (matches multiple chars)
      - _ (matches one char)
  - Aggregates
    - Count: `SELECT COUNT(*) FROM table` - Counts all rows in table.
      - Really the only useful one in web sec (rather than dump a table, just count the rows to get an idea of it's size first).
  - Determining version (e.g. `SELECT <thing_from_below_list>`)
    - `@@Version` - MS SQL (or "SQL Server", stupid name but MS likes to give generic names)
    - `Version()` - MySQL (and PostgreSQL I think)
    - `sqlite_version()` - SQLite
  - Cool input to test for weird shit:
    ```
    '";<lol/>../--#`ls`
    ```
  - WAFs
    - Stripping payloads (terrible)
      - Embed dummies: `' UNUNIONION ...`
    - Blocking completely (better, but prefer not needing it)
  - Mitigations (most to least effective)
    - Parameterised queries (all SQL libraries these days make it clear in their docs how to pass in params: RTFM)
    - WAFs, as above
    - No errors or data returned
      - Boolean based.
      - Timing Attacks
      - Out-of-Band Attacks (in-built functions like `load_file`)
- Local File Inclusion (LFI)
- Server-Side Template Injection (SSTI)
  - `{{ "hello " + "world" }}` => `"hello world"`
  - e.g. `{{ "".__class__.__mro__[1].__subclasses__() }}`



```python
import path

p = path.Path(user_input)
p.begins
with open() as f:
    return f.read()

render_string("{{drink}} " + user_input + "", drinks=[])
```


Notes:
https://hamishwhc.com/6843
https://featherbear.cc/tutoring-unsw-23t1-cs6443/
https://lwaugh.io/6443/