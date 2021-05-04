#!/bin/bash

## Put the path of absorbtion_images
##	relative to this scripts location here.
rel_path='.'
rel_destination_path='../file_list.txt'
echo -e 'time(s)\t''cat\t''file_list' > $rel_destination_path

# Replace with the times measured
for t in 0 15 20 60 90 240
do
	for first_char in 'S' 'N' 'D' 'L'
	do
		echo -e "$t" '\t' "'$first_char'" '\t' "[ " $( ls $rel_path | grep "^$first_char.*=$t" | sed "s/^.*$/\'&\', /g" ) " ]" | sed 's/, *]/ ]/g' >> $rel_destination_path
	done
done
