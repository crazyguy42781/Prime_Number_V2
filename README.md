# Prime Number Gap V2
This is version 2 of Prime Number Gap.

The main premise of this program is to start a block with a
array of 5 * 10^9 = 5 billion bits. Its called the Genesis block. After the
Gensis block is completed. It gets loaded and the primes
are ran against the following blocks. It will continue 
to process the completed blocks till the second to last one
runs on the last block. 

I understand that the name on this project is called Prime Number
Gap V2. It has evolved into the largest prime collection. The premise
of this program now is to save the prims in binary format i.e.(10011101).
With this in mind. The 1, 3, 7, 9 spots are saved. That is already a 60%
in file storage space. 

# Database Files
There will be two file types saved in the database folder. It will be json
and binary. The json file will hold all the details of the binary file. 
Each file type will have its own folder. In the main Database directory there
will be a file called progress.json. It will hold the information of files that
are processed and in the que. This is to ensure it will pick up from where it
left off incase the program errors our or crashes.

Each of the database files will be labeled block-xxxx.json/.bin. The genesis
files starts at 0 then increases to as far as may blocks you want to make. Evey
block is processed with 5b bits. After it is completed. It is reduced to 40% or smaller
of its original size. The more files you have the gaps between primes get larger
which will help reduce the file size.