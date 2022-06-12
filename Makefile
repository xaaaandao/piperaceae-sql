#!/bin/bash
current_date = `date +"d%dm%ma%y"`

download:
	@wget -O $(current_date).csv https://api.splink.org.br/records/format/csv/family/Piperaceae/images/yes
	"baixando arquivo de nome: $(current_date).csv"
