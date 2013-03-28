Copy Queue
==========

A command line "cp" and "mv" that use a queue.

Usage
-----

    cpq file1 /trash/movies/
    cpq file2 /trash/movies
    mvq file3 /trash/movies/

All the three files are put in a queue and only one is
processed at a given time.

Motivation
----------

If you launch the previous 3 commands with "cp" and "mv" in
the background, then all three will run concurrently, thus
your machine will slow down because of the I/O operations.
If you launch them in the foreground, then you have to wait
until one finishes and then you can start the next one.

You can always use a graphical file manager that supports a
copy queue but I prefer to work in bash in combination with
the good old Midnight Commander. And in MC I didn't find this
feature.
