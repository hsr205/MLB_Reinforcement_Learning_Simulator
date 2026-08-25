# Install Instructions

You need to have OPAM and Dune installed, the project structure is such:

For dune, I installed it through Opam, opam isntall dune

dune-project - root config file, store meta data, dependencies & settings
bin/ - main entriy point, has main.ml and a dune config file that tells the system to compile the binary
lib/ - core logic, the juicy stuff
test/ - you got this one