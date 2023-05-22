import typing as tp


def reformat_git_log(inp: tp.IO[str], out: tp.IO[str]) -> None:
    """Reads git log from `inp` stream, reformats it and prints to `out` stream

    Expected input format: `<sha-1>\t<date>\t<author>\t<email>\t<message>`
    Output format: `<first 7 symbols of sha-1>.....<message>`
    """
    line = inp.readline()
    while line != "":
        if line[-1] == "\n":
            l = line.split('\t')
            n = l[0][:7] + ('.' * (74 - len(l[-1]))) + l[-1]
            out.write(n)
            line = inp.readline()
        else:
            l = line.split('\t')
            n = l[0][:7] + ('.' * (73 - len(l[-1]))) + l[-1]
            out.write(n)
            line = inp.readline()
