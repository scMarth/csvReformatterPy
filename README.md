# csvReformatterPy
A python program that reformats CSVs into a readable text file

## Example:

##### Input:

```
$ cat test.csv
field_one,fieldtwo,fieldthree
value_1_1,value_1_2,value_1_3
value_2_1,value_2_2,value_2_3
value_3_1,value_3_2,value_3_3
value_4_1,value_4_2,value_4_3
```

##### Output:

```
$ cat test_formatted.txt
Record 1:
        field_one: "value_1_1"
        fieldtwo: "value_1_2"
        fieldthree: "value_1_3"

Record 2:
        field_one: "value_2_1"
        fieldtwo: "value_2_2"
        fieldthree: "value_2_3"

Record 3:
        field_one: "value_3_1"
        fieldtwo: "value_3_2"
        fieldthree: "value_3_3"

Record 4:
        field_one: "value_4_1"
        fieldtwo: "value_4_2"
        fieldthree: "value_4_3"
```
