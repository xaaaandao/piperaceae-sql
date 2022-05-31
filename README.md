# dados-imagens

to linux:
`
$ sudo apt-get install -y mysql-server-8.0 mysql-client-8.0
`

to execute mysql:
`
$ sudo su
$ mysql --local-infile=1 -u root -p
`

to download csv:
`
$ make download
`

to create:
`
$ make create
`

to import:
`
$ make import
`

to get samples of pr|sc|rs|sul:
`
$ make pr|sc|rs|sul
`