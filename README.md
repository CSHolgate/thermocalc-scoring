# thermocalc-scoring

Usage (in MS-DOS):

`python tc.py "{""Nb"":70, ""Ru"":15, ""Ti"":15}"`

> Note: the double quotes around each dictionary key seems to be necessary for windows to accept the keys of the dictionary.
> 
> The values in the dictionary are given as moles. Thermo-Calc will handle the normalization for this automatically. Therefore, if the language model predicts the same element in both the BCC and B2 we can just some the values together for the purpose of going into Thermo-Calc.

Sample output is given in `sample_output.txt`.

