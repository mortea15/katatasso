# katatasso
*κατατάσσω - classify*

*katatasso* is a multi-class email classifier written in Python using scikit-learn.

## Installation
**Optional: Create a virtual environment**
```bash
virtualenv .env
source .env/bin/activate    # *nix
.\.env\Scripts\activate     # win
```
**Install**
```bash
$ git clone git@github.com:mortea15/katatasso.git
$ cd katatasso && pip3 install .
```
```bash
$ pip3 install git+ssh://git@github.com/mortea15/katatasso.git
```
## Usage
**Set env vars**
```bash
$ cp env.vars.example env.vars
$ vim env.vars
$ source env.vars
```
### CLI
#### Tag training data
**Run the server**
1. `$ katag`
2. Open `localhost:5000` in your browser
3. Tag emails

#### Train the model
```bash
$ katatasso -t
```

#### Classify
```bash
$ katatasso -f <FILENAME> -c
$ cat <FILENAME> | katatasso -s -c
```

#### Help
```
$ katatasso --help
usage: katatasso [-h] (-f INPUT_FILE | -s) [-t] [-c] [-d FORMAT] [-o OUTPUT_FILE] [-v]

      -f, --infile            Extract entities from file
      -s, --stdin             Extract entities from STDIN

      -t, --train             Train and create a model for classification
      -c, --classify          Classify the text

      -o, --outfile           Output results to this file
      -d, --format            Output results as this format.
                              Available formats: [plain (default), json]

      -v, --verbose           Increase verbosity (can be used twice, e.g. -vv)
      -h, --help              Print this message
```

## Resources
