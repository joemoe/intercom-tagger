# Intercom Tagger

Intercom Tagger is a tool that let's you add Intercom users to a tag. This is 
handy as it might be hard to filter users for using the Intercom built in
interface. At the moment you can use a text file containing one attribute value
per line and a query running on a CrateDB database as inputs.

## Setup

Clone this repo.

```shell
git clone https://github.com/joemoe/intercom-tagger.git
```


Activate your virtualenv. Then install the requirements by running:

```shell
pip install -r requirements.txt
```


## Usage

The tool has a built in help.

```shell
tag.py -h
```

### Loading users from a file

You need to have a file which contains one attribute value per line. As
attribute you can use whatever you've setup on intercom, usually something like
`email` or `user_id`. 

A file containing user_ids would look like this:

```
e2a8d853ffbb0628da27ed06bcaf08b8
039535c41a975c837baee2174263f632
0ace7b7212d1a24b7021885858637a20
089b277181c30f754dae7b6c78f03968
113669609eb14c1b55b2bc34752f58c3
```

Then run, see the `-a` parameter passing the name of the attribute:

```shell
tag.py -f user_ids.txt -a user_id
```

### Loading files from a CrateDB

If you got your users in a CrateDB database you can pass an query along with 
some CrateDB hosts. In this example we are selecting the twitter id from the 
public CrateDB play cluster. We pass `twitter_id` as the attribute to work with.

```shell
tag.py -q "select \"user\"['id'] from tweets limit 10;" -c play.crate.io:80 -a twitter_id
```