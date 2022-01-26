# ParseShares
a crappy parser for [SharpShares](https://github.com/mitchmoser/SharpShares) output.

I'm a fan of this tool, but the output can be a firehose and difficult to grep through for the useful stuff.

Hopefully you find it useful too.

# Usage
1. obligatory `pip3 install -r requirements.txt` (or just `easy_intall argparse`)
1. run sharpshares, copy output from stdout or use `/outfile` option
1. paste output into file, or copy it
1. run `python3 parseshares.py -f sharpshares.log -p`

# Notes
1. I wrote this tool in approximately 15 minutes so don't be surprised when it breaks
1. please send feature/output format requests