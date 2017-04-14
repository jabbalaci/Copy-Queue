Copy Queue
==========

* Author:  Laszlo Szathmary, 2013 (<jabba.laci@gmail.com>)
* Website: <http://ubuntuincident.wordpress.com/2013/03/28/cpq-and-mvq/>
* GitHub:  <https://github.com/jabbalaci/Copy-Queue>

A command line "cp" and "mv" that use a queue.

Warning! I don't take any responsibility for any loss of data.
Use these scripts at your own risk.

Target operating systems: Unix/Linux. Tested with Python 2.7.

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

Installation
------------

In the file `config.py` you can customize all the directory
and file paths. For an easier understanding, I will explain
the usage of the scripts with the default values.

First, clone this project to the following directory:
`$HOME/python/Copy-Queue`.

Then create the directory `$HOME/bin` and add these two
symbolic links:

    cd $HOME/bin
    ln -s $HOME/python/Copy-Queue/cpq_mvq.py cpq
    ln -s $HOME/python/Copy-Queue/cpq_mvq.py mvq

Make sure that `$HOME/bin` is in your `PATH`.

Finally, create the directory `$HOME/bin/copy_queue`.

Now you are ready to use "cpq" and "mvq".

Tips
----

If there is a directory where you copy/move very often, then
you can add this directory to your `.bashrc` file. For instance,
I copy a lot of videos to my Android phone, thus I created the
following shortcut in my `.bashrc`:

    # Android's Video directory
    A='/media/jabba/2B9A-EB28/Video'
    export A

Then I can copy videos to my Android this way:

    cpq movie.avi $A

Another tip: the scripts create a log file. If you want to see
the copy/move progress, create the following alias:

    alias Q='tail -f $HOME/bin/copy_queue/daemon.log'

To check if the tasks are finished, just launch `Q`:

    $ Q


Update (20170415)
-----------------

I found today a simple Unix batch system called
task spooler ([AUR](https://aur.archlinux.org/packages/task-spooler/),
[PPA](https://launchpad.net/ubuntu/+source/task-spooler)).
Task spooler is more general than my approach since you can send
any Unix command in its queue. Task spooler is a better solution
than mine. It also provides more options, so I suggest using task spooler.
Here is a short video about its usage: <https://www.youtube.com/watch?v=wv8D8wT20ZY>.
