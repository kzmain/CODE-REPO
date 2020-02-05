
module load prun/default
module load python/3.6.0
module load hadoop/2.7.6
module load java/jdk-1.8.0

pip3 install venv
python3 -m venv env
source env/bin/activate

pip3 install -r requirements.txt
python3 -m spacy download en_core_web_sm