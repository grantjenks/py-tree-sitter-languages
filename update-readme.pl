#!/usr/bin/env -S perl -n
# Run
#
#   ./update-readme.pl repos.txt | sponge README.rst
#
# to update README.rst
BEGIN {
    @lines = ();
}
next unless (/github/);
chomp;
$url = $_;
$url =~ s= .*==;
$license = $url;
$license =~ s=https://github.com==;
$license = "gh api repos$license -q .license.name";
$license = `$license`;
push @lines, "* $url — licensed under the $license";

END {
    $filename = "README.rst";
    open my $file, '<', $filename or die "Unable to open file: $filename";
    while (<$file> ) {
        unless (m(\* https://github.com/.* — licensed under the)) {
            print;
        }
    }
    print @lines;
    close $file;
}
