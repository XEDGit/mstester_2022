# mstester (2022 subject)
Welcome to the minishell tester, this script will make you test your minishell in a very fast and comprehensive manner with the standard mode, or in a more dynamic and experimental way, thanks to the interactive mode.

## Run

Using tests file:
```shell
    ./tester.py [-oex] [tests_file] [file_line]
```
Interactive mode:
```shell
	./tester.py -i [-oex]
```
    tests_file:    Path to the text file containing the tests, one per line (default: "./mstester_2022/tests")
    file_line:     Tests only the specified line of the file specified byt file path [optional]

## Flags (optional)
    -h:          Display help text
    -i:          Interactive mode
    -o:          Print stdout of both minishell and bash
    -e:          Print stderr of both minishell and bash
    -x `path`:   Path to your minishell executable

## Troubleshooting
Make sure you have set the global variable `rl_outstream = stderr;` to set the output of readline to the stderr as bash does, you can find more informations [here](http://users.softlab.ntua.gr/facilities/documentation/unix/gnu/readline/readline_28.html)

If the script reports any error, make sure you're using the `-x path` flag and you're specifying the `tests_file`

## Tests crowdsourcing
The tests file is a crowdsourced collection of command to challenge your minishell, if you have some ideas about what to add feel free to create a pull request
