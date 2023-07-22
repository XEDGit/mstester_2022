# mstester (2022 subject)
Welcome to the minishell tester, this script will make you test your minishell in a very fast and comprehensive manner with the standard mode, or in a more dynamic and experimental way, thanks to the interactive mode.

## Run

Using tests file:
```shell
./tester.py [-oexd] [tests_file] [file_line]
```
    tests_file:    Path to the text file containing the tests, one per line (default: "./mstester_2022/tests")
    file_line:     Tests only the specified line of the file specified byt file path [optional]
Interactive mode:
```shell
./tester.py -i [-oexd]
```

## Flags (optional)
    -h:          Display help text
    -i:          Interactive mode
    -o:          Show stdout
    -e:          Show stderr
	-d:          Print `diff -u` between outputs
    -x `path`:   Path to your minishell executable

## Troubleshooting
Make sure you have set the global variable `rl_outstream = stderr;` to set the output of readline to the stderr as bash does, you can find more informations [here](http://users.softlab.ntua.gr/facilities/documentation/unix/gnu/readline/readline_28.html)

If the script reports any error, make sure you're using the `-x path` flag and you're specifying the `tests_file`

## Tests file
### Inside the tests file ';' represents '\n', it's used to execute multiple commands in the same test

The tests file is a crowdsourced collection of command to challenge your minishell, if you have some ideas about what to add feel free to create a pull request
