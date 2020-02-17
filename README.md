# Subdomain formatter v0.1c #
A short script that formats a list of subdomains to give a better insight into the domain structure of an organization.

## Usage ##
```
usage: formatter.py [-h] -i input_file [-b base_domain] [-p]

Subdomain formatter v0.1c

optional arguments:
  -h, --help      show this help message and exit
  -i input_file   Input file with a list of subdomains.
  -b base_domain  Base domain.
  -p              Flag: switch on paragraphed style.
```

## Example ##
For the following input file:
```
branch.github.com
brandguide.github.com
cla.github.com
classroom.github.com
cloud.github.com
community.github.com
education.github.com
edu.github.com
enterprise.github.com
f.cloud.github.com
github.com
help.github.com
import2.github.com
importer2.github.com
import.github.com
jira.github.com
jobs.github.com
lab.github.com
lab-sandbox.github.com
learn.github.com
mac-installer.github.com
maintainers.github.com
octostatus-production.github.com
pkg.github.com
porter2.github.com
porter.github.com
registry.github.com
review-lab.github.com
slack.github.com
smtp.github.com
staging-lab.github.com
status.github.com
styleguide.github.com
support.enterprise.github.com
visualstudio.github.com
vpn-ca.iad.github.com
vscode-auth.github.com
www.github.com
```
The program outputs the following lines. Inferred subdomains are marked with an asterisk, i.e. for the base domain `c.d`, if `a.b.c.d` is present, but `b.c.d` isn't, the latter will be added to the output with an asterisk at the end.
```
$ python3 formatter.py -i input_file.txt
github.com
	branch.github.com
	brandguide.github.com
	cla.github.com
	classroom.github.com
	cloud.github.com
		f.cloud.github.com
	community.github.com
	edu.github.com
	education.github.com
	enterprise.github.com
		support.enterprise.github.com
	help.github.com
	iad.github.com *
		vpn-ca.iad.github.com
	import.github.com
	import2.github.com
	importer2.github.com
	jira.github.com
	jobs.github.com
	lab.github.com
	lab-sandbox.github.com
	learn.github.com
	mac-installer.github.com
	maintainers.github.com
	octostatus-production.github.com
	pkg.github.com
	porter.github.com
	porter2.github.com
	registry.github.com
	review-lab.github.com
	slack.github.com
	smtp.github.com
	staging-lab.github.com
	status.github.com
	styleguide.github.com
	visualstudio.github.com
	vscode-auth.github.com
	www.github.com
```
